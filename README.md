# Document Scanner

A powerful Python-based document scanner application with a modern GUI. Automatically detects documents in images, applies perspective correction, and enhances the output for clear, professional-looking scans.

## Features

### Core Functionality
- ✅ **Automatic Document Detection** - Intelligently detects document edges in photos
- ✅ **Perspective Correction** - Transforms angled photos into flat, straight scans
- ✅ **Image Enhancement** - Multiple enhancement options including:
  - Black & White mode
  - Grayscale mode
  - Color preservation
  - Auto-enhancement
  - Brightness/Contrast adjustment
- ✅ **Document Templates** - 10 predefined templates for common document types:
  - Text Documents (A4, Letter)
  - Receipts
  - Business Cards
  - ID Cards & Passports
  - Invoices
  - Whiteboards
  - Book Pages
  - And more!
- ✅ **Image Filters** - 17+ professional filters including:
  - Artistic: Sepia, Vintage, Sketch, Cartoon, Oil Painting
  - Effects: Emboss, Posterize, Pixelate, Vignette
  - Color: Warm, Cool, Invert, High Contrast
  - Document: Specialized document scan filter
  - Blur: Artistic and Motion blur
- ✅ **Multiple Input Sources**
  - Load images from files
  - Camera capture (coming soon)
  - Batch processing
- ✅ **Multiple Output Formats** - Save as PDF, JPG, PNG, or TIFF
- ✅ **User-Friendly GUI** - Clean, intuitive interface built with PyQt5

### 🆕 Advanced Features

#### OCR (Text Recognition)
- **Extract Text** - Extract text from scanned documents using Tesseract OCR
- **Auto-Name Files** - Automatically name files based on extracted text content
- **Smart Metadata** - Extract dates, emails, phone numbers, and amounts
- **Search Documents** - Search for specific text within scanned documents
- **Multi-Language Support** - Supports multiple languages (eng, fra, spa, etc.)

#### Auto Enhancement
- **Auto Deskew** - Automatically straighten tilted documents
- **Auto Crop** - Intelligent cropping to remove borders
- **Shadow Removal** - Remove shadows and lighting variations
- **Auto White Balance** - Correct color temperature automatically
- **Full Enhancement Pipeline** - One-click complete document optimization

#### Annotation Tools
- **Add Text** - Add text annotations with custom positioning
- **Shapes** - Draw rectangles, circles, and arrows
- **Highlights** - Semi-transparent highlighting for emphasis
- **Stamps** - Professional stamps (APPROVED, CONFIDENTIAL, DRAFT, URGENT, etc.)
- **Date Stamps** - Add current date/time stamps
- **Signature Placeholders** - Add signature lines

#### Document Comparison
- **Side-by-Side View** - Compare two versions of a document
- **Difference Detection** - Automatically highlight changes
- **Similarity Scoring** - Calculate percentage similarity between documents
- **Detailed Reports** - Generate comparison reports with change statistics
- **Color-Coded Diff Maps** - Visual difference heat maps

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Install

