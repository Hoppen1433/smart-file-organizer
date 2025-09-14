#!/usr/bin/env python3
"""
Smart File Organizer - Undo System
Reverses file organization by moving files back to original locations
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

class OrganizationUndo:
    def __init__(self):
        self.home_dir = Path.home()
        self.organized_dir = self.home_dir / 'Documents' / 'auto_organized'
        self.backup_dir = self.home_dir / 'Documents' / 'file_organization_backups'
        self.log_file = self.backup_dir / 'organization_log.json'
        
    def get_recent_organizations(self):
        """Get list of recent organization operations"""
        if not self.log_file.exists():
            return []
            
        try:
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                return data.get('operations', [])
        except:
            return []
    
    def undo_latest_organization(self):
        """Undo the most recent organization operation"""
        operations = self.get_recent_organizations()
        
        if not operations:
            # Try emergency undo if no log exists
            return self.emergency_undo_from_organized_folder()
            
        latest = operations[-1]
        operation_id = latest.get('id')
        files_moved = latest.get('files_moved', [])
        
        print(f"🔄 Undoing organization operation: {operation_id}")
        print(f"📁 Moving {len(files_moved)} files back to original locations")
        
        success_count = 0
        failed_files = []
        
        for file_info in files_moved:
            try:
                current_path = Path(file_info['destination'])
                original_path = Path(file_info['source'])
                
                # Create original directory if it doesn't exist
                original_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file back
                if current_path.exists():
                    shutil.move(str(current_path), str(original_path))
                    print(f"✅ Moved back: {current_path.name}")
                    success_count += 1
                else:
                    print(f"⚠️  File not found: {current_path}")
                    failed_files.append(str(current_path))
                    
            except Exception as e:
                print(f"❌ Failed to move {file_info.get('filename', 'unknown')}: {e}")
                failed_files.append(file_info.get('filename', 'unknown'))
        
        # Remove the operation from log since it's been undone
        if success_count > 0:
            operations.pop()
            self.save_operations_log(operations)
        
        print(f"\n🎯 Undo Summary:")
        print(f"   ✅ Successfully moved back: {success_count} files")
        
        if failed_files:
            print(f"   ❌ Failed to move: {len(failed_files)} files")
            for failed in failed_files[:3]:
                print(f"      • {failed}")
            if len(failed_files) > 3:
                print(f"      ... and {len(failed_files) - 3} more")
        
        # Clean up empty directories
        self.cleanup_empty_directories()
        
        return success_count > 0
    
    def emergency_undo_from_organized_folder(self):
        """
        Emergency undo - move all files from organized folder back to Downloads
        Used when no operation log exists
        """
        if not self.organized_dir.exists():
            print("❌ No organized files found to undo")
            return False
            
        print("🆘 No organization log found - performing emergency undo")
        print("📁 Moving all organized files back to Downloads folder")
        
        downloads_dir = self.home_dir / 'Downloads'
        downloads_dir.mkdir(exist_ok=True)
        
        moved_count = 0
        failed_count = 0
        
        try:
            # Walk through all files in organized directory
            for root, dirs, files in os.walk(str(self.organized_dir)):
                for filename in files:
                    if filename.startswith('.'):
                        continue
                        
                    source_path = Path(root) / filename
                    dest_path = downloads_dir / filename
                    
                    # Handle filename conflicts
                    counter = 1
                    original_name = filename
                    while dest_path.exists():
                        name_parts = original_name.rsplit('.', 1)
                        if len(name_parts) == 2:
                            dest_path = downloads_dir / f"{name_parts[0]}_restored_{counter}.{name_parts[1]}"
                        else:
                            dest_path = downloads_dir / f"{original_name}_restored_{counter}"
                        counter += 1
                    
                    try:
                        shutil.move(str(source_path), str(dest_path))
                        print(f"✅ Restored: {filename}")
                        moved_count += 1
                    except Exception as e:
                        print(f"❌ Failed to restore {filename}: {e}")
                        failed_count += 1
            
            # Clean up empty directories
            self.cleanup_empty_directories()
            
            print(f"\n🎯 Emergency Undo Complete:")
            print(f"   ✅ Restored {moved_count} files to Downloads")
            if failed_count > 0:
                print(f"   ❌ Failed to restore {failed_count} files")
            print(f"   📁 Files are now in: {downloads_dir}")
            
            return moved_count > 0
            
        except Exception as e:
            print(f"❌ Emergency undo failed: {e}")
            return False
    
    def save_operations_log(self, operations):
        """Save operations log"""
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, 'w') as f:
                json.dump({'operations': operations}, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not update operations log: {e}")
    
    def cleanup_empty_directories(self):
        """Remove empty directories from organized folder"""
        try:
            if not self.organized_dir.exists():
                return
                
            for root, dirs, files in os.walk(str(self.organized_dir), topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    try:
                        # Check if directory is empty
                        if not any(dir_path.iterdir()):
                            dir_path.rmdir()
                            rel_path = dir_path.relative_to(self.organized_dir)
                            print(f"🗑️  Removed empty directory: {rel_path}")
                    except OSError:
                        # Directory not empty or permission error
                        pass
        except Exception:
            # Organized directory doesn't exist or other error
            pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 undo_organizer.py <operation_id>")
        print("       python3 undo_organizer.py latest")
        sys.exit(1)
    
    operation_id = sys.argv[1]
    undo_system = OrganizationUndo()
    
    print("🔄 Smart File Organizer - Undo System")
    print("=" * 50)
    
    if operation_id == 'latest':
        success = undo_system.undo_latest_organization()
    else:
        # For now, only support 'latest' - could extend for specific operation IDs
        success = undo_system.undo_latest_organization()
    
    if success:
        print("\n✅ Undo operation completed successfully!")
        print("Your files have been moved back to their original locations.")
        sys.exit(0)
    else:
        print("\n❌ Undo operation failed or no files to restore.")
        sys.exit(1)

if __name__ == "__main__":
    main()