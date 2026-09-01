#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const yaml = require('js-yaml');

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const STANDARD_FIELDS = new Set(['name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools']);
const OVERLAY_FIELDS = new Set([
  'arguments',
  'argument-hint',
  'disable-model-invocation',
  'paths',
  'icon',
  'color',
]);
const ALLOWED_FIELDS = new Set([...STANDARD_FIELDS, ...OVERLAY_FIELDS]);
const NAMED_ARGUMENTS = new Map([
  ['compile-kb', 'vault_path'],
  ['docs-tasks-creator', 'codebase_path output_dir'],
  ['document-terraform', 'repo_path output_dir spec_file'],
]);
const FIND_SKILLS_SHA256 = 'deddc03b4b5f50755b97fcdb737a786676992ef7e9be614d2cd2c71e0320bebf';
const COUPLING_RULES = [
  { code: 'windows-repo-path', pattern: /C:\\ai-kit(?:[\\/]|$)/gi, message: 'live canonical skill contains a Windows checkout path' },
  { code: 'convention-token', pattern: /\bCLAUDE\.md\b/gi, message: 'live canonical skill names a provider-private convention file' },
  { code: 'question-tool', pattern: /\bAskUserQuestion\b/g, message: 'live canonical skill names a provider question tool' },
  { code: 'planning-tool', pattern: /\bTodoWrite\b/g, message: 'live canonical skill names a provider planning tool' },
  { code: 'research-tool', pattern: /\b(?:Explore|Glob|Grep|Read)\b/g, message: 'live canonical skill names a provider file/research tool' },
  { code: 'worker-tool', pattern: /\b(?:Agent|Task)\s+(?:tool|subagent|worker)\b/g, message: 'live canonical skill names a provider worker tool' },
  { code: 'message-tool', pattern: /\bSendMessage\b/g, message: 'live canonical skill names a provider messaging tool' },
  { code: 'shell-tool', pattern: /\b(?:Bash|PowerShell)\b/g, message: 'live canonical skill names a provider shell' },
  { code: 'model-provider', pattern: /\b(?:Opus|Fable|Haiku|Claude Code|Codex CLI|Cursor CLI)\b/g, message: 'live canonical skill fixes a provider or model name' },
  { code: 'runner-token', pattern: /\/(?:goal|loop|schedule|tasks-loop)\b/g, message: 'live canonical skill embeds a provider-native runner token' },
];

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

function relative(root, file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function lineNumber(text, offset) {
  return text.slice(0, offset).split(/\r?\n/).length;
}

function snippet(text, offset, length) {
  const lineStart = text.lastIndexOf('\n', offset - 1) + 1;
  const lineEnd = text.indexOf('\n', offset);
  return text.slice(lineStart, lineEnd < 0 ? text.length : lineEnd).trim().slice(0, 220);
}

function addFinding(result, { code, file, message, offset = 0, kind = 'structural', detail = '' }) {
  if (kind === 'coupling' && result.mode === 'structural') return;
  const severity = kind === 'coupling' && result.mode === 'transitional' ? 'warning'
    : kind === 'documentation' && result.mode !== 'final' ? 'warning'
      : 'error';
  const finding = {
    severity,
    code,
    file: relative(result.root, file),
    line: lineNumber(result.sourceByFile.get(file) ?? '', offset),
    message,
    detail,
  };
  result.findings.push(finding);
  if (severity === 'error') result.errors.push(finding);
  else result.warnings.push(finding);
}

function parseFrontmatter(raw, file, result) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/.exec(raw);
  if (!match) {
    addFinding(result, { code: 'frontmatter-fence', file, message: 'SKILL.md must have a closed YAML frontmatter block', kind: 'profile' });
    return null;
  }
  try {
    const value = yaml.load(match[1], { json: false });
    if (!isPlainObject(value)) {
      addFinding(result, { code: 'frontmatter-mapping', file, message: 'frontmatter must parse as a YAML mapping', offset: 0, kind: 'profile' });
      return null;
    }
    return { value, yamlText: match[1], body: raw.slice(match[0].length), offset: 0 };
  } catch (error) {
    addFinding(result, {
      code: 'strict-yaml',
      file,
      message: `strict js-yaml parse failed: ${error.reason ?? error.message}`,
      offset: 0,
      kind: 'profile',
    });
    return null;
  }
}