1. Clone the repository:
```bash
git clone https://github.com/adbeka/doc-scanner.git
cd doc-scanner
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Basic Workflow

1. **Load an Image**
   - Click "Load Image" button
   - Select a photo containing a document
   - The image will appear in the preview

2. **Scan the Document**
   - Click "Scan Document" button
   - The app will automatically detect document edges
   - Perspective correction is applied
   - Result appears in the bottom panel

3. **Enhance (Optional)**
   - Choose color mode (B&W, Grayscale, or Color)
   - Adjust brightness and contrast sliders
   - Click "Auto Enhance" for automatic optimization
   - Apply document templates for specific document types
   - Add artistic or effect filters

4. **Apply Templates & Filters (Optional)**
   - **Templates**: Select a document template (Receipt, Business Card, etc.)
     - Click "Apply Template" to automatically optimize for that document type
   - **Filters**: Choose an image filter (Sepia, Vintage, etc.)
     - Click "Apply Filter" to add artistic or enhancement effects
   - Templates and filters can be combined for unique results

5. **Save the Result**
   - Click "Save Result"
   - Choose output format
   - Select destination folder

### 🆕 Advanced Workflow

#### Using OCR (Text Recognition)
1. After scanning a document, click **"Extract Text"**
2. View extracted text with confidence scores
3. Copy text to clipboard for use elsewhere
4. Use **"Auto-Name File"** to automatically name your scan based on content

#### Auto Enhancement
1. Click **"Auto Deskew"** to straighten tilted documents
2. Click **"Auto Crop"** to remove unnecessary margins
3. Or use **"Full Auto Enhancement"** for complete optimization:
   - Automatic deskewing
   - Intelligent cropping
   - White balance correction
   - Shadow removal
   - Contrast enhancement
   - Sharpening

#### Adding Annotations
1. Select annotation type from dropdown (Text, Rectangle, Highlight, etc.)
2. Click **"Add Annotation"** 
3. For text annotations, enter your text when prompted
4. Annotations appear at predefined positions
5. Use **"Clear Annotations"** to remove all annotations

#### Comparing Documents
1. After scanning your document, click **"Load Document to Compare"**
2. Select a second version of the document
3. Click **"Compare Documents"**
4. View side-by-side comparison with highlighted differences
5. See detailed similarity report with statistics

### Document Templates

Document templates are optimized presets for specific document types:

- **Text Document**: Perfect for letters, contracts, forms
- **Receipt**: High contrast for faded receipts
- **Business Card**: Preserves colors and logos
- **ID Card**: Optimized for ID cards with photos
- **Invoice**: Clean, crisp tables and text
- **Whiteboard**: Removes background, enhances markers
- **Book Page**: Optimal for scanning books
- **Magazine**: Preserves photos and colors
- **Passport**: Official document quality
- **Photo Document**: Mixed text and photos

See [TEMPLATES_AND_FILTERS.md](TEMPLATES_AND_FILTERS.md) for detailed documentation.

### Image Filters

Apply professional filters to your scans:

- **Artistic**: Sepia, Vintage, Sketch, Cartoon, Oil Painting
- **Effects**: Emboss, Posterize, Pixelate, Vignette, Edge Enhance
- **Color**: Warm, Cool, Invert, High Contrast B&W
- **Blur**: Artistic Blur, Motion Blur
- **Document**: Specialized document scan filter

Run the demo to see all filters in action:
```bash
python demo_features.py
```

### Tips for Best Results

- **Good Lighting**: Ensure the document is well-lit with minimal shadows
- **Contrast**: Place documents on a contrasting background
- **Angle**: Capture the entire document with all four corners visible
- **Distance**: Get close enough that the document fills most of the frame
- **Flatness**: Keep the document as flat as possible

## Project Structure

```
doc-scanner/
├── src/                      # Core scanning logic
│   ├── scanner.py           # Document detection and transformation
│   ├── image_processor.py   # Image enhancement functions
│   ├── templates.py         # Document templates
│   ├── filters.py           # Image filters
│   ├── batch_processor.py   # Batch processing
│   ├── ocr_engine.py        # OCR text extraction (NEW!)
│   ├── auto_enhance.py      # Auto enhancement tools (NEW!)
│   ├── annotations.py       # Annotation tools (NEW!)
│   ├── document_compare.py  # Document comparison (NEW!)
│   ├── utils.py             # Helper utilities
│   └── constants.py         # Configuration constants
├── gui/                     # GUI components
│   ├── main_window.py       # Main application window
│   ├── edge_adjuster.py     # Manual edge adjustment
│   └── page_thumbnails.py   # Multi-page thumbnails
├── tests/                   # Unit tests
│   ├── test_scanner.py
│   ├── test_templates.py
│   └── test_filters.py
├── data/
│   ├── sample_images/       # Test images
│   └── output/             # Scanned outputs
├── main.py                  # Application entry point
├── demo_features.py         # Demo for templates & filters
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── TEMPLATES_AND_FILTERS.md # Templates & filters documentation
└── README.md              # This file
```

## Configuration

Edit `config.yaml` to customize default settings:

```yaml
default:
  output_format: "pdf"
  color_mode: "bw"

processing:
  edge_detection:
    threshold1: 50
    threshold2: 150

output:
  pdf_quality: 95
  image_dpi: 300
```

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-qt

# Run tests
pytest tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_scanner.py

# Run with coverage
pytest --cov=src tests/
```

## Roadmap

### Phase 1: MVP ✅
- [x] Basic document detection
- [x] Perspective correction
- [x] Simple GUI
- [x] Image enhancement
- [x] Save functionality

### Phase 2: Advanced Features ✅
- [x] Batch processing
- [x] Manual corner adjustment
- [x] Advanced enhancement options
- [x] PDF multi-page support
- [x] Document templates
- [x] Image filters
- [x] Undo/Redo functionality

### Phase 3: Pro Features ✅
- [x] OCR text extraction
- [x] Auto-naming based on content
- [x] Auto deskew and crop
- [x] Annotation tools
- [x] Document comparison
- [ ] Camera integration with live preview
- [ ] Cloud storage integration
- [ ] Mobile app version
- [ ] Document organization system

## Technologies Used

- **Python 3.8+** - Core programming language
- **OpenCV** - Computer vision and image processing
- **NumPy** - Numerical operations
- **PyQt5** - GUI framework
- **scikit-image** - Image processing algorithms
- **Pillow** - Image handling
- **Tesseract OCR** - Text extraction (optional)
- **pytesseract** - Python wrapper for Tesseract

## OCR Setup (Optional)

For text extraction features, install Tesseract OCR:

### Windows
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location (C:\Program Files\Tesseract-OCR)
3. Add to PATH or set in code:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### macOS
```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
```

### Additional Languages
```bash
# For other languages, install language packs
# Example for French:
sudo apt-get install tesseract-ocr-fra  # Linux
brew install tesseract-lang             # macOS
```

After installing Tesseract, OCR features will be automatically enabled in the application.

## Troubleshooting

### Common Issues

**Issue**: "Could not detect document"
- **Solution**: Ensure good lighting and clear document edges. Try adjusting camera angle or using a contrasting background.

**Issue**: "OCR Not Available"
- **Solution**: Install Tesseract OCR (see OCR Setup section above) and pytesseract (`pip install pytesseract`)

**Issue**: Application won't start
- **Solution**: Verify all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Poor scan quality
- **Solution**: Use higher resolution images, ensure good lighting, and try the Auto Enhance feature.

### Getting Help

- Check the [Issues](https://github.com/adbeka/doc-scanner/issues) page
- Create a new issue with details about your problem
- Include error messages and screenshots if applicable

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV community for excellent documentation
- PyQt5 for the powerful GUI framework
- All contributors and users of this project

## Contact

Project Link: [https://github.com/adbeka/doc-scanner](https://github.com/adbeka/doc-scanner)

---

**Note**: This is an MVP (Minimum Viable Product) release. More features are being actively developed. Check the roadmap section for upcoming features!