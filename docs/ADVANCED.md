# Advanced Features Guide

Discover the powerful features that make Smart File Organizer more than just a basic file sorter.

## 📷 Smart Screenshot Organization

### Temporal Clustering
The system automatically groups related screenshots taken within 5 minutes of each other:

```bash
# Organize screenshots with intelligent grouping
./organize screenshots

# Preview the groupings first
./organize screenshots --dry-run
```

**What it does:**
- Detects screenshot sequences (like documenting a process)
- Groups them in dedicated sequence folders
- Preserves workflow context
- Analyzes content for better categorization

### Content-Aware Categorization
Screenshots are analyzed for:
- **Medical content**: Clinical guidelines, study materials, research papers
- **Educational content**: Lecture slides, study guides, quiz results
- **Development content**: Code snippets, error messages, documentation
- **Personal content**: Social media, conversations, references

### Time-Based Intelligence
The system considers when screenshots were taken:
- **Morning/Afternoon**: Often professional or academic content
- **Evening**: Study sessions or personal projects  
- **Late Night**: Deep work, coding, or research

## 🎯 Screenshot-to-Action Workflow

Transform visual notes into actionable tasks:

```bash
# Convert screenshots into action items
./organize actions

# Interactive mode for careful review
./organize actions interactive

# Auto-create high-confidence actions
./organize actions auto
```

### Action Categories
- **Follow-up**: Items requiring future investigation
- **Reference**: Information to reference later
- **Decision**: Options requiring evaluation
- **Learn**: Topics to study in depth
- **Track**: Progress or metrics to monitor

### Smart Priority Assignment
- **High**: Old screenshots (14+ days) or decision items
- **Medium**: Follow-up items and learning tasks
- **Low**: Reference materials and tracking items

## 🗂️ Intelligent Subfolder Organization

Automatically organize files within categories into logical subfolders:

```bash
# Organize all categories
./organize subfolders all

# Organize specific category
./organize subfolders medical

# Preview changes
./organize subfolders education --dry-run
```

### Medical Subfolders
- `clinical_guidelines/` - Protocols and treatment guides
- `study_materials/` - USMLE, exam prep, notes
- `research_papers/` - Academic papers and studies
- `reference_materials/` - Quick reference guides
- `medical_images/` - Radiology, pathology images

### Education Subfolders
- `lecture_materials/` - Slides and presentations
- `study_resources/` - Notes, guides, summaries
- `assignments/` - Homework and projects
- `exam_prep/` - Test materials and practice
- `flashcards/` - Anki decks and review cards

## 🧠 Context-Aware File Analysis

### Multi-Factor Categorization
The system analyzes multiple signals:
1. **Filename patterns** - Keywords and structure
2. **File extensions** - Type-based categorization
3. **Folder context** - Where files are found
4. **Content patterns** - Domain-specific terminology
5. **Time context** - When files were created/modified

### Professional Domain Optimization
Specially optimized for:
- **Medical professionals** - Clinical terminology, research patterns
- **Students** - Academic structure, study materials
- **Developers** - Code patterns, technical documentation
- **Researchers** - Academic papers, methodology, data

### Learning System
The organizer gets smarter over time by:
- Analyzing your file patterns
- Adapting to your terminology
- Learning from organization decisions
- Improving categorization accuracy

## 🔄 Automated Workflows

### Batch Processing
Process large numbers of files efficiently:
```bash
# Process entire folders recursively
./organize folder ~/Downloads

# Handle subfolders and nested structures
./organize folder ~/Documents/Unsorted
```

### Duplicate Handling
Sophisticated duplicate management:
- **Timestamp suffixes** for true duplicates
- **Content analysis** to avoid false positives
- **Preserve originals** with clear naming
- **Log all moves** for easy reversal

### Empty Folder Cleanup
Automatic maintenance:
- Remove empty folders after organization
- Clean up temporary files
- Maintain folder structure integrity
- Preserve important empty folders

## 📊 Advanced Statistics and Reporting

### Organization Statistics
```bash
# View detailed category statistics
python3 scripts/subfolder_organizer.py stats
```

Get insights on:
- Files per category
- Organization completion status
- Subfolder distribution
- System usage patterns

### Action Item Management
Track your screenshot-derived tasks:
- **Pending actions** by priority
- **Due date tracking** with smart defaults
- **Progress monitoring** over time
- **Context preservation** for easy review

## 🎨 Customization Options

### Custom Keywords
Add domain-specific terms to improve categorization:

```python
# Edit in downloads_organizer.py
self.medical_keywords.extend([
    'your-specialty-terms',
    'custom-abbreviations',
    'domain-specific-words'
])
```

### Category Modification
Add new categories or modify existing ones:

```python
# Add new destination
self.destinations['research_data'] = self.base_path / "research_data"

# Add categorization keywords
self.research_data_keywords = ['dataset', 'analysis', 'results']
```

### Screenshot Patterns
Customize screenshot recognition patterns:

```python
# Support different screenshot naming conventions
screenshot_patterns = [
    "Screenshot *.png",     # macOS default
    "Screen Shot *.png",    # Alternative macOS
    "screenshot*.png"       # Various systems
]
```

## 🚀 Performance Optimization

### Large File Handling
Optimized for processing thousands of files:
- **Recursive processing** without memory issues
- **Progress indicators** for large batches
- **Error handling** that doesn't stop the process
- **Logging** for tracking and debugging

### Network Drive Compatibility
Works with:
- Cloud storage folders (Dropbox, Google Drive, OneDrive)
- Network attached storage (NAS)
- External drives and USB storage
- Symbolic links and mounted volumes

## 🔒 Safety Features

### Non-Destructive Operations
- **Dry run mode** for all operations
- **Detailed previews** before any changes
- **Comprehensive logging** of all actions
- **Reversible operations** with clear audit trails

### Data Integrity
- **Preserves file metadata** (timestamps, permissions)
- **Handles edge cases** gracefully
- **Validates moves** before completion
- **Rollback capabilities** through logs

## 🌟 Pro Tips

### Workflow Integration
1. **Daily Organization**: Set up automated daily runs
2. **Project-Specific**: Create temporary categories for active projects
3. **Seasonal Cleanup**: Use for periodic major reorganizations
4. **Backup Preparation**: Organize before backing up to cloud storage

### Efficiency Maximization
1. **Start with dry runs** to understand the system
2. **Process in chunks** for large collections
3. **Use subfolders** to maintain organization over time
4. **Regular screenshot processing** to prevent accumulation

### Advanced Usage Patterns
1. **Research Workflows**: Organize papers → Create action items → Track progress
2. **Study Sessions**: Screenshot notes → Convert to action items → Schedule review
3. **Development Projects**: Organize code → Document with screenshots → Track issues

The Smart File Organizer becomes more powerful the more you use it. These advanced features work together to create a comprehensive file management system that adapts to your workflow and grows with your needs.
