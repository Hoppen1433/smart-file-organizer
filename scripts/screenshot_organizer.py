#!/usr/bin/env python3
"""
Smart Screenshot Organizer
Intelligently organizes screenshots using content analysis and temporal clustering.

This script analyzes screenshots to understand their content and context, then
organizes them into meaningful categories and sequences. Perfect for managing
the accumulation of screenshots from work, study, and personal activities.
"""

import os
import sys
import shutil
import re
from pathlib import Path
from datetime import datetime, timedelta

class SmartScreenshotOrganizer:
    def __init__(self, source_folder=None):
        """
        Initialize the Smart Screenshot Organizer.
        
        Args:
            source_folder (str, optional): Specific folder to process screenshots from
        """
        self.base_path = Path.home() / "Documents" / "organized_files"
        self.source_path = Path(source_folder).expanduser() if source_folder else None
        
        # Destination structure for organized screenshots
        self.destinations = {
            'medical': {
                'base': self.base_path / "medical" / "screenshots",
                'subdirs': {
                    'clinical': 'clinical_references',
                    'study': 'study_materials', 
                    'research': 'research_content',
                    'reference': 'quick_references'
                }
            },
            'education': {
                'base': self.base_path / "education" / "screenshots",
                'subdirs': {
                    'lectures': 'lecture_content',
                    'assignments': 'coursework',
                    'study': 'study_sessions',
                    'reference': 'educational_refs'
                }
            },
            'projects': {
                'base': self.base_path / "projects" / "screenshots",
                'subdirs': {
                    'code': 'code_snippets',
                    'design': 'design_mockups',
                    'errors': 'debugging_help',
                    'documentation': 'tech_docs'
                }
            },
            'personal': {
                'base': self.base_path / "personal" / "screenshots", 
                'subdirs': {
                    'general': 'general_screenshots',
                    'social': 'conversations',
                    'reference': 'quick_saves',
                    'ideas': 'inspiration'
                }
            }
        }
        
        # Time-based context patterns for better categorization
        self.time_contexts = {
            'morning': (6, 12),      # 6 AM - 12 PM: Often work/study
            'afternoon': (12, 17),   # 12 PM - 5 PM: Meetings/clinical work
            'evening': (17, 22),     # 5 PM - 10 PM: Study/personal projects
            'late_night': (22, 6)    # 10 PM - 6 AM: Deep work/personal time
        }
        
        # Enhanced keyword patterns for intelligent categorization
        self.keyword_patterns = {
            'medical': {
                'clinical': ['clinical', 'patient', 'hospital', 'diagnosis', 'treatment', 'protocol'],
                'study': ['usmle', 'step', 'medical school', 'exam', 'anatomy', 'physiology'],
                'research': ['research', 'pubmed', 'journal', 'study', 'clinical trial'],
                'reference': ['guideline', 'reference', 'chart', 'algorithm', 'flowchart']
            },
            'education': {
                'lectures': ['lecture', 'slides', 'presentation', 'class', 'professor'],
                'assignments': ['assignment', 'homework', 'project', 'submission'],
                'study': ['study', 'notes', 'review', 'flashcard', 'quiz'],
                'reference': ['textbook', 'reference', 'guide', 'manual']
            },
            'projects': {
                'code': ['code', 'programming', 'function', 'variable', 'github'],
                'design': ['design', 'mockup', 'wireframe', 'ui', 'interface'],
                'errors': ['error', 'debug', 'exception', 'traceback', 'failed'],
                'documentation': ['documentation', 'api', 'tutorial', 'guide', 'readme']
            }
        }
        
        # Screenshots taken within this timeframe are considered related
        self.sequence_threshold = timedelta(minutes=5)

    def extract_screenshot_metadata(self, file_path):
        """
        Extract timestamp and metadata from screenshot filename.
        
        Supports various screenshot naming patterns from different systems.
        
        Args:
            file_path (Path): Path to screenshot file
            
        Returns:
            dict or None: Metadata dictionary with timestamp and context
        """
        filename = file_path.name
        
        # macOS screenshot pattern: Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png
        mac_pattern = r'Screenshot (\d{4})-(\d{2})-(\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2}) ([AP]M)\.png'
        match = re.match(mac_pattern, filename)
        
        if match:
            year, month, day, hour, minute, second, ampm = match.groups()
            
            # Convert to 24-hour format
            hour = int(hour)
            if ampm == 'PM' and hour != 12:
                hour += 12
            elif ampm == 'AM' and hour == 12:
                hour = 0
                
            try:
                timestamp = datetime(int(year), int(month), int(day), hour, int(minute), int(second))
                return {
                    'timestamp': timestamp,
                    'time_context': self.get_time_context(timestamp),
                    'day_of_week': timestamp.strftime('%A'),
                    'age_days': (datetime.now() - timestamp).days
                }
            except ValueError:
                pass
        
        # Try other common patterns or fall back to file modification time
        try:
            stat_time = file_path.stat().st_mtime
            timestamp = datetime.fromtimestamp(stat_time)
            return {
                'timestamp': timestamp,
                'time_context': self.get_time_context(timestamp),
                'day_of_week': timestamp.strftime('%A'),
                'age_days': (datetime.now() - timestamp).days
            }
        except:
            return None

    def get_time_context(self, timestamp):
        """
        Determine time-based context for better categorization.
        
        Args:
            timestamp (datetime): When the screenshot was taken
            
        Returns:
            str: Time context (morning, afternoon, evening, late_night)
        """
        hour = timestamp.hour
        
        for context, (start, end) in self.time_contexts.items():
            if context == 'late_night':
                # Handle overnight period
                if hour >= start or hour < end:
                    return context
            elif start <= hour < end:
                return context
        
        return 'unknown'

    def analyze_screenshot_content(self, file_path, metadata):
        """
        Analyze screenshot for content-based categorization.
        
        Uses filename analysis, folder context, and timing patterns to
        determine the most appropriate category and subcategory.
        
        Args:
            file_path (Path): Path to screenshot
            metadata (dict): Screenshot metadata
            
        Returns:
            dict: Analysis results with category scores
        """
        filename = file_path.name.lower()
        folder_context = str(file_path.parent).lower()
        analysis_text = f"{filename} {folder_context}"
        
        category_scores = {}
        
        # Analyze against keyword patterns
        for main_category, subcategories in self.keyword_patterns.items():
            category_scores[main_category] = {}
            
            for subcat, keywords in subcategories.items():
                score = sum(1 for keyword in keywords if keyword in analysis_text)
                if score > 0:
                    category_scores[main_category][subcat] = score
        
        # Enhance scores based on timing context
        if metadata:
            time_context = metadata['time_context']
            day = metadata['day_of_week']
            
            # Time-based scoring adjustments
            if time_context == 'late_night':
                # Late night often means personal projects or deep work
                if 'projects' in category_scores:
                    for subcat in category_scores['projects']:
                        category_scores['projects'][subcat] += 1
                        
            elif time_context in ['morning', 'afternoon'] and day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                # Weekday business hours suggest professional/academic content
                for category in ['medical', 'education']:
                    if category in category_scores:
                        for subcat in category_scores[category]:
                            category_scores[category][subcat] += 1
        
        return category_scores

    def find_screenshot_sequences(self, file_list):
        """
        Identify sequences of related screenshots taken close together in time.
        
        Groups screenshots that were likely taken as part of the same workflow
        or documentation session.
        
        Args:
            file_list (list): List of screenshot file paths
            
        Returns:
            dict: Dictionary of sequences with their constituent files
        """
        if not file_list:
            return {}
            
        # Extract timestamps and sort
        timestamped_files = []
        for file_path in file_list:
            metadata = self.extract_screenshot_metadata(file_path)
            if metadata:
                timestamped_files.append((file_path, metadata['timestamp']))
        
        timestamped_files.sort(key=lambda x: x[1])
        
        # Group into sequences
        sequences = {}
        current_sequence = []
        sequence_id = 0
        
        for i, (file_path, timestamp) in enumerate(timestamped_files):
            if i == 0:
                current_sequence = [file_path]
            else:
                prev_timestamp = timestamped_files[i-1][1]
                time_gap = timestamp - prev_timestamp
                
                if time_gap <= self.sequence_threshold:
                    # Part of current sequence
                    current_sequence.append(file_path)
                else:
                    # End current sequence, start new one
                    if len(current_sequence) > 1:
                        sequences[f"sequence_{sequence_id}"] = {
                            'files': current_sequence.copy(),
                            'start_time': timestamped_files[i-len(current_sequence)][1],
                            'duration': prev_timestamp - timestamped_files[i-len(current_sequence)][1]
                        }
                        sequence_id += 1
                    current_sequence = [file_path]
        
        # Don't forget the last sequence
        if len(current_sequence) > 1:
            sequences[f"sequence_{sequence_id}"] = {
                'files': current_sequence.copy(),
                'start_time': timestamped_files[-len(current_sequence)][1],
                'duration': timestamped_files[-1][1] - timestamped_files[-len(current_sequence)][1]
            }
            
        return sequences

    def get_best_category(self, file_path, sequences=None):
        """
        Determine the best category and subcategory for a screenshot.
        
        Args:
            file_path (Path): Screenshot file path
            sequences (dict): Screenshot sequences for context
            
        Returns:
            tuple: (main_category, subcategory, sequence_info)
        """
        metadata = self.extract_screenshot_metadata(file_path)
        content_scores = self.analyze_screenshot_content(file_path, metadata)
        
        # Check if part of a sequence
        sequence_info = None
        if sequences:
            for seq_name, seq_data in sequences.items():
                if file_path in seq_data['files']:
                    sequence_info = {
                        'name': seq_name,
                        'size': len(seq_data['files']),
                        'duration': seq_data['duration']
                    }
                    break
        
        # Find best category and subcategory
        best_category = 'personal'  # Default fallback
        best_subcategory = 'general'
        max_score = 0
        
        for category, subcats in content_scores.items():
            for subcat, score in subcats.items():
                if score > max_score:
                    max_score = score
                    best_category = category
                    best_subcategory = subcat
        
        # Fallback logic if no clear category
        if max_score == 0 and metadata:
            time_context = metadata['time_context']
            if time_context == 'late_night':
                best_category = 'projects'
                best_subcategory = 'code'
            elif time_context in ['morning', 'afternoon']:
                best_category = 'education'
                best_subcategory = 'reference'
        
        return best_category, best_subcategory, sequence_info

    def organize_screenshots(self, source_folder=None, dry_run=False):
        """
        Main screenshot organization function.
        
        Args:
            source_folder (str, optional): Folder to process
            dry_run (bool): Preview changes without moving files
        """
        # Determine source paths
        if source_folder:
            source_paths = [Path(source_folder).expanduser()]
        elif self.source_path:
            source_paths = [self.source_path]
        else:
            # Default locations where screenshots accumulate
            source_paths = [
                Path.home() / "Desktop",
                Path.home() / "Downloads"
            ]
        
        # Collect all screenshots
        all_screenshots = []
        for path in source_paths:
            if path.exists():
                # Find screenshot files with various patterns
                patterns = ["Screenshot *.png", "Screen Shot *.png", "screenshot*.png"]
                for pattern in patterns:
                    screenshots = list(path.rglob(pattern))
                    all_screenshots.extend([s for s in screenshots if s.is_file()])
        
        # Remove duplicates
        all_screenshots = list(set(all_screenshots))
        
        if not all_screenshots:
            print("📷 No screenshots found to organize")
            return
            
        print(f"📷 Found {len(all_screenshots)} screenshots to analyze")
        
        # Analyze sequences first for context
        sequences = self.find_screenshot_sequences(all_screenshots)
        if sequences:
            total_in_sequences = sum(len(seq['files']) for seq in sequences.values())
            print(f"🔗 Detected {len(sequences)} screenshot sequences ({total_in_sequences} files)")
        
        # Categorize screenshots
        organization_plan = {}
        
        for screenshot in all_screenshots:
            category, subcategory, sequence_info = self.get_best_category(screenshot, sequences)
            
            if category not in organization_plan:
                organization_plan[category] = {}
            if subcategory not in organization_plan[category]:
                organization_plan[category][subcategory] = []
                
            organization_plan[category][subcategory].append({
                'file': screenshot,
                'sequence': sequence_info
            })
        
        # Execute or preview organization
        if dry_run:
            print("\n🧪 DRY RUN - Screenshot organization preview:")
            print("=" * 50)
            
            for category, subcats in organization_plan.items():
                print(f"\n📂 {category.upper()}:")
                for subcat, files in subcats.items():
                    print(f"  📁 {subcat}: {len(files)} screenshots")
                    
                    # Show examples and sequence info
                    for i, file_info in enumerate(files[:3]):
                        filename = file_info['file'].name
                        seq_info = ""
                        if file_info['sequence']:
                            seq = file_info['sequence']
                            seq_info = f" [sequence: {seq['size']} files]"
                        print(f"    • {filename}{seq_info}")
                        
                    if len(files) > 3:
                        print(f"    • ... and {len(files) - 3} more")
                        
            total_files = sum(len(files) for subcats in organization_plan.values() for files in subcats.values())
            print(f"\n📊 Total: {total_files} screenshots would be organized")
            
        else:
            print("\n📦 Organizing screenshots...")
            moved_count = 0
            
            for category, subcats in organization_plan.items():
                for subcat, files in subcats.items():
                    # Create destination directory
                    if category in self.destinations:
                        dest_base = self.destinations[category]['base']
                        subdir_name = self.destinations[category]['subdirs'].get(subcat, subcat)
                        dest_folder = dest_base / subdir_name
                    else:
                        dest_folder = self.base_path / category / "screenshots" / subcat
                    
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    
                    # Move files with sequence grouping
                    for file_info in files:
                        src_file = file_info['file']
                        sequence = file_info['sequence']
                        
                        # Create sequence subfolder if part of a sequence
                        if sequence and sequence['size'] > 2:
                            final_dest = dest_folder / sequence['name']
                            final_dest.mkdir(exist_ok=True)
                        else:
                            final_dest = dest_folder
                        
                        dest_path = final_dest / src_file.name
                        
                        # Handle duplicates
                        if dest_path.exists():
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            stem, suffix = src_file.stem, src_file.suffix
                            dest_path = final_dest / f"{stem}_{timestamp}{suffix}"
                        
                        try:
                            shutil.move(str(src_file), str(dest_path))
                            moved_count += 1
                        except Exception as e:
                            print(f"✗ Failed to move {src_file.name}: {e}")
                
                category_total = sum(len(files) for files in subcats.values())
                print(f"  ✅ {category}: {category_total} screenshots")
            
            print(f"\n✅ Organized {moved_count} screenshots with intelligent categorization!")
            print(f"📁 Screenshots organized in: {self.base_path}")

