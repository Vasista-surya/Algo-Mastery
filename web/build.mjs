import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { algorithms, product } from './catalog.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const output = resolve(here, 'dist');

await rm(output, { recursive: true, force: true });
await mkdir(join(output, 'assets'), { recursive: true });
for (const file of ['index.html', 'styles.css', 'app.mjs', 'catalog.mjs', 'labs.mjs', 'manifest.json']) {
  await cp(join(here, file), join(output, file));
}
await cp(join(here, 'assets'), join(output, 'assets'), { recursive: true });
const manifest = {
  product: product.name,
  version: product.version,
  algorithmCount: algorithms.length,
  generatedAt: new Date().toISOString(),
  releaseStatus: product.release.status,
  source: 'web/build.mjs'
};
await writeFile(join(output, 'build-meta.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(`Built ${algorithms.length} algorithm modules to ${output}`);
