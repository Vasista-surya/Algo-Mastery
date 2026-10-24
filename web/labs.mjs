export function sortSteps(values) {
  const working = [...values];
  const steps = [{ values: [...working], active: [], sorted: [] }];
  const settled = [];
  for (let end = working.length - 1; end > 0; end -= 1) {
    let swapped = false;
    for (let index = 0; index < end; index += 1) {
      steps.push({ values: [...working], active: [index, index + 1], sorted: [...settled] });
      if (working[index] > working[index + 1]) {
        [working[index], working[index + 1]] = [working[index + 1], working[index]];
        swapped = true;
        steps.push({ values: [...working], active: [index, index + 1], sorted: [...settled] });
      }
    }
    settled.push(end);
    steps.push({ values: [...working], active: [], sorted: [...settled] });
    if (!swapped) break;
  }
  steps.push({ values: [...working], active: [], sorted: working.map((_, index) => index) });
  return steps;
}

export function binarySteps(values, target) {
  const steps = [];
  let left = 0;
  let right = values.length - 1;
  let result = -1;
  while (left <= right) {
    const middle = Math.floor((left + right) / 2);
    steps.push({ values: [...values], left, right, middle, result, note: `Compare ${values[middle]} with target ${target}.` });
    if (values[middle] === target) {
      result = middle;
      steps.push({ values: [...values], left, right, middle, result, note: `Found ${target} at index ${middle}.` });
      break;
    }
    if (values[middle] < target) left = middle + 1;
    else right = middle - 1;
  }
  if (result === -1) steps.push({ values: [...values], left, right, middle: -1, result, note: `${target} is not present; the interval is empty.` });
  return steps;
}

export function kadaneSteps(values) {
  let current = values[0];
  let best = values[0];
  const steps = [{ values: [...values], index: 0, current, best }];
  for (let index = 1; index < values.length; index += 1) {
    current = Math.max(values[index], current + values[index]);
    best = Math.max(best, current);
    steps.push({ values: [...values], index, current, best });
  }
  return steps;
}

export const graphFixture = {
  nodes: [{ id: 0, x: 18, y: 50 }, { id: 1, x: 43, y: 23 }, { id: 2, x: 43, y: 77 }, { id: 3, x: 70, y: 23 }, { id: 4, x: 82, y: 73 }],
  edges: [[0, 1], [0, 2], [1, 3], [2, 3], [2, 4], [3, 4]]
};

export function bfsSteps() {
  const adjacency = new Map(graphFixture.nodes.map((node) => [node.id, []]));
  graphFixture.edges.forEach(([from, to]) => adjacency.get(from).push(to));
  const queue = [0];
  const visited = new Set([0]);
  const steps = [{ current: -1, visited: [], queue: [0], edge: null, note: 'The source vertex 0 enters the queue.' }];
  while (queue.length) {
    const current = queue.shift();
    steps.push({ current, visited: [...visited], queue: [...queue], edge: null, note: `Dequeue ${current}; inspect its neighbors in input order.` });
    for (const neighbor of adjacency.get(current)) {
      steps.push({ current, visited: [...visited], queue: [...queue], edge: [current, neighbor], note: `Inspect edge ${current} → ${neighbor}.` });
      if (!visited.has(neighbor)) {
        visited.add(neighbor);
        queue.push(neighbor);
        steps.push({ current, visited: [...visited], queue: [...queue], edge: [current, neighbor], note: `Queue ${neighbor}; it has not been visited yet.` });
      }
    }
  }
  steps.push({ current: -1, visited: [...visited], queue: [], edge: null, note: `Traversal complete: ${[...visited].join(' → ')}.` });
  return steps;
}
