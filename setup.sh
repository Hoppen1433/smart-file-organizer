#!/bin/bash
# Smart File Organizer Setup Script
# Prepares the system for intelligent file organization

set -e  # Exit on any error

echo "🗂️  Smart File Organizer Setup"
echo "==============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set up directories
ORGANIZED_FILES_DIR="$HOME/Documents/organized_files"
LOGS_DIR="$ORGANIZED_FILES_DIR/logs"

print_status "Setting up directory structure..."

# Create main organized files directory
if [ ! -d "$ORGANIZED_FILES_DIR" ]; then
    mkdir -p "$ORGANIZED_FILES_DIR"
    print_success "Created organized files directory: $ORGANIZED_FILES_DIR"
else
    print_status "Organized files directory already exists"
fi

# Create category directories
CATEGORIES=("medical" "education" "research" "personal" "projects" "writing" "software" "documents" "temp_screenshots" "actions")

for category in "${CATEGORIES[@]}"; do
    category_dir="$ORGANIZED_FILES_DIR/$category"
    if [ ! -d "$category_dir" ]; then
        mkdir -p "$category_dir"
        print_success "Created category: $category"
    fi
done

# Create logs directory
if [ ! -d "$LOGS_DIR" ]; then
    mkdir -p "$LOGS_DIR"
    print_success "Created logs directory"
fi

# Make scripts executable
print_status "Making scripts executable..."

chmod +x "$SCRIPT_DIR/organize"
print_success "Made organize script executable"

# Make all Python scripts executable
for script in "$SCRIPT_DIR/scripts"/*.py; do
    if [ -f "$script" ]; then
        chmod +x "$script"
    fi
done
print_success "Made Python scripts executable"

# Check Python version
print_status "Checking Python installation..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.6 or later."
    exit 1
fi

# Check required Python modules
print_status "Checking required Python modules..."

REQUIRED_MODULES=("pathlib" "shutil" "re" "json" "datetime")
MISSING_MODULES=()

for module in "${REQUIRED_MODULES[@]}"; do
    if ! python3 -c "import $module" 2>/dev/null; then
        MISSING_MODULES+=("$module")
    fi
done

if [ ${#MISSING_MODULES[@]} -eq 0 ]; then
    print_success "All required Python modules are available"
else
    print_warning "Some modules may need to be installed: ${MISSING_MODULES[*]}"
    print_status "Most of these are built-in Python modules and should be available by default"
fi

# Create initial configuration
print_status "Creating initial configuration..."

# Create a simple config file
CONFIG_FILE="$ORGANIZED_FILES_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << EOF
{
  "version": "1.0",
  "created": "$(date -Iseconds)",
  "base_path": "$ORGANIZED_FILES_DIR",
  "categories": {
    "medical": {
      "description": "Medical documents, research papers, clinical materials",
      "enabled": true
    },
    "education": {
      "description": "Study materials, courses, lectures, assignments",
      "enabled": true
    },
    "research": {
      "description": "Academic papers, data analysis, research protocols",
      "enabled": true
    },
    "personal": {
      "description": "Photos, music, personal documents, tracking data",
      "enabled": true
    },
    "projects": {
      "description": "Code, development files, technical documentation",
      "enabled": true
    },
    "writing": {
      "description": "Articles, books, creative writing, professional documents",
      "enabled": true
    },
    "software": {
      "description": "Applications, installers, development tools",
      "enabled": true
    }
  },
  "features": {
    "screenshot_organization": true,
    "action_item_creation": true,
    "subfolder_organization": true,
    "duplicate_handling": true
  }
}
EOF
    print_success "Created configuration file: $CONFIG_FILE"
fi

# Create welcome README in organized files
README_FILE="$ORGANIZED_FILES_DIR/README.md"
if [ ! -f "$README_FILE" ]; then
    cat > "$README_FILE" << 'EOF'
# Your Organized Files

Welcome to your Smart File Organizer system! This directory contains all your intelligently organized files.

## 📂 Categories

- **📚 education/** - Study materials, courses, lectures, assignments
- **🏥 medical/** - Medical documents, research papers, clinical materials
- **🔬 research/** - Academic papers, data analysis, research protocols  
- **💼 personal/** - Photos, music, personal documents, tracking data
- **⚙️ projects/** - Code, development files, technical documentation
- **✍️ writing/** - Articles, books, creative writing, documents
- **💾 software/** - Applications, installers, development tools
- **📄 documents/** - General documents and files
- **📷 temp_screenshots/** - Screenshots (automatically cleaned up)
- **🎯 actions/** - Action items created from screenshots

## 🚀 Quick Commands

```bash
# Organize your Downloads folder
./organize downloads

# Organize any folder (preview first)
./organize folder ~/Desktop --dry-run
./organize folder ~/Desktop

# Smart screenshot organization
./organize screenshots

# Convert screenshots to action items
./organize actions

# Organize loose files within categories
./organize subfolders all
```

## 📊 System Information

- **Created:** $(date)
- **Base Path:** $ORGANIZED_FILES_DIR
- **Logs:** $LOGS_DIR

Your files are organized automatically based on intelligent content analysis. The system learns from your patterns and gets better over time!

---
*Generated by Smart File Organizer*
EOF
    print_success "Created welcome README"
fi

# Test the system
print_status "Testing the organization system..."

# Test basic functionality
if "$SCRIPT_DIR/organize" > /dev/null 2>&1; then
    print_success "Organization system is working correctly"
else
    print_error "There may be an issue with the organization system"
fi

# Development mode setup
if [ "$1" = "--dev" ]; then
    print_status "Setting up development mode..."
    
    # Create example files for testing
    EXAMPLES_DIR="$SCRIPT_DIR/examples"
    mkdir -p "$EXAMPLES_DIR"
    
    # Create sample files
    touch "$EXAMPLES_DIR/sample_medical_paper.pdf"
    touch "$EXAMPLES_DIR/study_notes.txt"
    touch "$EXAMPLES_DIR/research_data.csv"
    touch "$EXAMPLES_DIR/personal_photo.jpg"
    touch "$EXAMPLES_DIR/python_script.py"
    touch "$EXAMPLES_DIR/article_draft.md"
    
    print_success "Created example files for testing"
fi

# Final setup summary
echo ""
echo "✅ Setup Complete!"
echo "=================="
echo ""
echo "📁 Organized files location: $ORGANIZED_FILES_DIR"
echo "📋 Logs location: $LOGS_DIR"
echo ""
echo "🚀 Quick Start:"
echo "  1. Run: ./organize downloads"
echo "  2. Or try: ./organize folder ~/Desktop --dry-run"
echo ""
echo "📚 For more options: ./organize (shows all commands)"
echo "📖 Documentation: Check the docs/ folder"
echo ""

# Add to PATH suggestion
if [[ ":$PATH:" != *":$SCRIPT_DIR:"* ]]; then
    print_status "Optional: Add to your PATH for global access"
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\""
    echo ""
fi

print_success "Smart File Organizer is ready to use!"
