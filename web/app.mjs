import { algorithms, algorithmsBySlug, categories, categoryInfo, languageSourceUrl, product, sourceUrl } from './catalog.mjs';
import { bfsSteps, binarySteps, graphFixture, kadaneSteps, sortSteps } from './labs.mjs';

const root = document.querySelector('#app');
const sidebar = document.querySelector('#sidebar');
const toastRegion = document.querySelector('#toast-region');
const globalSearch = document.querySelector('#global-search');
const breadcrumb = document.querySelector('#breadcrumb');
const savedDot = document.querySelector('#saved-dot');

const storageKeys = { bookmarks: 'algo-mastery-bookmarks', recent: 'algo-mastery-recent' };
const state = {
  selectedCategory: 'all',
  query: '',
  sort: 'name',
  bookmarks: readStorage(storageKeys.bookmarks, []),
  recent: readStorage(storageKeys.recent, []),
  lab: null,
  labTimer: null,
  currentRoute: ''
};

function readStorage(key, fallback) {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return Array.isArray(value) ? value : fallback;
  } catch {
    return fallback;
  }
}

function saveStorage(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* private browsing can deny storage */ }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

function currentPath() {
  const raw = window.location.hash.replace(/^#\/?/, '').replace(/\/$/, '');
  const pathOnly = raw.split('?')[0];
  return pathOnly ? pathOnly.split('/') : [''];
}

function routeName(path = currentPath()) {
  if (!path[0]) return 'home';
  return path[0];
}

function routeLabel(path = currentPath()) {
  if (!path[0]) return 'Overview';
  if (path[0] === 'algorithm') return algorithmsBySlug[path[1]]?.name || 'Algorithm';
  const labels = { home: 'Overview', explore: 'Explore algorithms', dashboard: 'My dashboard', download: 'Android app', about: 'About', docs: 'Documentation' };
  return labels[path[0]] || 'Not found';
}

function updateBreadcrumb(path) {
  breadcrumb.innerHTML = `<span>Workspace</span><span class="breadcrumb-separator">/</span><strong>${escapeHtml(routeLabel(path))}</strong>`;
}

function setSearch(value = '') {
  state.query = value;
  if (globalSearch) globalSearch.value = value;
}

function showToast(message, tone = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast ${tone}`;
  toast.innerHTML = `<span class="toast-icon">${tone === 'error' ? '!' : '✓'}</span><span>${escapeHtml(message)}</span>`;
  toastRegion.append(toast);
  window.setTimeout(() => toast.remove(), 3200);
}

function isBookmarked(slug) { return state.bookmarks.includes(slug); }

function toggleBookmark(slug) {
  if (isBookmarked(slug)) {
    state.bookmarks = state.bookmarks.filter((item) => item !== slug);
    showToast('Removed from your saved algorithms.');
  } else {
    state.bookmarks = [slug, ...state.bookmarks];
    showToast('Saved to your dashboard.');
  }
  saveStorage(storageKeys.bookmarks, state.bookmarks);
  updateSavedDot();
}

function updateSavedDot() {
  savedDot?.classList.toggle('visible', state.bookmarks.length > 0);
}

function setSidebarOpen(open) {
  sidebar.classList.toggle('open', open);
  document.querySelector('#menu-toggle')?.setAttribute('aria-expanded', String(open));
}

function recordRecent(slug) {
  state.recent = [slug, ...state.recent.filter((item) => item !== slug)].slice(0, 6);
  saveStorage(storageKeys.recent, state.recent);
}

function openAlgorithm(slug) {
  if (!algorithmsBySlug[slug]) return;
  recordRecent(slug);
  window.location.hash = `#/algorithm/${slug}`;
}

function categoryCount(id) { return algorithms.filter((algorithm) => algorithm.category === id).length; }

function categoryMark(id) {
  return categoryInfo(id).icon;
}

function renderSidebar() {
  const list = document.querySelector('#collection-list');
  if (!list) return;
  list.innerHTML = categories.filter((category) => category.id !== 'all').slice(0, 9).map((category) => `
    <a class="collection-item" href="#/explore?category=${encodeURIComponent(category.id)}">
      <span class="collection-icon">${escapeHtml(category.icon)}</span><span>${escapeHtml(category.label)}</span><span class="collection-count">${categoryCount(category.id)}</span>
    </a>`).join('');
  document.querySelector('#algorithm-count').textContent = algorithms.length;
  document.querySelectorAll('[data-nav]').forEach((link) => {
    const active = link.dataset.nav === routeName();
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
}

function iconForAlgorithm(algorithm) {
  return categoryMark(algorithm.category);
}

function complexityChips(algorithm) {
  return `<span>${escapeHtml(algorithm.complexity.time)}</span><span>${escapeHtml(algorithm.complexity.space)}</span>`;
}

function algorithmCard(algorithm) {
  const saved = isBookmarked(algorithm.slug);
  return `<article class="algorithm-card card-flat">
    <div class="algorithm-card-top"><span class="algorithm-mark">${escapeHtml(iconForAlgorithm(algorithm))}</span><button class="bookmark-button ${saved ? 'saved' : ''}" data-bookmark="${escapeHtml(algorithm.slug)}" aria-label="${saved ? 'Remove' : 'Save'} ${escapeHtml(algorithm.name)}">${saved ? '♥' : '♡'}</button></div>
    <h3>${escapeHtml(algorithm.name)}</h3>
    <p>${escapeHtml(algorithm.description)}</p>
    <div class="algorithm-card-meta">${complexityChips(algorithm)}</div>
    <div class="algorithm-card-footer"><span>${escapeHtml(algorithm.categoryLabel)}${algorithm.interactive ? ' · <b class="interactive-badge">Interactive</b>' : ''}</span><a href="#/algorithm/${escapeHtml(algorithm.slug)}">Open lesson&nbsp; ↗</a></div>
  </article>`;
}

function featuredCard(algorithm) {
  return `<a class="featured-card card-flat" href="#/algorithm/${escapeHtml(algorithm.slug)}"><div class="card-top"><span class="chip chip-accent">${escapeHtml(algorithm.categoryLabel)}</span><span class="algotype">${algorithm.interactive ? 'Interactive lab' : 'Guided lesson'}</span></div><h3>${escapeHtml(algorithm.name)}</h3><p>${escapeHtml(algorithm.description)}</p><div class="card-link"><span>Explore concept</span><span>→</span></div><i class="featured-glow"></i></a>`;
}

function renderOverview() {
  const categoryCards = categories.filter((category) => category.id !== 'all').slice(0, 8).map((category) => `<a class="category-card card-flat" href="#/explore?category=${encodeURIComponent(category.id)}"><div><span class="category-card-icon">${escapeHtml(category.icon)}</span><strong>${escapeHtml(category.label)}</strong><p>${escapeHtml(category.description)}</p></div><div class="category-card-footer"><span>${categoryCount(category.id)} modules</span><span>↗</span></div></a>`).join('');
  const featured = ['bubble-sort', 'binary-search', 'dijkstra'].map((slug) => featuredCard(algorithmsBySlug[slug])).join('');
  root.innerHTML = `
    <section class="overview-hero">
      <div class="hero-copy"><span class="eyebrow">Algorithm learning cockpit</span><h1>Turn complex algorithms into <span>clear understanding.</span></h1><p class="lede">Explore a verified collection of data structures and algorithms, see the idea in motion, and build intuition you can carry into your next problem.</p><div class="button-row"><a class="button button-primary" href="#/explore">Explore algorithms <span>↗</span></a><a class="button button-secondary" href="#/download">Download Android app <span>↓</span></a></div><div class="hero-meta"><span><strong>${algorithms.length}</strong> learning modules</span><i class="hero-meta-divider"></i><span><strong>3</strong> languages per module</span><i class="hero-meta-divider"></i><span><strong>0</strong> fake demos</span></div></div>
      <div class="hero-visual">
        <div class="hero-visual-header"><span>algorithm_trace / bubble_sort.py</span><span class="live-label">Live concept</span></div>
        <div class="hero-visual-body">
          <div class="code-preview">
            <div class="code-preview-head"><i class="code-dot"></i><i class="code-dot"></i><i class="code-dot"></i><span>trace.py</span></div>
            <pre><span class="token-purple">for</span> end <span class="token-purple">in</span> <span class="token-cyan">range</span>(len(values) - 1, 0, -1):
    <span class="token-purple">for</span> index <span class="token-purple">in</span> <span class="token-cyan">range</span>(end):
        <span class="token-purple">if</span> values[index] &gt; values[index + 1]:
            values[index], values[index + 1] = values[index + 1], values[index]</pre>
          </div>
          <div class="trace-preview">
            <div class="trace-preview-heading"><span>Current pass</span><span>3 comparisons</span></div>
            <div class="trace-bars" aria-label="Bubble sort example: 7, 3, 5, 1, 8, 2">
              <i style="--bar-height:72%"></i><i class="active" style="--bar-height:38%"></i><i class="active" style="--bar-height:58%"></i><i style="--bar-height:22%"></i><i class="settled" style="--bar-height:88%"></i><i style="--bar-height:48%"></i>
            </div>
            <div class="trace-legend"><span><i></i>Comparing</span><span><i></i>Settled</span></div>
          </div>
        </div>
      </div>
    </section>
    <section class="overview-grid"><div class="stats-row"><div class="stat-card card-flat"><div class="stat-top"><span>Verified catalog</span><span class="stat-icon">✦</span></div><strong>${algorithms.length}</strong><small>algorithms across ${categories.length - 1} tracks</small></div><div class="stat-card card-flat"><div class="stat-top"><span>Interactive labs</span><span class="stat-icon">◌</span></div><strong>${algorithms.filter((algorithm) => algorithm.interactive).length}</strong><small>tested step-by-step demos</small></div><div class="stat-card card-flat"><div class="stat-top"><span>Source languages</span><span class="stat-icon">⌘</span></div><strong>03</strong><small>Python · Java · C</small></div></div><div class="roadmap-card card-flat"><h3>A focused route through the repo</h3><p>A compact path for moving from intuition to harder constraints without losing the thread.</p><div class="roadmap-row"><span class="roadmap-number">01</span><div><strong>Foundations</strong><span>arrays, strings, sorting</span></div><div class="roadmap-progress"><i style="width:100%"></i></div></div><div class="roadmap-row"><span class="roadmap-number">02</span><div><strong>Structures</strong><span>lists, stacks, trees, heaps</span></div><div class="roadmap-progress"><i style="width:72%"></i></div></div><div class="roadmap-row"><span class="roadmap-number">03</span><div><strong>Strategy</strong><span>graphs, greedy, dynamic programming</span></div><div class="roadmap-progress"><i style="width:38%"></i></div></div></div></section>
    <section class="content-section"><div class="section-heading"><div><span class="eyebrow">Map the territory</span><h2>Choose a mental model.</h2><p>Browse the real categories already present in the repository.</p></div><a class="button button-ghost" href="#/explore">View all ${algorithms.length} modules →</a></div><div class="category-grid">${categoryCards}</div></section>
    <section class="content-section"><div class="section-heading"><div><span class="eyebrow">Start with a trace</span><h2>Concepts worth seeing move.</h2><p>These labs expose state changes rather than only printing a final answer.</p></div></div><div class="featured-grid">${featured}</div></section>
    <section class="download-strip"><div><span class="eyebrow">Take the cockpit with you</span><h2>A focused Android companion is in the build lane.</h2><p>The native app mirrors the dark learning workspace and keeps bookmarks local. The first installable release is clearly tracked instead of hidden behind a fake download.</p><a class="button button-secondary" href="#/download">See release status <span>→</span></a></div><div class="download-visual"><div class="phone-frame"><div class="phone-notch"></div><img src="./assets/mark.svg" alt="Algo-Mastery app icon" /><i class="phone-line"></i><i class="phone-line"></i><i class="phone-line"></i></div></div></section>`;
}

function filteredAlgorithms() {
  const query = state.query.trim().toLowerCase();
  let result = algorithms.filter((algorithm) => {
    const categoryMatch = state.selectedCategory === 'all' || algorithm.category === state.selectedCategory;
    const textMatch = !query || [algorithm.name, algorithm.description, algorithm.categoryLabel, algorithm.example].join(' ').toLowerCase().includes(query);
    return categoryMatch && textMatch;
  });
  if (state.sort === 'category') result = [...result].sort((a, b) => a.categoryLabel.localeCompare(b.categoryLabel) || a.name.localeCompare(b.name));
  if (state.sort === 'complexity') result = [...result].sort((a, b) => a.complexity.time.localeCompare(b.complexity.time) || a.name.localeCompare(b.name));
  if (state.sort === 'saved') result = [...result].sort((a, b) => Number(isBookmarked(b.slug)) - Number(isBookmarked(a.slug)) || a.name.localeCompare(b.name));
  return result;
}

function renderExplore() {
  const result = filteredAlgorithms();
  const categoryPills = categories.map((category) => `<button class="category-pill ${state.selectedCategory === category.id ? 'active' : ''}" data-category="${escapeHtml(category.id)}" aria-pressed="${state.selectedCategory === category.id}"><span>${escapeHtml(category.icon)}</span>${escapeHtml(category.label)}<span class="pill-count">${category.id === 'all' ? algorithms.length : categoryCount(category.id)}</span></button>`).join('');
  root.innerHTML = `<section class="explore-header"><div><span class="eyebrow">Verified catalog</span><h1>Find your next <span style="color:var(--violet-light)">aha moment.</span></h1><p>Every card maps to a real folder in the repository. Filter the collection by mental model, then open a lesson for contracts, complexity, source links, and—where supported—a working trace.</p></div><div class="explore-summary"><div class="summary-arc"><span>${result.length}<small>shown</small></span></div><span class="muted" style="font-size:10px">of ${algorithms.length}<br />modules</span></div></section><section class="filters-panel"><label class="filter-search" for="catalog-search"><span>⌕</span><input id="catalog-search" type="search" value="${escapeHtml(state.query)}" placeholder="Search by algorithm, category, or idea" autocomplete="off" /></label><label class="select-wrap" for="catalog-sort"><span>↕</span><select id="catalog-sort"><option value="name" ${state.sort === 'name' ? 'selected' : ''}>Sort by name</option><option value="category" ${state.sort === 'category' ? 'selected' : ''}>Sort by category</option><option value="complexity" ${state.sort === 'complexity' ? 'selected' : ''}>Sort by complexity</option><option value="saved" ${state.sort === 'saved' ? 'selected' : ''}>Saved first</option></select></label></section><div class="category-pills">${categoryPills}</div><section class="algorithm-grid">${result.length ? result.map(algorithmCard).join('') : `<div class="empty-state card-flat" style="grid-column:1/-1"><strong>No algorithm matches that search.</strong><p>Try a shorter phrase or reset the category filter to see the full verified catalog.</p><button class="button button-secondary" data-clear-filters>Reset filters</button></div>`}</section>`;
}

const snippets = {
  'bubble-sort': ['def bubble_sort(values):', '    for end in range(len(values) - 1, 0, -1):', '        swapped = False', '        for index in range(end):', '            if values[index] > values[index + 1]:', '                values[index], values[index + 1] = values[index + 1], values[index]', '                swapped = True', '        if not swapped:', '            break', '    return values'],
  'binary-search': ['def binary_search(values, key):', '    left, right = 0, len(values) - 1', '    while left <= right:', '        middle = (left + right) // 2', '        if values[middle] == key:', '            return middle', '        if values[middle] < key:', '            left = middle + 1', '        else:', '            right = middle - 1', '    return -1'],
  'kadane': ['def max_subarray(values):', '    best = current = values[0]', '    for value in values[1:]:', '        current = max(value, current + value)', '        best = max(best, current)', '    return best'],
  'bfs': ['def bfs(vertex_count, edges, source):', '    graph = [[] for _ in range(vertex_count)]', '    for start, end in edges:', '        graph[start].append(end)', '    queue, visited = [source], {source}', '    order = []', '    while queue:', '        vertex = queue.pop(0)', '        order.append(vertex)', '        for neighbor in graph[vertex]:', '            if neighbor not in visited:', '                visited.add(neighbor)', '                queue.append(neighbor)', '    return order']
};

function snippetFor(algorithm) {
  return snippets[algorithm.slug] || [`# ${algorithm.name}`, `# Source: ${algorithm.source}`, '', `# See the repository contract for the complete ${algorithm.name} implementation.`, `# Python · Java · C implementations are kept side by side.`];
}

function codeBlock(algorithm) {
  const lines = snippetFor(algorithm).map((line, index) => `<span class="line-no">${String(index + 1).padStart(2, '0')}</span>${escapeHtml(line)}`).join('\n');
  return `<div class="code-card card-flat"><div class="code-card-header"><span>Python reference shape</span><a href="${escapeHtml(sourceUrl(algorithm))}" target="_blank" rel="noreferrer">Open source ↗</a></div><pre>${lines}</pre></div>`;
}

function conceptCopy(algorithm) {
  const copy = {
    sorting: ['The key idea is a changing invariant: after each pass, one more part of the sequence is known to be in the right place.', 'Use the small example to watch comparisons change the state. The repository implementation keeps signed integers, duplicates, and edge cases explicit.'],
    searching: ['Search algorithms trade preparation for fewer comparisons. Always check the input contract: only Linear Search accepts unsorted values in this repository.', 'The useful question is not only “did we find it?” but “which interval can no longer contain it?”'],
    arrays: ['Array techniques compress a repeated scan into a small amount of state: a running best, a cumulative total, or two moving boundaries.', 'The implementations are deliberately strict about empty inputs, ordering, widths, and index semantics.'],
    strings: ['String matching is a study in reused evidence. A mismatch does not always mean every previous comparison was wasted.', 'Matches are literal, case-sensitive, and overlapping; the detail page follows the repository’s exact contract.'],
    graphs: ['A graph algorithm is a policy for choosing the next frontier. Change the policy and you change what the algorithm can prove.', 'Edges are directed unless the repository contract says otherwise. Negative cycles and unreachable vertices are intentionally surfaced, not hidden.'],
    'dynamic-programming': ['Dynamic programming turns a large search into smaller decisions whose results can be reused.', 'Write down the state meaning first, then the recurrence. The implementation’s bounds and return values are part of the lesson.'],
    backtracking: ['Backtracking explores a decision tree, but the quality of the pruning rule controls whether the search stays teachable.', 'Every solution is validated against the original input contract; no result is fabricated when a board or placement is impossible.']
  };
  return copy[algorithm.category] || ['This lesson is anchored in the runnable implementation already in the repository.', 'Read the contract first, trace a small example, and then open the matching Python, Java, or C source.'];
}

function detailLab(algorithm) {
  if (!algorithm.interactive) return '';
  const intro = algorithm.interactive === 'sort' ? 'Use play, pause, and step to watch adjacent comparisons move the sorted boundary.' : algorithm.interactive === 'binary' ? 'Change the key and step through the shrinking interval on a sorted array.' : algorithm.interactive === 'kadane' ? 'Trace the current best ending at each value and the global best seen so far.' : 'Explore the queue frontier as the graph is visited layer by layer.';
  return `<section class="lab-card card learning-card" data-lab="${escapeHtml(algorithm.interactive)}" data-slug="${escapeHtml(algorithm.slug)}"><div class="lab-head"><div><h3>Interactive trace</h3><p>${intro}</p></div><div class="lab-controls"><button class="lab-control" data-lab-action="reset" aria-label="Reset trace">↺</button><button class="lab-control" data-lab-action="step" aria-label="Step forward">›</button><button class="lab-control primary" data-lab-action="play">▶ <span>Play trace</span></button></div></div>${labMarkup(algorithm)}</section>`;
}

function labMarkup(algorithm) {
  if (algorithm.interactive === 'sort') return `<div class="lab-body"><div class="lab-input-row"><div class="field field-array"><label for="lab-sort-array">Array values</label><input id="lab-sort-array" value="7, 3, 5, 1, 8, 2" inputmode="numeric" aria-label="Comma separated array values" /></div><button class="button button-secondary" data-lab-action="apply">Apply input</button></div><p class="lab-message" data-lab-message>Ready to trace a bubble sort pass.</p><div class="bars-stage" data-lab-stage></div><div class="timeline"><span data-lab-step>Step 0 / 0</span><div class="timeline-track"><i data-lab-progress></i></div><div class="speed-wrap"><span>Speed</span><input data-lab-speed type="range" min="250" max="1200" step="50" value="650" /></div></div></div>`;
  if (algorithm.interactive === 'binary') return `<div class="lab-body"><div class="lab-input-row"><div class="field field-array"><label for="lab-binary-array">Sorted values</label><input id="lab-binary-array" value="2, 4, 7, 11, 15, 20, 29" inputmode="numeric" /></div><div class="field" style="width:100px"><label for="lab-binary-target">Target</label><input id="lab-binary-target" value="15" inputmode="numeric" /></div><button class="button button-secondary" data-lab-action="apply">Apply input</button></div><p class="lab-message" data-lab-message>Ready to narrow the search window.</p><div class="search-lab"><div class="search-values" data-lab-stage></div><div class="lab-progress-note" data-lab-note>Step through the first comparison.</div></div><div class="timeline"><span data-lab-step>Step 0 / 0</span><div class="timeline-track"><i data-lab-progress></i></div></div></div>`;
  if (algorithm.interactive === 'kadane') return `<div class="lab-body"><div class="lab-input-row"><div class="field field-array"><label for="lab-kadane-array">Array values</label><input id="lab-kadane-array" value="-2, 1, -3, 4, -1, 2, 1, -5, 4" inputmode="numeric" /></div><button class="button button-secondary" data-lab-action="apply">Apply input</button></div><p class="lab-message" data-lab-message>Start with the first non-empty value.</p><div class="bars-stage" data-lab-stage></div><div class="timeline"><span data-lab-step>Step 0 / 0</span><div class="timeline-track"><i data-lab-progress></i></div></div></div>`;
  return `<div class="lab-body"><p class="lab-message" data-lab-message>Fixed example graph: edges follow the repository’s directed traversal convention.</p><div class="graph-stage" data-lab-stage></div><div class="timeline"><span data-lab-step>Step 0 / 0</span><div class="timeline-track"><i data-lab-progress></i></div></div></div>`;
}

function detailCopy(algorithm) {
  const [first, second] = conceptCopy(algorithm);
  const steps = algorithm.interactive === 'sort' ? ['Compare adjacent values from left to right.', 'Swap only when the left value is larger.', 'After a pass, the largest remaining value settles at the right edge.', 'Stop early when a pass makes no swaps.'] : algorithm.interactive === 'binary' ? ['Start with the full sorted interval.', 'Inspect the midpoint and compare it to the target.', 'Discard the half that cannot contain the target.', 'Return the index or -1 when the interval is empty.'] : algorithm.interactive === 'bfs' ? ['Seed a queue with the source vertex.', 'Remove the oldest vertex and inspect neighbors in input order.', 'Queue each unseen neighbor exactly once.', 'The visit order records layers from the source.'] : algorithm.interactive === 'kadane' ? ['Initialize the current and global best with the first value.', 'Choose between starting fresh or extending the current segment.', 'Update the global best after each position.', 'Keep the non-empty contract visible for all-negative input.'] : ['Read the contract and identify the state represented by each variable.', 'Trace the smallest useful example by hand.', 'Compare the invariant against the source implementation.', 'Test the documented boundary cases.'];
  return `<div class="concept-grid"><div class="concept-block"><h3>The mental model</h3><p>${escapeHtml(first)}</p></div><div class="concept-block"><h3>What to watch</h3><p>${escapeHtml(second)}</p></div></div><div style="height:18px"></div><h3>Trace it in four moves</h3><ol class="steps-list">${steps.map((step, index) => `<li><span class="step-number">${index + 1}</span><span>${escapeHtml(step)}</span></li>`).join('')}</ol>`;
}

function contractBullets(algorithm) {
  const common = ['Zero-based indices and return values follow the repository contract.', 'Inputs are validated before the algorithm mutates or reports a result.', 'Python, Java, and C versions are kept as independent implementations.'];
  const extra = algorithm.category === 'searching' ? 'Binary, jump, interpolation, and exponential search require ascending input.' : algorithm.category === 'graphs' ? 'Graph validation includes unreachable edges, cycles, and negative-edge rules.' : algorithm.category === 'sorting' ? 'Radix Sort accepts non-negative integers; Counting Sort uses a bounded value range.' : algorithm.category === 'strings' ? 'Matching is literal, case-sensitive, and includes overlapping matches.' : algorithm.category === 'trees' ? 'Tree height and diameter count edges, not nodes.' : 'Read the category README for exact limits and language-specific status codes.';
  return [...common, extra];
}

function renderAlgorithmDetail(slug) {
  const algorithm = algorithmsBySlug[slug];
  if (!algorithm) return renderNotFound();
  state.currentRoute = slug;
  const saved = isBookmarked(slug);
  const bullets = contractBullets(algorithm).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  root.innerHTML = `<a class="detail-back" href="#/explore">← Back to explorer</a><section class="detail-header"><div><span class="eyebrow">${escapeHtml(algorithm.categoryLabel)} / verified lesson</span><h1>${escapeHtml(algorithm.name)}</h1><p class="lede">${escapeHtml(algorithm.description)} ${escapeHtml(algorithm.example)}</p></div><div class="detail-actions"><button class="large-bookmark ${saved ? 'saved' : ''}" data-bookmark="${escapeHtml(algorithm.slug)}">${saved ? '♥ Saved' : '♡ Save lesson'}</button><a class="button button-primary" href="${escapeHtml(sourceUrl(algorithm))}" target="_blank" rel="noreferrer">Open source ↗</a></div></section><div class="detail-layout"><div><section class="learning-card card-flat"><div class="detail-tabs"><button class="detail-tab active">Concept</button><button class="detail-tab">Contract</button><button class="detail-tab">Source map</button></div>${detailCopy(algorithm)}</section>${detailLab(algorithm)}<div style="height:17px"></div>${codeBlock(algorithm)}</div><aside class="detail-side"><section class="complexity-card card-flat"><h3>Complexity profile</h3><div class="complexity-list"><div class="complexity-item"><span>Time</span><strong>${escapeHtml(algorithm.complexity.time)}</strong></div><div class="complexity-item"><span>Extra space</span><strong>${escapeHtml(algorithm.complexity.space)}</strong></div><div class="complexity-item"><span>Best case</span><strong>${escapeHtml(algorithm.complexity.best)}</strong></div></div></section><section class="contract-card card-flat"><h3>Contract notes</h3><p>Use the details as a guardrail when experimenting. This page only exposes behavior verified in the repository documentation and tests.</p><ul class="contract-list">${bullets}</ul></section><section class="source-card card-flat"><h3>Three-language source</h3><p>The same topic is available as standalone Python, Java, and C examples.</p><div class="source-links"><a class="source-link" href="${escapeHtml(sourceUrl(algorithm))}" target="_blank" rel="noreferrer"><span>Python implementation</span><span>↗</span></a><a class="source-link" href="${escapeHtml(languageSourceUrl(algorithm, 'java'))}" target="_blank" rel="noreferrer"><span>Java implementation</span><span>↗</span></a><a class="source-link" href="${escapeHtml(languageSourceUrl(algorithm, 'c'))}" target="_blank" rel="noreferrer"><span>C implementation</span><span>↗</span></a></div></section></aside></div>`;
  if (algorithm.interactive) initializeLab(algorithm);
}

function parseNumbers(raw, { sorted = false } = {}) {
  const values = String(raw).split(',').map((value) => value.trim()).filter(Boolean).map(Number);
  if (!values.length || values.some((value) => !Number.isInteger(value) || !Number.isSafeInteger(value))) throw new Error('Use a comma-separated list of safe integers.');
  if (sorted && values.some((value, index) => index > 0 && value < values[index - 1])) throw new Error('Binary search needs ascending input.');
  return values;
}

function labStateFor(algorithm) {
  if (state.lab?.slug === algorithm.slug) return state.lab;
  const stateByType = { sort: { slug: algorithm.slug, type: 'sort', values: [7, 3, 5, 1, 8, 2], steps: sortSteps([7, 3, 5, 1, 8, 2]), index: 0 }, binary: { slug: algorithm.slug, type: 'binary', values: [2, 4, 7, 11, 15, 20, 29], target: 15, steps: binarySteps([2, 4, 7, 11, 15, 20, 29], 15), index: 0 }, kadane: { slug: algorithm.slug, type: 'kadane', values: [-2, 1, -3, 4, -1, 2, 1, -5, 4], steps: kadaneSteps([-2, 1, -3, 4, -1, 2, 1, -5, 4]), index: 0 }, bfs: { slug: algorithm.slug, type: 'bfs', steps: bfsSteps(), index: 0 } };
  state.lab = stateByType[algorithm.interactive];
  return state.lab;
}

function initializeLab(algorithm) {
  const labState = labStateFor(algorithm);
  renderLabState(algorithm, labState);
}

function renderLabState(algorithm, labState) {
  const lab = document.querySelector(`[data-lab][data-slug="${CSS.escape(algorithm.slug)}"]`);
  if (!lab) return;
  const step = labState.steps[Math.min(labState.index, labState.steps.length - 1)];
  const stage = lab.querySelector('[data-lab-stage]');
  const message = lab.querySelector('[data-lab-message]');
  const stepLabel = lab.querySelector('[data-lab-step]');
  const progress = lab.querySelector('[data-lab-progress]');
  stage.dataset.step = String(labState.index);
  const percent = labState.steps.length <= 1 ? 100 : (labState.index / (labState.steps.length - 1)) * 100;
  if (stepLabel) stepLabel.textContent = `Step ${labState.index} / ${labState.steps.length - 1}`;
  if (progress) progress.style.width = `${percent}%`;
  if (labState.type === 'sort' || labState.type === 'kadane') {
    const max = Math.max(...step.values.map((value) => Math.abs(value)), 1);
    stage.innerHTML = step.values.map((value, index) => {
      const active = step.active?.includes(index) || labState.type === 'kadane' && index === step.index;
      const settled = step.sorted?.includes(index) || labState.type === 'kadane' && index <= step.index;
      return `<div class="bar-column ${active ? 'active' : ''} ${settled ? 'settled' : ''}" style="--bar-height:${Math.max(8, Math.abs(value) / max * 132)}px;--bar-index:${index}" title="Index ${index}: ${value}"><span class="bar-value">${escapeHtml(value)}</span><i class="bar ${active ? 'active' : ''} ${settled ? 'sorted' : ''}"></i><span class="bar-index">${index}</span></div>`;
    }).join('');
    if (message) message.textContent = labState.type === 'kadane' ? `At index ${step.index}: current = ${step.current}, best = ${step.best}.` : labState.index === labState.steps.length - 1 ? 'Sorted. The invariant holds across the full array.' : 'The highlighted pair is the current comparison.';
  } else if (labState.type === 'binary') {
    stage.innerHTML = step.values.map((value, index) => `<span class="search-value ${index === step.result ? 'found' : ''} ${index === step.middle ? 'mid' : ''} ${index >= step.left && index <= step.right ? '' : 'skipped'}" style="--tile-index:${index}" aria-label="${value}${index === step.middle ? ', midpoint' : ''}${index === step.result ? ', target found' : ''}">${escapeHtml(value)}<small>${index}</small></span>`).join('');
    const note = lab.querySelector('[data-lab-note]'); if (note) note.textContent = step.note;
    if (message) message.textContent = step.result >= 0 ? `Found at zero-based index ${step.result}.` : step.middle >= 0 ? `Window: ${step.left}…${step.right}.` : 'Search exhausted without a match.';
  } else {
    const viewBox = '0 0 100 100';
    const edgeKey = (edge) => edge ? `${edge[0]}-${edge[1]}` : '';
    const activeEdge = edgeKey(step.edge);
    stage.innerHTML = `<svg viewBox="${viewBox}" role="img" aria-label="Breadth-first search graph">${graphFixture.edges.map(([from, to]) => { const start = graphFixture.nodes[from]; const end = graphFixture.nodes[to]; return `<line class="graph-edge ${activeEdge === `${from}-${to}` ? 'active' : ''}" x1="${start.x}" y1="${start.y}" x2="${end.x}" y2="${end.y}" />`; }).join('')}${graphFixture.nodes.map((node) => `<g class="graph-node ${step.current === node.id ? 'active' : ''} ${step.visited.includes(node.id) ? 'visited' : ''}" transform="translate(${node.x} ${node.y})"><circle r="7"></circle><text y=".5">${node.id}</text></g>`).join('')}</svg>`;
    if (message) message.textContent = step.note;
  }
}

function resetLabFromInputs(algorithm) {
  try {
    if (algorithm.interactive === 'sort') { const values = parseNumbers(document.querySelector('#lab-sort-array')?.value); state.lab = { slug: algorithm.slug, type: 'sort', values, steps: sortSteps(values), index: 0 }; }
    if (algorithm.interactive === 'binary') { const values = parseNumbers(document.querySelector('#lab-binary-array')?.value, { sorted: true }); const target = Number(document.querySelector('#lab-binary-target')?.value); if (!Number.isInteger(target)) throw new Error('Target must be an integer.'); state.lab = { slug: algorithm.slug, type: 'binary', values, target, steps: binarySteps(values, target), index: 0 }; }
    if (algorithm.interactive === 'kadane') { const values = parseNumbers(document.querySelector('#lab-kadane-array')?.value); state.lab = { slug: algorithm.slug, type: 'kadane', values, steps: kadaneSteps(values), index: 0 }; }
    stopLabTimer(); renderLabState(algorithm, state.lab); const message = document.querySelector(`[data-slug="${CSS.escape(algorithm.slug)}"] [data-lab-message]`); if (message) { message.classList.remove('error'); }
  } catch (error) { const message = document.querySelector(`[data-slug="${CSS.escape(algorithm.slug)}"] [data-lab-message]`); if (message) { message.textContent = error.message; message.classList.add('error'); } }
}

function stopLabTimer() { if (state.labTimer) { window.clearInterval(state.labTimer); state.labTimer = null; } }

function playLab(algorithm) {
  stopLabTimer();
  const lab = document.querySelector(`[data-lab][data-slug="${CSS.escape(algorithm.slug)}"]`);
  const speed = Number(lab?.querySelector('[data-lab-speed]')?.value || 650);
  state.labTimer = window.setInterval(() => { if (!state.lab || state.lab.index >= state.lab.steps.length - 1) { stopLabTimer(); return; } state.lab.index += 1; renderLabState(algorithm, state.lab); }, Math.max(150, 1300 - speed));
}

function renderDashboard() {
  const bookmarked = state.bookmarks.map((slug) => algorithmsBySlug[slug]).filter(Boolean);
  const recent = state.recent.map((slug) => algorithmsBySlug[slug]).filter(Boolean);
  const recentMarkup = recent.length ? recent.map((algorithm) => `<a class="recent-item" href="#/algorithm/${escapeHtml(algorithm.slug)}"><span class="recent-icon">${escapeHtml(iconForAlgorithm(algorithm))}</span><span><strong>${escapeHtml(algorithm.name)}</strong><span>${escapeHtml(algorithm.categoryLabel)} · ${algorithm.interactive ? 'interactive lab' : 'guided lesson'}</span></span><span class="recent-arrow">→</span></a>`).join('') : `<div class="empty-state" style="padding:28px 10px"><strong>Your trail is empty.</strong><p>Open any lesson and it will appear here for quick return.</p><a class="button button-secondary" href="#/explore">Explore the catalog</a></div>`;
  const savedMarkup = bookmarked.length ? bookmarked.map(algorithmCard).join('') : `<div class="empty-state" style="grid-column:1/-1;padding:28px 10px"><strong>Save the ideas you want to revisit.</strong><p>Bookmarks stay in this browser only—no account or fake sync layer required.</p></div>`;
  root.innerHTML = `<section class="dashboard-header"><div><span class="eyebrow">Personal workspace</span><h1>Your learning trail.</h1><p>Local-only progress signals, built from what you actually explore.</p></div><a class="button button-primary" href="#/explore">Find a module <span>↗</span></a></section><section class="dashboard-grid"><section class="dashboard-card card-flat"><div class="dashboard-card-header"><div><h3>Recently explored</h3><p>Continue from the last concepts you opened.</p></div><span class="chip chip-cyan">${recent.length} recent</span></div><div class="recent-list">${recentMarkup}</div></section><section class="dashboard-card card-flat"><div class="dashboard-card-header"><div><h3>Workspace signals</h3><p>Honest counts from this browser session.</p></div><span class="chip chip-green">Local</span></div><div class="metric-grid"><div class="metric"><strong>${state.bookmarks.length}</strong><span>saved lessons</span></div><div class="metric"><strong>${recent.length}</strong><span>recent lessons</span></div><div class="metric"><strong>${algorithms.filter((algorithm) => algorithm.interactive).length}</strong><span>labs available</span></div></div><div style="height:18px"></div><p class="muted" style="font-size:10px;line-height:1.55;margin:0">No learning streak, score, or social activity is invented here. The dashboard reflects only actions you take in this browser.</p></section><section class="dashboard-card dashboard-card-wide card-flat"><div class="dashboard-card-header"><div><h3>Saved algorithms</h3><p>Pin a lesson from the explorer to keep its source and complexity close.</p></div><a class="button button-ghost" href="#/explore">Browse all →</a></div><div class="bookmark-grid">${savedMarkup}</div></section></section>`;
}

function renderDownload() {
  const releaseReady = product.release.status === 'released' && product.release.apkUrl;
  root.innerHTML = `<section class="download-page-header"><div><span class="eyebrow">Native Android companion</span><h1>Keep the logic <span style="color:var(--cyan)">close at hand.</span></h1><p>The Android application is a native Java learning workspace with the same visual language, local bookmarks, algorithm catalog, and mobile-first navigation. This page reports the release state honestly while the signed artifact is prepared.</p></div><div class="app-preview"><div class="app-icon-large"><img src="./assets/mark.svg" alt="Algo-Mastery app icon" /></div></div></section><section class="release-card card-flat"><div><span class="chip ${releaseReady ? 'chip-green' : 'chip-accent'}">${releaseReady ? 'Release available' : 'Development build lane'}</span><h2>${releaseReady ? 'Install the verified Android release.' : 'The first APK is not published yet.'}</h2><p>${releaseReady ? 'Download the real GitHub Release asset below. The version, package identifier, and checksum are sourced from the central release metadata.' : 'The repository contains the Android project and reproducible build instructions, but no public release asset is claimed until an APK is actually built and uploaded.'}</p><div class="button-row"><a class="button button-primary" ${releaseReady ? `href="${escapeHtml(product.release.apkUrl)}" download` : 'aria-disabled="true"'} ${releaseReady ? '' : 'tabindex="-1"'}>${releaseReady ? 'Download APK ↓' : 'APK pending release'}</a><a class="button button-secondary" href="#/docs">Read build instructions ↗</a></div></div><div class="release-meta"><div class="release-meta-row"><span>Version</span><strong>${escapeHtml(product.release.version)}${releaseReady ? '' : ' · dev'}</strong></div><div class="release-meta-row"><span>Package</span><strong>${escapeHtml(product.packageName)}</strong></div><div class="release-meta-row"><span>Artifact</span><strong>${escapeHtml(product.release.fileName)}</strong></div><div class="release-meta-row"><span>Size</span><strong>${escapeHtml(product.release.size)}</strong></div><div class="release-meta-row"><span>Integrity</span><strong>${escapeHtml(product.release.checksum)}</strong></div></div></section><section class="install-grid"><article class="install-card card-flat"><span class="install-number">01</span><h3>Build locally</h3><p>Install the Android SDK and run the Gradle wrapper from <code>android/</code>. Debug output is separated from the web source tree.</p></article><article class="install-card card-flat"><span class="install-number">02</span><h3>Verify the package</h3><p>Use <code>aapt dump badging</code> or <code>apkanalyzer</code> to confirm the package identifier, version, and launcher icon.</p></article><article class="install-card card-flat"><span class="install-number">03</span><h3>Publish a release</h3><p>Upload the real APK as a GitHub Release asset, add the URL and checksum to <code>web/catalog.mjs</code>, then rebuild the static site.</p></article></section>`;
}

function renderDocs() {
  root.innerHTML = `<section class="explore-header"><div><span class="eyebrow">Make it reproducible</span><h1>Build notes, not promises.</h1><p>Algo-Mastery keeps the original standalone algorithm collection intact, adds a static browser experience on top, and includes a native Android project for the core learning flow.</p></div></section><div class="docs-layout"><nav class="docs-nav card-flat"><a class="active" href="#docs-architecture">Architecture</a><a href="#docs-web">Web checks</a><a href="#docs-android">Android build</a><a href="#docs-release">APK release</a><a href="#docs-deploy">Deployment</a></nav><article class="docs-content card-flat"><h2 id="docs-architecture">Architecture</h2><p>The original repository is a framework-free collection of <strong>56 algorithm folders</strong> with Python, Java, and C implementations plus 182 Python tests. The web layer is intentionally dependency-light: static HTML, CSS, and ES modules in <code>web/</code>. Its catalog is derived from those real source paths, and interactive labs reimplement only a small set of well-tested teaching traces in the browser.</p><p>The Android companion is a native Java app in <code>android/</code>. It does not pretend to be a WebView wrapper: it has a native catalog, detail screens, local bookmarks, and a small bubble-sort trace that works without a network connection.</p><h2 id="docs-web">Web checks</h2><ul><li><code>npm run test</code> checks catalog completeness and pure visualization step generators.</li><li><code>npm run build</code> copies the static site to <code>web/dist/</code> and writes a build manifest.</li><li><code>python -m pytest -q</code> remains the repository’s required algorithm regression check.</li><li><code>python tools/check_examples.py</code> compiles and exercises all 168 language examples when C and Java are available.</li></ul><h2 id="docs-android">Android build</h2><p>From the repository root: <code>cd android</code>, then <code>./gradlew assembleDebug</code> (or <code>gradlew.bat assembleDebug</code> on Windows). The expected debug artifact is <code>android/app/build/outputs/apk/debug/app-debug.apk</code>. Release signing is intentionally not committed; use a private keystore outside version control for a public release.</p><h2 id="docs-release">APK release</h2><p>After a real build, calculate a checksum with <code>sha256sum app-debug.apk</code>, rename or sign the artifact for the release channel, and upload it to a GitHub Release. Update <code>product.release</code> in <code>web/catalog.mjs</code> with the release asset URL, version, size, and checksum. Then run <code>npm run build</code> so the download page points to the real asset.</p><h2 id="docs-deploy">Deployment</h2><p>Deploy <code>web/dist/</code> to any static host. Configure SPA fallback to <code>index.html</code> so hash routes and direct refreshes remain safe. GitHub Pages, Netlify, and Vercel can serve this folder without a server runtime. The APK itself belongs in a release asset, not in a fake empty download endpoint.</p></article></div>`;
}

function renderAbout() {
  root.innerHTML = `<section class="overview-hero" style="min-height:380px"><div><span class="eyebrow">A practical learning brand</span><h1>Premium enough for focus. Clear enough for beginners.</h1><p class="lede">Algo-Mastery is a visual layer over a carefully tested algorithm repository. It makes the code easier to enter without hiding the contracts, edge cases, or implementation choices that matter.</p><div class="button-row"><a class="button button-primary" href="#/explore">Explore the catalog ↗</a><a class="button button-secondary" href="${escapeHtml(product.repository)}" target="_blank" rel="noreferrer">Source repository ↗</a></div></div><div class="hero-visual" style="min-height:320px"><div class="hero-visual-header"><span>brand_system / algo-mastery</span><span class="live-label">Original mark</span></div><div style="display:grid;place-items:center;height:250px"><img src="./assets/logo.svg" style="width:min(80%,330px)" alt="Algo-Mastery logo" /></div></div></section><section class="content-section"><div class="section-heading"><div><span class="eyebrow">Design principles</span><h2>Quiet confidence, visible logic.</h2></div></div><div class="featured-grid"><article class="featured-card card-flat"><span class="chip chip-accent">01 / Preserve</span><h3>Keep the real source close.</h3><p>Every lesson links back to the exact Python, Java, and C file in the repository.</p></article><article class="featured-card card-flat"><span class="chip chip-cyan">02 / Explain</span><h3>Show the invariant.</h3><p>Interactive traces focus on state transitions, not decorative animation or fake progress.</p></article><article class="featured-card card-flat"><span class="chip chip-green">03 / Verify</span><h3>Tell the truth about release state.</h3><p>APK and deployment claims are marked as pending until their artifacts actually exist.</p></article></div></section>`;
}

function renderNotFound() {
  root.innerHTML = `<section class="not-found"><div><div class="not-found-mark">404</div><h2>That branch does not exist.</h2><p>The route is outside the current learning graph. Return to the overview or search the verified catalog.</p><div class="button-row" style="justify-content:center"><a class="button button-primary" href="#/">Back to overview</a><a class="button button-secondary" href="#/explore">Explore modules</a></div></div></section>`;
}

function parseExploreQuery(path) {
  if (path[0] !== 'explore') return;
  const queryIndex = window.location.hash.indexOf('?');
  if (queryIndex < 0) return;
  const params = new URLSearchParams(window.location.hash.slice(queryIndex + 1));
  if (categories.some((category) => category.id === params.get('category'))) state.selectedCategory = params.get('category');
}

function render() {
  stopLabTimer();
  const path = currentPath();
  parseExploreQuery(path);
  updateBreadcrumb(path);
  renderSidebar();
  if (routeName(path) !== 'algorithm') state.lab = null;
  switch (routeName(path)) {
    case 'home': renderOverview(); break;
    case 'explore': renderExplore(); break;
    case 'algorithm': renderAlgorithmDetail(path[1]); break;
    case 'dashboard': renderDashboard(); break;
    case 'download': renderDownload(); break;
    case 'docs': renderDocs(); break;
    case 'about': renderAbout(); break;
    default: renderNotFound();
  }
  window.scrollTo(0, 0);
  setSidebarOpen(false);
  updateSavedDot();
}

root.addEventListener('click', (event) => {
  const bookmark = event.target.closest('[data-bookmark]');
  if (bookmark) {
    event.preventDefault();
    toggleBookmark(bookmark.dataset.bookmark);
    const path = currentPath();
    if (routeName(path) === 'algorithm') renderAlgorithmDetail(path[1]);
    else if (routeName(path) === 'explore') renderExplore();
    else if (routeName(path) === 'dashboard') renderDashboard();
    return;
  }
  const category = event.target.closest('[data-category]');
  if (category) {
    state.selectedCategory = category.dataset.category;
    renderExplore();
    return;
  }
  if (event.target.closest('[data-clear-filters]')) {
    state.selectedCategory = 'all';
    setSearch('');
    state.sort = 'name';
    renderExplore();
    return;
  }
  const labAction = event.target.closest('[data-lab-action]');
  if (labAction) {
    const path = currentPath();
    const algorithm = algorithmsBySlug[path[1]];
    if (!algorithm?.interactive) return;
    const action = labAction.dataset.labAction;
    if (action === 'apply') resetLabFromInputs(algorithm);
    if (action === 'reset') { state.lab = null; initializeLab(algorithm); }
    if (action === 'step') { stopLabTimer(); if (state.lab.index < state.lab.steps.length - 1) state.lab.index += 1; renderLabState(algorithm, state.lab); }
    if (action === 'play') playLab(algorithm);
  }
});

root.addEventListener('input', (event) => {
  if (event.target.id === 'catalog-search') {
    state.query = event.target.value;
    const cursor = event.target.selectionStart;
    renderExplore();
    const input = document.querySelector('#catalog-search');
    input?.focus({ preventScroll: true });
    if (cursor !== null) input?.setSelectionRange(cursor, cursor);
  }
});

root.addEventListener('change', (event) => {
  if (event.target.id === 'catalog-sort') { state.sort = event.target.value; renderExplore(); }
});

globalSearch?.addEventListener('input', (event) => {
  state.query = event.target.value;
  if (routeName() !== 'explore') window.location.hash = '#/explore';
  else renderExplore();
});

globalSearch?.addEventListener('keydown', (event) => { if (event.key === 'Enter') { window.location.hash = '#/explore'; renderExplore(); } });
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && sidebar.classList.contains('open')) setSidebarOpen(false);
  if (event.key === '/' && !event.target.closest('input, textarea, select, [contenteditable="true"]')) {
    event.preventDefault();
    globalSearch?.focus();
  }
});
document.querySelector('#menu-toggle')?.addEventListener('click', () => setSidebarOpen(true));
document.querySelector('#sidebar-close')?.addEventListener('click', () => setSidebarOpen(false));
document.querySelector('#sidebar-scrim')?.addEventListener('click', () => setSidebarOpen(false));
window.addEventListener('hashchange', render);
window.addEventListener('storage', () => { state.bookmarks = readStorage(storageKeys.bookmarks, []); state.recent = readStorage(storageKeys.recent, []); render(); });

render();
