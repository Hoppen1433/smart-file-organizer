import React from 'react';

const SettingsPanel = ({ settings, onSaveSettings, onBack }) => {
  const handleSettingChange = (key, value) => {
    const newSettings = { ...settings, [key]: value };
    onSaveSettings(newSettings);
  };

  return (
    <div className="px-4 py-6 sm:px-0 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center mb-8">
        <button
          onClick={onBack}
          className="mr-4 text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ← Back
        </button>
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
          ⚙️ Settings
        </h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Organization Settings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            🗂️ Organization Settings
          </h3>
          
          <div className="space-y-6">
            {/* NLU Intelligence Status */}
            <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
              <div className="flex items-center space-x-3">
                <span className="text-2xl">🧠</span>
                <div>
                  <div className="font-medium text-green-800 dark:text-green-300">
                    NLU Intelligence Active
                  </div>
                  <p className="text-sm text-green-700 dark:text-green-400">
                    Advanced content analysis automatically detects and organizes any type of file intelligently
                  </p>
                </div>
              </div>
            </div>

            {/* Auto Index */}
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-gray-900 dark:text-white">
                  📊 Auto Index Files
                </label>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Automatically index organized files for AI search
                </p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.autoIndex}
                  onChange={(e) => handleSettingChange('autoIndex', e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
              </label>
            </div>

            {/* Organization Path */}
            <div>
              <label className="block text-sm font-medium text-gray-900 dark:text-white mb-2">
                📁 Organization Folder
              </label>
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={settings.organizationPath || '~/Documents/auto_organized'}
                  onChange={(e) => handleSettingChange('organizationPath', e.target.value)}
                  placeholder="~/Documents/auto_organized"
                  className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={async () => {
                    if (window.electronAPI) {
                      const folderPath = await window.electronAPI.selectFolder();
                      if (folderPath) {
                        handleSettingChange('organizationPath', folderPath);
                      }
                    }
                  }}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded-lg text-sm transition-colors btn-focus"
                >
                  Browse
                </button>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Where organized files will be stored
              </p>
            </div>
          </div>
        </div>

        {/* Appearance Settings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            🎨 Appearance
          </h3>
          
          <div className="space-y-6">
            {/* Theme Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-900 dark:text-white mb-3">
                🌗 Theme
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => handleSettingChange('theme', 'light')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    settings.theme === 'light'
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  }`}
                >
                  <div className="text-2xl mb-2">☀️</div>
                  <div className="text-sm font-medium text-gray-900 dark:text-white">Light</div>
                </button>
                <button
                  onClick={() => handleSettingChange('theme', 'dark')}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    settings.theme === 'dark'
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  }`}
                >
                  <div className="text-2xl mb-2">🌙</div>
                  <div className="text-sm font-medium text-gray-900 dark:text-white">Dark</div>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* About & Info */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            ℹ️ About
          </h3>
          
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">🗂️</span>
              <div>
                <div className="font-medium text-gray-900 dark:text-white">Smart File Organizer</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Desktop v2.1.0</div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <span className="text-2xl">🧠</span>
              <div>
                <div className="font-medium text-gray-900 dark:text-white">NLU-Enhanced Intelligence</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Content-aware file organization</div>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Intelligent file organization with natural language understanding - no modes needed, just works.
              </p>
            </div>

            <div className="flex space-x-4 pt-2">
              <button
                onClick={() => {
                  if (window.electronAPI) {
                    // Open GitHub repository
                    window.open('https://github.com/taiscoding/smart-file-organizer', '_blank');
                  }
                }}
                className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium"
              >
                📚 Documentation
              </button>
              <button
                onClick={() => {
                  if (window.electronAPI) {
                    // Open issues page
                    window.open('https://github.com/taiscoding/smart-file-organizer/issues', '_blank');
                  }
                }}
                className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium"
              >
                🐛 Report Issue
              </button>
            </div>
          </div>
        </div>

        {/* Advanced Settings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            🔧 Advanced
          </h3>
          
          <div className="space-y-4">
            <button
              onClick={async () => {
                if (window.electronAPI) {
                  try {
                    const stats = await window.electronAPI.getFileStatistics();
                    const organizePath = settings.organizationPath || 
                      (window.electronAPI.platform === 'win32' ? 
                        `${process.env.USERPROFILE}\\Documents\\SmartFileOrganizer` :
                        `${process.env.HOME}/Documents/SmartFileOrganizer`);
                    const dbPath = `${organizePath}/.file_index.db`;
                    window.electronAPI.showFile(dbPath);
                  } catch (err) {
                    alert('No file index found. Try indexing files first!');
                  }
                }
              }}
              className="w-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-4 py-3 rounded-lg text-sm font-medium transition-colors text-left"
            >
              📊 View File Index Database
            </button>
            
            <button
              onClick={() => {
                if (window.electronAPI) {
                  const organizePath = settings.organizationPath || 
                    (window.electronAPI.platform === 'win32' ? 
                      `${process.env.USERPROFILE}\\Documents\\auto_organized` :
                      `${process.env.HOME}/Documents/auto_organized`);
                  window.electronAPI.showFile(organizePath);
                }
              }}
              className="w-full bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-4 py-3 rounded-lg text-sm font-medium transition-colors text-left"
            >
              📁 Open Organization Folder
            </button>

            <button
              onClick={() => {
                // Clear all settings
                const defaultSettings = {
                  autoIndex: true,
                  organizationPath: '',
                  theme: 'dark'
                };
                onSaveSettings(defaultSettings);
              }}
              className="w-full bg-red-100 dark:bg-red-900 hover:bg-red-200 dark:hover:bg-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg text-sm font-medium transition-colors text-left"
            >
              🗑️ Reset to Default Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;
