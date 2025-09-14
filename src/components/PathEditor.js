import React, { useState, useEffect, useRef } from 'react';

const PathEditor = ({ 
  file, 
  basePath, 
  onPathChange, 
  onCancel, 
  existingPaths = [], 
  isOpen = false 
}) => {
  const [customPath, setCustomPath] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isCreatingNewFolder, setIsCreatingNewFolder] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen && file) {
      // Initialize with current file path
      const currentPath = file.category || 'personal';
      setCustomPath(currentPath);
      if (inputRef.current) {
        inputRef.current.focus();
        inputRef.current.select();
      }
    }
  }, [isOpen, file]);

  useEffect(() => {
    if (customPath && showSuggestions) {
      generateSuggestions(customPath);
    }
  }, [customPath, existingPaths]);

  const generateSuggestions = (input) => {
    const inputLower = input.toLowerCase();
    
    // Common path suggestions based on medical/academic workflow
    const commonPaths = [
      // Medical categories
      'medical',
      'medical/cardiology',
      'medical/neurology', 
      'medical/oncology',
      'medical/radiology',
      'medical/pathology',
      'medical/clinical_notes',
      'medical/lab_results',
      'medical/imaging',
      'medical/research',
      'medical/case_studies',
      'medical/protocols',
      
      // Education categories
      'education',
      'education/usmle',
      'education/usmle/step1',
      'education/usmle/step2',
      'education/residency',
      'education/courses',
      'education/textbooks',
      'education/lectures',
      'education/notes',
      
      // Research categories
      'research',
      'research/papers',
      'research/data',
      'research/analysis',
      'research/methodology',
      'research/literature_review',
      'research/grants',
      'research/presentations',
      
      // Projects categories  
      'projects',
      'projects/code',
      'projects/ai_ml',
      'projects/healthcare_tech',
      'projects/mobile_apps',
      'projects/web_development',
      'projects/data_science',
      'projects/prototypes',
      
      // Personal categories
      'personal',
      'personal/finance',
      'personal/health_records',
      'personal/insurance',
      'personal/legal',
      'personal/photos',
      'personal/documents',
      
      // Writing categories
      'writing',
      'writing/articles',
      'writing/blog_posts',
      'writing/research_papers',
      'writing/notes',
      'writing/drafts'
    ];

    // Add existing paths from the system
    const allPaths = [...new Set([...commonPaths, ...existingPaths])];
    
    // Filter and rank suggestions
    const filtered = allPaths
      .filter(path => 
        path.toLowerCase().includes(inputLower) || 
        inputLower.includes(path.toLowerCase())
      )
      .sort((a, b) => {
        // Prioritize exact matches
        if (a.toLowerCase() === inputLower) return -1;
        if (b.toLowerCase() === inputLower) return 1;
        
        // Then prioritize paths that start with input
        const aStarts = a.toLowerCase().startsWith(inputLower);
        const bStarts = b.toLowerCase().startsWith(inputLower);
        if (aStarts && !bStarts) return -1;
        if (bStarts && !aStarts) return 1;
        
        // Finally, alphabetical order
        return a.localeCompare(b);
      })
      .slice(0, 8); // Limit suggestions

    setSuggestions(filtered);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setCustomPath(value);
    setShowSuggestions(true);
    
    // Check if this would create a new folder
    const exists = existingPaths.includes(value);
    setIsCreatingNewFolder(!exists && value.length > 0);
  };

  const handleSuggestionClick = (suggestion) => {
    setCustomPath(suggestion);
    setShowSuggestions(false);
    setIsCreatingNewFolder(!existingPaths.includes(suggestion));
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
    } else if (e.key === 'Tab' && suggestions.length > 0) {
      e.preventDefault();
      setCustomPath(suggestions[0]);
      setShowSuggestions(false);
    }
  };

  const getFullPath = () => {
    const separator = window.electronAPI?.platform === 'win32' ? '\\' : '/';
    return `${basePath}${separator}${customPath.replace(/\//g, separator)}${separator}${file.name}`;
  };

  if (!isOpen || !file) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white flex items-center">
            <span className="mr-2">📁</span>
            Edit Destination Path
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Customize where <strong>{file.name}</strong> will be organized
          </p>
        </div>

        {/* Content */}
        <div className="px-6 py-4">
          {/* Current file info */}
          <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-900 rounded-lg">
            <div className="flex items-center">
              <span className="text-lg mr-2">📄</span>
              <div>
                <div className="font-medium text-gray-900 dark:text-white">{file.name}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Current category: <strong>{file.category}</strong>
                </div>
              </div>
            </div>
          </div>

          {/* Path input */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Destination Path
            </label>
            <div className="relative">
              <input
                ref={inputRef}
                type="text"
                value={customPath}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                onFocus={() => setShowSuggestions(true)}
                placeholder="e.g., medical/cardiology/case_studies"
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-white
                         focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 focus:border-transparent"
              />
              
              {/* Suggestions dropdown */}
              {showSuggestions && suggestions.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg max-h-60 overflow-y-auto">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(suggestion)}
                      className="w-full text-left px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 
                               text-gray-900 dark:text-white text-sm border-b border-gray-100 dark:border-gray-700 last:border-b-0"
                    >
                      <div className="flex items-center">
                        <span className="mr-2">📁</span>
                        <span>{suggestion}</span>
                        {existingPaths.includes(suggestion) && (
                          <span className="ml-auto text-xs text-green-600 dark:text-green-400">
                            ✓ Exists
                          </span>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
            
            {/* New folder indicator */}
            {isCreatingNewFolder && (
              <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded">
                <p className="text-sm text-blue-800 dark:text-blue-200 flex items-center">
                  <span className="mr-2">ℹ️</span>
                  This will create a new folder: <strong>{customPath}</strong>
                </p>
              </div>
            )}
          </div>

          {/* Full path preview */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Full Destination Path Preview
            </label>
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
              <code className="text-sm text-gray-800 dark:text-gray-200 break-all">
                {getFullPath()}
              </code>
            </div>
          </div>

          {/* Quick category buttons */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Quick Categories
            </label>
            <div className="flex flex-wrap gap-2">
              {[
                { path: 'medical', icon: '🏥', label: 'Medical' },
                { path: 'education', icon: '📚', label: 'Education' },
                { path: 'research', icon: '🔬', label: 'Research' },
                { path: 'projects', icon: '⚙️', label: 'Projects' },
                { path: 'personal', icon: '📱', label: 'Personal' },
                { path: 'writing', icon: '✍️', label: 'Writing' }
              ].map((category) => (
                <button
                  key={category.path}
                  onClick={() => handleSuggestionClick(category.path)}
                  className="flex items-center px-3 py-1 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 
                           rounded-full text-sm font-medium text-gray-700 dark:text-gray-300 transition-colors"
                >
                  <span className="mr-1">{category.icon}</span>
                  {category.label}
                </button>
              ))}
            </div>
          </div>

          {/* Keyboard shortcuts info */}
          <div className="mb-4 p-2 bg-gray-50 dark:bg-gray-900 rounded text-xs text-gray-600 dark:text-gray-400">
            <strong>💡 Tips:</strong> Use Tab to accept first suggestion • Enter to confirm • Escape to cancel • Use / for subfolders
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end space-x-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 
                     rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 font-medium"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={!customPath.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 
                     disabled:cursor-not-allowed font-medium flex items-center"
          >
            <span className="mr-2">✓</span>
            Save Path
            {isCreatingNewFolder && (
              <span className="ml-2 text-xs bg-blue-500 px-2 py-1 rounded">
                + New Folder
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PathEditor;