def main():
    """Main entry point for the Smart Screenshot Organizer."""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("📷 Smart Screenshot Organizer")
        print("Intelligently organize screenshots with content analysis and temporal clustering")
        print()
        print("Usage:")
        print("  python3 screenshot_organizer.py [source_folder] [options]")
        print()
        print("Examples:")
        print("  python3 screenshot_organizer.py")
        print("  python3 screenshot_organizer.py ~/Desktop --dry-run")
        print("  python3 screenshot_organizer.py ~/Downloads")
        print()
        print("Options:")
        print("  --dry-run    Preview organization without moving files")
        print("  -h, --help   Show this help message")
        print()
        print("Features:")
        print("  🧠 Content-aware categorization")
        print("  ⏰ Time-based context analysis")
        print("  🔗 Automatic sequence detection")
        print("  📂 Intelligent subfolder organization")
        print()
        return
    
    source_folder = None
    dry_run = '--dry-run' in sys.argv
    
    # Find source folder argument
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            source_folder = arg
            break
    
    print("📷 Smart Screenshot Organizer")
    print("Analyzing screenshots for intelligent organization...")
    print()
    
    organizer = SmartScreenshotOrganizer()
    organizer.organize_screenshots(source_folder, dry_run)

if __name__ == "__main__":
    main()
