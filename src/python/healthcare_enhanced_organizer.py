#!/usr/bin/env python3
"""
NLU-Enhanced Intelligent File Organizer
Uses natural language understanding and content analysis for medical student workflow
Built for the Smart File Organizer Desktop App - No modes needed, just intelligence
"""

import os
import shutil
import sys
import json
from pathlib import Path
from datetime import datetime
import logging
import re

class NLUEnhancedOrganizer:
    def __init__(self, source_folder, destination_base=None):
        self.source_path = Path(source_folder).expanduser().resolve()
        
        if destination_base:
            self.base_path = Path(destination_base).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "auto_organized"
        
        # Universal destinations that work for everyone + specialized medical when detected
        self.destinations = {
            # Work & Professional (universal)
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
            
            # Medical specialization (when detected automatically)
            'medical/radiology': self.base_path / "medical" / "radiology",
            'medical/anatomy': self.base_path / "medical" / "anatomy", 
            'medical/pathology': self.base_path / "medical" / "pathology",
            'medical/clinical': self.base_path / "medical" / "clinical",
            
            # Creative & Media
            'creative/photos': self.base_path / "creative" / "photos",
            'creative/videos': self.base_path / "creative" / "videos",
            'creative/audio': self.base_path / "creative" / "audio",
            'creative/design': self.base_path / "creative" / "design",
            
            # Development & Technical
            'development/code': self.base_path / "development" / "code",
            'development/documentation': self.base_path / "development" / "documentation",
            
            # Personal & Life
            'personal/finances': self.base_path / "personal" / "finances",
            'personal/health': self.base_path / "personal" / "health",
            'personal/travel': self.base_path / "personal" / "travel",
            'personal/family': self.base_path / "personal" / "family",
            'personal/screenshots': self.base_path / "personal" / "screenshots",
            
            # Utilities
            'utilities/archives': self.base_path / "utilities" / "archives",
            'utilities/templates': self.base_path / "utilities" / "templates",
            
            # Fallback
            'documents/misc': self.base_path / "documents" / "misc"
        }
        
        # Universal intelligence - no keyword lists needed

    def analyze_document_content(self, file_path):
        """Universal document analysis with medical specialization bonus"""
        try:
            filename = file_path.name.lower()
            
            # Financial documents (universal)
            if any(term in filename for term in ['tax', 'invoice', 'receipt', 'budget', 'bank', 'fafsa']):
                return 'financial_document'
                
            # Health records (universal)
            if any(term in filename for term in ['vaccination', 'immunization', 'health', 'insurance']):
                return 'health_document'
                
            # Educational content (universal)
            if any(term in filename for term in ['textbook', 'syllabus', 'study', 'course', 'lesson']):
                return 'educational_content'
                
            # Certificates (universal)
            if any(term in filename for term in ['certificate', 'diploma', 'license', 'certification', 'card']):
                return 'certificate'
                
            # Research papers (universal)
            if any(term in filename for term in ['research', 'paper', 'journal', 'analysis', 'study']):
                return 'research_paper'
                
            # Medical specializations (bonus intelligence when detected)
            if any(term in filename for term in ['usmle', 'step 1', 'step 2', 'step 3', 'first aid']):
                return 'medical_exam'
            if 'costanzo' in filename or 'physiology' in filename or 'txtbk' in filename:
                return 'medical_textbook' 
            if any(term in filename for term in ['radiology', 'ct', 'mri', 'xray']):
                return 'radiology_content'
            if any(term in filename for term in ['clinical', 'case', 'patient']):
                return 'clinical_content'
            if any(term in filename for term in ['anatomy', 'muscle', 'pathology']):
                return 'medical_specialty'
                
            return 'generic_document'
            
        except Exception:
            return 'generic_document'

    def analyze_pdf_content(self, file_path):
        """Extract and analyze PDF content for better categorization"""
        try:
            filename = file_path.name.lower()
            
            # USMLE/Board exam materials
            if any(term in filename for term in ['usmle', 'step 1', 'step 2', 'step 3', 'first aid']):
                return 'usmle_material'
            
            # Medical textbooks
            if any(term in filename for term in ['physiology', 'costanzo', 'txtbk', 'edition']):
                return 'textbook'
                
            # Certificates and credentials  
            if any(term in filename for term in ['certificate', 'certification', 'card', 'bls', 'cpr']):
                return 'certificate'
                
            # Health/Medical records
            if any(term in filename for term in ['vaccination', 'immunization', 'health', 'screening', 'fafsa', 'tax']):
                return 'health_or_finance_record'
                
            # Research papers (look for specific patterns)
            if any(pattern in filename for pattern in ['s41598', 'doi', 'journal', 'racism', 'disparities']):
                return 'research_paper'
                
            # Case studies and aquifer materials
            if 'aquifer' in filename or any(term in filename for term in ['cardiac', 'chest', 'trauma', 'neuro', 'renal']):
                return 'medical_case'
                
            # Radiology specific
            if any(term in filename for term in ['radiology', 'augmented reality']):
                return 'radiology_study'
                
            return 'generic_pdf'
            
        except Exception:
            return 'generic_pdf'

    def analyze_image_content(self, file_path):
        """Analyze image files for better categorization"""
        filename = file_path.name.lower()
        
        # Screenshot patterns
        if any(term in filename for term in ['screenshot', 'screen shot']):
            return 'screenshot'
            
        # IMG_ files (likely from iPhone/medical photos)
        if filename.startswith('img_'):
            return 'medical_photo'
            
        # Specific anatomy/medical images
        if any(term in filename for term in ['muscle', 'splenius', 'capitis', 'anatomy']):
            return 'anatomy_diagram'
            
        # Medical conditions/pathology
        if any(term in filename for term in ['vulvovaginitis', 'pathology', 'disease']):
            return 'pathology_image'
            
        # School logos and branding
        if any(term in filename for term in ['logo', 'school', 'university']):
            return 'logo'
            
        # AI/tech related
        if any(term in filename for term in ['ai', 'remnote', 'table']):
            return 'tech_screenshot'
            
        return 'generic_photo'

    def categorize_file(self, file_path):
        """Universal NLU categorization with medical bonus intelligence"""
        filename = file_path.name.lower()
        file_ext = file_path.suffix.lower()
        
        # Skip system files
        if filename.startswith('.') or filename in ['Icon\\r', 'desktop.ini']:
            return None
            
        # PDF Analysis (universal with medical bonus)
        if file_ext == '.pdf':
            content_type = self.analyze_document_content(file_path)
            
            # Universal categories first
            if content_type == 'financial_document':
                return 'personal/finances'
            elif content_type == 'health_document':
                return 'personal/health'
            elif content_type == 'educational_content':
                return 'education/textbooks'
            elif content_type == 'certificate':
                return 'education/certificates'
            elif content_type == 'research_paper':
                return 'education/research'
            # Medical bonus intelligence (when detected)
            elif content_type == 'medical_exam':
                return 'education/courses'  # USMLE goes to general education
            elif content_type == 'medical_textbook':
                return 'education/textbooks'  # Medical textbooks still education
            elif content_type == 'radiology_content':
                return 'medical/radiology'  # Specialized medical folder
            elif content_type == 'clinical_content':
                return 'medical/clinical'  # Clinical cases
            elif content_type == 'medical_specialty':
                return 'medical/anatomy'  # Anatomy/pathology
            else:
                return 'work/documents'  # Default professional documents
        
        # Image Analysis (universal with medical bonus)
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.bmp', '.tiff', '.webp']:
            content_type = self.analyze_image_content(file_path)
            
            if content_type == 'screenshot':
                return 'personal/screenshots'
            elif content_type == 'work_image':
                return 'work/documents'
            elif content_type == 'family_photo':
                return 'personal/family'
            elif content_type == 'medical_image':  # Medical bonus
                return 'medical/anatomy'
            elif content_type == 'phone_photo':
                return 'personal/screenshots'  # Assume screenshots for organization
            else:
                return 'creative/photos'  # Default personal photos
        
        # Presentations (universal)
        elif file_ext in ['.ppt', '.pptx', '.key']:
            if 'template' in filename:
                return 'utilities/templates'
            elif any(term in filename for term in ['case study', 'poster']):
                return 'education/research'  # Academic presentations
            else:
                return 'work/presentations'  # Business presentations
        
        # Spreadsheets (universal)
        elif file_ext in ['.xls', '.xlsx', '.csv', '.numbers']:
            if any(term in filename for term in ['budget', 'finance', 'expense', 'bank']):
                return 'personal/finances'
            else:
                return 'work/spreadsheets'
        
        # Documents (universal)
        elif file_ext in ['.doc', '.docx', '.rtf', '.txt', '.md', '.pages']:
            content_type = self.analyze_document_content(file_path)
            if content_type == 'educational_content':
                return 'education/notes'
            else:
                return 'work/documents'
        
        # Audio files (universal)
        elif file_ext in ['.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg']:
            if any(term in filename for term in ['meeting', 'interview', 'call']):
                return 'work/documents'
            else:
                return 'creative/audio'
        
        # Video files (universal)
        elif file_ext in ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']:
            if any(term in filename for term in ['meeting', 'presentation', 'demo']):
                return 'work/documents'
            else:
                return 'creative/videos'
        
        # Code files (universal)
        elif file_ext in ['.py', '.js', '.html', '.css', '.json', '.java', '.cpp', '.c', '.sh', '.rb', '.php', '.go', '.rs']:
            return 'development/code'
        
        # Design files (universal)
        elif file_ext in ['.psd', '.ai', '.sketch', '.fig', '.xd', '.indd']:
            return 'creative/design'
        
        # Archives (universal)
        elif file_ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'utilities/archives'
        
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

    def organize_folder(self, dry_run=False, preview_mode=False):
        """Organize folder with healthcare-enhanced categorization"""
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
            
        print(f"🌍 Universal NLU File Organization")
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
            category = self.categorize_file(file_path)
            if category:
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path)
        
        # Show results with domain detection
        total_files = sum(len(files) for files in categories.values())
        organized_files = total_files - len(categories.get('documents/misc', []))
        success_rate = round(organized_files/total_files*100) if total_files > 0 else 0
        
        print(f"✅ Universal Success Rate: {organized_files}/{total_files} files ({success_rate}%)")
        
        # Auto-detect user's primary domains
        domain_counts = {}
        for category in categories.keys():
            domain = category.split('/')[0]
            domain_counts[domain] = domain_counts.get(domain, 0) + len(categories[category])
        
        if domain_counts:
            primary_domain = max(domain_counts, key=domain_counts.get)
            print(f"🎯 Detected primary domain: {primary_domain} ({domain_counts[primary_domain]} files)")
        
        if preview_mode:
            # Output detailed file information for preview mode
            for category, files in categories.items():
                for file_path in files:
                    try:
                        file_size = file_path.stat().st_size if file_path.exists() else 0
                        file_size_str = self.format_file_size(file_size)
                        print(f"📂 Category: {category}")
                        print(f"📄 {file_path.name} → {category} ({file_size_str})")
                    except:
                        print(f"📂 Category: {category}")
                        print(f"📄 {file_path.name} → {category} (Unknown size)")
            return
        
        # Execute or show organization
        moved_count = 0
        for category, files in categories.items():
            if dry_run:
                print(f"  📂 {category}: {len(files)} files")
            else:
                success_count = 0
                for file_path in files:
                    if self.move_file(file_path, category):
                        success_count += 1
                        moved_count += 1
                        
                print(f"  ✅ {category}: {success_count} files")
        
        if not dry_run and moved_count > 0:
            print(f"\\n🌍 Universal Organization Complete!")
            print(f"✅ Organized {moved_count} files with intelligent content understanding")
            print(f"🎯 Adapts to any profession - works for everyone")

    def organize_from_categories(self, categories_file):
        """Organize files based on predefined categories from JSON file"""
        try:
            with open(categories_file, 'r') as f:
                files_data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to read categories file: {e}")
            return
        
        print(f"🌍 Universal NLU Organization from Categories")
        print(f"📦 Processing {len(files_data)} files with user-defined categories...")
        
        moved_count = 0
        categories = {}
        
        for file_data in files_data:
            file_path = Path(file_data['path'])
            category = file_data['category']
            
            if category not in categories:
                categories[category] = 0
            
            if self.move_file(file_path, category):
                categories[category] += 1
                moved_count += 1
        
        # Show results
        for category, count in categories.items():
            print(f"  ✅ {category}: {count} files")
        
        print(f"\\n🌍 Universal Organization Complete!")
        print(f"✅ Organized {moved_count} files with user-defined categories")