function checkStringField(fm, field, file, result) {
  if (fm[field] !== undefined && typeof fm[field] !== 'string') {
    addFinding(result, { code: 'field-shape', file, message: `${field} must be a string`, kind: 'profile' });
  }
}

function checkSkillProfile(skill, result) {
  const { name, file, frontmatter: fm } = skill;
  for (const key of Object.keys(fm)) {
    if (!ALLOWED_FIELDS.has(key)) {
      addFinding(result, { code: 'unknown-field', file, message: `unknown frontmatter field: ${key}`, kind: 'profile' });
    }
  }
  if (typeof fm.name !== 'string') {
    addFinding(result, { code: 'required-field', file, message: 'name is required and must be a string', kind: 'profile' });
  } else {
    if (fm.name !== name) {
      addFinding(result, { code: 'name-directory-mismatch', file, message: `name ${fm.name} does not equal directory ${name}`, kind: 'profile' });
    }
    if (!/^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$/.test(fm.name)) {
      addFinding(result, { code: 'name-bounds', file, message: 'name must be 1–64 lowercase alphanumeric/hyphen characters without edge hyphens', kind: 'profile' });
    }
  }
  if (typeof fm.description !== 'string' || fm.description.length === 0) {
    addFinding(result, { code: 'required-field', file, message: 'description is required and must be non-empty', kind: 'profile' });
  } else if (fm.description.length > 1024) {
    addFinding(result, { code: 'description-bounds', file, message: `description is ${fm.description.length} characters; maximum is 1,024`, kind: 'profile' });
  }
  checkStringField(fm, 'license', file, result);
  if (fm.compatibility !== undefined) {
    checkStringField(fm, 'compatibility', file, result);
    if (typeof fm.compatibility === 'string' && fm.compatibility.length > 500) {
      addFinding(result, { code: 'compatibility-bounds', file, message: `compatibility is ${fm.compatibility.length} characters; maximum is 500`, kind: 'profile' });
    }
  }
  if (fm.metadata !== undefined) {
    if (!isPlainObject(fm.metadata) || Object.entries(fm.metadata).some(([key, value]) => typeof key !== 'string' || typeof value !== 'string')) {
      addFinding(result, { code: 'field-shape', file, message: 'metadata must be a string-to-string map', kind: 'profile' });
    }
  }
  if (fm['allowed-tools'] !== undefined) {
    if (typeof fm['allowed-tools'] !== 'string' || fm['allowed-tools'].trim() === '') {
      addFinding(result, { code: 'field-shape', file, message: 'allowed-tools must be a non-empty space-separated scalar', kind: 'profile' });
    } else {
      result.notes.push(`${relative(result.root, file)}: allowed-tools is experimental and provider support is implementation-dependent`);
    }
  }
  if (fm.arguments !== undefined) {
    if (typeof fm.arguments !== 'string' || fm.arguments.trim() === '') {
      addFinding(result, { code: 'arguments-shape', file, message: 'arguments must be a non-empty scalar', kind: 'profile' });
    } else if (!NAMED_ARGUMENTS.has(name) || fm.arguments !== NAMED_ARGUMENTS.get(name)) {
      addFinding(result, { code: 'unjustified-overlay', file, message: 'arguments is allowed only with the reviewed named-input contract', kind: 'profile' });
    }
  }
  if (fm['argument-hint'] !== undefined) {
    if (name !== 'teach' || typeof fm['argument-hint'] !== 'string' || fm['argument-hint'].trim() === '') {
      addFinding(result, { code: 'unjustified-overlay', file, message: 'argument-hint is a reviewed Cursor overlay only for teach', kind: 'profile' });
    }
  }
  if (fm['disable-model-invocation'] !== undefined) {
    if (name !== 'teach' || fm['disable-model-invocation'] !== true) {
      addFinding(result, { code: 'unjustified-overlay', file, message: 'disable-model-invocation is a reviewed explicit-only overlay only for teach', kind: 'profile' });
    }
  }
  for (const field of ['paths', 'icon', 'color']) {
    if (fm[field] !== undefined && name !== 'teach') {
      addFinding(result, { code: 'unjustified-overlay', file, message: `${field} is an unjustified Cursor overlay on ${name}`, kind: 'profile' });
    }
  }
  if (name === 'teach' && fm.paths !== undefined) {
    const validPaths =
      (typeof fm.paths === 'string' && fm.paths.trim() !== '') ||
      (Array.isArray(fm.paths) && fm.paths.length > 0 && fm.paths.every((value) => typeof value === 'string' && value.trim() !== ''));
    if (!validPaths) {
      addFinding(result, { code: 'cursor-paths-shape', file, message: 'paths must be a non-empty string or a non-empty list of non-empty strings', kind: 'profile' });
    }
  }
  if (name === 'teach' && fm.icon !== undefined && (typeof fm.icon !== 'string' || fm.icon.trim() === '')) {
    addFinding(result, { code: 'cursor-icon-shape', file, message: 'icon must be a non-empty string', kind: 'profile' });
  }
  if (name === 'teach' && fm.color !== undefined) {
    const colors = new Set(['default', 'green', 'cyan', 'blue', 'purple', 'magenta', 'orange', 'yellow', 'red', 'brand']);
    if (typeof fm.color !== 'string' || !colors.has(fm.color)) {
      addFinding(result, { code: 'cursor-color-shape', file, message: 'color must be a documented Cursor badge color', kind: 'profile' });
    }
  }
}

