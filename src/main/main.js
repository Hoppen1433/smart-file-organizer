const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const { spawn } = require('cross-spawn');
const fs = require('fs');
const chokidar = require('chokidar');

class SmartFileOrganizerApp {
  constructor() {
    this.mainWindow = null;
    this.organizationInProgress = false;
    this.setupApp();
  }

  setupApp() {
    app.whenReady().then(() => {
      this.createWindow();
      this.setupIPC();
    });

    // Open organized files folder
    ipcMain.handle('open-organized-folder', async () => {
      const organizePath = path.join(require('os').homedir(), 'Documents', 'auto_organized');
      
      try {
        // Create folder if it doesn't exist
        if (!fs.existsSync(organizePath)) {
          fs.mkdirSync(organizePath, { recursive: true });
        }
        
        // Open in Finder/Explorer
        await shell.openPath(organizePath);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Get file statistics
    ipcMain.handle('get-file-statistics', async () => {
      const organizePath = path.join(require('os').homedir(), 'Documents', 'auto_organized');
      
      if (!fs.existsSync(organizePath)) {
        return {
          totalFiles: 0,
          medicalFiles: 0,
          categories: 0,
          lastOrganized: 'Never'
        };
      }
      
      let totalFiles = 0;
      let medicalFiles = 0;
      const categories = new Set();
      let lastModified = 0;
      
      try {
        // Recursively count files
        const countFiles = (dir) => {
          const items = fs.readdirSync(dir);
          for (const item of items) {
            if (item.startsWith('.')) continue;
            
            const fullPath = path.join(dir, item);
            const stats = fs.statSync(fullPath);
            
            if (stats.isDirectory()) {
              const relativePath = path.relative(organizePath, fullPath);
              if (relativePath) categories.add(relativePath);
              countFiles(fullPath);
            } else {
              totalFiles++;
              if (fullPath.includes('medical')) medicalFiles++;
              if (stats.mtime.getTime() > lastModified) {
                lastModified = stats.mtime.getTime();
              }
            }
          }
        };
        
        countFiles(organizePath);
        
        return {
          totalFiles,
          medicalFiles,
          categories: categories.size,
          lastOrganized: lastModified > 0 ? new Date(lastModified).toLocaleDateString() : 'Never'
        };
      } catch (error) {
        console.error('Error calculating statistics:', error);
        return {
          totalFiles: 0,
          medicalFiles: 0,
          categories: 0,
          lastOrganized: 'Error'
        };
      }
    });

    // Get app version
    ipcMain.handle('get-app-version', () => {
      return app.getVersion();
    });

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createWindow();
      }
    });
  }

  createWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1200,
      height: 800,
      minWidth: 800,
      minHeight: 600,
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        enableRemoteModule: false,
        preload: path.join(__dirname, 'preload.js')
      },
      titleBarStyle: 'hiddenInset',
      icon: path.join(__dirname, '../../assets/icon.png'),
      show: false
    });

    // Load the app directly from our HTML file
    const startUrl = `file://${path.join(__dirname, '../../build/index.html')}`;
    
    this.mainWindow.loadURL(startUrl);

    // Show window when ready
    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
    });

    // Open external links in browser
    this.mainWindow.webContents.setWindowOpenHandler(({ url }) => {
      shell.openExternal(url);
      return { action: 'deny' };
    });

    if (isDev) {
      this.mainWindow.webContents.openDevTools();
    }
  }

  setupIPC() {
    // Select folder for organization
    ipcMain.handle('select-folder', async () => {
      const result = await dialog.showOpenDialog(this.mainWindow, {
        properties: ['openDirectory'],
        title: 'Select folder to organize'
      });
      
      if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0];
      }
      return null;
    });

    // Select files for organization
    ipcMain.handle('select-files', async () => {
      const result = await dialog.showOpenDialog(this.mainWindow, {
        properties: ['openFile', 'multiSelections'],
        title: 'Select files to organize'
      });
      
      if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths;
      }
      return null;
    });

    // Organize files with NLU intelligence
    ipcMain.handle('organize-files', async (event, options) => {
      const { sourcePath, dryRun } = options;
      
      return new Promise((resolve, reject) => {
        if (this.organizationInProgress) {
          reject(new Error('Organization already in progress'));
          return;
        }

        this.organizationInProgress = true;
        
        // Always use the NLU-enhanced organizer
        const scriptPath = path.join(__dirname, '../python', 'healthcare_enhanced_organizer.py');
        const args = [scriptPath, sourcePath];
        
        if (dryRun) {
          args.push('--dry-run');
        }

        // Spawn Python process
        const pythonProcess = spawn('python3', args, {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          const chunk = data.toString();
          output += chunk;
          
          // Send real-time updates to renderer
          event.sender.send('organization-progress', {
            type: 'stdout',
            data: chunk
          });
        });

        pythonProcess.stderr.on('data', (data) => {
          const chunk = data.toString();
          errorOutput += chunk;
          
          event.sender.send('organization-progress', {
            type: 'stderr',
            data: chunk
          });
        });

        pythonProcess.on('close', (code) => {
          this.organizationInProgress = false;
          
          if (code === 0) {
            const summary = this.parseOrganizationOutput(output);
            
            // If no files were processed, still count this as success but indicate it
            resolve({
              success: true,
              output: output,
              summary: summary,
              isEmpty: summary.filesProcessed === 0
            });
          } else {
            reject(new Error(`Organization failed with code ${code}: ${errorOutput}`));
          }
        });

        pythonProcess.on('error', (error) => {
          this.organizationInProgress = false;
          reject(new Error(`Failed to start organization: ${error.message}`));
        });
      });
    });

    // Query medical files
    ipcMain.handle('query-medical-files', async (event, query) => {
      return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../python/medical_query_system.py');
        const pythonProcess = spawn('python3', [scriptPath, 'query', query], {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            resolve({
              success: true,
              results: this.parseQueryResults(output)
            });
          } else {
            reject(new Error(`Query failed: ${errorOutput}`));
          }
        });
      });
    });

    // Index medical files
    ipcMain.handle('index-medical-files', async () => {
      return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../python/medical_query_system.py');
        const pythonProcess = spawn('python3', [scriptPath, 'index'], {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            resolve({
              success: true,
              output: output
            });
          } else {
            reject(new Error(`Indexing failed: ${errorOutput}`));
          }
        });
      });
    });

    // Open file in default application
    ipcMain.handle('open-file', async (event, filePath) => {
      try {
        await shell.openPath(filePath);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Show file in finder/explorer
    ipcMain.handle('show-file', async (event, filePath) => {
      shell.showItemInFolder(filePath);
      return { success: true };
    });

    // Preview file content
    ipcMain.handle('preview-file', async (event, filePath) => {
      try {
        const stats = fs.statSync(filePath);
        const ext = path.extname(filePath).toLowerCase();
        
        // File size limit for preview (5MB)
        if (stats.size > 5 * 1024 * 1024) {
          return 'File too large to preview (>5MB)';
        }
        
        // Handle different file types
        if (['.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.css', '.xml', '.yml', '.yaml'].includes(ext)) {
          const content = fs.readFileSync(filePath, 'utf-8');
          // Truncate if too long
          if (content.length > 50000) {
            return content.substring(0, 50000) + '\n\n... (truncated for preview)';
          }
          return content;
        } else if (['.pdf'].includes(ext)) {
          return 'PDF Preview not available in this version. Use the "Open" button to view the file.';
        } else if (['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'].includes(ext)) {
          return 'Image preview not available in this version. Use the "Open" button to view the file.';
        } else {
          return `Preview not available for ${ext} files. Use the "Open" button to view the file.`;
        }
      } catch (error) {
        return `Error reading file: ${error.message}`;
      }
    });

    // Quick Look file using Mac's system preview
    ipcMain.handle('quick-look-file', async (event, filePath) => {
      try {
        console.log('Quick Look attempt for:', filePath);
        
        // First check if file exists
        if (!fs.existsSync(filePath)) {
          console.log('File does not exist:', filePath);
          throw new Error(`File not found: ${filePath}`);
        }
        
        // Use Mac's Quick Look via shell command with absolute path
        const absolutePath = path.resolve(filePath);
        console.log('Using absolute path:', absolutePath);
        
        const qlProcess = spawn('qlmanage', ['-p', absolutePath], {
          stdio: ['ignore', 'pipe', 'pipe'],
          detached: false
        });
        
        let qlOutput = '';
        let qlError = '';
        
        qlProcess.stdout.on('data', (data) => {
          qlOutput += data.toString();
        });
        
        qlProcess.stderr.on('data', (data) => {
          qlError += data.toString();
        });
        
        return new Promise((resolve) => {
          qlProcess.on('close', (code) => {
            console.log(`qlmanage exit code: ${code}`);
            console.log(`qlmanage output: ${qlOutput}`);
            console.log(`qlmanage error: ${qlError}`);
            
            if (code === 0) {
              resolve({ success: true, message: 'Quick Look opened successfully' });
            } else {
              // Fallback to system default
              shell.openPath(absolutePath).then(() => {
                resolve({ success: true, message: 'Opened with default application' });
              }).catch((err) => {
                resolve({ success: false, error: `Failed to open: ${err.message}` });
              });
            }
          });
        });
        
      } catch (error) {
        console.log('Quick Look error:', error);
        // Fallback to regular file opening if Quick Look fails
        try {
          await shell.openPath(filePath);
          return { success: true, message: 'File opened with default application' };
        } catch (fallbackError) {
          return { success: false, error: `Failed to open file: ${fallbackError.message}` };
        }
      }
    });

    // Get AI learning insights
    ipcMain.handle('get-ai-insights', async () => {
      return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../python/ai_learning_system.py');
        const pythonProcess = spawn('python3', [scriptPath, 'insights'], {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            try {
              const insights = JSON.parse(output);
              resolve(insights);
            } catch (e) {
              resolve({ message: 'No learning data available' });
            }
          } else {
            reject(new Error(`AI insights failed: ${errorOutput}`));
          }
        });
      });
    });

    // Record AI correction for learning
    ipcMain.handle('record-ai-correction', async (event, correction) => {
      return new Promise((resolve, reject) => {
        const { filename, originalCategory, correctedCategory, aiConfidence } = correction;
        
        const scriptPath = path.join(__dirname, '../python/ai_learning_system.py');
        const args = [scriptPath, 'record', filename, originalCategory, correctedCategory];
        
        const pythonProcess = spawn('python3', args, {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            resolve({ success: true, message: 'AI correction recorded' });
          } else {
            reject(new Error(`Failed to record correction: ${errorOutput}`));
          }
        });
      });
    });

    // Preview organization with NLU
    ipcMain.handle('preview-organization', async (event, options) => {
      const { sourcePath } = options;
      
      return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../python', 'healthcare_enhanced_organizer.py');
        const args = [scriptPath, sourcePath, '--preview-mode'];

        const pythonProcess = spawn('python3', args, {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            const previewData = this.parsePreviewOutput(output, sourcePath);
            resolve(previewData);
          } else {
            reject(new Error(`Preview failed with code ${code}: ${errorOutput}`));
          }
        });

        pythonProcess.on('error', (error) => {
          reject(new Error(`Failed to start preview: ${error.message}`));
        });
      });
    });

    // Undo last organization
    ipcMain.handle('undo-organization', async (event, organizationId) => {
      return new Promise((resolve, reject) => {
        const scriptPath = path.join(__dirname, '../python/undo_organizer.py');
        const args = [scriptPath, organizationId || 'latest'];

        const pythonProcess = spawn('python3', args, {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          const chunk = data.toString();
          output += chunk;
          
          event.sender.send('organization-progress', {
            type: 'undo-progress',
            data: chunk
          });
        });

        pythonProcess.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code === 0) {
            resolve({
              success: true,
              message: 'Organization successfully undone',
              output: output
            });
          } else {
            reject(new Error(`Undo failed with code ${code}: ${errorOutput}`));
          }
        });

        pythonProcess.on('error', (error) => {
          reject(new Error(`Failed to start undo: ${error.message}`));
        });
      });
    });

    // Organize files with specific categories (from preview mode)
    ipcMain.handle('organize-files-with-categories', async (event, options) => {
      const { files } = options;
      
      return new Promise((resolve, reject) => {
        if (this.organizationInProgress) {
          reject(new Error('Organization already in progress'));
          return;
        }

        this.organizationInProgress = true;
        
        // Create temporary JSON file with category mappings
        const tempFile = path.join(__dirname, '../python/temp_categories.json');
        fs.writeFileSync(tempFile, JSON.stringify(files, null, 2));
        
        const scriptPath = path.join(__dirname, '../python', 'healthcare_enhanced_organizer.py');
        const args = [scriptPath, '--from-categories', tempFile];

        const pythonProcess = spawn('python3', args, {
          stdio: ['pipe', 'pipe', 'pipe']
        });

        let output = '';
        let errorOutput = '';

        pythonProcess.stdout.on('data', (data) => {
          const chunk = data.toString();
          output += chunk;
          
          event.sender.send('organization-progress', {
            type: 'stdout',
            data: chunk
          });
        });

        pythonProcess.stderr.on('data', (data) => {
          const chunk = data.toString();
          errorOutput += chunk;
          
          event.sender.send('organization-progress', {
            type: 'stderr',
            data: chunk
          });
        });

        pythonProcess.on('close', (code) => {
          this.organizationInProgress = false;
          
          // Clean up temp file
          try {
            fs.unlinkSync(tempFile);
          } catch (e) {
            console.log('Could not delete temp file:', e.message);
          }
          
          if (code === 0) {
            const summary = this.parseOrganizationOutput(output);
            resolve({
              success: true,
              output: output,
              summary: summary
            });
          } else {
            reject(new Error(`Organization failed with code ${code}: ${errorOutput}`));
          }
        });

        pythonProcess.on('error', (error) => {
          this.organizationInProgress = false;
          reject(new Error(`Failed to start organization: ${error.message}`));
        });
      });
    });
  }

  parseOrganizationOutput(output) {
    // Parse the Python script output to extract useful information
    const lines = output.split('\n');
    let filesProcessed = 0;
    let categoriesFound = {};
    let healthcareFiles = 0;

    for (const line of lines) {
      // Look for organization completion message
      if (line.includes('Organized') && line.includes('files')) {
        const match = line.match(/(\d+) files/);
        if (match) {
          filesProcessed = parseInt(match[1]);
        }
      }
      
      // Look for NLU success rate
      if (line.includes('NLU Success Rate:')) {
        const match = line.match(/(\d+)\/(\d+) files \((\d+)%\)/);
        if (match) {
          filesProcessed = parseInt(match[1]);
        }
      }

      // Parse category completion - look for ✅ Category: X files
      if (line.includes('✅') && line.includes(':') && line.includes('files')) {
        const match = line.match(/✅\s*([^:]+):\s*(\d+)/);
        if (match) {
          const category = match[1].trim();
          const count = parseInt(match[2]);
          categoriesFound[category] = count;
        }
      }
      
      // Alternative parsing for category completion
      if (line.match(/^\s*✅\s+[^:]+:\s+\d+\s+files/)) {
        const match = line.match(/✅\s+([^:]+):\s+(\d+)\s+files/);
        if (match) {
          const category = match[1].trim();
          const count = parseInt(match[2]);
          categoriesFound[category] = count;
          if (category.includes('medical')) {
            healthcareFiles += count;
          }
        }
      }
    }
    
    // If we didn't find specific counts but the process completed, estimate
    if (filesProcessed === 0 && output.includes('Complete')) {
      const moveMatches = output.match(/✅/g);
      if (moveMatches) {
        filesProcessed = Object.values(categoriesFound).reduce((sum, count) => sum + count, 0);
      }
    }

    return {
      filesProcessed,
      healthcareFiles,
      categoriesFound,
      rawOutput: output
    };
  }

  parseQueryResults(output) {
    // Parse query results from Python script
    const lines = output.split('\\n');
    const results = [];
    
    let currentFile = null;
    for (const line of lines) {
      if (line.includes('📄')) {
        if (currentFile) {
          results.push(currentFile);
        }
        currentFile = {
          filename: line.replace('📄', '').trim(),
          category: '',
          modified: '',
          path: ''
        };
      } else if (currentFile) {
        if (line.includes('📂 Category:')) {
          currentFile.category = line.replace('📂 Category:', '').trim();
        } else if (line.includes('📅 Modified:')) {
          currentFile.modified = line.replace('📅 Modified:', '').trim();
        } else if (line.includes('📍 Path:')) {
          currentFile.path = line.replace('📍 Path:', '').trim();
        }
      }
    }
    
    if (currentFile) {
      results.push(currentFile);
    }

    return results;
  }

  parsePreviewOutput(output, sourcePath) {
    // Parse preview output to extract file list with categories
    const lines = output.split('\n');
    const files = [];
    let destinationPath = '';
    
    let currentFile = null;
    for (const line of lines) {
      // Extract destination path
      if (line.includes('Destination:') || line.includes('Output directory:')) {
        destinationPath = line.split(':')[1]?.trim() || '';
      }
      
      // Parse file information
      if (line.includes('📄') || line.includes('File:')) {
        if (currentFile) {
          files.push(currentFile);
        }
        const fileName = line.replace('📄', '').replace('File:', '').trim();
        currentFile = {
          name: fileName,
          category: 'downloads/misc',
          size: 'Unknown',
          path: path.join(sourcePath, fileName)
        };
      } else if (currentFile && line.includes('→')) {
        // Parse category assignment: "File.pdf → medical/imaging"
        const categoryMatch = line.match(/→\s*([^\s]+)/); 
        if (categoryMatch) {
          currentFile.category = categoryMatch[1].trim();
        }
      } else if (currentFile && (line.includes('Category:') || line.includes('📂'))) {
        const categoryMatch = line.match(/(?:Category:|📂)\s*([^\n]+)/);
        if (categoryMatch) {
          currentFile.category = categoryMatch[1].trim();
        }
      }
    }
    
    if (currentFile) {
      files.push(currentFile);
    }
    
    // If no files were parsed from output, try to scan directory directly
    if (files.length === 0) {
      try {
        const dirFiles = fs.readdirSync(sourcePath);
        for (const file of dirFiles) {
          const filePath = path.join(sourcePath, file);
          const stats = fs.statSync(filePath);
          if (stats.isFile()) {
            files.push({
              name: file,
              category: this.categorizeFile(file),
              size: this.formatFileSize(stats.size),
              path: filePath
            });
          }
        }
      } catch (error) {
        console.error('Error scanning directory:', error);
      }
    }
    
    return {
      files,
      destinationPath: destinationPath || path.join(process.env.HOME || process.env.USERPROFILE, 'Documents', 'auto_organized')
    };
  }

  categorizeFile(fileName) {
    const lower = fileName.toLowerCase();
    const ext = path.extname(fileName).toLowerCase();
    
    // Medical files - be more aggressive
    if (lower.includes('ct') || lower.includes('mri') || lower.includes('xray') || lower.includes('dicom') || 
        lower.includes('scan') || lower.includes('radiology') || lower.includes('imaging')) {
      return 'medical/imaging';
    }
    if (lower.includes('lab') || lower.includes('blood') || lower.includes('cbc') || lower.includes('results') ||
        lower.includes('test') || lower.includes('report') || lower.includes('pathology')) {
      return 'medical/labs';
    }
    if (lower.includes('clinical') || lower.includes('patient') || lower.includes('medical') ||
        lower.includes('diagnosis') || lower.includes('treatment') || lower.includes('therapy')) {
      return 'medical/clinical_notes';
    }
    if (lower.includes('genetic') || lower.includes('genomic') || lower.includes('dna') ||
        lower.includes('gene') || lower.includes('chromosome')) {
      return 'medical/genomics';
    }
    if (lower.includes('medication') || lower.includes('prescription') || lower.includes('drug') ||
        lower.includes('pharma') || lower.includes('dose')) {
      return 'medical/medications';
    }
    if (lower.includes('muscle') || lower.includes('anatomy') || lower.includes('physiology') ||
        lower.includes('body') || lower.includes('organ') || lower.includes('system')) {
      return 'medical/anatomy';
    }
    
    // Education - be more aggressive
    if (lower.includes('lecture') || lower.includes('course') || lower.includes('study') ||
        lower.includes('usmle') || lower.includes('exam') || lower.includes('test') ||
        lower.includes('school') || lower.includes('class') || lower.includes('lesson')) {
      return 'education/courses';
    }
    if (lower.includes('textbook') || lower.includes('book') || lower.includes('chapter') ||
        ext === '.pdf' && lower.includes('guide')) {
      return 'education/textbooks';
    }
    
    // Research - be more aggressive  
    if (lower.includes('research') || lower.includes('paper') || lower.includes('study') ||
        lower.includes('analysis') || lower.includes('data') || lower.includes('statistics') ||
        lower.includes('publication') || lower.includes('journal')) {
      return 'research/papers';
    }
    
    // Projects - be more aggressive
    if (lower.includes('code') || lower.includes('script') || ext === '.py' || ext === '.js' ||
        ext === '.html' || ext === '.css' || ext === '.json' || ext === '.sh') {
      return 'projects/code';
    }
    if (lower.includes('project') || lower.includes('app') || lower.includes('development') ||
        lower.includes('prototype') || lower.includes('build')) {
      return 'projects/development';
    }
    
    // Personal files
    if (lower.includes('budget') || lower.includes('finance') || lower.includes('money') ||
        lower.includes('expense') || lower.includes('income')) {
      return 'personal/finance';
    }
    if (lower.includes('photo') || ext === '.jpg' || ext === '.jpeg' || ext === '.png' ||
        ext === '.gif' || ext === '.bmp' || ext === '.tiff') {
      return 'personal/photos';
    }
    
    // Documents by file type
    if (ext === '.pdf') {
      return 'documents/pdfs';
    }
    if (ext === '.doc' || ext === '.docx') {
      return 'documents/word';
    }
    if (ext === '.xls' || ext === '.xlsx') {
      return 'documents/excel';
    }
    if (ext === '.ppt' || ext === '.pptx') {
      return 'documents/powerpoint';
    }
    
    // Screenshots
    if (lower.includes('screenshot') || lower.includes('screen shot') || lower.includes('capture')) {
      return 'screenshots';
    }
    
    // Video files
    if (ext === '.mp4' || ext === '.mov' || ext === '.avi' || ext === '.mkv') {
      return 'media/videos';
    }
    
    // Audio files
    if (ext === '.mp3' || ext === '.wav' || ext === '.flac' || ext === '.aac') {
      return 'media/audio';
    }
    
    // Archive files
    if (ext === '.zip' || ext === '.rar' || ext === '.7z' || ext === '.tar') {
      return 'archives';
    }
    
    // Only use misc for truly unrecognizable files
    return 'documents/misc';
  }

  formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  }
}

// Initialize the app
new SmartFileOrganizerApp();
