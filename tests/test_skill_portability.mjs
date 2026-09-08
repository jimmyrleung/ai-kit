#!/usr/bin/env node

import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkRepository } from '../scripts/check-skill-portability.mjs';
import { bundleSkillReferences } from '../scripts/bundle-skill-references.mjs';

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
  fs.cpSync(path.join(REPO_ROOT, 'docs', 'contracts'), path.join(root, 'docs', 'contracts'), { recursive: true });
  for (const name of ['provider-capabilities.md', 'output-filename-contract.md']) {
    fs.copyFileSync(path.join(REPO_ROOT, 'docs', name), path.join(root, 'docs', name));
  }
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
    ['name-1', (raw) => raw.replace(/^name:.*$/m, 'name: a'), 'name-bounds', false],
    ['name-64', (raw) => raw.replace(/^name:.*$/m, `name: ${'a'.repeat(64)}`), 'name-bounds', false],
    ['name-consecutive-hyphens', (raw) => raw.replace(/^name:.*$/m, 'name: analyze--work'), 'name-bounds', true],
    ['name-leading-hyphen', (raw) => raw.replace(/^name:.*$/m, 'name: -analyze'), 'name-bounds', true],
    ['name-trailing-hyphen', (raw) => raw.replace(/^name:.*$/m, 'name: analyze-'), 'name-bounds', true],
    ['compatibility-empty', (raw) => raw.replace(/^(---\r?\n)/, '$1compatibility: ""\n'), 'compatibility-bounds', true],
    ['compatibility-1', (raw) => raw.replace(/^(---\r?\n)/, '$1compatibility: x\n'), 'compatibility-bounds', false],
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
  for (const replacement of ['missing-skill', 'techspec']) {
    const root = copyFixture();
    try {
      const file = path.join(root, 'INVENTORY.md');
      const raw = fs.readFileSync(file, 'utf8');
      fs.writeFileSync(file, raw.replace('| `analyze-work` |', `| \`${replacement}\` |`));
      const result = checkRepository(root, 'final');
      assertHasCode(result, 'inventory-membership-drift');
      assert.equal(hasCode(result, 'population-count-drift'), false);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  }

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

function testMatchingNameBoundariesAndLinkedPopulation() {
  for (const name of ['a', 'a'.repeat(64), 'analyze--work']) {
    const root = copyFixture();
    try {
      mutateSkill(root, 'analyze-work', (raw) => raw.replace(/^name:.*$/m, `name: ${name}`));
      fs.renameSync(path.join(root, 'skills', 'analyze-work'), path.join(root, 'skills', name));
      const result = checkRepository(root, 'structural');
      assert.equal(hasCode(result, 'name-directory-mismatch'), false);
      assert.equal(hasCode(result, 'name-bounds'), name.includes('--'));
      if (!name.includes('--')) assertNoErrors(result);
    } finally {
      fs.rmSync(root, { recursive: true, force: true });
    }
  }
  const root = copyFixture();
  try {
    const source = path.join(root, 'skills', 'analyze-work');
    const target = path.join(root, 'linked-analyze-work');
    fs.renameSync(source, target);
    fs.symlinkSync(target, source, process.platform === 'win32' ? 'junction' : 'dir');
    const result = checkRepository(root, 'final');
    assertNoErrors(result);
    assert.equal(result.skills.filter((skill) => skill.name === 'analyze-work').length, 1);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
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

function testSelfContainedReferences() {
  const root = copyFixture();
  const detached = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-kit-detached-'));
  try {
    assert.deepEqual(bundleSkillReferences(root).findings, []);
    const source = path.join(root, 'docs', 'contracts', 'authorized-work.md');
    const before = bundleSkillReferences(root).files;
    const oldTimes = new Map(before.map((file) => [file, fs.statSync(path.join(root, file)).mtimeMs]));
    assert.deepEqual(bundleSkillReferences(root, { write: true }).written, []);
    for (const [file, time] of oldTimes) assert.equal(fs.statSync(path.join(root, file)).mtimeMs, time);

    const crlfOutput = path.join(root, before[0]);
    const originalOutput = fs.readFileSync(crlfOutput, 'utf8');
    const crlfText = originalOutput.replace(/\r?\n/g, '\r\n');
    fs.writeFileSync(crlfOutput, crlfText, 'utf8');
    assert.deepEqual(bundleSkillReferences(root).findings, []);
    fs.writeFileSync(
      crlfOutput,
      crlfText.replace('Edit the maintained source', 'Edit this maintained source'),
      'utf8',
    );
    assertHasCode(checkRepository(root, 'final'), 'skill-reference-drift');
    fs.writeFileSync(crlfOutput, originalOutput, 'utf8');

    fs.appendFileSync(source, '\nFixture rule: keep this generated instruction.\n');
    assertHasCode(checkRepository(root, 'final'), 'skill-reference-drift');
    const repaired = bundleSkillReferences(root, { write: true });
    assert.equal(repaired.findings.length, 0);
    const affected = before.filter((file) => file.endsWith('/authorized-work.md'));
    assert.deepEqual([...repaired.written].sort(), [...affected].sort());
    for (const file of affected) assert.match(fs.readFileSync(path.join(root, file), 'utf8'), /Fixture rule/);
    assert.deepEqual(bundleSkillReferences(root).findings, []);

    // A transitive dependency is included even when the skill never links to it directly.
    const feedback = path.join(root, 'skills', 'record-decision', 'references', 'shared', 'feedback.md');
    const evidence = path.join(path.dirname(feedback), 'change-evidence.md');
    assert.equal(fs.existsSync(evidence), true);
    assert.match(fs.readFileSync(feedback, 'utf8'), /\]\(change-evidence\.md\)/);
    fs.unlinkSync(evidence);
    assertHasCode(checkRepository(root, 'final'), 'skill-reference-drift');
    assert.deepEqual(bundleSkillReferences(root, { write: true }).findings, []);

    // Copy every skill separately; every generated document link resolves in that copy.
    // Source-tree identity is deliberately unavailable to this link-resolution check.
    for (const name of fs.readdirSync(path.join(root, 'skills'))) {
      const dest = path.join(detached, name);
      fs.cpSync(path.join(root, 'skills', name), dest, { recursive: true });
      const shared = path.join(dest, 'references', 'shared');
      if (!fs.existsSync(shared)) continue;
      for (const file of fs.readdirSync(shared)) {
        const text = fs.readFileSync(path.join(shared, file), 'utf8');
        for (const match of text.matchAll(/\]\(([^\s)]+)(?:\s+"[^"]*")?\)/g)) {
          if (/^(?:[a-z]+:|#)/i.test(match[1])) continue;
          const target = path.resolve(shared, match[1].split('#')[0]);
          assert.equal(target.startsWith(dest + path.sep), true);
          assert.equal(fs.statSync(target).isFile(), true);
        }
      }
    }

    // Unknown transitive sources fail preflight before any generated file changes.
    const snapshot = new Map(bundleSkillReferences(root).files.map((file) => [file, fs.readFileSync(path.join(root, file), 'utf8')]));
    fs.appendFileSync(source, '\n[Missing source](not-a-contract.md)\n');
    const failure = bundleSkillReferences(root, { write: true });
    assert.equal(failure.findings[0].code, 'skill-reference-input');
    assert.deepEqual(failure.written, []);
    for (const [file, text] of snapshot) assert.equal(fs.readFileSync(path.join(root, file), 'utf8'), text);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
    fs.rmSync(detached, { recursive: true, force: true });
  }
}

function testReferenceOwnershipAndCycles() {
  const root = copyFixture();
  try {
    const dir = path.join(root, 'skills', 'analyze-work', 'references', 'shared');
    const unowned = path.join(dir, 'owner-notes.md');
    fs.writeFileSync(unowned, 'Preserve these notes.\n');
    assert.equal(bundleSkillReferences(root, { write: true }).findings[0].code, 'skill-reference-input');
    assert.equal(fs.readFileSync(unowned, 'utf8'), 'Preserve these notes.\n');
    fs.renameSync(unowned, path.join(root, 'owner-notes.md'));

    const unused = path.join(dir, 'unused.md');
    fs.writeFileSync(unused, '<!-- Generated by bundle-skill-references; fixture -->\n');
    assertHasCode(checkRepository(root, 'final'), 'skill-reference-drift');
    assert.equal(bundleSkillReferences(root, { write: true }).retired.includes('skills/analyze-work/references/shared/unused.md'), true);
    assert.equal(fs.existsSync(unused), false);

    const source = path.join(root, 'docs', 'contracts', 'authorized-work.md');
    fs.appendFileSync(source, '\n[Engineering](engineering-change.md#engineering-change-contract)\n');
    fs.appendFileSync(path.join(root, 'docs', 'contracts', 'engineering-change.md'), '\n[Authorization](authorized-work.md)\n');
    assert.deepEqual(bundleSkillReferences(root, { write: true }).findings, []);
    assert.match(fs.readFileSync(path.join(dir, 'authorized-work.md'), 'utf8'), /engineering-change\.md#engineering-change-contract/);
    assert.deepEqual(bundleSkillReferences(root).findings, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

function testReferenceDefinitionsAndOutputLinks() {
  const root = copyFixture();
  try {
    mutateSkill(root, 'onboard-me', (raw) => raw.replace(
      '(references/shared/feedback.md)', '[feedback-rules]',
    ) + '\n[feedback-rules]: <references/shared/feedback.md> "Feedback rules"\n');
    const source = path.join(root, 'docs', 'contracts', 'feedback.md');
    fs.appendFileSync(source, '\nUse [filename rules][names].\n[names]: ../output-filename-contract.md#contract\n');
    assert.deepEqual(bundleSkillReferences(root, { write: true }).findings, []);
    const shared = path.join(root, 'skills', 'onboard-me', 'references', 'shared');
    assert.equal(fs.existsSync(path.join(shared, 'feedback.md')), true);
    assert.equal(fs.existsSync(path.join(shared, 'change-evidence.md')), true);
    assert.equal(fs.existsSync(path.join(shared, 'output-filename-contract.md')), true);
    assert.match(fs.readFileSync(path.join(shared, 'feedback.md'), 'utf8'),
      /\[names\]: output-filename-contract\.md#contract/);
    assertNoErrors(checkRepository(root, 'final'));

    fs.appendFileSync(source, '\n[missing]: missing-reference.md\n');
    assert.equal(bundleSkillReferences(root, { write: true }).findings[0].code, 'skill-reference-input');
    fs.writeFileSync(source, fs.readFileSync(source, 'utf8').replace('\n[missing]: missing-reference.md\n', ''));

    // Directory junctions are available on Windows without file-symlink privileges.
    const saved = path.join(root, 'saved-shared');
    fs.renameSync(shared, saved);
    fs.symlinkSync(saved, shared, process.platform === 'win32' ? 'junction' : 'dir');
    const failure = bundleSkillReferences(root, { write: true });
    assert.equal(failure.findings[0].code, 'skill-reference-input');
    assert.match(failure.findings[0].message, /uses a link|linked skill dependency/);
    assert.deepEqual(failure.written, []);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

function testDependencyDestinationSyntax() {
  // Assert the required graph independently of the generator's parsing expression.
  const forms = [
    (target) => `[rules](${target} 'Rule title')`,
    (target) => `[rules](${target} (Rule title))`,
    (target) => `[rules](<${target}>\n  "Rule title")`,
    (target) => `[rules](\n  ${target}\n  'Rule title')`,
    (target) => `[rules][rule-id]\n\n[rule-id]:\n  ${target}\n`,
    (target) => `[rules][rule-id]\n\n[rule-id]:\r\n\t<${target}>\r\n  (Rule title)\r\n`,
  ];
  for (const render of forms) {
    const root = copyFixture();
    try {
      mutateSkill(root, 'onboard-me', (raw) => raw.replace(
        '[the feedback contract](references/shared/feedback.md)',
        render('references/shared/feedback.md'),
      ));
      const source = path.join(root, 'docs', 'contracts', 'feedback.md');
      fs.appendFileSync(source, '\n' + render('../output-filename-contract.md#contract') + '\n');
      const result = bundleSkillReferences(root, { write: true });
      assert.deepEqual(result.findings, []);
      assert.deepEqual(result.retired, []);
      const shared = path.join(root, 'skills', 'onboard-me', 'references', 'shared');
      for (const name of ['feedback.md', 'change-evidence.md', 'output-filename-contract.md']) {
        assert.equal(fs.statSync(path.join(shared, name)).isFile(), true, name);
      }
      assert.ok(fs.readFileSync(path.join(shared, 'feedback.md'), 'utf8')
        .includes(render('output-filename-contract.md#contract').replace(/\r\n/g, '\n')));
      assertNoErrors(checkRepository(root, 'final'));
      fs.unlinkSync(path.join(shared, 'output-filename-contract.md'));
      assertHasCode(checkRepository(root, 'final'), 'skill-reference-drift');
      assert.deepEqual(bundleSkillReferences(root, { write: true }).findings, []);

      fs.appendFileSync(source, '\n' + render('missing-reference.md') + '\n');
      const rejected = bundleSkillReferences(root, { write: true });
      assert.equal(rejected.findings[0].code, 'skill-reference-input');
      assert.deepEqual(rejected.written, []);
      assert.deepEqual(rejected.retired, []);
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
testMatchingNameBoundariesAndLinkedPopulation();
testCouplingModesAndClasses();
testSelfContainedReferences();
testReferenceOwnershipAndCycles();
testReferenceDefinitionsAndOutputLinks();
testDependencyDestinationSyntax();
console.log('test_skill_portability: all fixtures passed');
