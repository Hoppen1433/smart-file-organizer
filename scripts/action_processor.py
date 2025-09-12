#!/usr/bin/env python3
"""
Screenshot Action Processor
Converts screenshots into actionable items with smart categorization.

This script analyzes screenshots to identify potential action items, then helps
you convert them into organized tasks with due dates and context. Perfect for
turning visual notes and reminders into a structured workflow.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta

class ScreenshotActionProcessor:
    def __init__(self):
        """Initialize the Screenshot Action Processor."""
        self.base_path = Path.home() / "Documents" / "organized_files"
        self.screenshots_path = self.base_path / "screenshots"
        self.actions_path = self.base_path / "actions"
        self.actions_path.mkdir(parents=True, exist_ok=True)
        
        # Action categories with clear purposes and timeframes
        self.action_categories = {
            'follow_up': {
                'description': 'Items requiring future investigation or action',
                'examples': ['Quiz results to review', 'Research papers to read', 'Code snippets to implement'],
                'default_days': 7,
                'priority': 'medium'
            },
            'reference': {
                'description': 'Information to reference later',
                'examples': ['Medical protocols', 'API documentation', 'Study materials'],
                'default_days': 30,
                'priority': 'low'
            },
            'decision': {
                'description': 'Requires a decision or choice',
                'examples': ['Treatment options', 'Architecture choices', 'Study strategies'],
                'default_days': 3,
                'priority': 'high'
            },
            'learn': {
                'description': 'Topics to study or learn more about',
                'examples': ['New concepts', 'Programming techniques', 'Research areas'],
                'default_days': 14,
                'priority': 'medium'
            },
            'track': {
                'description': 'Progress or metrics to monitor',
                'examples': ['Self-assessments', 'Learning milestones', 'Health metrics'],
                'default_days': 30,
                'priority': 'low'
            }
        }
        
        # Pattern recognition for automatic categorization
        self.context_patterns = {
            'follow_up': [
                r'quiz.*result', r'test.*score', r'assessment.*result', r'follow.?up',
                r'reminder', r'later', r'check.*back', r'review.*this',
                r'action.*item', r'to.?do', r'task'
            ],
            'reference': [
                r'protocol', r'procedure', r'documentation', r'manual', r'guide',
                r'reference', r'how.?to', r'tutorial', r'cheat.*sheet'
            ],
            'decision': [
                r'vs\.?', r'\bor\b', r'choice', r'option', r'decide', r'consider',
                r'pros.*cons', r'compare', r'evaluate', r'which.*better'
            ],
            'learn': [
                r'learn', r'study', r'research', r'understand', r'explore',
                r'deep.*dive', r'investigate', r'new.*concept', r'tutorial'
            ],
            'track': [
                r'progress', r'milestone', r'metric', r'score', r'rating',
                r'track', r'monitor', r'measure', r'results', r'outcome'
            ]
        }

    def extract_screenshot_metadata(self, file_path):
        """Extract metadata from screenshot file."""
        filename = file_path.name
        
        # Parse macOS screenshot naming pattern
        pattern = r'Screenshot (\d{4})-(\d{2})-(\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2}) ([AP]M)\.png'
        match = re.match(pattern, filename)
        
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
                    'age_days': (datetime.now() - timestamp).days,
                    'day_of_week': timestamp.strftime('%A'),
                    'time_of_day': self.get_time_context(timestamp.hour)
                }
            except ValueError:
                pass
        
        # Fall back to file modification time
        try:
            stat_time = file_path.stat().st_mtime
            timestamp = datetime.fromtimestamp(stat_time)
            return {
                'timestamp': timestamp,
                'age_days': (datetime.now() - timestamp).days,
                'day_of_week': timestamp.strftime('%A'),
                'time_of_day': self.get_time_context(timestamp.hour)
            }
        except:
            return None

    def get_time_context(self, hour):
        """Get time-based context for screenshot."""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 22:
            return 'evening'
        else:
            return 'late_night'

    def analyze_screenshot_for_actions(self, screenshot_path):
        """Analyze a screenshot to identify potential action items."""
        filename = screenshot_path.name
        folder_path = str(screenshot_path.parent)
        metadata = self.extract_screenshot_metadata(screenshot_path)
        
        # Create analysis text from available context
        analysis_text = f"{filename} {folder_path}".lower()
        
        # Analyze against pattern categories
        action_suggestions = []
        
        for action_type, patterns in self.context_patterns.items():
            score = 0
            matched_patterns = []
            
            for pattern in patterns:
                if re.search(pattern, analysis_text, re.IGNORECASE):
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                action_suggestions.append({
                    'type': action_type,
                    'confidence': min(score / 3, 1.0),  # Normalize to 0-1
                    'matched_patterns': matched_patterns,
                    'suggested_days': self.action_categories[action_type]['default_days'],
                    'priority': self.action_categories[action_type]['priority']
                })
        
        # Sort by confidence
        action_suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Context-based adjustments
        if metadata and metadata['age_days'] > 14:
            for suggestion in action_suggestions:
                if suggestion['type'] == 'follow_up':
                    suggestion['priority'] = 'high'
                    suggestion['suggested_days'] = 3
        
        return {
            'screenshot_path': screenshot_path,
            'metadata': metadata,
            'folder_context': str(screenshot_path.parent.name),
            'action_suggestions': action_suggestions[:3],
            'auto_suggestion': action_suggestions[0] if action_suggestions else None
        }

    def create_action_item(self, analysis, action_type, custom_note="", custom_days=None):
        """Create an actionable item from screenshot analysis."""
        action_id = f"screenshot_action_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        screenshot_name = analysis['screenshot_path'].name
        
        # Calculate due date
        if custom_days:
            due_date = datetime.now() + timedelta(days=custom_days)
        else:
            default_days = self.action_categories[action_type]['default_days']
            due_date = datetime.now() + timedelta(days=default_days)
        
        # Determine priority
        priority = self.action_categories[action_type]['priority']
        if analysis['metadata'] and analysis['metadata']['age_days'] > 14:
            priority = 'high'
        
        action_item = {
            'id': action_id,
            'created_date': datetime.now().isoformat(),
            'due_date': due_date.isoformat(),
            'action_type': action_type,
            'status': 'pending',
            'priority': priority,
            'screenshot_info': {
                'filename': screenshot_name,
                'path': str(analysis['screenshot_path']),
                'folder_context': analysis['folder_context'],
                'age_days': analysis['metadata']['age_days'] if analysis['metadata'] else 0
            },
            'description': self.generate_action_description(analysis, action_type),
            'custom_note': custom_note,
            'tags': self.generate_tags(analysis, action_type)
        }
        
        return action_item

    def generate_action_description(self, analysis, action_type):
        """Generate a descriptive action item title."""
        screenshot_name = analysis['screenshot_path'].stem
        folder_context = analysis['folder_context']
        
        templates = {
            'follow_up': f"Follow up on: {screenshot_name}",
            'reference': f"Reference material: {screenshot_name}",
            'decision': f"Make decision about: {screenshot_name}",
            'learn': f"Study/learn: {screenshot_name}",
            'track': f"Track progress on: {screenshot_name}"
        }
        
        base_description = templates.get(action_type, f"Action needed: {screenshot_name}")
        
        if folder_context and folder_context != 'screenshots':
            base_description += f" (from {folder_context})"
            
        return base_description

    def generate_tags(self, analysis, action_type):
        """Generate relevant tags for the action item."""
        tags = [action_type]
        
        # Add folder-based tags
        folder_context = analysis['folder_context']
        if folder_context:
            tags.append(folder_context.lower().replace(' ', '_'))
        
        # Add time-based tags
        if analysis['metadata']:
            age_days = analysis['metadata']['age_days']
            if age_days > 30:
                tags.append('old_screenshot')
            elif age_days > 7:
                tags.append('week_old')
            else:
                tags.append('recent')
                
            tags.append(analysis['metadata']['time_of_day'])
        
        return tags

    def scan_screenshots_for_actions(self, folder_path=None, interactive=True):
        """Scan screenshots and suggest actions."""
        if folder_path:
            screenshots = list(Path(folder_path).expanduser().rglob("Screenshot *.png"))
        else:
            screenshots = []
            # Check common screenshot locations
            locations = [
                self.screenshots_path,
                Path.home() / "Desktop",
                Path.home() / "Downloads"
            ]
            
            for location in locations:
                if location.exists():
                    screenshots.extend(location.rglob("Screenshot *.png"))
        
        if not screenshots:
            print("📷 No screenshots found to process for actions")
            return []
        
        print(f"🔍 Analyzing {len(screenshots)} screenshots for potential actions...")
        
        action_candidates = []
        
        for screenshot in screenshots:
            analysis = self.analyze_screenshot_for_actions(screenshot)
            if analysis['action_suggestions']:
                action_candidates.append(analysis)
        
        print(f"🎯 Found {len(action_candidates)} screenshots with potential actions")
        
        if not action_candidates:
            print("✅ No actionable screenshots found!")
            return []
        
        if interactive:
            return self.interactive_action_creation(action_candidates)
        else:
            return self.auto_create_actions(action_candidates)

    def interactive_action_creation(self, candidates):
        """Interactive workflow for creating actions from screenshots."""
        created_actions = []
        
        print("\n🎯 Interactive Action Creation")
        print("=" * 60)
        print("Review each screenshot and choose what action to create (if any)")
        print()
        
        for i, analysis in enumerate(candidates, 1):
            screenshot_name = analysis['screenshot_path'].name
            folder_context = analysis['folder_context']
            
            print(f"📸 {i}/{len(candidates)}: {screenshot_name}")
            print(f"📁 Context: {folder_context}")
            
            if analysis['metadata']:
                age = analysis['metadata']['age_days']
                time_context = analysis['metadata']['time_of_day']
                print(f"📅 Age: {age} days old, captured during {time_context}")
            
            print("\n🎯 Suggested actions:")
            for j, suggestion in enumerate(analysis['action_suggestions'], 1):
                confidence = int(suggestion['confidence'] * 100)
                action_type = suggestion['type']
                days = suggestion['suggested_days']
                priority = suggestion['priority']
                
                description = self.action_categories[action_type]['description']
                print(f"   {j}. {action_type.upper()} ({confidence}% confidence, {priority} priority)")
                print(f"      → {description}")
                print(f"      → Due in {days} days")
            
            print("\nOptions:")
            if analysis['action_suggestions']:
                for j in range(len(analysis['action_suggestions'])):
                    print(f"  {j+1}: Create '{analysis['action_suggestions'][j]['type']}' action")
            print("  c: Create custom action")
            print("  s: Skip this screenshot")
            print("  q: Quit and save progress")
            
            while True:
                choice = input("\nYour choice: ").strip().lower()
                
                if choice == 'q':
                    print("👋 Exiting action creation...")
                    return created_actions
                elif choice == 's':
                    print("⏭️  Skipped")
                    break
                elif choice == 'c':
                    print("\nCustom action creation:")
                    action_types = list(self.action_categories.keys())
                    for j, atype in enumerate(action_types, 1):
                        desc = self.action_categories[atype]['description']
                        print(f"  {j}. {atype} - {desc}")
                    
                    try:
                        type_choice = int(input("Choose action type (1-5): ")) - 1
                        if 0 <= type_choice < len(action_types):
                            action_type = action_types[type_choice]
                            custom_note = input("Custom note (optional): ").strip()
                            
                            try:
                                custom_days = input("Days until due (press Enter for default): ").strip()
                                custom_days = int(custom_days) if custom_days else None
                            except ValueError:
                                custom_days = None
                            
                            action = self.create_action_item(analysis, action_type, custom_note, custom_days)
                            created_actions.append(action)
                            print(f"✅ Created custom action: {action['description']}")
                            break
                    except (ValueError, IndexError):
                        print("❌ Invalid choice")
                
                elif choice.isdigit():
                    try:
                        suggestion_idx = int(choice) - 1
                        if 0 <= suggestion_idx < len(analysis['action_suggestions']):
                            suggestion = analysis['action_suggestions'][suggestion_idx]
                            custom_note = input("Optional note (press Enter to skip): ").strip()
                            
                            action = self.create_action_item(analysis, suggestion['type'], custom_note)
                            created_actions.append(action)
                            print(f"✅ Created action: {action['description']}")
                            break
                        else:
                            print("❌ Invalid choice number")
                    except ValueError:
                        print("❌ Please enter a valid number")
                else:
                    print("❌ Invalid choice. Please try again.")
            
            print("\n" + "─" * 60 + "\n")
        
        return created_actions

    def auto_create_actions(self, candidates):
        """Automatically create actions for high-confidence suggestions."""
        created_actions = []
        
        print("🤖 Auto-creating actions for high-confidence screenshots...")
        
        for analysis in candidates:
            if analysis['auto_suggestion'] and analysis['auto_suggestion']['confidence'] > 0.6:
                action = self.create_action_item(analysis, analysis['auto_suggestion']['type'])
                created_actions.append(action)
                print(f"✅ Auto-created: {action['description']}")
        
        return created_actions

    def save_actions(self, actions):
        """Save actions to the system."""
        if not actions:
            print("📝 No actions to save")
            return
        
        # Load existing actions
        actions_file = self.actions_path / "screenshot_actions.json"
        existing_actions = []
        
        if actions_file.exists():
            try:
                with open(actions_file, 'r') as f:
                    existing_actions = json.load(f)
            except:
                existing_actions = []
        
        # Add new actions
        existing_actions.extend(actions)
        
        # Save back to file
        try:
            with open(actions_file, 'w') as f:
                json.dump(existing_actions, f, indent=2, default=str)
            
            print(f"💾 Saved {len(actions)} new actions to {actions_file}")
            
            # Create readable summary
            self.create_action_summary(existing_actions)
            
        except Exception as e:
            print(f"❌ Failed to save actions: {e}")

    def create_action_summary(self, all_actions):
        """Create a readable markdown summary of actions."""
        summary_file = self.actions_path / "action_summary.md"
        
        # Filter pending actions and sort by priority and due date
        pending_actions = [a for a in all_actions if a.get('status', 'pending') == 'pending']
        
        def priority_score(action):
            priorities = {'high': 3, 'medium': 2, 'low': 1}
            return priorities.get(action.get('priority', 'medium'), 2)
        
        pending_actions.sort(key=lambda x: (
            -priority_score(x),  # Higher priority first
            x.get('due_date', '9999-12-31')  # Earlier due date first
        ))
        
        try:
            with open(summary_file, 'w') as f:
                f.write("# Screenshot Action Items\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"**Total Actions:** {len(all_actions)}\n")
                f.write(f"**Pending:** {len(pending_actions)}\n\n")
                
                if pending_actions:
                    f.write("## Pending Actions\n\n")
                    
                    current_priority = None
                    for action in pending_actions:
                        priority = action.get('priority', 'medium')
                        
                        if priority != current_priority:
                            f.write(f"### {priority.title()} Priority\n\n")
                            current_priority = priority
                        
                        due_date = action.get('due_date', '')[:10]  # Just the date part
                        description = action.get('description', 'No description')
                        filename = action.get('screenshot_info', {}).get('filename', 'Unknown')
                        custom_note = action.get('custom_note', '')
                        tags = ', '.join(action.get('tags', []))
                        
                        f.write(f"- **{description}**\n")
                        f.write(f"  - 📅 Due: {due_date}\n")
                        f.write(f"  - 📷 Screenshot: `{filename}`\n")
                        if custom_note:
                            f.write(f"  - 📝 Note: {custom_note}\n")
                        if tags:
                            f.write(f"  - 🏷️ Tags: {tags}\n")
                        f.write("\n")
                else:
                    f.write("No pending actions found.\n")
                
                f.write("\n---\n")
                f.write("*Generated by Smart File Organizer - Screenshot Action Processor*\n")
            
            print(f"📋 Action summary created: {summary_file}")
            
        except Exception as e:
            print(f"❌ Failed to create summary: {e}")

def main():
    """Main entry point for the Screenshot Action Processor."""
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("🎯 Screenshot Action Processor")
        print("Convert your screenshots into actionable items with smart categorization")
        print()
        print("Usage:")
        print("  python3 action_processor.py [mode] [options]")
        print()
        print("Modes:")
        print("  interactive  Interactive action creation (default)")
        print("  auto        Automatic action creation for high-confidence items")
        print("  scan        Just scan and show potential actions")
        print()
        print("Options:")
        print("  --folder PATH  Process screenshots from specific folder")
        print()
        print("Action Types:")
        processor = ScreenshotActionProcessor()
        for action_type, info in processor.action_categories.items():
            print(f"  📋 {action_type}: {info['description']}")
        print()
        return
    
    # Parse arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'interactive'
    folder_path = None
    
    if '--folder' in sys.argv:
        try:
            folder_idx = sys.argv.index('--folder')
            if folder_idx + 1 < len(sys.argv):
                folder_path = sys.argv[folder_idx + 1]
        except (IndexError, ValueError):
            print("❌ Invalid --folder option")
            return
    
    print("🎯 Screenshot Action Processor")
    print("Converting screenshots into actionable workflow items")
    print("=" * 60)
    
    processor = ScreenshotActionProcessor()
    
    try:
        if mode == 'scan':
            actions = processor.scan_screenshots_for_actions(folder_path, interactive=False)
            print(f"\n📊 Analysis complete: Found {len(actions)} actionable screenshots")
        elif mode == 'auto':
            actions = processor.scan_screenshots_for_actions(folder_path, interactive=False)
            processor.save_actions(actions)
        elif mode == 'interactive':
            actions = processor.scan_screenshots_for_actions(folder_path, interactive=True)
            if actions:
                processor.save_actions(actions)
                print(f"\n🎉 Created {len(actions)} action items from your screenshots!")
            else:
                print("\n✅ No actions created this session")
        else:
            print(f"❌ Unknown mode: {mode}")
            print("Available modes: interactive, auto, scan")
    
    except KeyboardInterrupt:
        print("\n👋 Action processing interrupted by user")
    except Exception as e:
        print(f"❌ Error during processing: {e}")

if __name__ == "__main__":
    main()
