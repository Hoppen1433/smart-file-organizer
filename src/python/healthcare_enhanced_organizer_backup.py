#!/usr/bin/env python3
"""
Healthcare-Enhanced Universal Organizer
Advanced medical file recognition with specialized healthcare categorization
Built for the future of patient-controlled healthcare data organization
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
import logging
import re

class HealthcareEnhancedOrganizer:
    def __init__(self, source_folder, destination_base=None):
        self.source_path = Path(source_folder).expanduser().resolve()
        
        if destination_base:
            self.base_path = Path(destination_base).expanduser().resolve()
        else:
            self.base_path = Path.home() / "Documents" / "SmartFileOrganizer"
        
        # Enhanced destinations with healthcare specialization
        self.destinations = {
            'medical': self.base_path / "medical",
            'medical_imaging': self.base_path / "medical" / "imaging",
            'medical_labs': self.base_path / "medical" / "labs", 
            'medical_clinical_notes': self.base_path / "medical" / "clinical_notes",
            'medical_genomics': self.base_path / "medical" / "genomics",
            'medical_research': self.base_path / "medical" / "research",
            'medical_medications': self.base_path / "medical" / "medications",
            'education': self.base_path / "education",
            'research': self.base_path / "research", 
            'personal': self.base_path / "personal",
            'projects': self.base_path / "projects",
            'writing': self.base_path / "writing",
            'software': self.base_path / "software",
            'temp': self.base_path / "temp"
        }
        
        # Core medical keywords
        self.medical_keywords = [
            'residency', 'usmle', 'step', 'osce', 'clerkship', 'medical',
            'surgery', 'cardio', 'neuro', 'psychiatry', 'pediatrics',
            'obstetrics', 'gynecology', 'internal medicine', 'pathology',
            'radiology', 'anesthesiology', 'emergency medicine', 'family medicine',
            'cv', 'personal statement', 'eras', 'match', 'nbme', 'shelf',
            'uworld', 'free 120', 'cerclage', 'healthcore', 'pacs', 'sankofa',
            'permit', 'accommodations', 'dr hy', 'high yield', 'rapid rescue',
            'ob-gyn', 'gastro', 'heme', 'pulmonary', 'renal', 'rheum', 'endo', 'derm'
        ]
        
        # DICOM and Medical Imaging Keywords
        self.imaging_keywords = [
            'dicom', 'dcm', 'ct scan', 'mri', 'x-ray', 'xray', 'ultrasound', 
            'echocardiogram', 'echo', 'mammogram', 'pet scan', 'bone scan',
            'radiograph', 'angiogram', 'fluoroscopy', 'nuclear medicine',
            'imaging', 'radiology', 'scan', 'contrast', 'axial', 'sagittal',
            'coronal', 'anteroposterior', 'lateral', 'view', 'slice',
            'hounsfield', 't1 weighted', 't2 weighted', 'flair', 'dwi',
            'gradient echo', 'spin echo', 'perfusion', 'diffusion'
        ]
        
        # Laboratory Keywords 
        self.lab_keywords = [
            'cbc', 'complete blood count', 'cmp', 'comprehensive metabolic',
            'bmp', 'basic metabolic', 'lipid panel', 'liver function',
            'thyroid function', 'tsh', 't4', 't3', 'glucose', 'a1c',
            'hemoglobin', 'hematocrit', 'platelet', 'wbc', 'rbc',
            'sodium', 'potassium', 'chloride', 'co2', 'bun', 'creatinine',
            'ast', 'alt', 'alkaline phosphatase', 'bilirubin', 'albumin',
            'troponin', 'bnp', 'nt-probnp', 'creatine kinase', 'ck-mb',
            'psa', 'cea', 'ca 19-9', 'ca 125', 'alpha fetoprotein',
            'urinalysis', 'culture', 'sensitivity', 'gram stain',
            'blood gas', 'arterial', 'venous', 'lactate', 'ph',
            'pathology', 'biopsy', 'cytology', 'histology', 'microscopy'
        ]
        
        # Clinical Documentation Keywords
        self.clinical_keywords = [
            'history and physical', 'h&p', 'progress note', 'discharge summary',
            'operative report', 'procedure note', 'consultation', 'admission note',
            'soap note', 'assessment and plan', 'differential diagnosis',
            'chief complaint', 'hpi', 'history present illness', 'review systems',
            'physical exam', 'vital signs', 'impression', 'plan',
            'medication reconciliation', 'allergy list', 'problem list',
            'care plan', 'treatment plan', 'follow up', 'recommendations',
            'clinical decision', 'documentation', 'medical record',
            'patient care', 'nursing note', 'physician order'
        ]
        
        # Genomics and Precision Medicine Keywords
        self.genomics_keywords = [
            'genome', 'genomic', 'genetic', 'dna', 'rna', 'sequencing',
            'variant', 'mutation', 'polymorphism', 'snp', 'cnv',
            'whole genome', 'whole exome', 'targeted sequencing',
            'pharmacogenomics', 'personalized medicine', 'precision medicine',
            'biomarker', 'gene expression', 'methylation', 'epigenetic',
            'gwas', 'genome wide association', 'allele frequency',
            'vcf', 'variant call format', 'bam', 'sam', 'fastq',
            'illumina', 'nanopore', 'pacbio', 'sanger', 'next generation'
        ]
        
        # Medication and Pharmacology Keywords
        self.medication_keywords = [
            'prescription', 'medication', 'drug', 'pharmacy', 'dosage',
            'administration', 'side effects', 'adverse reactions', 'contraindications',
            'drug interaction', 'pharmacokinetics', 'pharmacodynamics',
            'half life', 'clearance', 'bioavailability', 'metabolism',
            'formulary', 'generic', 'brand name', 'therapeutic class',
            'mechanism action', 'indication', 'contraindication',
            'black box warning', 'fda approval', 'clinical trial',
            'dose adjustment', 'renal dosing', 'hepatic dosing'
        ]
        
        # Medical Research Keywords
        self.medical_research_keywords = [
            'clinical trial', 'randomized controlled', 'rct', 'cohort study',
            'case control', 'meta analysis', 'systematic review',
            'epidemiology', 'biostatistics', 'power analysis', 'sample size',
            'statistical significance', 'p value', 'confidence interval',
            'odds ratio', 'relative risk', 'hazard ratio', 'kaplan meier',
            'survival analysis', 'regression analysis', 'anova',
            'irb', 'institutional review board', 'ethics committee',
            'informed consent', 'protocol', 'inclusion criteria',
            'exclusion criteria', 'primary endpoint', 'secondary endpoint',
            'adverse event', 'serious adverse event', 'data monitoring'
        ]
        
        # File Extensions for Healthcare
        self.medical_extensions = {
            'imaging': ['.dcm', '.dicom', '.nii', '.nifti', '.img', '.hdr'],
            'genomics': ['.vcf', '.bam', '.sam', '.fastq', '.fasta', '.bed', '.gff'],
            'data': ['.csv', '.xlsx', '.sas7bdat', '.dta', '.sav']
        }
        
        # Other category keywords
        self.education_keywords = [
            'anki', 'flashcards', 'study', 'notes', 'lecture', 'presentation',
            'quiz', 'exam', 'test', 'assignment', 'homework', 'syllabus',
            'biochem', 'genetics', 'metabolism', 'microbiology', 'immunology',
            'step 1', 'step2ck', 'free 120', 'nbme explanations', 'hyguru'
        ]
        
        self.research_keywords = [
            'research', 'paper', 'journal', 'pubmed', 'study', 'clinical trial',
            'manuscript', 'publication', 'data', 'analysis', 'statistics', 
            'methodology', 'protocol', 'IRB', 'consent'
        ]
        
        self.projects_keywords = [
            'code', 'programming', 'development', 'software', 'app', 'website',
            'github', 'repository', 'algorithm', 'function', 'class', 'module',
            'sankofa', 'pacs', 'ai', 'machine learning', 'neural', 'model'
        ]
        
        self.writing_keywords = [
            'writing', 'book', 'novel', 'story', 'essay', 'article', 'blog',
            'manuscript', 'draft', 'chapter', 'poetry', 'creative', 'publish'
        ]

    def is_medical_imaging_file(self, file_path):
        """Detect medical imaging files by extension and content"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # DICOM and imaging extensions
        if any(filename.endswith(ext) for ext in self.medical_extensions['imaging']):
            return True
            
        # Imaging keywords in filename or path
        if any(keyword in file_path_str for keyword in self.imaging_keywords):
            return True
            
        # Pattern recognition for medical imaging
        imaging_patterns = [
            r'ct[_\s]scan', r'mri[_\s]scan', r'x[-_\s]?ray',
            r'ultrasound', r'echo.*gram', r'mammo.*gram'
        ]
        
        for pattern in imaging_patterns:
            if re.search(pattern, file_path_str):
                return True
                
        return False

    def is_lab_result_file(self, file_path):
        """Detect laboratory result files"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Lab keywords in filename or path
        if any(keyword in file_path_str for keyword in self.lab_keywords):
            return True
            
        # Common lab report patterns
        lab_patterns = [
            r'lab[_\s]result', r'blood[_\s]work', r'pathology[_\s]report',
            r'culture[_\s]result', r'biopsy[_\s]report'
        ]
        
        for pattern in lab_patterns:
            if re.search(pattern, file_path_str):
                return True
                
        return False

    def is_clinical_documentation(self, file_path):
        """Detect clinical notes and documentation"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Clinical documentation keywords
        if any(keyword in file_path_str for keyword in self.clinical_keywords):
            return True
            
        # Clinical document patterns
        clinical_patterns = [
            r'progress[_\s]note', r'discharge[_\s]summary', r'h&p',
            r'operative[_\s]report', r'consultation[_\s]note'
        ]
        
        for pattern in clinical_patterns:
            if re.search(pattern, file_path_str):
                return True
                
        return False

    def is_genomics_file(self, file_path):
        """Detect genomics and precision medicine files"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Genomics file extensions
        if any(filename.endswith(ext) for ext in self.medical_extensions['genomics']):
            return True
            
        # Genomics keywords
        if any(keyword in file_path_str for keyword in self.genomics_keywords):
            return True
            
        return False

    def is_medication_file(self, file_path):
        """Detect medication and pharmacy files"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Medication keywords
        if any(keyword in file_path_str for keyword in self.medication_keywords):
            return True
            
        # Medication patterns
        med_patterns = [
            r'prescription[_\s]list', r'medication[_\s]list', r'drug[_\s]interaction',
            r'pharmacy[_\s]record', r'formulary'
        ]
        
        for pattern in med_patterns:
            if re.search(pattern, file_path_str):
                return True
                
        return False

    def is_medical_research_file(self, file_path):
        """Detect medical research files"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Medical research keywords
        if any(keyword in file_path_str for keyword in self.medical_research_keywords):
            return True
            
        return False

    def get_file_category(self, file_path):
        """Enhanced categorization with healthcare specialization"""
        filename = file_path.name.lower()
        file_path_str = str(file_path).lower()
        
        # Skip system files
        if filename.startswith('.') or filename in ['Icon\\r']:
            return None
        
        # Healthcare-specific categorization (highest priority)
        if self.is_medical_imaging_file(file_path):
            return 'medical_imaging'
        elif self.is_lab_result_file(file_path):
            return 'medical_labs'
        elif self.is_clinical_documentation(file_path):
            return 'medical_clinical_notes'
        elif self.is_genomics_file(file_path):
            return 'medical_genomics'
        elif self.is_medication_file(file_path):
            return 'medical_medications'
        elif self.is_medical_research_file(file_path):
            return 'medical_research'
        
        # General medical categorization
        elif any(keyword in file_path_str for keyword in self.medical_keywords):
            return 'medical'
            
        # Other existing categories
        elif any(keyword in file_path_str for keyword in self.projects_keywords):
            return 'projects'
        elif any(keyword in file_path_str for keyword in self.education_keywords):
            return 'education'
        elif any(keyword in file_path_str for keyword in self.research_keywords):
            return 'research'
        elif any(keyword in file_path_str for keyword in self.writing_keywords):
            return 'writing'
            
        # File extension based categorization
        elif filename.endswith(('.py', '.js', '.html', '.css', '.json', '.tsx', '.jsx')):
            return 'projects'
        elif filename.endswith('.pdf'):
            return 'medical'  # Default for PDFs
        elif filename.endswith(('.csv', '.xlsx')) and any(kw in filename for kw in ['study', 'anki', 'flashcard']):
            return 'education'
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.heic', '.gif', '.mp3', '.mp4')):
            return 'personal'
        elif filename.endswith(('.md', '.txt', '.rtf')):
            return 'writing'
        
        return 'temp'

    def move_file(self, src_path, category):
        """Move file to appropriate destination with healthcare awareness"""
        if category not in self.destinations:
            return False
            
        dest_folder = self.destinations[category]
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Preserve relative path structure
        try:
            relative_to_source = src_path.relative_to(self.source_path)
            if len(relative_to_source.parts) > 1:
                context_path = dest_folder / relative_to_source.parent
                context_path.mkdir(parents=True, exist_ok=True)
                dest_path = context_path / src_path.name
            else:
                dest_path = dest_folder / src_path.name
        except ValueError:
            dest_path = dest_folder / src_path.name
        
        # Handle duplicates with timestamp
        if dest_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = src_path.stem, timestamp, src_path.suffix
            dest_path = dest_path.parent / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            
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
        
        # Collect all files recursively
        files_to_process = []
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                files_to_process.append(file_path)
        
        if not files_to_process:
            print(f"📁 No files found in {self.source_path.name}")
            return
            
        print(f"🏥 Healthcare-Enhanced File Organization")
        print(f"🔍 Found {len(files_to_process)} files in {self.source_path.name}...")
        
        if dry_run:
            print("\\n🧪 DRY RUN - Would organize with healthcare specialization:")
        else:
            print(f"\\n📦 Organizing {self.source_path.name} → {self.base_path.name}/ (Healthcare-Enhanced):")
            
        # Categorize files
        categories = {}
        healthcare_files = 0
        
        for file_path in files_to_process:
            category = self.get_file_category(file_path)
            if category:
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_path)
                
                # Count healthcare-specific files
                if category.startswith('medical_'):
                    healthcare_files += 1
        
        # Show healthcare detection summary
        if healthcare_files > 0:
            print(f"🏥 Detected {healthcare_files} healthcare-specific files")
        
        # Show/execute organization
        moved_count = 0
        for category, files in categories.items():
            category_display = category.replace('medical_', 'medical/')
            
            if dry_run:
                print(f"  📂 {category_display}: {len(files)} files")
                for file_path in files[:3]:
                    rel_path = file_path.relative_to(self.source_path)
                    print(f"    • {rel_path}")
                if len(files) > 3:
                    print(f"    • ... and {len(files) - 3} more")
            else:
                for file_path in files:
                    if self.move_file(file_path, category):
                        moved_count += 1
                        if moved_count % 50 == 0:
                            print(f"  ✓ Processed {moved_count} files...")
                            
                print(f"  ✅ {category_display}: {len(files)} files")
        
        if not dry_run and moved_count > 0:
            print(f"\\n🏥 Healthcare-Enhanced Organization Complete!")
            print(f"✅ Organized {moved_count} files with medical specialization")
            if healthcare_files > 0:
                print(f"🔬 {healthcare_files} files organized into specialized medical categories")

def main():
    if len(sys.argv) < 2:
        print("🏥 Healthcare-Enhanced Universal Organizer")
        print("Advanced medical file recognition with specialized categorization")
        print()
        print("Usage:")
        print("  python3 healthcare_enhanced_organizer.py <source_folder> [destination_base] [--dry-run] [--preview-mode]")
        print()
        print("Examples:")
        print("  python3 healthcare_enhanced_organizer.py ~/Desktop")
        print("  python3 healthcare_enhanced_organizer.py ~/Downloads --dry-run")
        print("  python3 healthcare_enhanced_organizer.py '/Medical Files' ~/organized")
        print("  python3 healthcare_enhanced_organizer.py ~/Desktop --preview-mode")
        print()
        print("Healthcare Specializations:")
        print("  • Medical imaging (DICOM, CT, MRI, X-rays)")
        print("  • Laboratory results (CBC, CMP, pathology)")
        print("  • Clinical documentation (H&P, progress notes)")
        print("  • Genomics data (VCF, BAM, FASTQ)")
        print("  • Medication records")
        print("  • Medical research files")
        print()
        print("Default destination: ~/Documents/SmartFileOrganizer/")
        return
    
    source_folder = sys.argv[1]
    destination_base = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    dry_run = '--dry-run' in sys.argv
    preview_mode = '--preview-mode' in sys.argv
    
    organizer = HealthcareEnhancedOrganizer(source_folder, destination_base)
    organizer.organize_folder(dry_run=dry_run, preview_mode=preview_mode)

if __name__ == "__main__":
    main()
