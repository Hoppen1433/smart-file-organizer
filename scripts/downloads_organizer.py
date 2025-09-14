#!/usr/bin/env python3
"""
Downloads Auto-Organizer
Automatically categorizes and organizes files from Downloads folder into logical categories.

This script intelligently analyzes filenames, extensions, and content patterns to:
- Sort files into categories (medical, education, personal, projects, etc.)
- Handle duplicates safely with timestamps
- Clean up empty folders and temporary files
- Preserve folder structure while organizing loose files
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime, timedelta
import logging

class DownloadsOrganizer:
    def __init__(self):
        """Initialize the Downloads organizer with default paths and categories."""
        self.downloads_path = Path.home() / "Downloads"
        self.base_path = Path.home() / "Documents" / "organized_files"
        
        # Main destination categories
        self.destinations = {
            'medical': self.base_path / "medical",
            'education': self.base_path / "education", 
            'research': self.base_path / "research",
            'personal': self.base_path / "personal",
            'projects': self.base_path / "projects",
            'writing': self.base_path / "writing",
            'software': self.base_path / "software",
            'screenshots': self.base_path / "temp_screenshots"
        }
        
        # Keywords for intelligent categorization
        # Medical terms - optimized for healthcare professionals and students
        self.medical_keywords = [
            'medical', 'surgery', 'clinical', 'patient', 'diagnosis', 'treatment',
            'usmle', 'step', 'residency', 'clerkship', 'rotation',
            'cardiology', 'neurology', 'psychiatry', 'pediatrics', 'radiology',
            'pathology', 'pharmacology', 'anatomy', 'physiology',
            'cv', 'personal statement', 'match', 'interview',
            'protocol', 'guidelines', 'evidence', 'study', 'trial'
        ]
        
        # Education and learning materials
        self.education_keywords = [
            'study', 'notes', 'lecture', 'course', 'class', 'assignment',
            'exam', 'test', 'quiz', 'homework', 'syllabus', 'textbook',
            'flashcards', 'review', 'prep', 'tutorial', 'guide',
            'biochemistry', 'biology', 'chemistry', 'physics', 'mathematics'
        ]
        
        # Research and academic work
        self.research_keywords = [
            'research', 'paper', 'journal', 'publication', 'manuscript',
            'data', 'analysis', 'methodology', 'results', 'discussion',
            'statistics', 'survey', 'experiment', 'hypothesis', 'conclusion'
        ]
        
        # Software and development
        self.software_keywords = [
            'app', 'software', 'program', 'installer', 'setup',
            'code', 'programming', 'development', 'github', 'repository'
        ]

        # Setup logging
        log_path = self.base_path / "logs"
        log_path.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_path / 'organizer.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def get_file_category(self, file_path):
        """
        Analyze a file and determine its appropriate category.
        
        Uses filename analysis, extension patterns, and content keywords to
        intelligently categorize files into the most appropriate destination.
        
        Args:
            file_path (Path): Path to the file to categorize
            
        Returns:
            str or None: Category name, or None if file should be skipped
        """
        filename = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Skip system files and hidden files
        if filename.startswith('.') or filename in ['Icon\r', 'Thumbs.db']:
            return None
            
        # Screenshot handling - immediate categorization for cleanup
        if filename.startswith('screenshot') or 'screenshot' in filename:
            return 'screenshots'
            
        # Software installers and applications
        if file_ext in ['.app', '.pkg', '.dmg', '.exe', '.msi'] or \
           (file_ext == '.zip' and any(word in filename for word in ['installer', 'setup', 'install'])):
            return 'software'
            
        # Analyze content based on keywords
        text_to_analyze = f"{filename} {str(file_path.parent).lower()}"
        
        # Medical content gets highest priority for healthcare professionals
        if any(keyword in text_to_analyze for keyword in self.medical_keywords):
            return 'medical'
            
        # Educational materials
        if any(keyword in text_to_analyze for keyword in self.education_keywords):
            return 'education'
            
        # Research papers and academic work
        if any(keyword in text_to_analyze for keyword in self.research_keywords):
            return 'research'
            
        # Software and development files
        if any(keyword in text_to_analyze for keyword in self.software_keywords):
            return 'projects'
            
        # File extension based classification
        if file_ext == '.pdf':
            return 'medical'  # Default assumption for PDFs
        elif file_ext in ['.py', '.js', '.html', '.css', '.json', '.md']:
            return 'projects'
        elif file_ext in ['.jpg', '.jpeg', '.png', '.heic', '.gif', '.mp4', '.mp3']:
            return 'personal'
        elif file_ext in ['.csv', '.xlsx'] and 'data' in filename:
            return 'research'
        elif file_ext in ['.txt', '.docx', '.pages'] and any(word in filename for word in ['note', 'draft', 'writing']):
            return 'writing'
        
        # Default fallback
        return 'personal'

    def move_file(self, src_path, category):
        """
        Safely move a file to its destination category folder.
        
        Handles duplicate files by adding timestamps and creates destination
        directories as needed.
        
        Args:
            src_path (Path): Source file path
            category (str): Destination category
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if category not in self.destinations:
            logging.warning(f"Unknown category: {category}")
            return False
            
        dest_folder = self.destinations[category]
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_folder / src_path.name
        
        # Handle duplicate files by adding timestamp
        if dest_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem, suffix = src_path.stem, src_path.suffix
            dest_path = dest_folder / f"{stem}_{timestamp}{suffix}"
            
        try:
            shutil.move(str(src_path), str(dest_path))
            logging.info(f"Moved {src_path.name} to {category}/")
            return True
        except Exception as e:
            logging.error(f"Failed to move {src_path.name}: {e}")
            print(f"✗ Failed to move {src_path.name}: {e}")
            return False

    def cleanup_old_screenshots(self, days_old=7):
        """
        Remove old screenshots to prevent accumulation.
        
        Args:
            days_old (int): Delete screenshots older than this many days
        """
        screenshot_folder = self.destinations['screenshots']
        if not screenshot_folder.exists():
            return
            
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        for file_path in screenshot_folder.iterdir():
            if file_path.is_file():
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        logging.info(f"Deleted old screenshot: {file_path.name}")
                    except Exception as e:
                        logging.error(f"Failed to delete {file_path.name}: {e}")
                        
        if deleted_count > 0:
            print(f"🗑️  Cleaned up {deleted_count} old screenshots")

    def cleanup_empty_folders(self):
        """Remove empty folders after organizing files."""
        def remove_empty_dirs(directory):
            removed_count = 0
            try:
                for item in directory.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        # Recursively check subdirectories first
                        removed_count += remove_empty_dirs(item)
                        
                        # Check if directory is now empty
                        try:
                            if not any(item.iterdir()):
                                item.rmdir()
                                removed_count += 1
                                logging.info(f"Removed empty folder: {item.name}")
                        except Exception:
                            pass  # Folder not empty or permission issue
            except Exception:
                pass  # Directory may not exist or be accessible
            return removed_count
            
        removed_count = remove_empty_dirs(self.downloads_path)
        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} empty folders")

    def organize_downloads(self, dry_run=False):
        """
        Main organization function - processes all files in Downloads folder.
        
        Recursively processes all files, including those in subfolders,
        and organizes them into appropriate categories.
        
        Args:
            dry_run (bool): If True, only show what would be moved without actually moving
        """
        if not self.downloads_path.exists():
            print("❌ Downloads folder not found!")
            return
            
        # Collect all files recursively, excluding hidden files
        files_to_process = []
        
        def collect_files(directory):
            try:
                for item in directory.iterdir():
                    if item.is_file() and not item.name.startswith('.'):
                        files_to_process.append(item)
                    elif item.is_dir() and not item.name.startswith('.'):
                        collect_files(item)  # Recursive call for subfolders
            except PermissionError:
                print(f"⚠️  Permission denied accessing {directory}")
                
        collect_files(self.downloads_path)
        
        if not files_to_process:
            print("📁 Downloads folder is already clean!")
            return
            
        print(f"🔍 Found {len(files_to_process)} files to organize...")
        
        if dry_run:
            print("\n🧪 DRY RUN MODE - No files will be moved:\n")
        else:
            print("\n📦 Organizing files from Downloads:\n")
            
        # Categorize and organize files
        moved_count = 0
        category_counts = {}
        
        for file_path in files_to_process:
            category = self.get_file_category(file_path)
            
            if category is None:
                continue
                
            # Track category statistics
            category_counts[category] = category_counts.get(category, 0) + 1
                
            # Show relative path for files in subfolders
            try:
                relative_path = file_path.relative_to(self.downloads_path)
                display_name = str(relative_path) if '/' in str(relative_path) else file_path.name
            except ValueError:
                display_name = file_path.name
                
            if dry_run:
                print(f"Would move: {display_name} → {category}/")
            else:
                if self.move_file(file_path, category):
                    moved_count += 1
                    print(f"✓ Moved {display_name} → {category}/")
                    
        # Show summary
        if category_counts:
            print(f"\n📊 Organization Summary:")
            for category, count in sorted(category_counts.items()):
                print(f"  📂 {category}: {count} files")
                    
        if not dry_run:
            # Cleanup operations
            self.cleanup_old_screenshots()
            self.cleanup_empty_folders()
            
            if moved_count > 0:
                print(f"\n✅ Successfully organized {moved_count} files!")
                print(f"📁 Files organized into: {self.base_path}")
            else:
                print("\n✅ Downloads folder was already organized!")
            
        logging.info(f"Organization complete: {moved_count} files processed")

def main():
    """Main entry point for the script."""
    import sys
    
    print("🗂️  Downloads Auto-Organizer")
    print("Intelligently organizes your Downloads folder")
    print()
    
    # Check for help flag
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage:")
        print("  python3 downloads_organizer.py [--dry-run]")
        print()
        print("Options:")
        print("  --dry-run, -d    Preview changes without moving files")
        print()
        print("Categories:")
        print("  📚 education    Study materials, courses, textbooks")
        print("  🏥 medical      Clinical resources, medical papers")
        print("  🔬 research     Academic papers, data analysis")
        print("  💼 personal     Photos, music, personal documents")
        print("  ⚙️ projects     Code, development files")
        print("  ✍️ writing      Books, articles, creative content")
        print("  💾 software     Applications, installers")
        print()
        return
    
    # Check for dry run flag
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    
    organizer = DownloadsOrganizer()
    organizer.organize_downloads(dry_run=dry_run)

if __name__ == "__main__":
    main()
