# Smart File Organizer

**A comprehensive file organization system that intelligently categorizes and manages your digital files with zero cognitive overhead.**

Transform your cluttered downloads, desktop, and document folders into a clean, organized system that works automatically. Built for professionals who need their files organized but don't want to think about it.

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/smart-file-organizer.git
   cd smart-file-organizer
   ```

2. **Run the setup**:
   ```bash
   ./setup.sh
   ```

3. **Organize your first folder**:
   ```bash
   ./organize downloads    # Organize your Downloads folder
   ./organize folder ~/Desktop --dry-run  # Preview Desktop organization
   ```

## ✨ Features

### 🧠 **Smart Categorization**
- **Content-Aware**: Analyzes filenames, extensions, and context to intelligently categorize files
- **Professional Focus**: Optimized for academic, medical, and technical professionals
- **Learning System**: Gets better over time as you use it

### 📂 **Universal Organization**
- **Any Folder**: Can organize downloads, desktop, documents, or any folder you specify
- **Preserves Structure**: Maintains folder hierarchies while organizing loose files
- **Non-Destructive**: Always preview changes with `--dry-run` before committing

### 📷 **Screenshot Intelligence**
- **Temporal Clustering**: Groups related screenshots taken within minutes of each other
- **Context Analysis**: Understands what type of content you're capturing
- **Action Items**: Converts screenshots into actionable tasks automatically

### 🔄 **Automated Workflows**
- **Subfolder Organization**: Organizes loose files within existing categories
- **Duplicate Handling**: Safely manages duplicate files with timestamps
- **Cleanup Tools**: Removes empty folders and manages temporary files

## 📋 **Categories**

The system organizes files into these intelligent categories:

- **📚 Education**: Study materials, flashcards, lecture slides, exam prep
- **🏥 Medical**: Clinical resources, research papers, medical images, USMLE materials  
- **🔬 Research**: Academic papers, data analysis, protocols, manuscripts
- **💼 Personal**: Photos, music, personal documents, tracking data
- **⚙️ Projects**: Code, development files, documentation, configuration
- **✍️ Writing**: Books, articles, creative writing, drafts
- **💾 Software**: Applications, installers, development tools

Each category has intelligent subfolders that automatically organize related content.

## 🛠️ **Commands**

### Basic Organization
```bash
./organize downloads                    # Organize Downloads folder
./organize folder ~/Desktop            # Organize any folder
./organize folder ~/Desktop --dry-run  # Preview changes first
./organize documents                    # Organize Documents folder
```

### Advanced Features
```bash
./organize screenshots              # Smart screenshot organization
./organize screenshots --dry-run   # Preview screenshot organization
./organize actions                  # Convert screenshots to actionable items
./organize subfolders all          # Organize loose files in all categories
./organize subfolders medical      # Organize loose files in medical category
```

### System Management
```bash
./organize links list              # Manage quick access links
./organize links add ~/Projects    # Add frequently used folders
```

## 📊 **Smart Screenshot Features**

### Temporal Clustering
- Groups screenshots taken within 5 minutes as related sequences
- Maintains workflow context (coding sessions, study materials, etc.)
- Preserves the story behind rapid captures

### Content Recognition
- **Medical Content**: USMLE materials, clinical guidelines, research papers
- **Educational**: Lecture slides, study guides, quiz results
- **Development**: Code snippets, error messages, documentation
- **Personal**: Social media, conversations, general references

### Action Item Generation
Screenshots can be automatically converted into actionable tasks:
- **Follow-up**: Quiz results, assessments requiring action
- **Reference**: Documentation and guides to reference later
- **Learning**: Concepts requiring deeper study
- **Decision**: Options requiring evaluation
- **Progress**: Items to track over time

## 🔧 **Configuration**

### Customizing Categories
The system can be customized by editing the keyword patterns in the organizer scripts:

```python
# Add custom keywords to existing categories
medical_keywords = ['your-custom-terms', 'medical-abbreviations']
education_keywords = ['study-materials', 'course-names']
```

### Adding New Categories
1. Update the `destinations` dictionary in the main organizer
2. Add keyword patterns for the new category
3. Update the categorization logic

### Time-Based Context
Screenshot organization considers timing:
- **Morning (6-12)**: Usually academic or professional content
- **Afternoon (12-17)**: Clinical work or meetings  
- **Evening (17-22)**: Study sessions or project work
- **Late Night (22-4)**: Deep work, coding, or research

## 📁 **Project Structure**

```
smart-file-organizer/
├── organize                    # Main command launcher
├── setup.sh                   # Installation script
├── scripts/
│   ├── downloads_organizer.py  # Downloads folder organization
│   ├── universal_organizer.py  # Any folder organization
│   ├── screenshot_organizer.py # Smart screenshot handling
│   ├── action_processor.py     # Screenshot-to-action conversion
│   └── subfolder_organizer.py  # Within-category organization
├── docs/
│   ├── SETUP.md               # Detailed setup instructions
│   ├── ADVANCED.md            # Advanced features guide
│   └── CUSTOMIZATION.md       # Customization options
└── examples/
    ├── before-after/          # Example transformations
    └── configurations/        # Sample configurations
```

## 🎯 **Use Cases**

### For Students
- Automatically organize study materials by subject
- Convert screenshot notes into study action items
- Manage research papers and course documents
- Track progress on assignments and projects

### For Medical Professionals
- Organize clinical guidelines and protocols
- Manage USMLE study materials by step and subject
- Handle medical images and research papers
- Convert clinical screenshots into follow-up items

### For Developers
- Organize code snippets and documentation
- Handle project files and configuration
- Convert error screenshots into debugging tasks
- Manage technical references and tutorials

### For Researchers  
- Organize academic papers by topic and methodology
- Manage data files and analysis scripts
- Handle research protocols and documentation
- Track manuscript versions and revisions

## 🔒 **Privacy & Safety**

- **Non-Destructive**: Always use `--dry-run` to preview changes
- **Local Only**: All processing happens on your machine
- **Backup Friendly**: Preserves original file timestamps and metadata
- **Reversible**: Maintains clear organization structure for easy manual adjustments

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
chmod +x setup.sh organize
./setup.sh --dev
```

## 📝 **License**

MIT License - See [LICENSE](LICENSE) for details.

## 🙋‍♂️ **Support**

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Join community discussions for tips and customizations
- **Documentation**: Check the `docs/` folder for detailed guides

---

**Built for professionals who want their digital life organized without the cognitive overhead.** 

*Transform chaos into clarity, automatically.*