const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // File and folder selection
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  selectFiles: () => ipcRenderer.invoke('select-files'),
  
  // File organization
  organizeFiles: (options) => ipcRenderer.invoke('organize-files', options),
  previewOrganization: (options) => ipcRenderer.invoke('preview-organization', options),
  organizeFilesWithCategories: (options) => ipcRenderer.invoke('organize-files-with-categories', options),
  undoOrganization: (organizationId) => ipcRenderer.invoke('undo-organization', organizationId),
  onOrganizationProgress: (callback) => ipcRenderer.on('organization-progress', callback),
  removeOrganizationProgressListener: (callback) => ipcRenderer.removeListener('organization-progress', callback),
  
  // AI Learning System
  getAIInsights: () => ipcRenderer.invoke('get-ai-insights'),
  recordAICorrection: (correction) => ipcRenderer.invoke('record-ai-correction', correction),
  
  // Medical file queries
  queryMedicalFiles: (query) => ipcRenderer.invoke('query-medical-files', query),
  indexMedicalFiles: () => ipcRenderer.invoke('index-medical-files'),
  
  // File operations
  openFile: (filePath) => ipcRenderer.invoke('open-file', filePath),
  showFile: (filePath) => ipcRenderer.invoke('show-file', filePath),
  previewFile: (filePath) => ipcRenderer.invoke('preview-file', filePath),
  quickLookFile: (filePath) => ipcRenderer.invoke('quick-look-file', filePath),
  
  // App info
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getFileStatistics: () => ipcRenderer.invoke('get-file-statistics'),
  openOrganizedFolder: () => ipcRenderer.invoke('open-organized-folder'),
  
  // Utility functions
  platform: process.platform
});
