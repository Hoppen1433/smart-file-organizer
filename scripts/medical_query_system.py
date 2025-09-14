#!/usr/bin/env python3
"""
AI Query Interface for Healthcare Files
Natural language queries over organized medical data
Prototype for future EHR AI-RAG system
"""

import os
import sys
from pathlib import Path
import json
import re
from datetime import datetime, timedelta
import sqlite3

class MedicalFileQuerySystem:
    def __init__(self, base_path=None):
        if base_path:
            self.base_path = Path(base_path).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "auto_organized"
            
        self.medical_path = self.base_path / "medical"
        
        # Initialize file database
        self.db_path = self.base_path / "_system" / "medical_file_index.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for file indexing"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_files (
                id INTEGER PRIMARY KEY,
                filepath TEXT UNIQUE,
                filename TEXT,
                category TEXT,
                subcategory TEXT,
                file_type TEXT,
                date_created TIMESTAMP,
                date_modified TIMESTAMP,
                keywords TEXT,
                indexed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def index_medical_files(self):
        """Index all medical files for querying"""
        if not self.medical_path.exists():
            print("❌ Medical folder not found. Run organization first.")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        print("🔍 Indexing medical files for AI queries...")
        
        indexed_count = 0
        for file_path in self.medical_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                # Extract file metadata
                rel_path = str(file_path.relative_to(self.base_path))
                filename = file_path.name
                category = "medical"
                
                # Determine subcategory from path
                path_parts = file_path.relative_to(self.medical_path).parts
                subcategory = path_parts[0] if path_parts else "general"
                
                file_type = file_path.suffix.lower()
                date_created = datetime.fromtimestamp(file_path.stat().st_ctime)
                date_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # Extract keywords from filename and path
                keywords = self._extract_keywords(filename, str(file_path))
                
                # Insert or update in database
                cursor.execute('''
                    INSERT OR REPLACE INTO medical_files 
                    (filepath, filename, category, subcategory, file_type, 
                     date_created, date_modified, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (rel_path, filename, category, subcategory, file_type, 
                      date_created, date_modified, keywords))
                
                indexed_count += 1
                
        conn.commit()
        conn.close()
        
        print(f"✅ Indexed {indexed_count} medical files")
        
    def _extract_keywords(self, filename, filepath):
        """Extract relevant keywords from filename and path"""
        text = f"{filename} {filepath}".lower()
        
        # Medical specialty keywords
        medical_terms = [
            'cardiology', 'neurology', 'psychiatry', 'pediatrics', 'surgery',
            'radiology', 'pathology', 'emergency', 'internal medicine',
            'obstetrics', 'gynecology', 'dermatology', 'oncology',
            'ct scan', 'mri', 'x-ray', 'ultrasound', 'echocardiogram',
            'cbc', 'metabolic', 'lipid', 'thyroid', 'glucose', 'a1c',
            'biopsy', 'pathology', 'lab result', 'blood work',
            'prescription', 'medication', 'dosage', 'pharmacy',
            'genome', 'genetic', 'variant', 'sequencing'
        ]
        
        found_keywords = []
        for term in medical_terms:
            if term in text:
                found_keywords.append(term)
                
        return ','.join(found_keywords)
        
    def query_files(self, query):
        """Process natural language query and return relevant files"""
        print(f"🔍 Processing query: '{query}'")
        
        # Parse query intent
        query_lower = query.lower()
        
        # Time-based filters
        time_filter = self._parse_time_filter(query_lower)
        
        # Category filters
        category_filter = self._parse_category_filter(query_lower)
        
        # Keyword filters
        keyword_filter = self._parse_keyword_filter(query_lower)
        
        # Build SQL query
        sql_conditions = []
        sql_params = []
        
        if time_filter:
            sql_conditions.append("date_modified >= ?")
            sql_params.append(time_filter)
            
        if category_filter:
            sql_conditions.append("subcategory = ?")
            sql_params.append(category_filter)
            
        if keyword_filter:
            sql_conditions.append("(filename LIKE ? OR keywords LIKE ?)")
            keyword_param = f"%{keyword_filter}%"
            sql_params.extend([keyword_param, keyword_param])
        
        # Construct full query
        base_query = "SELECT * FROM medical_files"
        if sql_conditions:
            base_query += " WHERE " + " AND ".join(sql_conditions)
        base_query += " ORDER BY date_modified DESC"
        
        # Execute query
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(base_query, sql_params)
        results = cursor.fetchall()
        conn.close()
        
        return self._format_results(results, query)
        
    def _parse_time_filter(self, query):
        """Extract time-based filters from query"""
        if "2024" in query:
            return datetime(2024, 1, 1)
        elif "2023" in query:
            return datetime(2023, 1, 1)
        elif "last month" in query:
            return datetime.now() - timedelta(days=30)
        elif "last week" in query:
            return datetime.now() - timedelta(days=7)
        elif "recent" in query or "latest" in query:
            return datetime.now() - timedelta(days=30)
        return None
        
    def _parse_category_filter(self, query):
        """Extract category filters from query"""
        category_map = {
            'imaging': 'imaging',
            'lab': 'labs', 
            'laboratory': 'labs',
            'clinical': 'clinical_notes',
            'notes': 'clinical_notes',
            'genetic': 'genomics',
            'genomic': 'genomics',
            'medication': 'medications',
            'drug': 'medications',
            'research': 'research'
        }
        
        for keyword, category in category_map.items():
            if keyword in query:
                return category
        return None
        
    def _parse_keyword_filter(self, query):
        """Extract specific medical keywords from query"""
        medical_keywords = [
            'cardiology', 'cardiac', 'heart',
            'neurology', 'neuro', 'brain',
            'ct scan', 'mri', 'x-ray', 'ultrasound',
            'cbc', 'blood', 'glucose', 'cholesterol',
            'abnormal', 'normal', 'elevated'
        ]
        
        for keyword in medical_keywords:
            if keyword in query:
                return keyword
        return None
        
    def _format_results(self, results, original_query):
        """Format query results for display"""
        if not results:
            return f"❌ No files found for query: '{original_query}'"
            
        output = [f"🔍 Found {len(results)} files for: '{original_query}'\\n"]
        
        for row in results:
            filepath, filename, category, subcategory, file_type = row[1:6]
            date_modified = datetime.fromisoformat(row[7])
            
            # Format date
            if date_modified.date() == datetime.now().date():
                date_str = "Today"
            elif date_modified.date() == (datetime.now() - timedelta(days=1)).date():
                date_str = "Yesterday"
            else:
                date_str = date_modified.strftime("%Y-%m-%d")
                
            output.append(f"📄 {filename}")
            output.append(f"   📂 Category: {subcategory}")
            output.append(f"   📅 Modified: {date_str}")
            output.append(f"   📍 Path: {filepath}")
            output.append("")
            
        return "\\n".join(output)
        
    def demo_queries(self):
        """Run demonstration queries"""
        print("🏥 AI Medical File Query System - Demo")
        print("=====================================\\n")
        
        demo_queries = [
            "Show me all cardiology files from 2024",
            "Find my lab results with abnormal values", 
            "List imaging studies by body system",
            "Recent clinical notes",
            "All medication files",
            "Genetic testing results"
        ]
        
        for query in demo_queries:
            print(self.query_files(query))
            print("-" * 50)

def main():
    if len(sys.argv) < 2:
        print("🏥 AI Medical File Query System")
        print("Natural language queries over organized medical data")
        print()
        print("Usage:")
        print("  python3 medical_query_system.py index")
        print("  python3 medical_query_system.py query \"Show me cardiology files from 2024\"")
        print("  python3 medical_query_system.py demo")
        print()
        print("Example queries:")
        print("  • \"Show me all cardiology files from 2024\"")
        print("  • \"Find my lab results with abnormal values\"")
        print("  • \"List imaging studies by body system\"")
        print("  • \"Recent clinical notes\"")
        print("  • \"All medication files\"")
        print("  • \"Genetic testing results\"")
        return
        
    command = sys.argv[1]
    query_system = MedicalFileQuerySystem()
    
    if command == "index":
        query_system.index_medical_files()
    elif command == "query" and len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        print(query_system.query_files(query))
    elif command == "demo":
        query_system.demo_queries()
    else:
        print("❌ Invalid command. Use 'index', 'query', or 'demo'")

if __name__ == "__main__":
    main()
