import React, { useState, useCallback, useEffect } from 'react';
import ActivityTracker from '../utils/activityTracker';

const Dashboard = ({ onOrganizeFiles, settings, setCurrentView }) => {
  const [dragActive, setDragActive] = useState(false);
  const [recentActivity, setRecentActivity] = useState([]);
  const [activityTracker] = useState(new ActivityTracker());
  
  useEffect(() => {
    setRecentActivity(activityTracker.getActivities());
  }, [activityTracker]);
  
  const addActivity = (action, details = {}) => {
    const updatedActivities = activityTracker.addActivity(action, details);
    setRecentActivity(updatedActivities);
  };

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const files = Array.from(e.dataTransfer.files);
      if (files.length === 1 && files[0].type === '') {
        const folderPath = files[0].path;
        // Always preview first - never organize directly
        onOrganizeFiles(folderPath, { dryRun: true });
        addActivity(`Previewing organization for dropped folder`);
      }
    }
  }, [onOrganizeFiles, addActivity]);

  // Main workflow: Always preview first
  const handlePreviewOrganization = async () => {
    if (window.electronAPI) {
      const folderPath = await window.electronAPI.selectFolder();
      if (folderPath) {
        addActivity(`Previewing organization for: ${folderPath.split('/').pop()}`);
        onOrganizeFiles(folderPath, { dryRun: true });
      }
    }
  };

  // Quick organize for power users (still shows preview first)
  const handleQuickOrganize = async () => {
    if (window.electronAPI) {
      const folderPath = await window.electronAPI.selectFolder();
      if (folderPath) {
        addActivity(`Quick preview for: ${folderPath.split('/').pop()}`);
        onOrganizeFiles(folderPath, { dryRun: true });
      }
    }
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Simplified Hero */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          🗂️ Smart File Organizer
        </h2>
        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
          Intelligent file organization with complete control. Preview where files will go, edit paths, then organize.
        </p>
      </div>

      {/* Main Action Area */}
      <div className="mb-8">
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-all duration-200 ${
            dragActive
              ? 'border-blue-400 bg-blue-50 dark:bg-blue-900/20 scale-102'
              : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="space-y-6">
            <div className="text-6xl">📁</div>
            
            <div>
              <h3 className={`text-xl font-medium ${
                dragActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-900 dark:text-white'
              }`}>
                Drop a folder here or select one to organize
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mt-2">
                Files will be previewed first - you choose exactly where they go
              </p>
            </div>
            
            {/* Primary Action - Always Preview First */}
            <div className="space-y-4">
              <button
                onClick={handlePreviewOrganization}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg font-medium text-lg transition-colors btn-focus flex items-center mx-auto space-x-2"
              >
                <span className="text-xl">🔍</span>
                <span>Select Folder & Preview Organization</span>
              </button>
              
              <p className="text-sm text-gray-500 dark:text-gray-400">
                ↑ This always shows you exactly where files will go before moving anything
              </p>
            </div>

            {/* Secondary Actions */}
            <div className="flex flex-wrap justify-center gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button
                onClick={() => {
                  if (window.electronAPI) {
                    const organizePath = settings.organizationPath || 
                      (process.env.HOME ? 
                        `${process.env.HOME}/Documents/auto_organized` :
                        `${process.env.USERPROFILE}\\Documents\\auto_organized`);
                    addActivity('Opened organized files folder');
                    window.electronAPI.showFile(organizePath);
                  }
                }}
                className="text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-1"
              >
                <span>📁</span>
                <span>Open Organized Files</span>
              </button>
              
              <button
                onClick={() => setCurrentView('query')}
                className="text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-1"
              >
                <span>🔍</span>
                <span>Search Files</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Workflow Explanation */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg p-6 mb-8">
        <h3 className="text-lg font-medium text-blue-900 dark:text-blue-200 mb-3 flex items-center">
          <span className="mr-2">💡</span>
          How File Organization Works
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-800 dark:text-blue-300">
          <div className="flex items-start space-x-2">
            <span className="text-lg">1️⃣</span>
            <div>
              <div className="font-medium">Preview First</div>
              <div>See exactly where each file will go</div>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-lg">2️⃣</span>
            <div>
              <div className="font-medium">Edit Paths</div>
              <div>Change destinations, preview content</div>
            </div>
          </div>
          <div className="flex items-start space-x-2">
            <span className="text-lg">3️⃣</span>
            <div>
              <div className="font-medium">Organize</div>
              <div>Files move exactly where you specified</div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Features - Simplified */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <FeatureCard
          icon="👁️"
          title="Preview Everything"
          description="See file content and exact destinations before organizing"
        />
        <FeatureCard
          icon="✏️"
          title="Full Path Control"
          description="Edit complete file paths - choose Downloads vs Documents"
        />
        <FeatureCard
          icon="🔄"
          title="Immediate Undo"
          description="Every organization can be reversed instantly"
        />
        <FeatureCard
          icon="🧠"
          title="Smart Suggestions"
          description="Auto-complete paths based on content and existing structure"
        />
        <FeatureCard
          icon="🏥"
          title="Medical Intelligence"
          description="Recognizes medical files, research papers, clinical data"
        />
        <FeatureCard
          icon="🛡️"
          title="Safe & Local"
          description="All processing happens on your machine - complete privacy"
        />
      </div>

      {/* Recent Activity - Simplified */}
      {recentActivity.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            📈 Recent Activity
          </h3>
          <div className="space-y-2">
            {recentActivity.slice(0, 5).map((activity) => (
              <div key={activity.id} className="flex items-center justify-between py-2">
                <span className="text-gray-900 dark:text-white text-sm">{activity.action}</span>
                <span className="text-xs text-gray-500 dark:text-gray-400">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
    <div className="text-3xl mb-3">{icon}</div>
    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">{title}</h3>
    <p className="text-gray-600 dark:text-gray-300 text-sm">{description}</p>
  </div>
);

export default Dashboard;