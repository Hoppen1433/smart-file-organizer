import React, { useState, useEffect } from 'react';

const PathEditor = ({ 
  file, 
  currentPath,
  basePath,
  onPathChange, 
  onCancel, 
  existingPaths = []
}) => {
  const [customPath, setCustomPath] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    if (file && currentPath) {
      setCustomPath(currentPath);
    }
  }, [file, currentPath]);

  const generateSuggestions = (input) => {
    const inputLower = input.toLowerCase();
    
    // Smart suggestions based on file content and existing structure
    const commonPaths = [
      // Base directories
      '/Users/theodoreaddo/Documents/auto_organized/medical',
      '/Users/theodoreaddo/Documents/auto_organized/education', 
      '/Users/theodoreaddo/Documents/auto_organized/research',
      '/Users/theodoreaddo/Documents/auto_organized/projects',
      '/Users/theodoreaddo/Documents/auto_organized/personal',
      '/Users/theodoreaddo/Downloads/medical',
      '/Users/theodoreaddo/Downloads/organized',
      
      // Medical subcategories
      '/Users/theodoreaddo/Documents/auto_organized/medical/cardiology',
      '/Users/theodoreaddo/Documents/auto_organized/medical/radiology',
      '/Users/theodoreaddo/Documents/auto_organized/medical/case_studies',
      '/Users/theodoreaddo/Documents/auto_organized/medical/research',
      
      // Education paths
      '/Users/theodoreaddo/Documents/auto_organized/education/usmle',
      '/Users/theodoreaddo/Documents/auto_organized/education/residency',
      
      // Research paths
      '/Users/theodoreaddo/Documents/auto_organized/research/papers',
      '/Users/theodoreaddo/Documents/auto_organized/research/data'
    ];

    const filtered = [...commonPaths, ...existingPaths]
      .filter(path => path.toLowerCase().includes(inputLower))
      .sort((a, b) => a.localeCompare(b))
      .slice(0, 6);

    setSuggestions(filtered);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setCustomPath(value);
    setShowSuggestions(true);
    generateSuggestions(value);
  };

  const handleSuggestionClick = (suggestion) => {
    setCustomPath(suggestion);
    setShowSuggestions(false);
  };

  const handleSubmit = () => {
    if (customPath.trim()) {
      onPathChange(customPath.trim());
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSubmit();
    } else if (e.key === 'Escape') {
      onCancel();
    }
  };

  return (
    <div className="relative">
      <input
        type="text"
        value={customPath}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onFocus={() => setShowSuggestions(true)}
        placeholder="Type full path... e.g., /Users/yourusername/Documents/medical"
        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                 bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm
                 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
      />
      
      {/* Suggestions dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg max-h-40 overflow-y-auto">
          {suggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className="w-full text-left px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 
                       text-gray-900 dark:text-white text-sm border-b border-gray-100 dark:border-gray-700 last:border-b-0"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
      
      <div className="mt-2 flex space-x-2">
        <button
          onClick={handleSubmit}
          className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700"
        >
          ✓ Save
        </button>
        <button
          onClick={onCancel}
          className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600"
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

const OrganizationPreview = ({ previewData, onCategoryChange, onOrganizeNow, onBack, settings }) => {
  const [files, setFiles] = useState([]);
  const [editingFileId, setEditingFileId] = useState(null);
  const [existingPaths, setExistingPaths] = useState([]);

  useEffect(() => {
    if (previewData?.files) {
      const enhancedFiles = previewData.files.map((file, index) => {
        // Clean filename - remove any arrow notation that might exist
        let cleanName = file.name;
        if (cleanName.includes(' → ')) {
          cleanName = cleanName.split(' → ')[0];
        }
        
        return {
          ...file,
          id: `file_${index}`,
          name: cleanName,
          originalPath: getFullDestinationPath(file),
          currentPath: getFullDestinationPath(file),
          hasBeenEdited: false
        };
      });
      setFiles(enhancedFiles);
      
      // Extract existing paths
      const paths = [...new Set(enhancedFiles.map(f => f.currentPath))];
      setExistingPaths(paths);
    }
  }, [previewData]);

  const getFullDestinationPath = (file) => {
    const basePath = settings?.organizationPath || previewData?.destinationPath || 
      '/Users/theodoreaddo/Documents/auto_organized';
    const categoryPath = file.category || 'misc';
    return `${basePath}/${categoryPath}`;
  };

  const handlePathEdit = (fileId, newPath) => {
    setFiles(prevFiles => 
      prevFiles.map(file => 
        file.id === fileId 
          ? { ...file, currentPath: newPath, hasBeenEdited: true }
          : file
      )
    );
    setEditingFileId(null);
    
    // Update existing paths
    if (!existingPaths.includes(newPath)) {
      setExistingPaths(prev => [...prev, newPath]);
    }
  };

  const getCategoryCounts = () => {
    const counts = {};
    files.forEach(file => {
      const dir = file.currentPath.split('/').pop() || 'misc';
      counts[dir] = (counts[dir] || 0) + 1;
    });
    return counts;
  };

  const totalFiles = files.length;
  const organizableFiles = files.filter(f => !f.currentPath.includes('misc')).length;

  if (!previewData) {
    return (
      <div className="text-center py-12">
        <div className="text-4xl mb-4">🔍</div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Analyzing Files...</h2>
        <p className="text-gray-600 dark:text-gray-300">Scanning folder and categorizing files for preview...</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">🎯 Smart Organization Preview</h1>
          <button
            onClick={onBack}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 font-medium"
          >
            ← Back to Dashboard
          </button>
        </div>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-2">
          Review and customize exactly where each file will be organized
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
          <div className="text-2xl font-bold text-gray-900 dark:text-white">{totalFiles}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Total Files Found</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
          <div className="text-2xl font-bold text-green-600 dark:text-green-400">{organizableFiles}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Will Organize</div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 text-center">
          <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{files.filter(f => f.hasBeenEdited).length}</div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Custom Paths</div>
        </div>
      </div>

      {/* Clean File List */}
      <div className="mb-8">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">📄 Files & Destinations</h3>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
          <div className="max-h-96 overflow-y-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50 dark:bg-gray-700 sticky top-0">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">File</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Destination Path</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {files.map((file) => (
                  <tr key={file.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-4 py-3">
                      <div className="flex items-center">
                        <span className="text-lg mr-2">📄</span>
                        <div>
                          <div className="font-medium text-gray-900 dark:text-white">{file.name}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            {file.size || 'Unknown size'}
                            {file.hasBeenEdited && (
                              <span className="ml-2 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 px-1 rounded">
                                ✏️ Modified
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {editingFileId === file.id ? (
                        <PathEditor
                          file={file}
                          currentPath={file.currentPath}
                          existingPaths={existingPaths}
                          onPathChange={(newPath) => handlePathEdit(file.id, newPath)}
                          onCancel={() => setEditingFileId(null)}
                        />
                      ) : (
                        <div className="font-mono text-xs text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-900 rounded px-2 py-1">
                          {file.currentPath}/{file.name}
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex space-x-2">
                        <button
                          onClick={async () => {
                            console.log('Quick Look button clicked for file:', file);
                            console.log('File path:', file.path);
                            
                            if (window.electronAPI) {
                              try {
                                const result = await window.electronAPI.quickLookFile(file.path);
                                console.log('Quick Look result:', result);
                                
                                if (!result.success) {
                                  alert('Quick Look failed: ' + result.error);
                                }
                              } catch (error) {
                                console.error('Quick Look error:', error);
                                alert('Quick Look error: ' + error.message);
                              }
                            } else {
                              alert('Electron API not available');
                            }
                          }}
                          className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-200 text-xs font-medium flex items-center"
                        >
                          <span className="mr-1">👁️</span>
                          Quick Look
                        </button>
                        <button
                          onClick={() => setEditingFileId(file.id)}
                          className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200 text-xs font-medium flex items-center"
                        >
                          <span className="mr-1">✏️</span>
                          Edit Path
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 pb-8">
        <button
          onClick={onBack}
          className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 font-medium"
        >
          ← Back to Dashboard
        </button>
        <button
          onClick={() => onOrganizeNow(files)}
          className="px-8 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium flex items-center"
        >
          <span className="mr-2">🚀</span>
          Organize Now ({organizableFiles} files)
        </button>
      </div>
    </div>
  );
};

export default OrganizationPreview;