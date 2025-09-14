import React, { useState, useCallback } from 'react';

const QueryInterface = ({ settings }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [indexing, setIndexing] = useState(false);

  const suggestedQueries = settings.healthcareMode ? [
    'cardiology files from 2024',
    'recent lab results',
    'imaging studies',
    'abnormal values',
    'genetic testing results',
    'clinical notes',
    'medication lists',
    'research papers neurology'
  ] : [
    'files from this week',
    'recent screenshots',
    'project files',
    'study materials',
    'images and photos',
    'documents and PDFs'
  ];

  const handleSearch = useCallback(async () => {
    if (!query.trim() || !window.electronAPI) return;

    setLoading(true);
    setHasSearched(true);

    try {
      const response = await window.electronAPI.queryMedicalFiles(query);
      if (response.success) {
        setResults(response.results || []);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.error('Query failed:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, [query]);

  const handleKeyPress = useCallback((e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  }, [handleSearch]);

  const handleIndexFiles = useCallback(async () => {
    if (!window.electronAPI) return;

    setIndexing(true);
    try {
      await window.electronAPI.indexMedicalFiles();
      // Show success message
    } catch (error) {
      console.error('Indexing failed:', error);
    } finally {
      setIndexing(false);
    }
  }, []);

  const handleSuggestedQuery = useCallback((suggestedQuery) => {
    setQuery(suggestedQuery);
  }, []);

  const handleOpenFile = useCallback(async (filePath) => {
    if (window.electronAPI) {
      await window.electronAPI.openFile(filePath);
    }
  }, []);

  const handleShowFile = useCallback(async (filePath) => {
    if (window.electronAPI) {
      await window.electronAPI.showFile(filePath);
    }
  }, []);

  return (
    <div className="px-4 py-6 sm:px-0 max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          🔍 {settings.healthcareMode ? 'AI Medical File Search' : 'Smart File Search'}
        </h2>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          {settings.healthcareMode 
            ? 'Search your organized medical files using natural language queries'
            : 'Find your organized files quickly with intelligent search'
          }
        </p>
      </div>

      {/* Search Interface */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 mb-8">
        <div className="mb-6">
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Search Query
          </label>
          <div className="flex space-x-4">
            <input
              type="text"
              id="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={settings.healthcareMode 
                ? 'Try: "cardiology files from 2024" or "recent lab results"'
                : 'Try: "files from this week" or "project documents"'
              }
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-3 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors btn-focus flex items-center"
            >
              {loading ? (
                <>
                  <div className="spinner mr-2" />
                  Searching...
                </>
              ) : (
                <>
                  🔍 Search
                </>
              )}
            </button>
          </div>
        </div>

        {/* Index Button */}
        <div className="flex justify-between items-center mb-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
          <div>
            <h3 className="font-medium text-gray-900 dark:text-white">File Index</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Index your organized files to enable AI search
            </p>
          </div>
          <button
            onClick={handleIndexFiles}
            disabled={indexing}
            className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-medium transition-colors btn-focus flex items-center"
          >
            {indexing ? (
              <>
                <div className="spinner mr-2" />
                Indexing...
              </>
            ) : (
              '📊 Index Files'
            )}
          </button>
        </div>

        {/* Suggested Queries */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            💡 Suggested Queries
          </h3>
          <div className="flex flex-wrap gap-2">
            {suggestedQueries.map((suggestedQuery, index) => (
              <button
                key={index}
                onClick={() => handleSuggestedQuery(suggestedQuery)}
                className="bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-3 py-1 rounded-full text-sm transition-colors"
              >
                {suggestedQuery}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {hasSearched && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Search Results
          </h3>

          {loading ? (
            <div className="text-center py-8">
              <div className="spinner mx-auto mb-4" />
              <p className="text-gray-600 dark:text-gray-400">Searching files...</p>
            </div>
          ) : results.length > 0 ? (
            <div className="space-y-4">
              {results.map((file, index) => (
                <FileResult
                  key={index}
                  file={file}
                  onOpenFile={handleOpenFile}
                  onShowFile={handleShowFile}
                  healthcareMode={settings.healthcareMode}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-4xl mb-4">📄</div>
              <p className="text-gray-600 dark:text-gray-400">
                {query ? `No files found for "${query}"` : 'Enter a search query to find files'}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                Make sure to index your files first for better search results
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const FileResult = ({ file, onOpenFile, onShowFile, healthcareMode }) => {
  const getCategoryBadge = (category) => {
    if (!healthcareMode) return null;

    const badges = {
      'Imaging': { icon: '🔬', color: 'purple' },
      'Labs': { icon: '🧪', color: 'green' },
      'Clinical Notes': { icon: '📋', color: 'blue' },
      'Genomics': { icon: '🧬', color: 'yellow' },
      'Medications': { icon: '💊', color: 'red' },
      'Research': { icon: '📚', color: 'indigo' }
    };

    const badge = badges[category];
    if (!badge) return null;

    return (
      <span className={`medical-badge ${badge.color.toLowerCase()}`}>
        {badge.icon} {category}
      </span>
    );
  };

  const getFileIcon = (filename) => {
    const ext = filename.toLowerCase().split('.').pop();
    const iconMap = {
      pdf: '📄',
      doc: '📄',
      docx: '📄',
      txt: '📝',
      md: '📝',
      jpg: '🖼️',
      jpeg: '🖼️',
      png: '🖼️',
      gif: '🖼️',
      mp4: '🎥',
      mp3: '🎵',
      zip: '📦',
      dcm: '🏥',
      dicom: '🏥',
      vcf: '🧬',
      bam: '🧬',
      fastq: '🧬'
    };
    return iconMap[ext] || '📄';
  };

  return (
    <div className="file-result border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-lg transition-all cursor-pointer">
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3 mb-2">
            <span className="text-2xl">{getFileIcon(file.filename)}</span>
            <div className="flex-1">
              <h4 className="text-lg font-medium text-gray-900 dark:text-white truncate">
                {file.filename}
              </h4>
              <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400 mt-1">
                <span>📅 {file.modified}</span>
                {getCategoryBadge(file.category)}
              </div>
            </div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-300 truncate">
            📍 {file.path}
          </p>
        </div>

        <div className="flex space-x-2 ml-4">
          <button
            onClick={() => onOpenFile(file.path)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm transition-colors btn-focus"
            title="Open file"
          >
            Open
          </button>
          <button
            onClick={() => onShowFile(file.path)}
            className="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded text-sm transition-colors btn-focus"
            title="Show in folder"
          >
            Show
          </button>
        </div>
      </div>
    </div>
  );
};

export default QueryInterface;
