import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { algorithms, categories, languageSourceUrl, product, sourceUrl } from '../catalog.mjs';
import { bfsSteps, binarySteps, kadaneSteps, sortSteps } from '../labs.mjs';

const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

test('catalog exposes every repository algorithm exactly once', async () => {
  assert.equal(algorithms.length, 56);
  assert.equal(new Set(algorithms.map((algorithm) => algorithm.slug)).size, algorithms.length);
  assert.equal(categories.length - 1, 15);
  for (const algorithm of algorithms) {
    await access(resolve(repoRoot, algorithm.source));
    const javaSource = algorithm.source.replace(/\.py$/, '.java').replace('Bubble-Sort.java', 'BubbleSort.java');
    const cSource = algorithm.source.replace(/\.py$/, '.c').replace('Bubble-Sort.c', 'BubbleSort.c');
    await access(resolve(repoRoot, javaSource));
    await access(resolve(repoRoot, cSource));
  }
});

test('release metadata does not claim an APK before an artifact exists', () => {
  assert.equal(product.release.status, 'development');
  assert.equal(product.release.apkUrl, '');
});

test('source URLs preserve paths with spaces', () => {
  const search = algorithms.find((algorithm) => algorithm.slug === 'binary-search');
  assert.match(sourceUrl(search), /Searching%20Algorithms\/Binary%20Search\/BinarySearch\.py$/);
  const bubble = algorithms.find((algorithm) => algorithm.slug === 'bubble-sort');
  assert.match(languageSourceUrl(bubble, 'java'), /Sorting-Algorithms\/BubbleSort\/BubbleSort\.java$/);
});

test('static entry points include accessible navigation and a manifest', async () => {
  const html = await readFile(resolve(repoRoot, 'web/index.html'), 'utf8');
  assert.match(html, /id="app"/);
  assert.match(html, /aria-label="Primary navigation"/);
  assert.match(html, /manifest\.json/);
});

test('Vercel publishes the generated web output from the repository root', async () => {
  const config = JSON.parse(await readFile(resolve(repoRoot, 'vercel.json'), 'utf8'));
  assert.equal(config.buildCommand, 'npm --prefix web run build');
  assert.equal(config.outputDirectory, 'web/dist');
});

test('interactive trace generators preserve the algorithm contracts', () => {
  const sorted = sortSteps([7, 3, 5, 1]).at(-1).values;
  assert.deepEqual(sorted, [1, 3, 5, 7]);

  const found = binarySteps([2, 4, 7, 11, 15], 15).at(-1);
  assert.equal(found.result, 4);

  const missing = binarySteps([2, 4, 7, 11, 15], 6).at(-1);
  assert.equal(missing.result, -1);

  const kadane = kadaneSteps([-2, 1, -3, 4, -1, 2, 1, -5, 4]).at(-1);
  assert.equal(kadane.best, 6);

  const bfs = bfsSteps().at(-1);
  assert.deepEqual(bfs.visited, [0, 1, 2, 3, 4]);
});
