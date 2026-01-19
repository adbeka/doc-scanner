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
- ✅ **Multiple Input Sources**
  - Load images from files
  - Camera capture (coming soon)
  - Batch processing (coming soon)
- ✅ **Multiple Output Formats** - Save as PDF, JPG, PNG, or TIFF
- ✅ **User-Friendly GUI** - Clean, intuitive interface built with PyQt5

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

4. **Save the Result**
   - Click "Save Result"
   - Choose output format
   - Select destination folder

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
│   ├── utils.py             # Helper utilities
│   └── constants.py         # Configuration constants
├── gui/                     # GUI components
│   └── main_window.py       # Main application window
├── tests/                   # Unit tests
├── data/
│   ├── sample_images/       # Test images
│   └── output/             # Scanned outputs
├── main.py                  # Application entry point
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
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

### Phase 2: Advanced Features 🚧
- [ ] Camera integration with live preview
- [ ] Batch processing
- [ ] Manual corner adjustment
- [ ] Advanced enhancement options
- [ ] PDF multi-page support

### Phase 3: Pro Features 🔮
- [ ] OCR text extraction
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

## Troubleshooting

### Common Issues

**Issue**: "Could not detect document"
- **Solution**: Ensure good lighting and clear document edges. Try adjusting camera angle or using a contrasting background.

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