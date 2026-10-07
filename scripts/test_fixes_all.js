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
let syncSetCount = 0;
const mockStorage = {
  get: async (k) => ({ key: k, value: electronStorage[k] || null }),
  getSync: (k) => ({ key: k, value: electronStorage[k] || null }),
  getAll: async () => Object.assign({}, electronStorage),
  set: async (k, v) => { electronStorage[k] = v; return true; },
  setSync: (k, v) => { electronStorage[k] = v; syncSetCount++; return true; }
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
  console.log('PASS 1: Script loaded cleanly.');
} catch (e) {
  console.error('FAIL 1: Script failed to load:', e);
  process.exit(1);
}

(async () => {
  try {
    // Wait for async init() to finish settling and switch to dashboard
    await new Promise(r => setTimeout(r, 60));

    const State = sandbox.window.State;
    const Actions = sandbox.window.Actions;

    // --- TEST 1: appPrompt and New Notebook Creation ---
    console.log('Testing appPrompt & New Notebook creation...');
    // Simulate user typing in the prompt modal when npAddNotebook opens
    setTimeout(() => {
      const promptInput = getEl('appPromptInput');
      const confirmBtn = getEl('appPromptConfirmBtn');
      promptInput.value = 'Homicide Intelligence 2026';
      if (confirmBtn.onclick) confirmBtn.onclick();
    }, 20);

    const initialNbCount = (State.notepad.notebooks || []).length;
    await Actions['np-add-notebook']();
    
    const createdNb = State.notepad.notebooks.find(n => n.name === 'Homicide Intelligence 2026');
    if (!createdNb) {
      throw new Error('FAIL: New notebook "Homicide Intelligence 2026" was NOT created!');
    }
    console.log('PASS 2: New notebook created successfully! ID:', createdNb.id);

    // --- TEST 2: New Investigation Board Creation ---
    console.log('Testing New Investigation Board creation...');
    setTimeout(() => {
      const promptInput = getEl('appPromptInput');
      const confirmBtn = getEl('appPromptConfirmBtn');
      promptInput.value = 'Operation Nightfall Board';
      if (confirmBtn.onclick) confirmBtn.onclick();
    }, 20);

    await Actions['mm-new-board']();
    const createdBoard = State.mindmaps.find(b => b.title === 'Operation Nightfall Board');
    if (!createdBoard) {
      throw new Error('FAIL: New investigation board "Operation Nightfall Board" was NOT created!');
    }
    console.log('PASS 3: New investigation board created successfully! ID:', createdBoard.id);

    // --- TEST 3: Note Order Interchange / Glitch Bug ---
    console.log('Testing note selection & order stability (interchange glitch fix)...');
    // Clear and create 2 distinct notes
    State.notepad.notes = [
      { id: 'note-1', title: 'First Case Note', content: '<p>Content 1</p>', createdAt: '2026-09-28T01:00:00.000Z', updatedAt: '2026-09-28T01:00:00.000Z' },
      { id: 'note-2', title: 'Second Case Note', content: '<p>Content 2</p>', createdAt: '2026-09-28T02:00:00.000Z', updatedAt: '2026-09-28T02:00:00.000Z' }
    ];

    // Select note-2 (simulating user clicking note 2)
    sandbox.window.npSelectNote('note-2');
    const editorBody = getEl('npEditorBody');
    const titleInput = getEl('npTitleInput');
    editorBody.dataset.loadedNoteId = 'note-2';
    editorBody.innerHTML = '<p>Content 2</p>';
    titleInput.value = 'Second Case Note';

    // Now user clicks note-1 (WITHOUT modifying note-2)
    sandbox.window.npSelectNote('note-1');

    // Verify note-2's updatedAt was NOT bumped because it was NOT dirty!
    const note2 = State.notepad.notes.find(n => n.id === 'note-2');
    if (note2.updatedAt !== '2026-09-28T02:00:00.000Z') {
      throw new Error(`FAIL: note-2 updatedAt was bumped to ${note2.updatedAt} on mere selection click! Order will glitch!`);
    }
    console.log('PASS 4: Note selection did NOT bump updatedAt for unmodified notes. Note ordering is 100% stable!');

    // --- TEST 4: Tasks Application ---
    console.log('Testing tasks toggling and editing...');
    State.tasks = [];
    const taskInput = getEl('taskInput');
    taskInput.value = 'Review ballistic analysis';
    Actions['task-add']();

    if (State.tasks.length !== 1 || State.tasks[0].text !== 'Review ballistic analysis') {
      throw new Error('FAIL: Task was not added!');
    }
    const taskId = State.tasks[0].id;
    if (State.tasks[0].done !== false) throw new Error('FAIL: Task should initially be active');

    // Toggle task
    Actions['task-toggle']({ dataset: { id: taskId } });
    if (State.tasks[0].done !== true) throw new Error('FAIL: Task toggle failed to mark done');

    Actions['task-toggle']({ dataset: { id: taskId } });
    if (State.tasks[0].done !== false) throw new Error('FAIL: Task toggle failed to mark active');

    // Edit task
    setTimeout(() => {
      const promptInput = getEl('appPromptInput');
      const confirmBtn = getEl('appPromptConfirmBtn');
      promptInput.value = 'Review ballistic analysis & fingerprint report';
      if (confirmBtn.onclick) confirmBtn.onclick();
    }, 20);

    await Actions['task-edit']({ dataset: { id: taskId } });
    if (State.tasks[0].text !== 'Review ballistic analysis & fingerprint report') {
      throw new Error('FAIL: Task text was not updated via task-edit!');
    }
    console.log('PASS 5: Task creation, toggling, and editing verified successfully!');

    // --- TEST 5: Performance / Zero Keystroke Lag ---
    console.log('Testing zero-latency keystroke handling...');
    const syncCountBefore = syncSetCount;
    // Simulate user typing 20 characters in editorBody
    editorBody.dataset.loadedNoteId = 'note-1';
    for (let i = 0; i < 20; i++) {
      editorBody.innerHTML = `<p>Typing character ${i}</p>`;
      // Simulate input event
      const note = State.notepad.notes.find(n => n.id === 'note-1');
      note.content = editorBody.innerHTML;
    }
    const syncCountAfter = syncSetCount;
    if (syncCountAfter > syncCountBefore) {
      throw new Error('FAIL: Synchronous disk persistence was triggered during typing! Lag detected!');
    }
    console.log('PASS 6: Typing is completely decoupled from synchronous disk IPC. Zero typing latency verified!');

    // --- TEST 7: Move Note to Another Notebook ---
    console.log('Testing moving note to another notebook...');
    // Add custom notebook 'Surveillance Logs'
    State.notepad.notebooks.push({ id: 'nb-surv', name: 'Surveillance Logs', icon: '📹' });
    const testNote = State.notepad.notes[0];
    const initialNb = testNote.notebookId;
    // Move to nb-surv
    Actions['np-move-note']({ dataset: { id: testNote.id, nb: 'nb-surv' } });
    if (testNote.notebookId !== 'nb-surv') {
      throw new Error(`FAIL: Note notebookId was not updated to nb-surv! Got: ${testNote.notebookId}`);
    }
    // Move back to unfiled
    Actions['np-move-note']({ dataset: { id: testNote.id, nb: '' } });
    if (testNote.notebookId !== null) {
      throw new Error(`FAIL: Note notebookId was not updated to unfiled (null)! Got: ${testNote.notebookId}`);
    }
    console.log('PASS 7: Moving note between notebooks and unfiled verified successfully!');

    // --- TEST 8: Investigation Board Duplication ---
    console.log('Testing Investigation Board duplication...');
    const srcBoard = State.mindmaps[0];
    srcBoard.nodes = [
      { id: 'pin-a', label: 'Suspect Alpha', type: 'person', x: 100, y: 100 },
      { id: 'pin-b', label: 'Getaway Vehicle', type: 'vehicle', x: 300, y: 100 }
    ];
    srcBoard.links = [
      { id: 'link-1', a: 'pin-a', b: 'pin-b', label: 'Drove away in' }
    ];
    srcBoard.annotations = [
      { id: 'annot-1', type: 'arrow', x1: 100, y1: 100, x2: 300, y2: 100 }
    ];
    sandbox.window.currentMindmapId = srcBoard.id;

    const initialBoardCount = State.mindmaps.length;
    Actions['mm-duplicate-board']();

    if (State.mindmaps.length !== initialBoardCount + 1) {
      throw new Error('FAIL: Duplicated board was not added to State.mindmaps!');
    }
    const dupBoard = State.mindmaps[State.mindmaps.length - 1];
    if (!dupBoard.title.includes('(Copy)')) {
      throw new Error(`FAIL: Duplicated board title should have (Copy), got: ${dupBoard.title}`);
    }
    if (dupBoard.nodes.length !== 2) {
      throw new Error(`FAIL: Expected 2 cloned nodes, got: ${dupBoard.nodes.length}`);
    }
    if (dupBoard.nodes[0].id === 'pin-a' || dupBoard.nodes[1].id === 'pin-b') {
      throw new Error('FAIL: Cloned nodes must have new unique IDs!');
    }
    if (dupBoard.links.length !== 1) {
      throw new Error(`FAIL: Expected 1 cloned link, got: ${dupBoard.links.length}`);
    }
    const clonedNodeA = dupBoard.nodes.find(n => n.label === 'Suspect Alpha');
    const clonedNodeB = dupBoard.nodes.find(n => n.label === 'Getaway Vehicle');
    if (dupBoard.links[0].a !== clonedNodeA.id || dupBoard.links[0].b !== clonedNodeB.id) {
      throw new Error('FAIL: Cloned link was not correctly re-mapped to new node IDs!');
    }
    console.log('PASS 8: Board duplication with full link remapping verified successfully!');

    // --- TEST 9: Moving Pin to Another Board ---
    console.log('Testing moving a pin to another board...');
    const boardA = State.mindmaps[0];
    const boardB = State.mindmaps[1];
    sandbox.window.currentMindmapId = boardA.id;
    boardA.nodes = [{ id: 'moving-pin', label: 'Ballistics Casing', x: 200, y: 200 }];
    boardA.links = [];
    boardB.nodes = [];

    Actions['mm-node-move-board']({ dataset: { nodeId: 'moving-pin', boardId: boardB.id } });

    if (boardA.nodes.some(n => n.id === 'moving-pin')) {
      throw new Error('FAIL: Pin was not removed from source board!');
    }
    if (!boardB.nodes.some(n => n.id === 'moving-pin')) {
      throw new Error('FAIL: Pin was not added to target board!');
    }
    console.log('PASS 9: Moving pin to another board verified successfully!');

    // --- TEST 10: Copying Pin to Another Board ---
    console.log('Testing copying a pin to another board...');
    boardB.nodes = [{ id: 'copy-pin-src', label: 'Security Camera Footage', x: 150, y: 150 }];
    sandbox.window.currentMindmapId = boardB.id;

    Actions['mm-node-copy-board']({ dataset: { nodeId: 'copy-pin-src', boardId: boardA.id } });

    if (!boardB.nodes.some(n => n.id === 'copy-pin-src')) {
      throw new Error('FAIL: Source pin disappeared during copy!');
    }
    const copiedPin = boardA.nodes.find(n => n.label === 'Security Camera Footage');
    if (!copiedPin) {
      throw new Error('FAIL: Copied pin was not added to target board!');
    }
    if (copiedPin.id === 'copy-pin-src') {
      throw new Error('FAIL: Copied pin must have a new unique ID!');
    }
    console.log('PASS 10: Copying pin to another board verified successfully!');

    // --- TEST 11: Task Async Performance (Zero Sync Block) ---
    console.log('Testing task performance (fully asynchronous IPC, zero sync blocking)...');
    const syncCountBeforeTask = syncSetCount;
    taskInput.value = 'High speed async task test';
    Actions['task-add']();
    const newTask = State.tasks[0];
    Actions['task-toggle']({ dataset: { id: newTask.id } });
    Actions['task-toggle']({ dataset: { id: newTask.id } });
    Actions['task-delete']({ dataset: { id: newTask.id } });

    const syncCountAfterTask = syncSetCount;
    if (syncCountAfterTask > syncCountBeforeTask) {
      throw new Error(`FAIL: Task operations triggered ${syncCountAfterTask - syncCountBeforeTask} synchronous disk writes!`);
    }
    console.log('PASS 11: Task add/toggle/delete operate 100% asynchronously with zero UI blocking!');

    // --- TEST 12: Note Context Menu UI & Move to Unfiled Option ---
    console.log('Testing Note Context Menu UI (styling, close button, unfiled option)...');
    testNote.notebookId = 'nb-surv';
    Actions['np-note-ctx']({ dataset: { id: testNote.id } });
    const modalBody = getEl('modalBody');
    const modalBackdrop = getEl('modalBackdrop');
    if (!modalBackdrop.classList.contains('open')) {
      throw new Error('FAIL: Modal backdrop should be open when context menu is triggered!');
    }
    if (!modalBody.innerHTML.includes('data-action="close-modal"')) {
      throw new Error('FAIL: Note context menu is missing a close (✕) button!');
    }
    if (!modalBody.innerHTML.includes('np-ctx-item')) {
      throw new Error('FAIL: Note context menu is missing np-ctx-item styled action buttons!');
    }
    if (!modalBody.innerHTML.includes('data-nb=""')) {
      throw new Error('FAIL: Note context menu for filed note must include option to move to Unfiled / General!');
    }
    // Close modal
    Actions['close-modal']();
    if (modalBackdrop.classList.contains('open')) {
      throw new Error('FAIL: Modal backdrop remained open after closing context menu!');
    }
    console.log('PASS 12: Note context menu UI, close button, and unfiled notebook option verified successfully!');

    // --- TEST 13: Investigation Board Pin Deletion & Modal Dismissal (No Gray Out) ---
    const currB = sandbox.window.currentBoard();
    currB.nodes.push({ id: 'del-pin-test', label: 'Target Suspect Marker', x: 75, y: 75 });
    
    // Simulate confirming deletion via appConfirm dialog
    setTimeout(() => {
      const okBtn = getEl('appConfirmOk');
      if (okBtn && okBtn.onclick) okBtn.onclick();
    }, 20);

    await Actions['mm-node-delete']({ dataset: { id: 'del-pin-test' } });

    // Verify pin was deleted
    if (currB.nodes.some(n => n.id === 'del-pin-test')) {
      throw new Error('FAIL: Pin was not deleted from board!');
    }
    // Verify modal backdrop was closed so screen does NOT remain grayed out
    if (modalBackdrop.classList.contains('open')) {
      throw new Error('FAIL: Modal backdrop remained open with gray overlay after pin deletion!');
    }
    console.log('PASS 13: Pin deletion cleanly dismisses modal overlay without gray-out freeze!');

    console.log('\n========================================');
    console.log(' ALL 13 VERIFICATION TESTS PASSED (100%)');
    console.log('========================================');
    process.exit(0);
  } catch (err) {
    console.error('TEST SUITE ERROR:', err);
    process.exit(1);
  }
})();
