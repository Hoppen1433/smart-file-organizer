import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import OrganizationProgress from './components/OrganizationProgress';
import OrganizationPreview from './components/OrganizationPreview';
import PostOrganizationResults from './components/PostOrganizationResults';
import QueryInterface from './components/QueryInterface';
import SettingsPanel from './components/SettingsPanel';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [organizationInProgress, setOrganizationInProgress] = useState(false);
  const [organizationData, setOrganizationData] = useState(null);
  const [previewData, setPreviewData] = useState(null);
  const [appVersion, setAppVersion] = useState('');
  const [settings, setSettings] = useState({
    autoIndex: true,
    organizationPath: '',
    theme: 'light'
  });

  useEffect(() => {
    // Get app version
    if (window.electronAPI) {
      window.electronAPI.getAppVersion().then(version => {
        setAppVersion(version);
      });
    }

    // Load settings from localStorage
    const savedSettings = localStorage.getItem('smartFileOrganizerSettings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  const saveSettings = useCallback((newSettings) => {
    setSettings(newSettings);
    localStorage.setItem('smartFileOrganizerSettings', JSON.stringify(newSettings));
  }, []);

  const handleOrganizeFiles = useCallback(async (sourcePath, options = {}) => {
    if (!window.electronAPI) return;

    try {
      // Always preview first - this is the new default behavior
      if (options.dryRun !== false) {
        // Show preview mode
        setCurrentView('preview');
        const previewResult = await window.electronAPI.previewOrganization({
          sourcePath
        });
        setPreviewData(previewResult);
      } else {
        // Only when explicitly organizing after preview
        setOrganizationInProgress(true);
        setCurrentView('organization');

        const organizationOptions = {
          sourcePath,
          dryRun: false
        };

        const result = await window.electronAPI.organizeFiles(organizationOptions);
        
        setOrganizationData(result);
        
        // Auto-index if enabled
        if (settings.autoIndex) {
          await window.electronAPI.indexMedicalFiles();
        }
      }
    } catch (error) {
      console.error('Organization failed:', error);
      setOrganizationData({
        success: false,
        error: error.message
      });
    } finally {
      setOrganizationInProgress(false);
    }
  }, [settings.autoIndex]);

  const handleOrganizeNow = useCallback(async (modifiedFiles) => {
    if (!window.electronAPI) return;

    try {
      setOrganizationInProgress(true);
      setCurrentView('organization');
      
      const result = await window.electronAPI.organizeFilesWithCategories({
        files: modifiedFiles
      });
      
      setOrganizationData(result);
      
      if (settings.autoIndex) {
        await window.electronAPI.indexMedicalFiles();
      }
    } catch (error) {
      console.error('Organization failed:', error);
      setOrganizationData({
        success: false,
        error: error.message
      });
    } finally {
      setOrganizationInProgress(false);
    }
  }, [settings.autoIndex]);

  const handleProgressUpdate = useCallback((event, data) => {
    // Handle real-time progress updates from Python scripts
    console.log('Progress update:', data);
  }, []);

  useEffect(() => {
    if (window.electronAPI) {
      window.electronAPI.onOrganizationProgress(handleProgressUpdate);
      
      return () => {
        window.electronAPI.removeOrganizationProgressListener(handleProgressUpdate);
      };
    }
  }, [handleProgressUpdate]);

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return (
          <Dashboard
            onOrganizeFiles={handleOrganizeFiles}
            settings={settings}
            setCurrentView={setCurrentView}
          />
        );
      case 'query':
        return (
          <QueryInterface
            settings={settings}
          />
        );
      case 'preview':
        return (
          <OrganizationPreview
            previewData={previewData}
            settings={settings}
            onCategoryChange={(fileId, newCategory) => {
              console.log(`File ${fileId} category changed to: ${newCategory}`);
            }}
            onOrganizeNow={handleOrganizeNow}
            onBack={() => {
              setCurrentView('dashboard');
              setPreviewData(null);
            }}
          />
        );
      case 'organization':
        return (
          <OrganizationProgress
            inProgress={organizationInProgress}
            data={organizationData}
            onBack={() => {
              if (organizationData && organizationData.success) {
                setCurrentView('results');
              } else {
                setCurrentView('dashboard');
              }
            }}
          />
        );
      case 'results':
        return (
          <PostOrganizationResults
            organizationData={organizationData}
            settings={settings}
            onBack={() => {
              setCurrentView('dashboard');
              setOrganizationData(null);
            }}
            onUndo={async () => {
              try {
                setCurrentView('organization');
                setOrganizationInProgress(true);
                
                const result = await window.electronAPI.undoOrganization('latest');
                
                if (result.success) {
                  alert('✅ Organization successfully undone! Files have been moved back to their original locations.');
                  setCurrentView('dashboard');
                  setOrganizationData(null);
                } else {
                  alert('❌ Undo failed: ' + (result.error || 'Unknown error'));
                }
              } catch (error) {
                console.error('Undo failed:', error);
                alert('❌ Undo failed: ' + error.message);
              } finally {
                setOrganizationInProgress(false);
              }
            }}
          />
        );
      case 'settings':
        return (
          <SettingsPanel
            settings={settings}
            onSaveSettings={saveSettings}
            onBack={() => setCurrentView('dashboard')}
          />
        );
      default:
        return <Dashboard onOrganizeFiles={handleOrganizeFiles} settings={settings} />;
    }
  };

  return (
    <div className={`App ${settings.theme === 'dark' ? 'dark' : ''}`}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                    🗂️ Smart File Organizer
                  </h1>
                </div>
              </div>
              
              <nav className="flex space-x-4">
                <button
                  onClick={() => setCurrentView('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'dashboard'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200'
                      : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                  }`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setCurrentView('query')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'query'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200'
                      : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                  }`}
                >
                  🔍 Query
                </button>
                <button
                  onClick={() => setCurrentView('settings')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentView === 'settings'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200'
                      : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                  }`}
                >
                  ⚙️ Settings
                </button>
              </nav>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {renderCurrentView()}
        </main>

        {/* Footer */}
        <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
              <div>
                Smart File Organizer v{appVersion} - NLU-Enhanced Intelligence
              </div>
              <div>
                Built with intelligent content analysis
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
