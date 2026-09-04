// Read-only: validate observation tags against the caller's canonical README.
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

export function checkObservationTags(readme, text) {
  const section = readme.match(/^## Tags[^\n]*\n([\s\S]*?)(?=^## |$(?![\s\S]))/m);
  if (!section) throw new Error('README has no Tags section');
  const allowed = new Set([...section[1].matchAll(/`([a-z_]+)`/g)].map(m => m[1]));
  if (!allowed.size) throw new Error('README Tags section has no tag names');
  const records = text.split(/(?=^### Observation \d+)/m)
    .filter(s => /^### Observation \d+/.test(s));
  if (!records.length) return ['No numbered observations found'];
  const errors = [], seen = new Set();
  for (const record of records) {
    const id = record.match(/^### Observation (\d+)/)[1];
    if (seen.has(id)) errors.push('Observation ' + id + ': duplicate number');
    seen.add(id);
    const field = record.match(/^- \*\*friction_observed:\*\*([\s\S]*?)(?=\n- \*\*|$(?![\s\S]))/m);
    const tags = field ? [...field[1].matchAll(/\btag:\s*`?([a-z_]+)`?\s*(?=\r?$)/gm)] : [];
    if (tags.length !== 1 || !allowed.has(tags[0][1])) {
      errors.push('Observation ' + id + ': expected one canonical tag at the end of friction_observed');
    }
  }
  return errors;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [readmePath, ...files] = process.argv.slice(2);
  if (!readmePath || !files.length) {
    process.stderr.write('Usage: node check-observation-tags.mjs README.md observation.md [...]\n');
    process.exitCode = 2;
  } else {
    try {
      const readme = fs.readFileSync(readmePath, 'utf8');
      let count = 0;
      for (const file of files) {
        const errors = checkObservationTags(readme, fs.readFileSync(file, 'utf8'));
        for (const error of errors) process.stderr.write(file + ': ' + error + '\n');
        count += errors.length;
      }
      process.exitCode = count ? 1 : 0;
      if (!count) process.stdout.write('Observation tags: pass\n');
    } catch (error) {
      process.stderr.write('Observation tag check failed: ' + error.message + '\n');
      process.exitCode = 2;
    }
  }
}
