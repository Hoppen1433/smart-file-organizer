#!/usr/bin/env python3
"""
AI Learning System for Smart File Organizer
Learns from user categorization edits to improve future suggestions
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict, Counter

class AILearningSystem:
    def __init__(self, organized_folder=None):
        if organized_folder:
            self.organized_path = Path(organized_folder).expanduser().resolve()
        else:
            self.organized_path = Path.home() / "Documents" / "SmartFileOrganizer"
        
        self.learning_db = self.organized_path / ".ai_learning.db"
        self.patterns_file = self.organized_path / ".learned_patterns.json"
        
        self.create_learning_database()
        
    def create_learning_database(self):
        """Create database to store user corrections and learning patterns"""
        self.organized_path.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        # User corrections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_corrections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_category TEXT NOT NULL,
                corrected_category TEXT NOT NULL,
                file_extension TEXT,
                keywords TEXT,
                correction_date TEXT,
                confidence_before REAL,
                user_feedback TEXT
            )
        ''')
        
        # Learning patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_value TEXT NOT NULL,
                target_category TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                usage_count INTEGER DEFAULT 1,
                last_updated TEXT,
                success_rate REAL DEFAULT 1.0
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                preference_type TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                category_context TEXT,
                strength REAL DEFAULT 1.0,
                created_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def record_user_correction(self, filename, original_category, corrected_category, user_feedback=None):
        """Record when user corrects AI categorization"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        # Extract features from filename
        file_path = Path(filename)
        file_extension = file_path.suffix.lower()
        keywords = self.extract_keywords(filename)
        
        cursor.execute('''
            INSERT INTO user_corrections 
            (filename, original_category, corrected_category, file_extension, keywords, correction_date, user_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            original_category,
            corrected_category,
            file_extension,
            ' '.join(keywords),
            datetime.now().isoformat(),
            user_feedback
        ))
        
        conn.commit()
        conn.close()
        
        # Update learned patterns
        self.update_learning_patterns(filename, corrected_category)
        
        print(f"📚 Learned: {filename} → {corrected_category}")
        
    def extract_keywords(self, filename):
        """Extract meaningful keywords from filename"""
        # Remove extension and convert to lowercase
        name = Path(filename).stem.lower()
        
        # Split on common separators
        keywords = re.split(r'[_\-\s\.]+', name)
        
        # Filter meaningful keywords (length > 2, not numbers)
        meaningful_keywords = []
        for kw in keywords:
            if len(kw) > 2 and not kw.isdigit() and not re.match(r'^(the|and|for|with|from)$', kw):
                meaningful_keywords.append(kw)
                
        return meaningful_keywords
        
    def update_learning_patterns(self, filename, correct_category):
        """Update AI learning patterns based on user correction"""
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        file_path = Path(filename)
        extension = file_path.suffix.lower()
        keywords = self.extract_keywords(filename)
        
        # Learn from file extension
        if extension:
            cursor.execute('''
                INSERT OR REPLACE INTO learned_patterns 
                (pattern_type, pattern_value, target_category, confidence, usage_count, last_updated)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT confidence FROM learned_patterns 
                              WHERE pattern_type=? AND pattern_value=? AND target_category=?), 0.5) + 0.1,
                    COALESCE((SELECT usage_count FROM learned_patterns 
                              WHERE pattern_type=? AND pattern_value=? AND target_category=?), 0) + 1,
                    ?)
            ''', ('extension', extension, correct_category, 'extension', extension, correct_category,
                  'extension', extension, correct_category, datetime.now().isoformat()))
        
        # Learn from keywords
        for keyword in keywords:
            cursor.execute('''
                INSERT OR REPLACE INTO learned_patterns 
                (pattern_type, pattern_value, target_category, confidence, usage_count, last_updated)
                VALUES (?, ?, ?, 
                    COALESCE((SELECT confidence FROM learned_patterns 
                              WHERE pattern_type=? AND pattern_value=? AND target_category=?), 0.5) + 0.1,
                    COALESCE((SELECT usage_count FROM learned_patterns 
                              WHERE pattern_type=? AND pattern_value=? AND target_category=?), 0) + 1,
                    ?)
            ''', ('keyword', keyword, correct_category, 'keyword', keyword, correct_category,
                  'keyword', keyword, correct_category, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
    def get_ai_suggestion(self, filename):
        """Get improved AI categorization suggestion based on learned patterns"""
        if not self.learning_db.exists():
            return self.get_default_category(filename), 0.5
            
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        file_path = Path(filename)
        extension = file_path.suffix.lower()
        keywords = self.extract_keywords(filename)
        
        # Calculate confidence scores for different categories
        category_scores = defaultdict(float)
        
        # Check extension patterns
        if extension:
            cursor.execute('''
                SELECT target_category, confidence, usage_count 
                FROM learned_patterns 
                WHERE pattern_type = 'extension' AND pattern_value = ?
                ORDER BY confidence DESC, usage_count DESC
            ''', (extension,))
            
            for category, confidence, usage_count in cursor.fetchall():
                # Weight by confidence and usage frequency
                score = confidence * min(usage_count / 10.0, 1.0)
                category_scores[category] += score
        
        # Check keyword patterns
        for keyword in keywords:
            cursor.execute('''
                SELECT target_category, confidence, usage_count 
                FROM learned_patterns 
                WHERE pattern_type = 'keyword' AND pattern_value = ?
                ORDER BY confidence DESC, usage_count DESC
            ''', (keyword,))
            
            for category, confidence, usage_count in cursor.fetchall():
                score = confidence * min(usage_count / 5.0, 1.0)
                category_scores[category] += score * 0.8  # Keywords slightly less weight than extensions
        
        conn.close()
        
        if category_scores:
            # Get best category
            best_category = max(category_scores, key=category_scores.get)
            confidence = min(category_scores[best_category], 1.0)
            
            print(f"🤖 AI Suggestion: {filename} → {best_category} (confidence: {confidence:.2f})")
            return best_category, confidence
        else:
            # Fall back to default categorization
            return self.get_default_category(filename), 0.3
            
    def get_default_category(self, filename):
        """Default categorization logic (fallback)"""
        filename_lower = filename.lower()
        
        # Medical patterns
        medical_patterns = {
            'medical/imaging': ['ct', 'mri', 'xray', 'x-ray', 'dicom', 'scan', 'imaging'],
            'medical/labs': ['lab', 'blood', 'cbc', 'results', 'pathology', 'biopsy'],
            'medical/clinical_notes': ['clinical', 'patient', 'notes', 'chart', 'summary'],
            'medical/genomics': ['genetic', 'genomic', 'dna', 'gene', 'sequence'],
            'medical/medications': ['medication', 'prescription', 'drug', 'pharmacy'],
            'medical/research': ['research', 'study', 'trial', 'paper']
        }
        
        for category, keywords in medical_patterns.items():
            if any(kw in filename_lower for kw in keywords):
                return category
        
        # General patterns
        if any(kw in filename_lower for kw in ['medical', 'clinical', 'patient', 'doctor']):
            return 'medical'
        elif any(kw in filename_lower for kw in ['education', 'study', 'course', 'lecture']):
            return 'education'
        elif filename.endswith(('.py', '.js', '.html', '.css', '.json')):
            return 'projects/code'
        elif 'screenshot' in filename_lower:
            return 'screenshots'
        else:
            return 'downloads/misc'
            
    def get_learning_insights(self):
        """Generate insights about user preferences and AI learning"""
        if not self.learning_db.exists():
            return {"message": "No learning data available yet"}
            
        conn = sqlite3.connect(self.learning_db)
        cursor = conn.cursor()
        
        insights = {}
        
        # User correction statistics
        cursor.execute('SELECT COUNT(*) FROM user_corrections')
        total_corrections = cursor.fetchone()[0]
        insights['total_corrections'] = total_corrections
        
        # Most corrected categories
        cursor.execute('''
            SELECT original_category, COUNT(*) as correction_count
            FROM user_corrections 
            GROUP BY original_category 
            ORDER BY correction_count DESC 
            LIMIT 5
        ''')
        insights['most_corrected'] = cursor.fetchall()
        
        # User's preferred categories
        cursor.execute('''
            SELECT corrected_category, COUNT(*) as usage_count
            FROM user_corrections 
            GROUP BY corrected_category 
            ORDER BY usage_count DESC 
            LIMIT 5
        ''')
        insights['preferred_categories'] = cursor.fetchall()
        
        # Learned patterns strength
        cursor.execute('''
            SELECT pattern_type, COUNT(*) as pattern_count, AVG(confidence) as avg_confidence
            FROM learned_patterns 
            GROUP BY pattern_type
        ''')
        insights['pattern_strength'] = cursor.fetchall()
        
        conn.close()
        
        return insights
        
    def ask_clarification_questions(self, filename, suggested_category):
        """Generate clarifying questions to improve future categorization"""
        questions = []
        
        filename_lower = filename.lower()
        file_ext = Path(filename).suffix.lower()
        
        # Medical-specific questions
        if 'medical' in suggested_category:
            if any(term in filename_lower for term in ['report', 'result', 'summary']):
                questions.append({
                    "question": f"Is '{filename}' a clinical document that should be easily accessible for patient care?",
                    "options": ["Yes - High priority medical document", "No - Reference/research material", "Unsure"],
                    "learning_context": "document_priority"
                })
                
            if file_ext == '.pdf':
                questions.append({
                    "question": f"What type of medical document is '{filename}'?",
                    "options": ["Lab/Test Results", "Clinical Notes", "Research Paper", "Patient Education", "Insurance/Administrative"],
                    "learning_context": "medical_document_type"
                })
        
        # Project/code questions
        elif 'projects' in suggested_category:
            questions.append({
                "question": f"Is '{filename}' part of an active project or archived work?",
                "options": ["Active project - current work", "Archived - completed project", "Learning/tutorial material"],
                "learning_context": "project_status"
            })
        
        # General organization questions
        questions.append({
            "question": f"How often do you expect to access '{filename}'?",
            "options": ["Daily/Weekly", "Monthly", "Rarely - archival", "Never - can delete"],
            "learning_context": "access_frequency"
        })
        
        return questions[:2]  # Limit to 2 questions to avoid overwhelming user
        
def main():
    """Test the AI learning system"""
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 AI Learning System for Smart File Organizer")
        print("Usage:")
        print("  python3 ai_learning_system.py record <filename> <original_category> <corrected_category>")
        print("  python3 ai_learning_system.py suggest <filename>")
        print("  python3 ai_learning_system.py insights")
        return
        
    command = sys.argv[1]
    system = AILearningSystem()
    
    if command == 'record' and len(sys.argv) >= 5:
        filename = sys.argv[2]
        original = sys.argv[3]
        corrected = sys.argv[4]
        system.record_user_correction(filename, original, corrected)
        
    elif command == 'suggest' and len(sys.argv) >= 3:
        filename = sys.argv[2]
        category, confidence = system.get_ai_suggestion(filename)
        print(f"Suggested category: {category} (confidence: {confidence:.2f})")
        
        # Show clarification questions
        questions = system.ask_clarification_questions(filename, category)
        if questions:
            print("\\nClarification questions to improve AI:")
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q['question']}")
                for j, option in enumerate(q['options'], 1):
                    print(f"   {j}) {option}")
        
    elif command == 'insights':
        insights = system.get_learning_insights()
        print("📊 AI Learning Insights:")
        print(json.dumps(insights, indent=2))
        
    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()
