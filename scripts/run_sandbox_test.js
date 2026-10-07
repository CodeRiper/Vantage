
const vm = require('vm');
const fs = require('fs');

// Mock browser environment
const localStorageData = {};
const mockLocalStorage = {
  getItem: (k) => localStorageData[k] || null,
  setItem: (k, v) => { localStorageData[k] = String(v); },
  removeItem: (k) => { delete localStorageData[k]; },
  clear: () => { for (const k in localStorageData) delete localStorageData[k]; },
  get length() { return Object.keys(localStorageData).length; },
  key: (i) => Object.keys(localStorageData)[i] || null
};

const domStore = {};
const mockDocument = {
  getElementById: (id) => domStore[id] || { id, style: {}, classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } }, setAttribute(){}, addEventListener(){}, removeEventListener(){}, dataset: {} },
  querySelector: (sel) => ({ id: sel, style: {}, classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } }, setAttribute(){}, addEventListener(){}, removeEventListener(){}, dataset: {}, querySelector(){ return null; }, querySelectorAll(){ return []; } }),
  querySelectorAll: (sel) => [],
  addEventListener: () => {},
  removeEventListener: () => {},
  documentElement: { setAttribute: () => {}, style: { setProperty: () => {} } },
  createElement: (tag) => ({ tagName: tag.toUpperCase(), style: {}, classList: { add(){}, remove(){}, toggle(){} }, appendChild(){}, setAttribute(){}, dataset: {} }),
  body: { appendChild: () => {} }
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

const sandbox = {
  window: mockWindow,
  document: mockDocument,
  localStorage: mockLocalStorage,
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
vm.createContext(sandbox);

const codeToRun = fs.readFileSync('scripts/temp_code.js', 'utf-8');
vm.runInContext(codeToRun, sandbox);

console.log('Script loaded successfully in sandbox!');
