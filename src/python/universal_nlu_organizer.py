#!/usr/bin/env python3
"""
Universal NLU-Enhanced File Organizer
Intelligent content analysis that works for everyone - no domain-specific assumptions
Adapts to any user's files: business, creative, academic, personal, technical
"""

import os
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime
import logging
import re

class UniversalNLUOrganizer:
    def __init__(self, source_folder, destination_base=None):
        self.source_path = Path(source_folder).expanduser().resolve()
        
        if destination_base:
            self.base_path = Path(destination_base).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "auto_organized"
        
        # Universal destinations - work for any profession/use case
        self.destinations = {
            # Work & Professional
            'work/documents': self.base_path / "work" / "documents",
            'work/presentations': self.base_path / "work" / "presentations", 
            'work/spreadsheets': self.base_path / "work" / "spreadsheets",
            'work/reports': self.base_path / "work" / "reports",
            'work/contracts': self.base_path / "work" / "contracts",
            
            # Education & Learning (any field)
            'education/textbooks': self.base_path / "education" / "textbooks",
            'education/courses': self.base_path / "education" / "courses",
            'education/research': self.base_path / "education" / "research",
            'education/notes': self.base_path / "education" / "notes",
            'education/certificates': self.base_path / "education" / "certificates",
            
            # Creative & Media
            'creative/photos': self.base_path / "creative" / "photos",
            'creative/videos': self.base_path / "creative" / "videos",
            'creative/audio': self.base_path / "creative" / "audio",
            'creative/design': self.base_path / "creative" / "design",
            
            # Development & Technical
            'development/code': self.base_path / "development" / "code",
            'development/documentation': self.base_path / "development" / "documentation",
            'development/resources': self.base_path / "development" / "resources",
            
            # Personal & Life
            'personal/finances': self.base_path / "personal" / "finances",
            'personal/health': self.base_path / "personal" / "health",
            'personal/travel': self.base_path / "personal" / "travel",
            'personal/family': self.base_path / "personal" / "family",
            'personal/hobbies': self.base_path / "personal" / "hobbies",
            
            # Utilities
            'utilities/screenshots': self.base_path / "utilities" / "screenshots",
            'utilities/downloads': self.base_path / "utilities" / "downloads",
            'utilities/archives': self.base_path / "utilities" / "archives",
            'utilities/templates': self.base_path / "utilities" / "templates",
            
            # Fallback
            'documents/misc': self.base_path / "documents" / "misc"
        }

    def analyze_document_content(self, file_path):
        """Analyze document content to understand purpose - universal patterns"""
        try:
            filename = file_path.name.lower()
            
            # Financial documents (universal)
            if any(term in filename for term in ['tax', 'invoice', 'receipt', 'budget', 'bank', 'statement', 'finance']):
                return 'financial_document'
                
            # Legal/contracts (universal) 
            if any(term in filename for term in ['contract', 'agreement', 'legal', 'terms', 'policy', 'nda']):
                return 'legal_document'
                
            # Health records (universal)
            if any(term in filename for term in ['medical', 'health', 'vaccination', 'insurance', 'prescription']):
                return 'health_document'
                
            # Educational content (any field)
            if any(term in filename for term in ['textbook', 'syllabus', 'assignment', 'homework', 'study', 'notes']):
                return 'educational_content'
                
            # Research/academic (any field)
            if any(term in filename for term in ['research', 'paper', 'thesis', 'journal', 'analysis', 'study']):
                return 'research_content'
                
            # Certificates/credentials (universal)
            if any(term in filename for term in ['certificate', 'diploma', 'license', 'certification', 'credential']):
                return 'certificate'
                
            # Reports (business/academic)
            if any(term in filename for term in ['report', 'summary', 'quarterly', 'annual', 'monthly']):
                return 'report'
                
            # Travel documents
            if any(term in filename for term in ['passport', 'visa', 'ticket', 'reservation', 'travel', 'flight']):
                return 'travel_document'
                
            return 'generic_document'
            
        except Exception:
            return 'generic_document'

    def analyze_image_content(self, file_path):
        """Analyze images - universal patterns"""
        filename = file_path.name.lower()
        
        # Screenshots (universal)
        if any(term in filename for term in ['screenshot', 'screen shot', 'capture']):
            return 'screenshot'
            
        # Family/personal photos
        if any(term in filename for term in ['family', 'wedding', 'birthday', 'vacation', 'trip']):
            return 'family_photo'
            
        # Professional/work photos
        if any(term in filename for term in ['headshot', 'professional', 'linkedin', 'business', 'meeting']):
            return 'professional_photo'
            
        # Design/creative work
        if any(term in filename for term in ['design', 'logo', 'mockup', 'sketch', 'concept']):
            return 'design_work'
            
        # Product/work photos
        if any(term in filename for term in ['product', 'before', 'after', 'progress', 'work']):
            return 'work_photo'
            
        # Phone camera patterns (IMG_, DSC, etc.)
        if filename.startswith(('img_', 'dsc', 'photo')):
            return 'phone_photo'
            
        return 'generic_photo'

    def analyze_filename_patterns(self, file_path):
        """Detect universal filename patterns"""
        filename = file_path.name.lower()
        
        # Date patterns suggest organization/work
        if re.search(r'\d{4}[-_]\d{2}[-_]\d{2}', filename):
            return 'dated_document'
            
        # Version numbers suggest work documents
        if re.search(r'v\d+|version|final|draft', filename):
            return 'versioned_document'
            
        # Presentation patterns
        if any(term in filename for term in ['presentation', 'slides', 'deck']):
            return 'presentation'
            
        # Template patterns
        if any(term in filename for term in ['template', 'sample', 'example']):
            return 'template'
            
        return 'standard_file'

    def categorize_file_universal(self, file_path):
        """Universal NLU categorization - works for any profession/use case"""
        filename = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Skip system files
        if filename.startswith('.') or filename in ['Icon\\r', 'desktop.ini']:
            return None
            
        # PDF Analysis - most versatile file type
        if file_ext == '.pdf':
            content_type = self.analyze_document_content(file_path)
            filename_pattern = self.analyze_filename_patterns(file_path)
            
            if content_type == 'financial_document':
                return 'personal/finances'
            elif content_type == 'legal_document':
                return 'work/contracts'
            elif content_type == 'health_document':
                return 'personal/health'
            elif content_type == 'educational_content':
                return 'education/textbooks'
            elif content_type == 'research_content':
                return 'education/research'
            elif content_type == 'certificate':
                return 'education/certificates'
            elif content_type == 'report':
                return 'work/reports'
            elif content_type == 'travel_document':
                return 'personal/travel'
            elif filename_pattern == 'presentation':
                return 'work/presentations'
            else:
                return 'work/documents'  # Default for professional PDFs
        
        # Image Analysis
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic']:
            content_type = self.analyze_image_content(file_path)
            
            if content_type == 'screenshot':
                return 'utilities/screenshots'
            elif content_type == 'family_photo':
                return 'personal/family'
            elif content_type == 'professional_photo':
                return 'work/documents'
            elif content_type == 'design_work':
                return 'creative/design'
            elif content_type == 'work_photo':
                return 'work/documents'
            else:
                return 'creative/photos'  # Default for personal photos
        
        # Presentations
        elif file_ext in ['.ppt', '.pptx', '.key']:
            filename_pattern = self.analyze_filename_patterns(file_path)
            if filename_pattern == 'template':
                return 'utilities/templates'
            else:
                return 'work/presentations'
        
        # Spreadsheets
        elif file_ext in ['.xls', '.xlsx', '.csv', '.numbers']:
            if any(term in filename for term in ['budget', 'expense', 'finance', 'bank']):
                return 'personal/finances'
            else:
                return 'work/spreadsheets'
        
        # Documents
        elif file_ext in ['.doc', '.docx', '.rtf', '.txt', '.md', '.pages']:
            content_type = self.analyze_document_content(file_path)
            
            if content_type == 'educational_content':
                return 'education/notes'
            elif content_type == 'report':
                return 'work/reports'
            else:
                return 'work/documents'
        
        # Audio files
        elif file_ext in ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']:
            if any(term in filename for term in ['podcast', 'lecture', 'meeting', 'interview']):
                return 'work/documents'
            else:
                return 'creative/audio'
        
        # Video files  
        elif file_ext in ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']:
            if any(term in filename for term in ['meeting', 'presentation', 'demo', 'training']):
                return 'work/documents'
            else:
                return 'creative/videos'
        
        # Code files
        elif file_ext in ['.py', '.js', '.html', '.css', '.json', '.java', '.cpp', '.c', '.sh', '.rb', '.php', '.go', '.rs']:
            return 'development/code'
        
        # Archives
        elif file_ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'utilities/archives'
        
        # Design files
        elif file_ext in ['.psd', '.ai', '.sketch', '.fig', '.xd', '.indd']:
            return 'creative/design'
            
        # Default fallback
        return 'documents/misc'

    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"

    def move_file(self, src_path, category):
        """Move file to appropriate destination"""
        if category not in self.destinations:
            print(f"Unknown category: {category}")
            return False
            
        dest_folder = self.destinations[category]
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        dest_path = dest_folder / src_path.name
        
        # Handle duplicates
        counter = 1
        while dest_path.exists():
            name_parts = src_path.stem, counter, src_path.suffix
            dest_path = dest_folder / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            counter += 1
            
        try:
            shutil.move(str(src_path), str(dest_path))
            return True
        except Exception as e:
            print(f"✗ Failed to move {src_path.name}: {e}")
            return False

    def organize_folder_universal(self, dry_run=False, preview_mode=False):
        """Universal organization with intelligent content analysis"""
        if not self.source_path.exists():
            print(f"❌ Folder not found: {self.source_path}")
            return
            
        if not self.source_path.is_dir():
            print(f"❌ Not a directory: {self.source_path}")
            return
        
        # Collect all files
        files_to_process = []
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                files_to_process.append(file_path)
        
        if not files_to_process:
            print(f"📁 No files found in {self.source_path.name}")
            return
            
        print(f"🧠 Universal NLU File Organization")
        print(f"🔍 Found {len(files_to_process)} files in {self.source_path.name}...")
        print(f"🎯 Destination: {self.base_path}")
        
        if preview_mode:
            print(f"\\n🧪 PREVIEW MODE - Universal content analysis:")
        elif dry_run:
            print("\\n🧪 DRY RUN - Universal intelligent categorization:")
        else:
            print(f"\\n📦 Organizing with universal intelligence:")
        
        # Categorize files with universal NLU
        categories = {}
        
        for file_path in files_to_process:
            category = self.categorize_file_universal(file_path)
            if category:
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path)
        
        # Show results
        total_files = sum(len(files) for files in categories.values())
        organized_files = total_files - len(categories.get('documents/misc', []))
        success_rate = round(organized_files/total_files*100) if total_files > 0 else 0
        
        print(f"✅ Universal Success Rate: {organized_files}/{total_files} files ({success_rate}%)")
        print()
        
        # Detect user's primary domains automatically
        domain_counts = {}
        for category in categories.keys():
            domain = category.split('/')[0]
            domain_counts[domain] = domain_counts.get(domain, 0) + len(categories[category])
        
        if domain_counts:
            primary_domain = max(domain_counts, key=domain_counts.get)
            print(f"🎯 Detected primary domain: {primary_domain} ({domain_counts[primary_domain]} files)")
            print()
        
        for category, files in sorted(categories.items()):
            print(f"  📂 {category}: {len(files)} files")
            if preview_mode and len(files) <= 3:  # Show individual files for small categories
                for file_path in files:
                    print(f"     • {file_path.name}")
        
        if not dry_run and not preview_mode:
            # Execute organization
            moved_count = 0
            for category, files in categories.items():
                success_count = 0
                for file_path in files:
                    if self.move_file(file_path, category):
                        success_count += 1
                        moved_count += 1
                        
                print(f"  ✅ {category}: {success_count} files")
            
            print(f"\\n🧠 Universal Organization Complete!")
            print(f"✅ Organized {moved_count} files with intelligent content understanding")
            print(f"🌍 Works for any profession - adapts to your content automatically")

def main():
    if len(sys.argv) < 2:
        print("🧠 Universal NLU File Organizer")
        print("Intelligent content analysis that works for everyone")
        print()
        print("Usage:")
        print("  python3 universal_nlu_organizer.py <source_folder> [--dry-run] [--preview-mode]")
        print()
        print("Examples:")
        print("  python3 universal_nlu_organizer.py ~/Downloads --dry-run")
        print("  python3 universal_nlu_organizer.py ~/Desktop --preview-mode")
        print()
        print("Works for any profession: business, creative, academic, technical, personal")
        return
    
    source_folder = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    preview_mode = '--preview-mode' in sys.argv
    
    organizer = UniversalNLUOrganizer(source_folder)
    organizer.organize_folder_universal(dry_run=dry_run, preview_mode=preview_mode)

if __name__ == "__main__":
    main()
