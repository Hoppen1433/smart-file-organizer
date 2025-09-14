#!/usr/bin/env python3
"""
Universal Folder Organizer
Organize any folder you specify using intelligent categorization.

This script can organize any folder on your system, automatically sorting files
into logical categories while preserving folder structure and context.
Perfect for cleaning up Desktop, Documents, or any cluttered directory.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
import logging

class UniversalOrganizer:
    def __init__(self, source_folder, destination_base=None):
        """
        Initialize the Universal Organizer.
        
        Args:
            source_folder (str): Path to folder to organize
            destination_base (str, optional): Base path for organized files
        """
        self.source_path = Path(source_folder).expanduser().resolve()
        
        # Set destination - default to organized_files in Documents
        if destination_base:
            self.base_path = Path(destination_base).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "organized_files"
        
        # Destination categories with clear purposes
        self.destinations = {
            'medical': self.base_path / "medical",           # Medical and healthcare content
            'education': self.base_path / "education",       # Study materials and courses
            'research': self.base_path / "research",         # Academic papers and data
            'personal': self.base_path / "personal",         # Personal files and media
            'projects': self.base_path / "projects",         # Code and development work
            'writing': self.base_path / "writing",           # Creative and professional writing
            'software': self.base_path / "software",         # Applications and tools
            'documents': self.base_path / "documents"        # General documents
        }
        
        # Comprehensive keyword categorization system
        self.medical_keywords = [
            'medical', 'health', 'healthcare', 'clinical', 'patient', 'diagnosis',
            'treatment', 'therapy', 'surgery', 'hospital', 'doctor', 'physician',
            'usmle', 'step', 'residency', 'clerkship', 'rotation', 'medical school',
            'cardiology', 'neurology', 'oncology', 'psychiatry', 'pediatrics',
            'radiology', 'pathology', 'pharmacology', 'anatomy', 'physiology',
            'cv', 'resume', 'personal statement', 'match', 'interview'
        ]
        
        self.education_keywords = [
            'study', 'course', 'class', 'lecture', 'assignment', 'homework',
            'exam', 'test', 'quiz', 'notes', 'textbook', 'syllabus',
            'flashcards', 'review', 'prep', 'tutorial', 'guide', 'lesson',
            'university', 'college', 'school', 'academic', 'semester'
        ]
        
        self.research_keywords = [
            'research', 'paper', 'journal', 'study', 'publication', 'manuscript',
            'data', 'analysis', 'statistics', 'methodology', 'results',
            'experiment', 'hypothesis', 'survey', 'protocol', 'findings'
        ]
        
        self.projects_keywords = [
            'code', 'programming', 'development', 'software', 'app', 'website',
            'github', 'repository', 'project', 'algorithm', 'function',
            'database', 'api', 'framework', 'library', 'script'
        ]
        
        self.writing_keywords = [
            'writing', 'article', 'blog', 'book', 'novel', 'story', 'essay',
            'manuscript', 'draft', 'chapter', 'poetry', 'creative',
            'publish', 'author', 'editor', 'content', 'copy'
        ]
        
        # Setup logging
        log_dir = self.base_path / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_dir / 'organizer.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def get_file_category(self, file_path):
        """
        Determine the appropriate category for a file.
        
        Analyzes filename, path, and extension to intelligently categorize files.
        
        Args:
            file_path (Path): Path to the file to categorize
            
        Returns:
            str or None: Category name, or None to skip file
        """
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        file_ext = file_path.suffix.lower()
        
        # Skip system and hidden files
        if filename.startswith('.') or filename in ['Icon\r', 'Thumbs.db', '.DS_Store']:
            return None
            
        # Combine filename and path for context-aware analysis
        analysis_text = f"{filename} {file_path_str}"
        
        # Priority-based categorization
        
        # 1. Medical and healthcare (highest priority for professionals)
        if any(keyword in analysis_text for keyword in self.medical_keywords):
            return 'medical'
            
        # 2. Education and learning materials
        if any(keyword in analysis_text for keyword in self.education_keywords):
            return 'education'
            
        # 3. Research and academic work
        if any(keyword in analysis_text for keyword in self.research_keywords):
            return 'research'
            
        # 4. Projects and development
        if any(keyword in analysis_text for keyword in self.projects_keywords):
            return 'projects'
            
        # 5. Writing and creative content
        if any(keyword in analysis_text for keyword in self.writing_keywords):
            return 'writing'
            
        # File extension-based categorization
        
        # Development files
        if file_ext in ['.py', '.js', '.html', '.css', '.json', '.tsx', '.jsx', 
                        '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs']:
            return 'projects'
            
        # Documents and text files
        if file_ext in ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.pages']:
            # Context-sensitive PDF categorization
            if file_ext == '.pdf':
                if any(word in analysis_text for word in ['medical', 'clinical', 'health']):
                    return 'medical'
                elif any(word in analysis_text for word in ['research', 'paper', 'journal']):
                    return 'research'
                else:
                    return 'documents'  # General documents
            return 'documents'
            
        # Media files
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.webp',
                        '.mp4', '.mov', '.avi', '.mkv', '.mp3', '.wav', '.aac']:
            return 'personal'
            
        # Data and spreadsheets
        if file_ext in ['.csv', '.xlsx', '.xls', '.numbers']:
            if any(word in analysis_text for word in ['research', 'data', 'analysis']):
                return 'research'
            else:
                return 'personal'
                
        # Software and applications
        if file_ext in ['.app', '.pkg', '.dmg', '.exe', '.msi', '.deb', '.rpm']:
            return 'software'
            
        # Archives
        if file_ext in ['.zip', '.tar', '.gz', '.rar', '.7z']:
            # Check if it's a software installer
            if any(word in filename for word in ['install', 'setup', 'software']):
                return 'software'
            else:
                return 'documents'
        
        # Default fallback
        return 'personal'

    def preserve_folder_structure(self, src_path, dest_category):
        """
        Calculate destination path while preserving important folder context.
        
        Args:
            src_path (Path): Source file path
            dest_category (str): Destination category
            
        Returns:
            Path: Final destination path
        """
        dest_base = self.destinations[dest_category]
        
        try:
            # Get the relative path from source root
            relative_path = src_path.relative_to(self.source_path)
            
            # If file is in a subfolder, preserve the immediate parent folder
            if len(relative_path.parts) > 1:
                parent_folder = relative_path.parent
                dest_path = dest_base / parent_folder / src_path.name
            else:
                dest_path = dest_base / src_path.name
                
        except ValueError:
            # If not under source path, just use filename
            dest_path = dest_base / src_path.name
            
        return dest_path

    def move_file(self, src_path, category):
        """
        Safely move a file to its categorized destination.
        
        Args:
            src_path (Path): Source file path
            category (str): Destination category
            
        Returns:
            bool: True if move was successful
        """
        if category not in self.destinations:
            logging.warning(f"Unknown category: {category}")
            return False
            
        # Calculate destination with structure preservation
        dest_path = self.preserve_folder_structure(src_path, category)
        
        # Create destination directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle duplicate files
        if dest_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem, suffix = src_path.stem, src_path.suffix
            dest_path = dest_path.parent / f"{stem}_{timestamp}{suffix}"
            
        try:
            shutil.move(str(src_path), str(dest_path))
            logging.info(f"Moved {src_path} to {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to move {src_path}: {e}")
            print(f"✗ Failed to move {src_path.name}: {e}")
            return False

    def organize_folder(self, dry_run=False):
        """
        Organize the specified folder.
        
        Args:
            dry_run (bool): If True, preview changes without moving files
        """
        if not self.source_path.exists():
            print(f"❌ Folder not found: {self.source_path}")
            return
            
        if not self.source_path.is_dir():
            print(f"❌ Not a directory: {self.source_path}")
            return
        
        print(f"🔍 Analyzing folder: {self.source_path}")
        print(f"📁 Destination: {self.base_path}")
        print()
        
        # Collect all files recursively
        files_to_process = []
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                files_to_process.append(file_path)
        
        if not files_to_process:
            print(f"📂 No files found to organize in {self.source_path.name}")
            return
            
        print(f"📊 Found {len(files_to_process)} files to process")
        
        # Categorize files
        categories = {}
        for file_path in files_to_process:
            category = self.get_file_category(file_path)
            if category:
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path)
        
        if not categories:
            print("📁 No files need organization")
            return
        
        # Show organization plan
        if dry_run:
            print("\n🧪 DRY RUN - Preview of changes:\n")
            for category, files in categories.items():
                print(f"📂 {category.upper()}: {len(files)} files")
                # Show first few examples
                for file_path in files[:3]:
                    try:
                        rel_path = file_path.relative_to(self.source_path)
                        print(f"    • {rel_path}")
                    except ValueError:
                        print(f"    • {file_path.name}")
                if len(files) > 3:
                    print(f"    • ... and {len(files) - 3} more")
                print()
                
            print(f"📊 Total: {sum(len(files) for files in categories.values())} files would be organized")
            
        else:
            print(f"\n📦 Organizing {self.source_path.name} files:\n")
            
            moved_count = 0
            for category, files in categories.items():
                category_moved = 0
                for file_path in files:
                    if self.move_file(file_path, category):
                        moved_count += 1
                        category_moved += 1
                        
                        # Progress indicator for large batches
                        if moved_count % 20 == 0:
                            print(f"  ⏳ Processed {moved_count} files...")
                            
                print(f"  ✅ {category}: {category_moved} files organized")
            
            print(f"\n✅ Successfully organized {moved_count} files!")
            print(f"📁 Files are now organized in: {self.base_path}")
            
        logging.info(f"Organization complete: {len(files_to_process)} files processed")

def main():
    """Main entry point for the Universal Organizer."""
    if len(sys.argv) < 2:
        print("🗂️  Universal Folder Organizer")
        print("Intelligently organize any folder into logical categories")
        print()
        print("Usage:")
        print("  python3 universal_organizer.py <source_folder> [destination] [options]")
        print()
        print("Examples:")
        print("  python3 universal_organizer.py ~/Desktop")
        print("  python3 universal_organizer.py ~/Desktop --dry-run")
        print("  python3 universal_organizer.py ~/Downloads ~/Documents/my_organized")
        print("  python3 universal_organizer.py '/path with spaces' --dry-run")
        print()
        print("Options:")
        print("  --dry-run    Preview changes without moving files")
        print("  -h, --help   Show this help message")
        print()
        print("Categories:")
        print("  📚 education    Study materials, courses, assignments")
        print("  🏥 medical      Healthcare, clinical resources, medical papers")
        print("  🔬 research     Academic papers, data analysis, protocols")
        print("  💼 personal     Photos, music, personal documents")
        print("  ⚙️ projects     Code, development files, technical docs")
        print("  ✍️ writing      Articles, books, creative content")
        print("  💾 software     Applications, installers, tools")
        print("  📄 documents    General documents and files")
        print()
        return
    
    # Parse arguments
    source_folder = sys.argv[1]
    destination_base = None
    dry_run = False
    
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == '--dry-run':
            dry_run = True
        elif arg in ['-h', '--help']:
            main()  # Show help
            return
        elif not arg.startswith('--') and destination_base is None:
            destination_base = arg
    
    try:
        organizer = UniversalOrganizer(source_folder, destination_base)
        organizer.organize_folder(dry_run)
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Organization failed: {e}")

if __name__ == "__main__":
    main()
