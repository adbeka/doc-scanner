# Quick Start Guide

## Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python main.py
```

### Step 3: Scan Your First Document

1. **Load an image**: Click "Load Image" and select a photo of a document
2. **Scan**: Click "Scan Document" - the app will auto-detect and correct perspective
3. **Enhance**: Use the controls to adjust brightness, contrast, or apply B&W mode
4. **Save**: Click "Save Result" and choose your output format

## Example Usage

### Command Line Testing

You can also use the scanner programmatically:

```python
from src.scanner import DocumentScanner
from src.image_processor import ImageProcessor

# Initialize scanner
scanner = DocumentScanner()

# Load and scan an image
scanner.load_image("path/to/your/document.jpg")
result = scanner.scan_document()

# Apply enhancements
processor = ImageProcessor()
enhanced = processor.auto_enhance(result, mode='document')

# Save result
scanner.save_result("output/scanned_document.jpg", enhanced)
```

## Sample Workflow

### Scanning a Receipt
1. Take a photo of the receipt on a dark surface
2. Load the image in the app
3. Click "Scan Document"
4. Select "Black & White" mode
5. Adjust contrast if needed
6. Save as PDF

### Scanning a Form
1. Take a clear photo showing all four corners
2. Load and scan
3. Use "Auto Enhance" for best results
4. Select "Grayscale" to preserve form lines
5. Save as PNG for editing or PDF for archiving

## Tips

- **Better Detection**: Use good lighting and contrasting backgrounds
- **Clean Scans**: The "Auto Enhance" feature works great for most documents
- **Multiple Pages**: Scan each page separately, then use PDF tools to combine
- **Poor Results?**: Try adjusting brightness/contrast sliders manually

## Troubleshooting

**"Could not detect document"**
- Ensure all four corners are visible
- Use a contrasting background
- Improve lighting

**Blurry output**
- Use a higher resolution input image
- Try the sharpen feature (coming in Phase 2)

**App crashes on startup**
- Verify Python 3.8+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Next Steps

- Test with different document types
- Experiment with enhancement settings
- Check out the full documentation in README.md
- Report issues or request features on GitHub

---

Enjoy scanning! 📄✨
