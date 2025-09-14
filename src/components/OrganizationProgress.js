import React from 'react';

const OrganizationProgress = ({ inProgress, data, onBack }) => {
  if (!data) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">🔄</div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Getting Ready to Organize
        </h2>
        <p className="text-gray-600 dark:text-gray-300">
          Preparing to process your files...
        </p>
      </div>
    );
  }

  if (inProgress) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="text-6xl mb-4 pulse-animation">🔄</div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Organization in Progress
            </h2>
            <p className="text-gray-600 dark:text-gray-300">
              Intelligently categorizing your files with healthcare specialization...
            </p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-600 dark:text-gray-300 mb-2">
              <span>Processing files...</span>
              <span>Please wait</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <div 
                className="bg-blue-600 h-3 rounded-full progress-bar"
                style={{ width: '75%' }}
              />
            </div>
          </div>

          {/* Live Output */}
          <div className="bg-gray-100 dark:bg-gray-900 rounded-lg p-4 font-mono text-sm max-h-64 overflow-y-auto">
            <div className="text-green-600 dark:text-green-400">
              🏥 Healthcare-Enhanced File Organization
            </div>
            <div className="text-blue-600 dark:text-blue-400">
              🔍 Found files in folder...
            </div>
            <div className="text-yellow-600 dark:text-yellow-400">
              🏥 Detected healthcare-specific files
            </div>
            <div className="text-green-600 dark:text-green-400">
              ✅ Medical/Labs: Processing lab results...
            </div>
            <div className="text-green-600 dark:text-green-400">
              ✅ Medical/Imaging: Processing medical imaging...
            </div>
            <div className="animate-pulse text-gray-600 dark:text-gray-400">
              🔄 Processing remaining files...
            </div>
          </div>

          {/* Cancel Button */}
          <div className="mt-6 text-center">
            <button
              onClick={onBack}
              className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors btn-focus"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Organization Complete
  const { success, summary, error } = data;

  if (!success) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
          <div className="text-center">
            <div className="text-6xl mb-4">❌</div>
            <h2 className="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
              Organization Failed
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {error || 'An error occurred during file organization'}
            </p>
            <button
              onClick={onBack}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors btn-focus"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        {/* Success Header */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-2xl font-bold text-green-600 dark:text-green-400 mb-2">
            Organization Complete!
          </h2>
          <p className="text-gray-600 dark:text-gray-300">
            Your files have been successfully organized with healthcare intelligence
          </p>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon="📄"
            title="Files Processed"
            value={summary?.filesProcessed || 0}
            color="blue"
          />
          <StatCard
            icon="🏥"
            title="Healthcare Files"
            value={summary?.healthcareFiles || 0}
            color="red"
          />
          <StatCard
            icon="📂"
            title="Categories"
            value={Object.keys(summary?.categoriesFound || {}).length}
            color="green"
          />
        </div>

        {/* Categories Breakdown */}
        {summary?.categoriesFound && Object.keys(summary.categoriesFound).length > 0 && (
          <div className="mb-8">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
              📊 Organization Breakdown
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(summary.categoriesFound).map(([category, count]) => (
                <CategoryBreakdown
                  key={category}
                  category={category}
                  count={count}
                />
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4">
          <button
            onClick={() => {
              if (window.electronAPI) {
                const organizePath = process.env.HOME ? 
                  `${process.env.HOME}/Documents/SmartFileOrganizer` :
                  `${process.env.USERPROFILE}\\Documents\\SmartFileOrganizer`;
                window.electronAPI.showFile(organizePath);
              }
            }}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors btn-focus"
          >
            📁 Open Organized Folder
          </button>
          <button
            onClick={() => {
              if (window.electronAPI && summary?.healthcareFiles > 0) {
                window.electronAPI.indexMedicalFiles();
              }
            }}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors btn-focus"
          >
            🔍 Index for AI Search
          </button>
          <button
            onClick={onBack}
            className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-lg transition-colors btn-focus"
          >
            ← Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    red: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    green: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  };

  return (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 text-center">
      <div className="text-2xl mb-2">{icon}</div>
      <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
        {value.toLocaleString()}
      </div>
      <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${colorClasses[color]}`}>
        {title}
      </div>
    </div>
  );
};

const CategoryBreakdown = ({ category, count }) => {
  const getCategoryInfo = (cat) => {
    const categoryMap = {
      'medical': { icon: '🏥', name: 'Medical General', color: 'red' },
      'medical/imaging': { icon: '🔬', name: 'Medical Imaging', color: 'purple' },
      'medical/labs': { icon: '🧪', name: 'Laboratory Results', color: 'green' },
      'medical/clinical_notes': { icon: '📋', name: 'Clinical Notes', color: 'blue' },
      'medical/genomics': { icon: '🧬', name: 'Genomics', color: 'yellow' },
      'medical/medications': { icon: '💊', name: 'Medications', color: 'red' },
      'medical/research': { icon: '📚', name: 'Medical Research', color: 'indigo' },
      'education': { icon: '📚', name: 'Education', color: 'blue' },
      'projects': { icon: '⚙️', name: 'Projects', color: 'gray' },
      'personal': { icon: '📱', name: 'Personal', color: 'green' },
      'writing': { icon: '✍️', name: 'Writing', color: 'purple' }
    };

    return categoryMap[cat] || { icon: '📄', name: cat, color: 'gray' };
  };

  const info = getCategoryInfo(category);

  return (
    <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
      <div className="flex items-center">
        <span className="text-xl mr-3">{info.icon}</span>
        <span className="font-medium text-gray-900 dark:text-white">{info.name}</span>
      </div>
      <span className={`px-2 py-1 rounded-full text-sm font-medium medical-badge ${info.color}`}>
        {count} files
      </span>
    </div>
  );
};

export default OrganizationProgress;
