#!/usr/bin/env node

import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkRepository } from '../scripts/check-skill-portability.mjs';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function copyFixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-kit-portability-'));
  fs.cpSync(path.join(REPO_ROOT, 'skills'), path.join(root, 'skills'), { recursive: true });
  fs.mkdirSync(path.join(root, 'docs', 'rules'), { recursive: true });
  for (const file of ['README.md', 'INVENTORY.md']) {
    fs.copyFileSync(path.join(REPO_ROOT, file), path.join(root, file));
  }
  fs.copyFileSync(
    path.join(REPO_ROOT, 'docs', 'rules', 'skill-authoring.md'),
    path.join(root, 'docs', 'rules', 'skill-authoring.md'),
  );
  return root;
}

function mutateSkill(root, name, mutator) {
  const file = path.join(root, 'skills', name, 'SKILL.md');
  const before = fs.readFileSync(file, 'utf8');
  fs.writeFileSync(file, mutator(before), 'utf8');
  return file;
}

function addFrontmatter(root, name, line) {
  mutateSkill(root, name, (raw) => raw.replace(/^(---\r?\n)/, `$1${line}\n`));
}

function hasCode(result, code) {
  return result.findings.some((finding) => finding.code === code);
}

function assertHasCode(result, code) {
  assert.equal(hasCode(result, code), true, `expected ${code}; got ${result.findings.map((item) => item.code).join(', ')}`);
}

function assertNoErrors(result) {
  assert.deepEqual(result.errors, [], result.errors.map((item) => `${item.code}: ${item.message}`).join('\n'));
}

function testLiveProfilesAndTransition() {
  const structural = checkRepository(REPO_ROOT, 'structural');
  assert.equal(structural.skills.length, 31);
  assertNoErrors(structural);
  assert.equal(structural.findings.some((item) => item.severity === 'error' && item.code.includes('coupling')), false);
  assert.equal(structural.notes.some((item) => item.includes('allowed-tools')), false);

  const transitional = checkRepository(REPO_ROOT, 'transitional');
  assertNoErrors(transitional);
}

