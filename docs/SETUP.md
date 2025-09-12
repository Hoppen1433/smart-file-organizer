# Setup Guide

This guide will help you get the Smart File Organizer up and running on your system.

## 🚀 Quick Installation

1. **Clone or download** the repository to your preferred location
2. **Open Terminal** and navigate to the project directory
3. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

The setup script will automatically:
- Create the organized file directory structure
- Make all scripts executable
- Check for required dependencies
- Create initial configuration
- Test the system

## 📋 System Requirements

- **Operating System**: macOS, Linux, or Windows with WSL
- **Python**: Version 3.6 or later
- **Disk Space**: At least 100MB free for organized files
- **Permissions**: Read/write access to Documents folder

## 📁 Directory Structure

After setup, you'll have:

```
~/Documents/organized_files/
├── medical/           # Medical documents and research
├── education/         # Study materials and courses
├── research/          # Academic papers and data
├── personal/          # Photos, music, personal docs
├── projects/          # Code and development files
├── writing/           # Articles, books, creative content
├── software/          # Applications and installers
├── documents/         # General documents
├── temp_screenshots/  # Screenshots (auto-cleanup)
├── actions/          # Action items from screenshots
├── logs/             # System logs
└── config.json       # System configuration
```

## 🔧 Configuration

The system works out of the box with intelligent defaults, but you can customize:

### Changing the Base Directory

Edit `config.json` to change where files are organized:

```json
{
  "base_path": "/path/to/your/organized/files"
}
```

### Customizing Categories

You can enable/disable categories or modify their descriptions in `config.json`.

### Adding Custom Keywords

Edit the Python scripts to add domain-specific keywords for better categorization:

```python
# In downloads_organizer.py
self.medical_keywords = [
    'medical', 'clinical', 'your-custom-terms'
]
```

## 🧪 Testing Your Setup

1. **Basic test**:
   ```bash
   ./organize --help
   ```

2. **Dry run test**:
   ```bash
   ./organize folder ~/Desktop --dry-run
   ```

3. **Small test with Downloads**:
   ```bash
   ./organize downloads --dry-run
   ```

## 🔍 Troubleshooting

### Permission Errors
```bash
chmod +x organize
chmod +x scripts/*.py
```

### Python Module Issues
Most required modules are built-in. If you get import errors:
```bash
pip3 install --user [module_name]
```

### Path Not Found
Ensure you're running commands from the project directory, or add it to your PATH:
```bash
export PATH="$PATH:/path/to/smart-file-organizer"
```

## 🎯 First Organization

1. **Start with a dry run**:
   ```bash
   ./organize downloads --dry-run
   ```

2. **If the preview looks good, run it**:
   ```bash
   ./organize downloads
   ```

3. **Organize other folders**:
   ```bash
   ./organize folder ~/Desktop
   ./organize folder ~/Documents
   ```

4. **Set up screenshot organization**:
   ```bash
   ./organize screenshots --dry-run
   ./organize screenshots
   ```

## ⚡ Advanced Setup

### Automated Daily Organization
Add to your crontab for daily organization:
```bash
# Run daily at 11 PM
0 23 * * * /path/to/smart-file-organizer/organize downloads
```

### Integration with File Managers
Create shell shortcuts or add to your file manager's context menu for quick organization.

### Backup Integration
The organized structure works well with cloud sync services like Dropbox, Google Drive, or iCloud.

## 📞 Getting Help

- Check the logs in `~/Documents/organized_files/logs/`
- Review the configuration in `config.json`
- Run commands with `--dry-run` to preview changes
- Use `--help` flag on any command for detailed usage

Your Smart File Organizer is now ready to transform your digital chaos into organized clarity!
