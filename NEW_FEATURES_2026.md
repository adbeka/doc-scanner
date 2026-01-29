# New Features Added - January 2026

## Overview

Four powerful new feature sets have been added to the Document Scanner application, significantly expanding its capabilities beyond basic document scanning.

## 1. OCR (Optical Character Recognition) ✨

**Module**: `src/ocr_engine.py`

### Features
- **Text Extraction**: Extract all text from scanned documents
- **Smart Metadata**: Automatically extract dates, emails, phone numbers, URLs, and monetary amounts
- **Auto-Naming**: Automatically generate filenames based on document content
- **Multi-Language**: Support for multiple languages (English, French, Spanish, etc.)
- **Search**: Search for specific text within documents
- **Confidence Scoring**: Get confidence scores for extracted text

### Key Functions
```python
OCREngine.extract_text(image, lang='eng')        # Extract text with metadata
OCREngine.extract_text_simple(image)             # Quick text extraction
OCREngine.auto_name_from_text(text)              # Generate filename
OCREngine.extract_metadata(image)                # Extract structured data
OCREngine.search_text(image, search_term)        # Search for text
```

### GUI Integration
- **"Extract Text"** button - Opens dialog with extracted text and confidence
- **"Auto-Name File"** button - Suggests filename based on content
- Copy extracted text to clipboard

### Requirements
- `pytesseract>=0.3.10` (Python package)
- Tesseract OCR engine (system installation)

### Use Cases
- Digitizing paper documents
- Extracting information from receipts/invoices
- Creating searchable PDFs
- Organizing scans by content

---

## 2. Auto Enhancement 🎯

**Module**: `src/auto_enhance.py`

### Features
- **Auto Deskew**: Automatically straighten tilted documents (up to 10° correction)
- **Auto Crop**: Intelligent border removal and margin trimming
- **Shadow Removal**: Eliminate shadows from lighting
- **Auto White Balance**: Correct color temperature
- **Auto Contrast**: Histogram equalization with adaptive clipping
- **Auto Sharpen**: Intelligent sharpening
- **Full Pipeline**: Complete enhancement in one click

### Key Functions
```python
AutoEnhancer.auto_deskew(image)                  # Straighten document
AutoEnhancer.auto_crop(image)                    # Crop to content
AutoEnhancer.remove_shadows(image)               # Remove shadows
AutoEnhancer.auto_white_balance(image)           # Fix colors
AutoEnhancer.enhance_document(image)             # Full enhancement
```

### Algorithms
- **Deskew Detection**: 
  - Hough line transform for angle detection
  - Projection profile method
  - Average of multiple methods for accuracy
- **Crop Detection**: Contour-based content detection
- **Shadow Removal**: CLAHE on LAB color space

### GUI Integration
- **"Auto Deskew"** button - Straighten tilted documents
- **"Auto Crop"** button - Remove margins automatically
- **"Full Auto Enhancement"** button - Complete optimization pipeline

### Use Cases
- Fixing photos taken at angles
- Removing unwanted borders
- Correcting poor lighting conditions
- One-click professional results

---

## 3. Annotation Tools 📝

**Module**: `src/annotations.py`

### Features
- **Text Annotations**: Add custom text with background
- **Shapes**: Rectangles, circles, lines, arrows
- **Highlights**: Semi-transparent highlighting
- **Stamps**: Professional stamps (APPROVED, CONFIDENTIAL, etc.)
- **Date Stamps**: Current date/time stamps
- **Freehand Drawing**: Draw custom shapes
- **Persistent Annotations**: Save and reapply annotations

### Available Annotations
1. **Text** - Custom text with optional background
2. **Rectangle** - Boxes for emphasis (solid or outline)
3. **Circle** - Circular highlights (solid or outline)
4. **Arrow** - Directional arrows with customizable tips
5. **Highlight** - Semi-transparent overlays
6. **Line** - Straight or dashed lines
7. **Stamp** - Professional stamps:
   - APPROVED
   - REJECTED
   - CONFIDENTIAL
   - DRAFT
   - URGENT
   - COPY
   - VOID
   - RECEIVED
8. **Date Stamp** - Current date/time
9. **Freehand** - Custom drawings

### Key Functions
```python
AnnotationTools.add_text(image, text, position)        # Add text
AnnotationTools.add_rectangle(image, p1, p2)           # Add box
AnnotationTools.add_highlight(image, region)           # Highlight
AnnotationTools.add_stamp(image, stamp_type, pos)      # Add stamp
AnnotationTools.add_date_stamp(image, position)        # Add date
AnnotationTools.clear_annotations()                    # Clear all
```

