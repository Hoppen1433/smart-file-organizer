#!/usr/bin/env python3
"""
Medical Query System for Smart File Organizer
Provides AI-powered search and indexing of organized medical files
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import logging

class MedicalQuerySystem:
    def __init__(self, organized_folder=None):
        if organized_folder:
            self.base_path = Path(organized_folder).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "SmartFileOrganizer"
        
        self.db_path = self.base_path / "medical_index.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for file indexing"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                file_size INTEGER,
                file_modified TEXT,
                indexed_date TEXT,
                keywords TEXT,
                content_preview TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def index_medical_files(self):
        """Index all files in the organized medical folder"""
        print("🔍 Starting medical file indexing...")
        
        if not self.base_path.exists():
            print(f"❌ Organized folder not found: {self.base_path}")
            print("   Please organize some files first!")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing index
        cursor.execute("DELETE FROM medical_files")
        
        indexed_count = 0
        medical_keywords = [
            'anatomy', 'physiology', 'pathology', 'clinical', 'medical',
            'patient', 'diagnosis', 'treatment', 'therapy', 'prescription',
            'lab', 'blood', 'imaging', 'ct', 'mri', 'xray', 'ultrasound',
            'genetic', 'genomic', 'medication', 'drug', 'research'
        ]
        
        # Recursively scan all files
        for file_path in self.base_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    stats = file_path.stat()
                    
                    # Determine category from path
                    relative_path = file_path.relative_to(self.base_path)
                    category = str(relative_path.parent) if relative_path.parent != Path('.') else 'root'
                    
                    # Extract keywords from filename and path
                    text_to_analyze = f"{file_path.name} {str(file_path)}".lower()
                    found_keywords = [kw for kw in medical_keywords if kw in text_to_analyze]
                    
                    # Basic content preview for text files
                    content_preview = ""
                    if file_path.suffix.lower() in ['.txt', '.md', '.json']:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content_preview = f.read(500)  # First 500 chars
                        except:
                            content_preview = "Unable to read content"
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO medical_files 
                        (filename, filepath, category, file_size, file_modified, indexed_date, keywords, content_preview)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        file_path.name,
                        str(file_path),
                        category,
                        stats.st_size,
                        datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        datetime.now().isoformat(),
                        ','.join(found_keywords),
                        content_preview
                    ))
                    
                    indexed_count += 1
                    
                except Exception as e:
                    print(f"⚠️ Error indexing {file_path.name}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Medical file indexing complete!")
        print(f"📊 Indexed {indexed_count} files in the medical database")
        return indexed_count
    
    def query_files(self, search_query):
        """Search indexed medical files"""
        if not self.db_path.exists():
            print("❌ Medical index not found. Please run indexing first!")
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search in filename, category, keywords, and content
        search_terms = search_query.lower().split()
        
        results = []
        for term in search_terms:
            cursor.execute('''
                SELECT filename, filepath, category, file_size, file_modified, keywords, content_preview
                FROM medical_files 
                WHERE LOWER(filename) LIKE ? 
                   OR LOWER(category) LIKE ? 
                   OR LOWER(keywords) LIKE ?
                   OR LOWER(content_preview) LIKE ?
                ORDER BY file_modified DESC
            ''', (f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
            
            results.extend(cursor.fetchall())
        
        conn.close()
        
        # Remove duplicates and format results
        seen_files = set()
        unique_results = []
        
        for result in results:
            filepath = result[1]
            if filepath not in seen_files:
                seen_files.add(filepath)
                unique_results.append({
                    'filename': result[0],
                    'filepath': result[1],
                    'category': result[2],
                    'file_size': result[3],
                    'file_modified': result[4],
                    'keywords': result[5],
                    'content_preview': result[6][:100] + "..." if len(result[6]) > 100 else result[6]
                })
        
        return unique_results
    
    def print_query_results(self, results, query):
        """Print formatted query results"""
        print(f"🔍 Medical File Search Results for: '{query}'")
        print(f"📊 Found {len(results)} matching files\\n")
        
        if not results:
            print("❌ No files found matching your search.")
            print("💡 Tips:")
            print("   - Make sure you've indexed files first")
            print("   - Try broader search terms")
            print("   - Check if files are in the SmartFileOrganizer folder")
            return
        
        for i, result in enumerate(results, 1):
            print(f"📄 {i}. {result['filename']}")
            print(f"   📂 Category: {result['category']}")
            print(f"   📅 Modified: {result['file_modified']}")
            print(f"   📍 Path: {result['filepath']}")
            if result['keywords']:
                print(f"   🔑 Keywords: {result['keywords']}")
            if result['content_preview'].strip():
                print(f"   📝 Preview: {result['content_preview']}")
            print()

def main():
    if len(sys.argv) < 2:
        print("🏥 Medical Query System")
        print("AI-powered search and indexing for organized medical files")
        print()
        print("Usage:")
        print("  python3 medical_query_system.py index")
        print("  python3 medical_query_system.py query '<search_term>'")
        print()
        print("Examples:")
        print("  python3 medical_query_system.py index")
        print("  python3 medical_query_system.py query 'anatomy'")
        print("  python3 medical_query_system.py query 'ct scan'")
        return
    
    command = sys.argv[1].lower()
    query_system = MedicalQuerySystem()
    
    if command == 'index':
        query_system.index_medical_files()
    elif command == 'query':
        if len(sys.argv) < 3:
            print("❌ Please provide a search query")
            return
        
        search_query = ' '.join(sys.argv[2:])
        results = query_system.query_files(search_query)
        query_system.print_query_results(results, search_query)
    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'index' or 'query'")

if __name__ == "__main__":
    main()
