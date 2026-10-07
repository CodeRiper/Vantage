const { app, BrowserWindow, ipcMain, shell, Menu, Notification } = require('electron');
const path = require('path');
const fs = require('fs');

function dataFilePath() {
  return path.join(app.getPath('userData'), 'vantage-data.json');
}

let cache = null;

function loadData() {
  try {
    if (fs.existsSync(dataFilePath())) {
      const raw = fs.readFileSync(dataFilePath(), 'utf-8');
      if (raw && raw.trim()) return JSON.parse(raw);
    }
  } catch (e) {
    console.error('Failed reading primary data file, trying tmp fallback:', e);
  }
  try {
    const tmp = dataFilePath() + '.tmp';
    if (fs.existsSync(tmp)) {
      const rawTmp = fs.readFileSync(tmp, 'utf-8');
      if (rawTmp && rawTmp.trim()) {
        const parsed = JSON.parse(rawTmp);
        try { fs.writeFileSync(dataFilePath(), rawTmp, 'utf-8'); } catch(errWrite){}
        return parsed;
      }
    }
  } catch (eTmp) {
    console.error('Failed reading fallback tmp data file:', eTmp);
  }
  return {};
}

function getCache() {
  if (cache === null) cache = loadData();
  return cache;
}

let persistTimer = null;

function doPersist() {
  try {
    fs.mkdirSync(path.dirname(dataFilePath()), { recursive: true });
    // write to a temp file then rename, so a crash mid-write can never corrupt the store
    const payload = JSON.stringify(getCache());
    const tmp = dataFilePath() + '.tmp';
    try {
      fs.writeFileSync(tmp, payload, 'utf-8');
      fs.renameSync(tmp, dataFilePath());
    } catch (errRename) {
      fs.writeFileSync(dataFilePath(), payload, 'utf-8');
    }
    return true;
  } catch (e) {
    console.error('Vantage: failed to persist data', e);
    return false;
  }
}

function persistSync() {
  if (persistTimer) {
    clearTimeout(persistTimer);
    persistTimer = null;
  }
  return doPersist();
}

function persist() {
  if (!persistTimer) {
    persistTimer = setTimeout(() => {
      persistTimer = null;
      doPersist();
    }, 120);
  }
  return true;
}

app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('disable-renderer-backgrounding');

ipcMain.handle('storage-get', (evt, key) => {
  const data = getCache();
  if (!(key in data)) return null;
  return { key, value: data[key], shared: false };
});

ipcMain.handle('storage-get-all', () => {
  return getCache();
});

ipcMain.handle('storage-set', (evt, key, value) => {
  const data = getCache();
  data[key] = value;
  const ok = persist();
  if (!ok) return null;
  return { key, value, shared: false };
});

ipcMain.on('storage-set-sync', (evt, key, value) => {
  const data = getCache();
  data[key] = value;
  const ok = persistSync();
  evt.returnValue = ok;
});

ipcMain.on('storage-get-sync', (evt, key) => {
  const data = getCache();
  if (!(key in data)) {
    evt.returnValue = null;
  } else {
    evt.returnValue = { key, value: data[key], shared: false };
  }
});

ipcMain.handle('storage-delete', (evt, key) => {
  const data = getCache();
  const existed = key in data;
  delete data[key];
  persist();
  return { key, deleted: existed, shared: false };
});

ipcMain.handle('storage-list', (evt, prefix) => {
  const data = getCache();
  const keys = Object.keys(data).filter(k => !prefix || k.startsWith(prefix));
  return { keys, prefix: prefix || undefined, shared: false };
});

ipcMain.handle('storage-file-path', () => dataFilePath());

function revealDataFile() {
  persistSync();
  shell.showItemInFolder(dataFilePath());
}
ipcMain.handle('reveal-data-file', revealDataFile);

ipcMain.handle('show-notification', (evt, data) => {
  try {
    if (Notification.isSupported()) {
      const notif = new Notification({
        title: (data && data.title) || 'Vantage',
        body: (data && data.body) || '',
        icon: path.join(__dirname, 'icon.png')
      });
      notif.show();
      return true;
    }
  } catch (e) {
    console.error('Failed to show notification', e);
  }
  return false;
});

function createWindow() {
  const win = new BrowserWindow({
    width: 1360,
    height: 860,
    minWidth: 1000,
    minHeight: 640,
    show: false,
    backgroundColor: '#14161c',
    autoHideMenuBar: true,
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      spellcheck: false
    }
  });
  let shown = false;
  const showWindow = () => {
    if (!shown) {
      shown = true;
      win.maximize();
      win.show();
    }
  };
  win.once('ready-to-show', showWindow);
  setTimeout(showWindow, 150);

  win.on('close', () => {
    persistSync();
  });

  const menu = Menu.buildFromTemplate([
    {
      label: 'Vantage',
      submenu: [
        {
          label: 'Show data file',
          click: () => revealDataFile()
        },
        { role: 'reload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    }
  ]);
  Menu.setApplicationMenu(menu);

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  if (process.platform === 'win32') {
    try {
      app.setAppUserModelId('com.vantage.app');
    } catch (e) {
      console.error('Failed to set AppUserModelId:', e);
    }
  }
  createWindow();
});

app.on('before-quit', () => {
  persistSync();
});

app.on('will-quit', () => {
  persistSync();
});

app.on('window-all-closed', () => {
  persistSync();
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