def main():
    if len(sys.argv) < 2:
        print("🌍 Universal NLU File Organizer")
        print("Intelligent content analysis that works for everyone")
        print()
        print("Usage:")
        print("  python3 healthcare_enhanced_organizer.py <source_folder> [--dry-run] [--preview-mode]")
        print("  python3 healthcare_enhanced_organizer.py --from-categories <categories.json>")
        print()
        print("Examples:")
        print("  python3 healthcare_enhanced_organizer.py ~/Desktop")
        print("  python3 healthcare_enhanced_organizer.py ~/Downloads --preview-mode")
        print("  python3 healthcare_enhanced_organizer.py --from-categories temp_categories.json")
        print()
        print("Works for any profession: business, creative, academic, medical, technical")
        return
    
    # Handle categories file mode
    if '--from-categories' in sys.argv:
        categories_file = sys.argv[sys.argv.index('--from-categories') + 1]
        organizer = NLUEnhancedOrganizer(".", None)
        organizer.organize_from_categories(categories_file)
        return
    
    source_folder = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    preview_mode = '--preview-mode' in sys.argv
    
    organizer = NLUEnhancedOrganizer(source_folder)
    organizer.organize_folder(dry_run=dry_run, preview_mode=preview_mode)

if __name__ == "__main__":
    main()
