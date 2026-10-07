const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('storage', {
  get: (key) => ipcRenderer.invoke('storage-get', key),
  getSync: (key) => ipcRenderer.sendSync('storage-get-sync', key),
  getAll: () => ipcRenderer.invoke('storage-get-all'),
  set: (key, value) => ipcRenderer.invoke('storage-set', key, value),
  setSync: (key, value) => ipcRenderer.sendSync('storage-set-sync', key, value),
  delete: (key) => ipcRenderer.invoke('storage-delete', key),
  list: (prefix) => ipcRenderer.invoke('storage-list', prefix)
});

contextBridge.exposeInMainWorld('vantageApp', {
  isDesktop: true,
  showDataFile: () => ipcRenderer.invoke('reveal-data-file'),
  dataFilePath: () => ipcRenderer.invoke('storage-file-path'),
  notify: (title, body) => ipcRenderer.invoke('show-notification', { title, body })
});
