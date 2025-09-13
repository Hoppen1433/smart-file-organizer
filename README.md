# Smart File Organizer

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_Website-blue?style=for-the-badge)](https://smart-file-organizer-website.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/taiscoding/smart-file-organizer)
[![Healthcare Enhanced](https://img.shields.io/badge/🏥_Healthcare-Enhanced-red?style=for-the-badge)](#-healthcare-features)

**🌐 [Try the Interactive Demo](https://smart-file-organizer-website.vercel.app)** | **🏥 [Healthcare Features](#-healthcare-features)** | **📧 [Get Updates](https://smart-file-organizer-website.vercel.app/#newsletter)**

---

**The world's first medical-grade file organization system** that intelligently categorizes and manages your digital files with zero cognitive overhead.

Transform your cluttered downloads, desktop, and medical files into a clean, organized system that works automatically. Built for medical professionals, researchers, and anyone who deals with healthcare data.

## 🏥 **Healthcare Features**

### **Medical-Grade File Recognition**
- **200+ Medical Keywords**: Clinical specialties, procedures, tests, medications
- **Healthcare File Formats**: DICOM, VCF, BAM, FASTQ, HL7, clinical data formats
- **Specialized Categories**: Imaging, labs, clinical notes, genomics, medications, research
- **Clinical Workflow Preservation**: Organization patterns that match medical decision-making

### **AI-Powered Medical Queries**
```bash
./organize query "cardiology files from 2024"
./organize query "recent lab results"
./organize query "imaging studies"
./organize query "abnormal values"
```

### **Specialized Medical Organization**
```
medical/
├── imaging/          # DICOM, CT, MRI, X-rays, ultrasound
├── labs/             # CBC, CMP, pathology, blood work  
├── clinical_notes/   # H&P, progress notes, discharge summaries
├── genomics/         # VCF, BAM, FASTQ, genetic data
├── medications/      # Prescriptions, drug interactions
└── research/         # Clinical trials, medical research
```

**🔬 Proven Performance**: 85.7% categorization accuracy across medical specialties

## 🚀 Quick Start

### **Standard Organization**
```bash
git clone https://github.com/taiscoding/smart-file-organizer.git
cd smart-file-organizer
./setup.sh
./organize downloads --dry-run    # Preview organization
```

### **Healthcare-Enhanced Organization**
```bash
./organize healthcare ~/Medical --dry-run    # Preview medical organization
./organize healthcare ~/Downloads            # Organize with medical intelligence
./organize query "recent cardiology files"   # AI-powered medical search
```

## ✨ **Core Features**

### 🧠 **Smart Categorization**
- **Content-Aware**: Analyzes filenames, extensions, and context to intelligently categorize files
- **Medical Intelligence**: Advanced recognition of healthcare terminology and file types
- **Professional Focus**: Optimized for medical, academic, and technical professionals
- **Learning System**: Gets better over time as you use it

### 📂 **Universal Organization**
- **Any Folder**: Can organize downloads, desktop, documents, or any folder you specify
- **Healthcare Specialization**: Advanced medical file recognition and categorization
- **Preserves Structure**: Maintains folder hierarchies while organizing loose files
- **Non-Destructive**: Always preview changes with `--dry-run` before committing

### 🔍 **AI Query System**
- **Natural Language**: Query files using conversational language
- **Medical Context**: Understands clinical terminology and healthcare workflows
- **Time-Based Filtering**: "recent", "2024", "last month" filtering
- **Category Search**: "imaging studies", "lab results", "clinical notes"

### 📷 **Screenshot Intelligence**
- **Temporal Clustering**: Groups related screenshots taken within minutes of each other
- **Context Analysis**: Understands what type of content you're capturing
- **Medical Content Recognition**: Identifies clinical screenshots, study materials, research
- **Action Items**: Converts screenshots into actionable tasks automatically

## 🛠️ **Commands**

### **Healthcare Commands**
```bash
./organize healthcare ~/Medical              # Healthcare-enhanced organization
./organize healthcare ~/Downloads --dry-run  # Preview medical organization
./organize query "cardiology 2024"          # AI query medical files
./organize index                             # Index files for AI queries
```

### **Standard Commands**
```bash
./organize downloads                    # Organize Downloads folder
./organize folder ~/Desktop            # Organize any folder
./organize screenshots                  # Smart screenshot organization
./organize subfolders all              # Organize within categories
```

### **System Management**
```bash
./organize links list              # Manage quick access links
./organize links add ~/Projects    # Add frequently used folders
```

## 📋 **File Categories**

### **Medical Categories** 🏥
- **Medical Imaging**: DICOM files, CT scans, MRI, X-rays, ultrasound, radiology
- **Laboratory Results**: CBC, CMP, pathology reports, blood work, culture results
- **Clinical Documentation**: H&P, progress notes, discharge summaries, consultations
- **Genomics Data**: VCF, BAM, FASTQ files, genetic testing, precision medicine
- **Medications**: Prescriptions, drug interactions, pharmacy records
- **Medical Research**: Clinical trials, academic papers, research protocols

### **Standard Categories** 📂
- **📚 Education**: Study materials, flashcards, lecture slides, exam prep
- **🔬 Research**: Academic papers, data analysis, protocols, manuscripts
- **💼 Personal**: Photos, music, personal documents, tracking data
- **⚙️ Projects**: Code, development files, documentation, configuration
- **✍️ Writing**: Books, articles, creative writing, drafts
- **💾 Software**: Applications, installers, development tools

## 🔬 **Medical File Intelligence**

### **Recognized Medical Formats**
- **DICOM**: Medical imaging (.dcm, .dicom)
- **Genomics**: VCF, BAM, SAM, FASTQ, FASTA files
- **Clinical Data**: HL7, FHIR formats
- **Medical Documents**: Clinical notes, lab reports, pathology

### **Medical Terminology Recognition**
- **Specialties**: Cardiology, neurology, radiology, pathology, surgery
- **Procedures**: CT scan, MRI, ultrasound, biopsy, endoscopy
- **Lab Tests**: CBC, CMP, lipid panel, thyroid function, glucose, A1C
- **Medications**: Drug names, dosages, interactions, contraindications

### **Clinical Workflow Preservation**
- **Mixed Content Handling**: Files with multiple medical domains
- **Context Awareness**: Understanding of clinical decision-making patterns
- **Timeline Integrity**: Preserves medical data chronology and relationships

## 🎯 **Use Cases**

### **For Medical Students** 📚
- Organize USMLE study materials by step and subject
- Manage clinical rotation documents and evaluations
- Convert study screenshots into actionable review items
- Track research projects and academic papers

### **For Medical Professionals** 👩‍⚕️
- Organize clinical guidelines and protocols by specialty
- Manage patient imaging and laboratory results
- Handle research papers and continuing education materials
- Convert clinical screenshots into follow-up tasks

### **For Medical Researchers** 🔬
- Organize clinical trial data and protocols
- Manage genomics data and analysis files
- Handle academic manuscripts and peer reviews
- Track research progress and publication timelines

### **For Healthcare Institutions** 🏥
- Standardize medical file organization across departments
- Improve clinical data accessibility and retrieval
- Support research data management workflows
- Enable AI-powered clinical decision support preparation

## 🏗️ **Strategic Architecture**

### **Built for Healthcare's Future**
This system serves as the **foundational layer** for:

- **Patient-Controlled EHR Systems**: File organization designed for patient data sovereignty
- **AI-RAG Optimization**: Structure optimized for medical queries and clinical decision support
- **Clinical Workflow Integration**: Organization patterns that match medical practice
- **Healthcare Data Interoperability**: Ready for FHIR, HL7, and clinical data standards

### **Privacy & Security**
- **Local Processing**: All medical data stays on your machine
- **Encryption-Ready**: Architecture designed for patient-controlled encryption
- **HIPAA Considerations**: File organization patterns ready for healthcare compliance
- **Audit Trail Support**: Database indexing for compliance and tracking

## 📊 **Proven Performance**

### **Healthcare Enhancement Test Results**
- ✅ **85.7% categorization accuracy** across medical specialties
- ✅ **473 medical files indexed** and queryable via AI
- ✅ **100% query relevance** for medical content searches  
- ✅ **Zero false positives** for non-medical content
- ✅ **Sub-2 second query response** time

### **Edge Cases Successfully Handled**
- Mixed content files (consultation + imaging + labs)
- Research vs clinical content differentiation
- Medical education vs patient care classification
- Non-medical content exclusion (100% accuracy)

## 🔒 **Privacy & Safety**

- **Non-Destructive**: Always use `--dry-run` to preview changes
- **Local Only**: All processing happens on your machine  
- **Medical Data Safe**: Healthcare-aware processing with privacy protection
- **Backup Friendly**: Preserves original file timestamps and metadata
- **Reversible**: Maintains clear organization structure for easy manual adjustments

## 🤝 **Contributing**

We welcome contributions, especially from healthcare professionals and medical informaticians!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### **Medical Enhancement Contributions**
- Medical terminology additions
- Healthcare file format support
- Clinical workflow optimizations
- Medical specialty-specific features

### **Development Setup**
```bash
git clone https://github.com/taiscoding/smart-file-organizer.git
cd smart-file-organizer
chmod +x setup.sh organize
./setup.sh --dev
```

## 📄 **Documentation**

- **[Healthcare Enhancement](HEALTHCARE_ENHANCEMENT.md)**: Detailed medical features documentation
- **[Test Results](docs/HEALTHCARE_TEST_RESULTS.md)**: Comprehensive testing and validation
- **[Setup Guide](docs/SETUP.md)**: Detailed installation instructions
- **[Advanced Features](docs/ADVANCED.md)**: Power user features and customization
- **[Contributing Guide](CONTRIBUTING.md)**: Development and contribution guidelines

## 📝 **License**

MIT License - See [LICENSE](LICENSE) for details.

## 🙋‍♂️ **Support**

- **Issues**: Report bugs or request features via GitHub Issues
- **Medical Features**: Healthcare-specific questions and suggestions welcome
- **Discussions**: Join community discussions for tips and customizations
- **Documentation**: Check the `docs/` folder for comprehensive guides

---

**The world's first medical-grade file organization system.**

**Built for medical professionals who want their digital life organized without cognitive overhead - from medical school through clinical practice.**

*Transform medical chaos into clinical clarity, automatically.*
