const vm = require('vm');
const fs = require('fs');

const localStorageData = {};
const mockLocalStorage = {
  getItem: (k) => (k in localStorageData ? localStorageData[k] : null),
  setItem: (k, v) => { localStorageData[k] = String(v); },
  removeItem: (k) => { delete localStorageData[k]; },
  clear: () => { for (const k in localStorageData) delete localStorageData[k]; },
  get length() { return Object.keys(localStorageData).length; },
  key: (i) => Object.keys(localStorageData)[i] || null
};

function createMockElement(id = '', tag = 'DIV') {
  return {
    id,
    tagName: tag.toUpperCase(),
    value: '',
    innerHTML: '',
    textContent: '',
    style: {},
    classList: {
      _classes: new Set(),
      add(c){ this._classes.add(c); },
      remove(c){ this._classes.delete(c); },
      toggle(c, force){ if(force !== undefined) (force ? this._classes.add(c) : this._classes.delete(c)); else (this._classes.has(c)?this._classes.delete(c):this._classes.add(c)); },
      contains(c){ return this._classes.has(c); }
    },
    dataset: {},
    addEventListener: () => {},
    removeEventListener: () => {},
    setAttribute: () => {},
    getAttribute: () => null,
    appendChild: () => {},
    removeChild: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
    focus: () => {},
    blur: () => {},
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 600, right: 800, bottom: 600 })
  };
}

const elementCache = {};
function getEl(id, tag = 'DIV') {
  if (!elementCache[id]) elementCache[id] = createMockElement(id, tag);
  return elementCache[id];
}

const mockDocument = {
  getElementById: (id) => getEl(id),
  querySelector: (sel) => {
    if (sel.startsWith('#')) return getEl(sel.slice(1));
    return createMockElement('', 'DIV');
  },
  querySelectorAll: (sel) => [],
  addEventListener: () => {},
  removeEventListener: () => {},
  documentElement: {
    setAttribute: () => {},
    style: { setProperty: () => {} }
  },
  createElement: (tag) => createMockElement('', tag),
  body: createMockElement('body', 'BODY')
};

const mockWindow = {
  addEventListener: () => {},
  removeEventListener: () => {},
  localStorage: mockLocalStorage,
  document: mockDocument,
  innerWidth: 1200,
  innerHeight: 800,
  setTimeout: (fn, ms) => setTimeout(fn, ms),
  clearTimeout: (t) => clearTimeout(t),
  setInterval: (fn, ms) => setInterval(fn, ms),
  clearInterval: (t) => clearInterval(t),
  Blob: class { constructor(parts){ this.size = parts.join('').length; } },
  getSelection: () => ({ rangeCount: 0 })
};

const electronStorage = {};
const mockStorage = {
  get: async (k) => ({ key: k, value: electronStorage[k] || null }),
  getSync: (k) => ({ key: k, value: electronStorage[k] || null }),
  getAll: async () => Object.assign({}, electronStorage),
  set: async (k, v) => { electronStorage[k] = v; return true; },
  setSync: (k, v) => { electronStorage[k] = v; return true; }
};

const sandbox = {
  window: mockWindow,
  document: mockDocument,
  localStorage: mockLocalStorage,
  storage: mockStorage,
  vantageApp: { isDesktop: true },
  navigator: { userAgent: 'Node-Test' },
  console: console,
  setTimeout: (fn, ms) => setTimeout(fn, ms),
  clearTimeout: (t) => clearTimeout(t),
  setInterval: (fn, ms) => setInterval(fn, ms),
  clearInterval: (t) => clearInterval(t),
  Blob: mockWindow.Blob,
  URL: { createObjectURL: () => 'blob:mock', revokeObjectURL: () => {} },
  location: { reload: () => {} },
  confirm: () => true,
  prompt: () => 'Test',
  requestAnimationFrame: (cb) => setTimeout(cb, 16)
};

sandbox.window.window = sandbox.window;
sandbox.window.storage = mockStorage;
vm.createContext(sandbox);

const html = fs.readFileSync('resources/app/index.html', 'utf-8');
const s_start = html.indexOf('<script>') + 8;
const s_end = html.indexOf('</script>');
const codeToRun = html.substring(s_start, s_end);

try {
  vm.runInContext(codeToRun, sandbox);
  console.log('Script loaded successfully.');
} catch (e) {
  console.error('Failed to load script:', e);
  process.exit(1);
}

try {
  const State = sandbox.window.State;
  const flushAllUnsaved = sandbox.window.flushAllUnsaved;

  // 1. Test Journal Persistence
  State.journal.push({
    id: 'entry-test-1',
    date: '2026-09-28',
    content: 'Case notes for mission critical testing.',
    tags: ['intel', 'vantage']
  });
  console.log('Journal entries count:', State.journal.length);

  // 2. Test Sticky Notes Persistence
  State.sticky.push({
    id: 'sticky-test-1',
    x: 150,
    y: 200,
    w: 220,
    h: 180,
    content: 'Important pin board note',
    color: '#ffe066'
  });
  console.log('Sticky notes count:', State.sticky.length);

  // 3. Test flushAllUnsaved
  flushAllUnsaved();

  if (!electronStorage['journal'] || electronStorage['journal'].length === 0) {
    throw new Error('Journal was not persisted into storage!');
  }
  if (!electronStorage['sticky'] || electronStorage['sticky'].length === 0) {
    throw new Error('Sticky was not persisted into storage!');
  }
  if (!localStorageData['vantage_journal']) {
    throw new Error('Journal was not persisted into localStorage fallback!');
  }
  if (!localStorageData['vantage_sticky']) {
    throw new Error('Sticky was not persisted into localStorage fallback!');
  }

  console.log('JOURNAL & STICKY PERSISTENCE TEST PASSED 100%!');
  process.exit(0);
} catch (e) {
  console.error('TEST FAILED:', e);
  process.exit(1);
}