### GUI Integration
- Dropdown menu to select annotation type
- **"Add Annotation"** button
- **"Clear Annotations"** button
- Simple positioning (center or predefined locations)

### Use Cases
- Marking up documents for review
- Adding approval stamps
- Highlighting important sections
- Adding notes and comments
- Creating document workflows

---

## 4. Document Comparison 🔍

**Module**: `src/document_compare.py`

### Features
- **Difference Detection**: Automatically find changes between versions
- **Side-by-Side View**: Compare documents visually
- **Similarity Scoring**: Calculate percentage similarity (using SSIM)
- **Diff Map**: Color-coded heat map of differences
- **Change Classification**: Identify additions, removals, and modifications
- **Detailed Reports**: Generate comparison statistics
- **Document Alignment**: Automatic alignment of different perspectives

### Key Functions
```python
DocumentComparator.compare_documents(doc1, doc2)        # Find differences
DocumentComparator.compare_side_by_side(doc1, doc2)     # Side-by-side view
DocumentComparator.create_diff_map(doc1, doc2)          # Heat map
DocumentComparator.calculate_similarity(doc1, doc2)     # Similarity %
DocumentComparator.generate_comparison_report()         # Text report
```

### Comparison Methods
1. **Pixel Difference**: Direct pixel-by-pixel comparison
2. **Structural Similarity (SSIM)**: Perceptual similarity metric
3. **Feature Matching**: ORB feature-based alignment
4. **Contour Detection**: Find changed regions

### GUI Integration
- **"Load Document to Compare"** button - Load second document
- **"Compare Documents"** button - Run comparison
- Shows side-by-side view with highlighted differences
- Displays similarity percentage
- Opens detailed report dialog

### Use Cases
- Version control for documents
- Detecting unauthorized changes
- Proofreading revisions
- Contract comparison
- Quality assurance

---

## Technical Implementation

### Code Quality
- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Error handling
- ✅ Modular design
- ✅ Clean separation of concerns

### Performance
- Efficient algorithms for real-time processing
- Parallel processing where applicable
- Optimized OpenCV operations
- Caching for repeated operations

### Integration
All features are fully integrated into the GUI with:
- Intuitive button placement
- Progress indicators
- Error messages
- Status updates
- Keyboard shortcuts where appropriate

---

## Installation & Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### OCR Setup (Optional but Recommended)

**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

---

## Usage Examples

### Extract Text
```python
from src.ocr_engine import OCREngine

ocr = OCREngine()
result = ocr.extract_text(scanned_image)
print(result.get_clean_text())
print(f"Confidence: {result.confidence}%")
```

### Auto Enhance Document
```python
from src.auto_enhance import AutoEnhancer

enhancer = AutoEnhancer()
enhanced = enhancer.enhance_document(
    image, 
    deskew=True, 
    crop=True, 
    white_balance=True
)
```

### Add Annotations
```python
from src.annotations import AnnotationTools

annotator = AnnotationTools()
annotated = annotator.add_text(image, "DRAFT", (50, 50))
annotated = annotator.add_stamp(annotated, "confidential", (200, 200))
```

### Compare Documents
```python
from src.document_compare import DocumentComparator

comparator = DocumentComparator()
comparison, diffs = comparator.compare_documents(doc1, doc2)
similarity = comparator.calculate_similarity(doc1, doc2)
print(f"Similarity: {similarity:.1f}%")
print(f"Differences found: {len(diffs)}")
```

---

## Files Added

### Core Modules
1. `src/ocr_engine.py` (337 lines) - OCR functionality
2. `src/auto_enhance.py` (408 lines) - Auto enhancement
3. `src/annotations.py` (588 lines) - Annotation tools
4. `src/document_compare.py` (445 lines) - Document comparison

### Updates
- `gui/main_window.py` - Added UI controls and integration
- `requirements.txt` - Added pytesseract dependency
- `README.md` - Updated documentation

### Total Lines Added
**~2,000+ lines of new functionality**

---

## Future Enhancements

### Potential Additions
- [ ] Custom annotation colors
- [ ] Interactive annotation placement (click to position)
- [ ] Save/load annotation sets
- [ ] Batch OCR processing
- [ ] OCR language selection in GUI
- [ ] Advanced comparison algorithms
- [ ] Version history tracking
- [ ] Annotation templates
- [ ] Export comparison reports to PDF
- [ ] Cloud OCR integration

---

## Credits

Developed for the doc-scanner project
GitHub: https://github.com/adbeka/doc-scanner
Date: January 2026

---

## License

Same as the main project (see LICENSE file)