function scanCoupling(skill, names, result) {
  const { raw, file, frontmatter } = skill;
  const description = typeof frontmatter.description === 'string' ? frontmatter.description : '';
  const invocation = /\bInvoke as\s+\/[a-z0-9-]+/gi;
  for (const match of description.matchAll(invocation)) {
    addFinding(result, { code: 'invocation-suffix', file, message: 'description contains a provider-specific invocation suffix', offset: match.index ?? 0, kind: 'coupling', detail: match[0] });
  }
  if (names.length > 0) {
    const escaped = names.map((name) => name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
    const crossSkill = new RegExp(`(^|[^A-Za-z0-9_.])\\/(${escaped})(?![A-Za-z0-9-])`, 'g');
    for (const match of raw.matchAll(crossSkill)) {
      const tokenOffset = (match.index ?? 0) + match[1].length;
      addFinding(result, { code: 'cross-skill-invocation', file, message: 'canonical skill uses slash-form sibling invocation', offset: tokenOffset, kind: 'coupling', detail: match[0].trim() });
    }
  }
  for (const rule of COUPLING_RULES) {
    rule.pattern.lastIndex = 0;
    for (const match of raw.matchAll(rule.pattern)) {
      addFinding(result, { code: rule.code, file, message: rule.message, offset: match.index ?? 0, kind: 'coupling', detail: match[0] });
    }
  }
}

function parseYamlFile(file, result, codePrefix) {
  let raw;
  try {
    raw = fs.readFileSync(file, 'utf8');
  } catch (error) {
    addFinding(result, { code: `${codePrefix}-read`, file, message: `cannot read provider metadata: ${error.message}`, kind: 'profile' });
    return null;
  }
  try {
    const value = yaml.load(raw, { json: false });
    if (!isPlainObject(value)) {
      addFinding(result, { code: `${codePrefix}-mapping`, file, message: 'provider metadata must be a YAML mapping', kind: 'profile' });
      return null;
    }
    return value;
  } catch (error) {
    addFinding(result, { code: `${codePrefix}-yaml`, file, message: `strict js-yaml parse failed: ${error.reason ?? error.message}`, kind: 'profile' });
    return null;
  }
}

function checkTeachPolicies(root, result) {
  const teachFile = path.join(root, 'skills', 'teach', 'SKILL.md');
  const teach = result.skills.find((skill) => skill.name === 'teach');
  if (teach && teach.frontmatter['disable-model-invocation'] !== true) {
    addFinding(result, { code: 'teach-cursor-policy', file: teach.file, message: 'teach must be explicit-only under the Cursor overlay', kind: 'profile' });
  }
  const openaiFile = path.join(root, 'skills', 'teach', 'agents', 'openai.yaml');
  const openai = parseYamlFile(openaiFile, result, 'openai-profile');
  if (!openai) return;
  for (const key of Object.keys(openai)) {
    if (key !== 'policy' && key !== 'interface') {
      addFinding(result, { code: 'openai-unknown-field', file: openaiFile, message: `unknown Codex metadata field: ${key}`, kind: 'profile' });
    }
  }
  if (!isPlainObject(openai.policy) || openai.policy.allow_implicit_invocation !== false) {
    addFinding(result, { code: 'teach-codex-policy', file: openaiFile, message: 'policy.allow_implicit_invocation must be false for teach', kind: 'profile' });
  }
  if (openai.interface !== undefined && !isPlainObject(openai.interface)) {
    addFinding(result, { code: 'openai-interface-shape', file: openaiFile, message: 'Codex interface metadata must be a mapping', kind: 'profile' });
  }
}

function extractCount(file, text, result) {
  const basename = path.basename(file);
  let matches;
  if (basename === 'README.md') {
    matches = [...text.matchAll(/\b(\d+)\s+skills?\b/gi)].map((match) => Number(match[1]));
  } else if (basename === 'INVENTORY.md') {
    matches = [...text.matchAll(/\bskills?\s*\((\d+)\s+total\)|\b(\d+)\s+total\b/gi)]
      .map((match) => Number(match[1] ?? match[2]));
  } else {
    matches = [...text.matchAll(/\b(?:live\s+canonical\s+population|derived\s+live-skill\s+count)\D{0,20}(\d+)\b/gi)]
      .map((match) => Number(match[1]));
  }
  if (matches.length === 0) {
    addFinding(result, { code: 'population-count-missing', file, message: 'document has no derived live-skill count claim', kind: 'documentation' });
    return [];
  }
  return [...new Set(matches)];
}

function checkPopulationDocs(root, skillCount, result) {
  const documents = [
    path.join(root, 'README.md'),
    path.join(root, 'INVENTORY.md'),
    path.join(root, 'docs', 'rules', 'skill-authoring.md'),
  ];
  for (const file of documents) {
    let text;
    try {
      text = fs.readFileSync(file, 'utf8');
    } catch (error) {
      addFinding(result, { code: 'population-doc-read', file, message: `cannot read population document: ${error.message}`, kind: 'documentation' });
      continue;
    }
    result.sourceByFile.set(file, text);
    const counts = extractCount(file, text, result);
    if (counts.some((count) => count !== skillCount)) {
      addFinding(result, { code: 'population-count-drift', file, message: `documented counts ${counts.join(', ')} do not equal derived count ${skillCount}`, kind: 'documentation' });
    }
  }
}

function checkFindSkills(root, result) {
  const file = path.join(root, 'skills', 'find-skills', 'SKILL.md');
  try {
    const normalized = fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n');
    const digest = crypto.createHash('sha256').update(normalized, 'utf8').digest('hex');
    if (digest !== FIND_SKILLS_SHA256) {
      addFinding(result, { code: 'neutral-reference-changed', file, message: `find-skills hash ${digest} differs from the locked neutral reference`, kind: 'profile' });
    }
  } catch (error) {
    addFinding(result, { code: 'neutral-reference-read', file, message: `cannot read neutral reference: ${error.message}`, kind: 'profile' });
  }
}

export function checkRepository(root = REPO_ROOT, mode = 'final') {
  if (!['structural', 'transitional', 'final'].includes(mode)) {
    throw new Error(`unsupported mode: ${mode}`);
  }
  const result = {
    root: path.resolve(root),
    mode,
    skills: [],
    findings: [],
    errors: [],
    warnings: [],
    notes: [],
    sourceByFile: new Map(),
  };
  const skillsRoot = path.join(result.root, 'skills');
  let entries;
  try {
    entries = fs.readdirSync(skillsRoot, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  } catch (error) {
    addFinding(result, { code: 'skills-root-read', file: skillsRoot, message: `cannot enumerate skills with fs.readdirSync: ${error.message}`, kind: 'profile' });
    return result;
  }
  const names = [];
  for (const entry of entries) {
    let isDirectory = entry.isDirectory();
    if (!isDirectory && entry.isSymbolicLink()) {
      try { isDirectory = fs.statSync(path.join(skillsRoot, entry.name)).isDirectory(); } catch { isDirectory = false; }
    }
    if (!isDirectory) continue;
    names.push(entry.name);
    const file = path.join(skillsRoot, entry.name, 'SKILL.md');
    let raw;
    try {
      raw = fs.readFileSync(file, 'utf8');
    } catch (error) {
      addFinding(result, { code: 'skill-read', file, message: `cannot read canonical skill: ${error.message}`, kind: 'profile' });
      continue;
    }
    result.sourceByFile.set(file, raw);
    const parsed = parseFrontmatter(raw, file, result);
    if (!parsed) continue;
    const skill = { name: entry.name, file, raw, body: parsed.body, frontmatter: parsed.value };
    result.skills.push(skill);
    checkSkillProfile(skill, result);
  }
  result.skills.sort((a, b) => a.name.localeCompare(b.name));
  for (const skill of result.skills) scanCoupling(skill, names, result);
  checkTeachPolicies(result.root, result);
  checkFindSkills(result.root, result);
  checkPopulationDocs(result.root, result.skills.length, result);
  return result;
}

function printResult(result) {
  console.log(`ai-kit portability check (${result.mode})`);
  console.log(`  root    : ${result.root}`);
  console.log(`  skills  : ${result.skills.length}`);
  for (const finding of result.findings) {
    const location = `${finding.file}:${finding.line}`;
    const detail = finding.detail ? ` — ${finding.detail}` : '';
    console.log(`${finding.severity.toUpperCase()} [${finding.code}] ${location}: ${finding.message}${detail}`);
  }
  for (const note of result.notes) console.log(`NOTE ${note}`);
  console.log(`Result: errors=${result.errors.length}, warnings=${result.warnings.length}`);
}

function parseArgs(argv) {
  const args = { root: REPO_ROOT, mode: 'final' };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--root') {
      if (!argv[index + 1]) throw new Error('--root requires a path');
      args.root = path.resolve(argv[++index]);
    } else if (arg === '--mode') {
      if (!argv[index + 1]) throw new Error('--mode requires structural, transitional, or final');
      args.mode = argv[++index];
    } else if (arg === '--help' || arg === '-h') {
      console.log('Usage: node scripts/check-skill-portability.mjs [--mode structural|transitional|final] [--root <repo>]');
      process.exit(0);
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  return args;
}

if (fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  try {
    const args = parseArgs(process.argv.slice(2));
    const result = checkRepository(args.root, args.mode);
    printResult(result);
    process.exitCode = result.errors.length > 0 ? 1 : 0;
  } catch (error) {
    console.error(`Usage error: ${error.message}`);
    process.exitCode = 2;
  }
}
