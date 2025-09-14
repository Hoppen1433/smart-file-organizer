import React, { useState, useEffect } from 'react';

const PostOrganizationResults = ({ organizationData, settings, onBack, onUndo }) => {
  const [expandedCategories, setExpandedCategories] = useState({});
  const [showAllFiles, setShowAllFiles] = useState(false);

  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  if (!organizationData || !organizationData.success) {
    return null;
  }

  const { summary = {} } = organizationData;
  const { filesProcessed = 0, categoriesFound = {}, fileDetails = [] } = summary;

  const getOrganizationPath = () => {
    return settings?.organizationPath || 
      (process.env.HOME ? 
        `${process.env.HOME}/Documents/SmartFileOrganizer` :
        `${process.env.USERPROFILE}\\Documents\\SmartFileOrganizer`);
  };

  const getFullPath = (category, filename) => {
    const basePath = getOrganizationPath();
    const categoryPath = category.replace(/\//g, '/');
    return `${basePath}/${categoryPath}/${filename}`;
  };

  return (
    <div className="max-w-6xl mx-auto px-4">
      {/* Success Header */}
      <div className="text-center mb-8">
        <div className="text-6xl mb-4">✅</div>
        <h1 className="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
          Organization Complete!
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-4">
          Your files have been successfully organized with healthcare intelligence
        </p>
        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg p-4 max-w-2xl mx-auto">
          <p className="text-green-800 dark:text-green-200">
            <strong>📍 Files organized to:</strong> {getOrganizationPath()}
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap justify-center gap-4 mb-8">
        <button
          onClick={() => {
            if (window.electronAPI) {
              window.electronAPI.showFile(getOrganizationPath());
            }
          }}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
        >
          📁 Open Organized Folder
        </button>
        
        <button
          onClick={() => {
            if (window.electronAPI) {
              window.electronAPI.indexMedicalFiles();
            }
          }}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
        >
          🔍 Index for AI Search
        </button>

        {onUndo && (
          <button
            onClick={onUndo}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
          >
            ↩️ Undo Organization
          </button>
        )}

        <button
          onClick={onBack}
          className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg font-medium flex items-center transition-colors"
        >
          ← Back to Dashboard
        </button>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
            {filesProcessed}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Files Organized</div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-red-600 dark:text-red-400 mb-2">
            {Object.values(categoriesFound).reduce((sum, count) => sum + count, 0)}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Healthcare Files</div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6 text-center">
          <div className="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
            {Object.keys(categoriesFound).length}
          </div>
          <div className="text-gray-600 dark:text-gray-400">Categories Used</div>
        </div>
      </div>

      {/* Where Did My Files Go? */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
          📍 Where Did My Files Go?
        </h2>
        
        <div className="space-y-4">
          {Object.entries(categoriesFound).map(([category, count]) => (
            <div key={category} className="border border-gray-200 dark:border-gray-700 rounded-lg">
              <button
                onClick={() => toggleCategory(category)}
                className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-3">
                    {getCategoryIcon(category)}
                  </span>
                  <div>
                    <div className="font-medium text-gray-900 dark:text-white">
                      {category.replace(/\//g, ' › ')}
                    </div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      {count} files • {getFullPath(category, '').replace(/\/$/, '')}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (window.electronAPI) {
                        const categoryPath = getFullPath(category, '').replace(/\/$/, '');
                        window.electronAPI.showFile(categoryPath);
                      }
                    }}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
                  >
                    Open Folder
                  </button>
                  <span className="text-gray-400 dark:text-gray-500">
                    {expandedCategories[category] ? '▼' : '▶'}
                  </span>
                </div>
              </button>
              
              {expandedCategories[category] && (
                <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-900">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    Files in this category:
                  </div>
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {/* This would need actual file listings from the organization process */}
                    <div className="text-sm text-gray-500 dark:text-gray-400">
                      📄 Files organized to: <code className="bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded text-xs">
                        {getFullPath(category, '[filename]').replace('[filename]', '...')}
                      </code>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <h3 className="font-medium text-blue-900 dark:text-blue-200 mb-2">
            💡 Quick Tips:
          </h3>
          <ul className="text-sm text-blue-800 dark:text-blue-300 space-y-1">
            <li>• Click "Open Folder" next to any category to see those files</li>
            <li>• Your original files have been moved (not copied) to keep things organized</li>
            <li>• Use "Index for AI Search" to enable smart searching across all files</li>
            <li>• You can always reorganize files later by dragging them to different folders</li>
          </ul>
        </div>
      </div>

      {/* Manual Reorganization Options */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          🔧 Need to Reorganize?
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">
              🔍 Search & Move
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Find specific files and move them to different categories
            </p>
            <button
              onClick={() => {
                // Navigate to search
                window.location.hash = '#query';
              }}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm"
            >
              Open Search
            </button>
          </div>

          <div className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <h3 className="font-medium text-gray-900 dark:text-white mb-2">
              📁 Manual Organization
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
              Open the organized folder and drag files between categories
            </p>
            <button
              onClick={() => {
                if (window.electronAPI) {
                  window.electronAPI.showFile(getOrganizationPath());
                }
              }}
              className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm"
            >
              Open Folder
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const getCategoryIcon = (category) => {
  const iconMap = {
    'medical': '🏥',
    'medical/imaging': '🔬',
    'medical/labs': '🧪',
    'medical/clinical_notes': '📋',
    'medical/genomics': '🧬',
    'medical/medications': '💊',
    'medical/research': '📚',
    'education': '📚',
    'education/courses': '🎓',
    'education/textbooks': '📖',
    'projects': '⚙️',
    'projects/code': '💻',
    'projects/research': '🔬',
    'personal': '📱',
    'personal/finance': '💰',
    'personal/photos': '📷',
    'writing': '✍️',
    'writing/articles': '📄',
    'writing/notes': '📝',
    'screenshots': '📸',
    'downloads/misc': '📦'
  };
  return iconMap[category] || '📄';
};

export default PostOrganizationResults;