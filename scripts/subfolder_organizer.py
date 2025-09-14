#!/usr/bin/env python3
"""
Subfolder Organizer
Organizes loose files within existing categories into logical subfolders.

This script takes already categorized files and further organizes them into
meaningful subfolders, making it easier to find specific content within
each category. Perfect for maintaining organization over time.
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime
import logging

class SubFolderOrganizer:
    def __init__(self):
        """Initialize the Subfolder Organizer."""
        self.base_path = Path.home() / "Documents" / "organized_files"
        
        # Subfolder organization schemes for each category
        self.medical_subfolders = {
            'clinical_guidelines': ['guideline', 'protocol', 'clinical', 'treatment'],
            'study_materials': ['usmle', 'step', 'exam', 'study', 'review', 'notes'],
            'research_papers': ['research', 'paper', 'journal', 'study', 'trial'],
            'reference_materials': ['reference', 'manual', 'handbook', 'quick'],
            'patient_education': ['patient', 'education', 'handout', 'information'],
            'medical_images': ['.jpg', '.png', '.heic', '.gif', '.jpeg'],
            'forms_documents': ['form', 'consent', 'agreement', 'policy']
        }
        
        self.education_subfolders = {
            'lecture_materials': ['lecture', 'slides', 'presentation', 'class'],
            'study_resources': ['study', 'notes', 'review', 'guide', 'summary'],
            'assignments': ['assignment', 'homework', 'project', 'submission'],
            'textbooks': ['textbook', 'book', 'manual', 'handbook'],
            'exam_prep': ['exam', 'test', 'quiz', 'prep', 'practice'],
            'flashcards': ['flashcard', 'anki', '.apkg', '.ankiaddon'],
            'course_materials': ['course', 'curriculum', 'syllabus']
        }
        
        self.research_subfolders = {
            'academic_papers': ['.pdf', 'paper', 'journal', 'publication'],
            'data_analysis': ['.csv', '.xlsx', 'data', 'analysis', 'statistics'],
            'methodology': ['method', 'protocol', 'procedure', 'approach'],
            'presentations': ['.pptx', '.ppt', 'presentation', 'poster'],
            'manuscripts': ['manuscript', 'draft', 'writing', 'article'],
            'protocols': ['protocol', 'irb', 'consent', 'ethics']
        }
        
        self.personal_subfolders = {
            'photos': ['.jpg', '.jpeg', '.png', '.heic', '.gif', '.webp'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.pages'],
            'music_audio': ['.mp3', '.mp4', '.wav', '.aac', '.m4a'],
            'videos': ['.mov', '.avi', '.mkv', '.mp4', '.webm'],
            'data_tracking': ['.csv', '.xlsx', 'track', 'log', 'data'],
            'financial': ['financial', 'receipt', 'invoice', 'tax', 'budget'],
            'health_records': ['health', 'medical', 'appointment', 'prescription']
        }
        
        self.projects_subfolders = {
            'web_development': ['.html', '.css', '.js', '.tsx', '.jsx', '.vue'],
            'python_projects': ['.py', '.ipynb', '.pyw'],
            'documentation': ['.md', '.txt', 'readme', 'docs', 'documentation'],
            'configuration': ['.json', '.yaml', '.yml', '.toml', '.conf', 'config'],
            'databases': ['.sql', '.db', '.sqlite', 'database'],
            'mobile_development': ['.swift', '.kt', '.java', '.dart'],
            'archives': ['.zip', '.tar', '.gz', '.rar', '.7z']
        }
        
        self.writing_subfolders = {
            'books_novels': ['book', 'novel', 'chapter', 'fiction'],
            'articles_blogs': ['article', 'blog', 'essay', 'post'],
            'creative_writing': ['story', 'creative', 'poetry', 'poem'],
            'professional': ['report', 'proposal', 'business', 'professional'],
            'drafts': ['draft', 'rough', 'outline', 'notes'],
            'published': ['published', 'final', 'complete']
        }
        
        # Setup logging
        log_dir = self.base_path / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_dir / 'subfolder_organizer.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def categorize_file(self, file_path, subfolder_scheme):
        """
        Determine which subfolder a file should go to based on analysis.
        
        Args:
            file_path (Path): File to categorize
            subfolder_scheme (dict): Available subfolders and their keywords
            
        Returns:
            str: Best matching subfolder name
        """
        filename = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Score each subfolder based on matches
        subfolder_scores = {}
        
        for subfolder, keywords in subfolder_scheme.items():
            score = 0
            
            for keyword in keywords:
                if keyword.startswith('.'):  # File extension
                    if file_ext == keyword:
                        score += 3  # High weight for exact extension match
                else:  # Keyword in filename
                    if keyword in filename:
                        score += 1
            
            if score > 0:
                subfolder_scores[subfolder] = score
        
        # Return the highest scoring subfolder, or a catch-all
        if subfolder_scores:
            return max(subfolder_scores, key=subfolder_scores.get)
        else:
            # Return a catch-all folder based on file type
            if file_ext in ['.pdf', '.doc', '.docx', '.txt']:
                return 'documents' if 'documents' in subfolder_scheme else list(subfolder_scheme.keys())[-1]
            elif file_ext in ['.jpg', '.png', '.gif']:
                return 'images' if 'images' in subfolder_scheme else list(subfolder_scheme.keys())[-1]
            else:
                return list(subfolder_scheme.keys())[-1]  # Last folder as catch-all

    def organize_category(self, category_name, dry_run=False):
        """
        Organize loose files within a specific category.
        
        Args:
            category_name (str): Name of category to organize
            dry_run (bool): Preview changes without moving files
            
        Returns:
            bool: True if organization was successful
        """
        category_path = self.base_path / category_name
        
        if not category_path.exists():
            print(f"❌ Category '{category_name}' doesn't exist at {category_path}")
            return False
        
        # Get the appropriate subfolder scheme
        subfolder_schemes = {
            'medical': self.medical_subfolders,
            'education': self.education_subfolders,
            'research': self.research_subfolders,
            'personal': self.personal_subfolders,
            'projects': self.projects_subfolders,
            'writing': self.writing_subfolders
        }
        
        if category_name not in subfolder_schemes:
            print(f"⚠️  No organization scheme defined for '{category_name}'")
            print(f"Available categories: {', '.join(subfolder_schemes.keys())}")
            return False
            
        scheme = subfolder_schemes[category_name]
        
        # Find loose files (not in subdirectories, excluding screenshots folder)
        loose_files = []
        for item in category_path.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                loose_files.append(item)
        
        if not loose_files:
            print(f"✅ {category_name} - No loose files found (already organized)")
            return True
            
        print(f"📁 Organizing {len(loose_files)} loose files in '{category_name}'...")
        
        # Create subfolders if not in dry run mode
        if not dry_run:
            for subfolder in scheme.keys():
                (category_path / subfolder).mkdir(exist_ok=True)
        
        # Categorize and move files
        moves_by_subfolder = {}
        
        for file_path in loose_files:
            target_subfolder = self.categorize_file(file_path, scheme)
            
            if target_subfolder not in moves_by_subfolder:
                moves_by_subfolder[target_subfolder] = []
            moves_by_subfolder[target_subfolder].append(file_path)
        
        # Execute or preview moves
        total_moved = 0
        for subfolder, files in moves_by_subfolder.items():
            if dry_run:
                print(f"  📂 {subfolder}: {len(files)} files")
                # Show examples
                for file_path in files[:3]:
                    print(f"    • {file_path.name}")
                if len(files) > 3:
                    print(f"    • ... and {len(files) - 3} more")
            else:
                subfolder_path = category_path / subfolder
                moved_in_subfolder = 0
                
                for file_path in files:
                    dest_path = subfolder_path / file_path.name
                    
                    # Handle duplicates
                    if dest_path.exists():
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        stem, suffix = file_path.stem, file_path.suffix
                        dest_path = subfolder_path / f"{stem}_{timestamp}{suffix}"
                    
                    try:
                        shutil.move(str(file_path), str(dest_path))
                        moved_in_subfolder += 1
                        total_moved += 1
                        logging.info(f"Moved {file_path.name} to {subfolder}/")
                    except Exception as e:
                        logging.error(f"Failed to move {file_path.name}: {e}")
                        print(f"    ❌ Failed to move {file_path.name}: {e}")
                
                if moved_in_subfolder > 0:
                    print(f"  ✅ {subfolder}: {moved_in_subfolder} files")
        
        if not dry_run and total_moved > 0:
            print(f"  📊 Total files organized in {category_name}: {total_moved}")
            logging.info(f"Organized {total_moved} files in {category_name}")
            
        return True

    def organize_all_categories(self, dry_run=False):
        """
        Organize all categories that have defined schemes.
        
        Args:
            dry_run (bool): Preview changes without moving files
        """
        categories = ['medical', 'education', 'research', 'personal', 'projects', 'writing']
        
        if dry_run:
            print("🧪 SUBFOLDER ORGANIZATION DRY RUN:")
            print("Preview of how loose files would be organized into subfolders")
        else:
            print("🗂️  ORGANIZING LOOSE FILES INTO SUBFOLDERS:")
            print("Creating logical subfolders within each category")
        
        print("=" * 60)
        
        organized_count = 0
        
        for category in categories:
            if self.organize_category(category, dry_run):
                organized_count += 1
            print()
        
        if organized_count > 0:
            action = "would be organized" if dry_run else "organized"
            print(f"✅ {organized_count} categories {action} successfully")
        else:
            print("ℹ️  No categories needed subfolder organization")

    def show_category_stats(self):
        """Show statistics for each category and their organization status."""
        print("📊 Category Organization Statistics")
        print("=" * 50)
        
        categories = ['medical', 'education', 'research', 'personal', 'projects', 'writing', 'software', 'documents']
        
        for category in categories:
            category_path = self.base_path / category
            if category_path.exists():
                # Count loose files (files directly in category folder)
                loose_files = len([f for f in category_path.iterdir() 
                                if f.is_file() and not f.name.startswith('.')])
                
                # Count subdirectories
                subdirs = [d for d in category_path.iterdir() 
                          if d.is_dir() and not d.name.startswith('.')]
                subdir_count = len(subdirs)
                
                # Count total files
                total_files = len(list(category_path.rglob('*')))
                
                # Organization status
                status = "✅ Organized" if loose_files == 0 else f"📋 {loose_files} loose files"
                
                print(f"📁 {category}:")
                print(f"   {status}")
                print(f"   📊 {subdir_count} subfolders, {total_files} total items")
                
                # Show subfolder breakdown if organized
                if subdir_count > 0 and loose_files == 0:
                    for subdir in subdirs[:3]:  # Show first 3
                        file_count = len([f for f in subdir.iterdir() if f.is_file()])
                        print(f"      📂 {subdir.name}: {file_count} files")
                    if len(subdirs) > 3:
                        print(f"      📂 ... and {len(subdirs) - 3} more subfolders")
                        
                print()
            else:
                print(f"📁 {category}: ❌ Doesn't exist")
                print()

def main():
    """Main entry point for the Subfolder Organizer."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("🗂️  Subfolder Organizer")
        print("Organize loose files within categories into logical subfolders")
        print()
        print("Usage:")
        print("  python3 subfolder_organizer.py [command] [options]")
        print()
        print("Commands:")
        print("  stats                    Show organization statistics")
        print("  organize <category>      Organize a specific category")
        print("  all                      Organize all categories")
        print()
        print("Options:")
        print("  --dry-run               Preview changes without moving files")
        print()
        print("Categories:")
        print("  📚 education    Lecture materials, study resources, assignments")
        print("  🏥 medical      Clinical guidelines, study materials, research")
        print("  🔬 research     Academic papers, data analysis, methodology")
        print("  💼 personal     Photos, documents, music, data tracking")
        print("  ⚙️ projects     Web development, Python, documentation")
        print("  ✍️ writing      Books, articles, creative writing, drafts")
        print()
        print("Examples:")
        print("  python3 subfolder_organizer.py stats")
        print("  python3 subfolder_organizer.py organize medical --dry-run")
        print("  python3 subfolder_organizer.py all")
        return
    
    organizer = SubFolderOrganizer()
    
    if len(sys.argv) < 2:
        # Default: show statistics
        organizer.show_category_stats()
        return
    
    command = sys.argv[1].lower()
    dry_run = '--dry-run' in sys.argv
    
    if command == "stats":
        organizer.show_category_stats()
        
    elif command == "organize":
        if len(sys.argv) < 3:
            print("❌ Please specify a category to organize")
            print("Usage: python3 subfolder_organizer.py organize <category> [--dry-run]")
            print("Available categories: medical, education, research, personal, projects, writing")
            return
            
        category = sys.argv[2].lower()
        print(f"🗂️  Subfolder Organizer - {category.title()} Category")
        print()
        
        if organizer.organize_category(category, dry_run):
            if not dry_run:
                print(f"✅ {category.title()} category organization complete!")
        else:
            print(f"❌ Failed to organize {category} category")
            
    elif command == "all":
        organizer.organize_all_categories(dry_run)
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: stats, organize, all")
        print("Use 'python3 subfolder_organizer.py --help' for more information")

if __name__ == "__main__":
    main()