function testStrictYamlAndMappingFixtures() {
  const fixtures = [
    ['unquoted colon-space', (raw) => raw.replace(/^description:.*$/m, 'description: bad: scalar'), 'strict-yaml'],
    ['duplicate key', (raw) => raw.replace(/^(name:.*)$/m, '$1\nname: duplicate'), 'strict-yaml'],
    ['invalid scalar', (raw) => raw.replace(/^(name:.*)$/m, '$1\nmetadata: [unterminated'), 'strict-yaml'],
    ['non-mapping', () => '---\n- name\n---\n\nbody\n', 'frontmatter-mapping'],
  ];
  for (const [label, mutator, code] of fixtures) {
    const root = copyFixture();
    try {
      mutateSkill(root, 'analyze-work', mutator);
      const result = checkRepository(root, 'structural');
      assertHasCode(result, code);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
    assert.equal(typeof label, 'string');
  }
}

function testStandardBoundsAndUnknownFields() {
  const cases = [
    ['description-1024', (raw) => raw.replace(/^description:.*$/m, `description: "${'x'.repeat(1024)}"`), 'description-bounds', false],
    ['description-1025', (raw) => raw.replace(/^description:.*$/m, `description: "${'x'.repeat(1025)}"`), 'description-bounds', true],
    ['name-65', (raw) => raw.replace(/^name:.*$/m, `name: ${'a'.repeat(65)}`), 'name-bounds', true],
    ['compatibility-500', (raw) => raw.replace(/^(---\r?\n)/, `$1compatibility: "${'x'.repeat(500)}"\n`), 'compatibility-bounds', false],
    ['compatibility-501', (raw) => raw.replace(/^(---\r?\n)/, `$1compatibility: "${'x'.repeat(501)}"\n`), 'compatibility-bounds', true],
    ['unknown-field', (raw) => raw.replace(/^(---\r?\n)/, '$1unknown-field: true\n'), 'unknown-field', true],
  ];
  for (const [label, mutator, code, shouldFail] of cases) {
    const root = copyFixture();
    try {
      mutateSkill(root, 'analyze-work', mutator);
      const result = checkRepository(root, 'structural');
      assert.equal(hasCode(result, code), shouldFail, `${label}: unexpected ${code} result`);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  }
}

function testProviderProfilesAndTeachPolicies() {
  const valid = copyFixture();
  try {
    addFrontmatter(valid, 'teach', 'paths: "**/*.md"');
    addFrontmatter(valid, 'teach', 'icon: "book"');
    addFrontmatter(valid, 'teach', 'color: "purple"');
    const result = checkRepository(valid, 'structural');
    assertNoErrors(result);
  } finally {
    fs.rmSync(valid, { recursive: true, force: true });
  }

  const validPathList = copyFixture();
  try {
    addFrontmatter(validPathList, 'teach', 'paths: ["**/*.md", "lessons/**/*.html"]');
    assertNoErrors(checkRepository(validPathList, 'structural'));
  } finally {
    fs.rmSync(validPathList, { recursive: true, force: true });
  }

  for (const [field, value, code] of [
    ['paths', '{ unexpected: mapping }', 'cursor-paths-shape'],
    ['paths', '[]', 'cursor-paths-shape'],
    ['icon', '42', 'cursor-icon-shape'],
    ['color', 'false', 'cursor-color-shape'],
    ['color', 'chartreuse', 'cursor-color-shape'],
  ]) {
    const invalid = copyFixture();
    try {
      addFrontmatter(invalid, 'teach', `${field}: ${value}`);
      assertHasCode(checkRepository(invalid, 'structural'), code);
    } finally {
      fs.rmSync(invalid, { recursive: true, force: true });
    }
  }

  const unjustified = copyFixture();
  try {
    addFrontmatter(unjustified, 'analyze-work', 'paths: "src/**"');
    assertHasCode(checkRepository(unjustified, 'structural'), 'unjustified-overlay');
  } finally {
    fs.rmSync(unjustified, { recursive: true, force: true });
  }

  const malformed = copyFixture();
  try {
    const file = path.join(malformed, 'skills', 'teach', 'agents', 'openai.yaml');
    fs.writeFileSync(file, 'policy: [not closed\n', 'utf8');
    assertHasCode(checkRepository(malformed, 'structural'), 'openai-profile-yaml');
  } finally {
    fs.rmSync(malformed, { recursive: true, force: true });
  }

  const unknown = copyFixture();
  try {
    const file = path.join(unknown, 'skills', 'teach', 'agents', 'openai.yaml');
    fs.writeFileSync(file, 'policy:\n  allow_implicit_invocation: false\nunknown: true\n', 'utf8');
    assertHasCode(checkRepository(unknown, 'structural'), 'openai-unknown-field');
  } finally {
    fs.rmSync(unknown, { recursive: true, force: true });
  }
}

function testPopulationAndNeutralReference() {
  const drifted = copyFixture();
  try {
    const file = path.join(drifted, 'README.md');
    const raw = fs.readFileSync(file, 'utf8');
    fs.writeFileSync(file, raw.replace('31 skills', '32 skills'), 'utf8');
    assertHasCode(checkRepository(drifted, 'final'), 'population-count-drift');
  } finally {
    fs.rmSync(drifted, { recursive: true, force: true });
  }

  const added = copyFixture();
  try {
    const dir = path.join(added, 'skills', 'fixture-skill');
    fs.mkdirSync(dir);
    fs.writeFileSync(dir + '/SKILL.md', '---\nname: fixture-skill\ndescription: Fixture skill\n---\n', 'utf8');
    assertHasCode(checkRepository(added, 'final'), 'population-count-drift');
  } finally {
    fs.rmSync(added, { recursive: true, force: true });
  }

  const changed = copyFixture();
  try {
    mutateSkill(changed, 'find-skills', (raw) => `${raw}\n`);
    assertHasCode(checkRepository(changed, 'structural'), 'neutral-reference-changed');
  } finally {
    fs.rmSync(changed, { recursive: true, force: true });
  }

  const crlf = copyFixture();
  try {
    mutateSkill(crlf, 'find-skills', (raw) => raw.replace(/\r?\n/g, '\r\n'));
    assert.equal(hasCode(checkRepository(crlf, 'structural'), 'neutral-reference-changed'), false);
  } finally {
    fs.rmSync(crlf, { recursive: true, force: true });
  }
}

function testCouplingModesAndClasses() {
  const fixtures = [
    ['invocation-suffix', 'Invoke as /analyze-work'],
    ['cross-skill-invocation', '/teach'],
    ['windows-repo-path', 'C:\\ai-kit\\skills'],
    ['convention-token', 'CLAUDE.md'],
    ['question-tool', 'AskUserQuestion'],
    ['planning-tool', 'TodoWrite'],
    ['research-tool', 'Explore'],
    ['worker-tool', 'Agent tool'],
    ['message-tool', 'SendMessage'],
    ['shell-tool', 'Bash'],
    ['model-provider', 'Opus'],
    ['runner-token', '/loop'],
  ];
  for (const [code, token] of fixtures) {
    const root = copyFixture();
    try {
      mutateSkill(root, 'analyze-work', (raw) => code === 'invocation-suffix'
        ? raw.replace(/^(description:\s*")([^"\n]*)(")$/m, (_, prefix, description, suffix) => `${prefix}${description} ${token}${suffix}`)
        : `${raw}\n${token}\n`);
      const transitional = checkRepository(root, 'transitional');
      assert.equal(transitional.errors.length, 0, `${code} incorrectly blocked transition`);
      assertHasCode(transitional, code);
      const final = checkRepository(root, 'final');
      assertHasCode(final, code);
      assert.equal(final.errors.some((item) => item.code === code), true);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  }
}

testLiveProfilesAndTransition();
testStrictYamlAndMappingFixtures();
testStandardBoundsAndUnknownFields();
testProviderProfilesAndTeachPolicies();
testPopulationAndNeutralReference();
testCouplingModesAndClasses();
console.log('test_skill_portability: all fixtures passed');
