# Development Guide

## For Developers

This guide is for developers who want to contribute to or extend the Document Scanner application.

## Architecture Overview

### Core Components

1. **Scanner Module** (`src/scanner.py`)
   - Document detection algorithm
   - Perspective transformation
   - Main scanning workflow

2. **Image Processor** (`src/image_processor.py`)
   - Image enhancement functions
   - Color mode conversions
   - Noise reduction and sharpening

3. **Utilities** (`src/utils.py`)
   - Helper functions
   - Image loading/saving
   - Geometric calculations

4. **GUI** (`gui/main_window.py`)
   - PyQt5-based interface
   - Event handling
   - Threading for responsiveness

## Development Setup

### Prerequisites

- Python 3.8+
- pip and virtualenv
- Git
- IDE (VS Code, PyCharm recommended)

### Setting Up

```bash
# Clone repository
git clone https://github.com/adbeka/doc-scanner.git
cd doc-scanner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (including dev dependencies)
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/ -v

# Check code style
black src/ gui/ tests/
flake8 src/ gui/ tests/
```

## Project Structure

```
src/
  ├── scanner.py          - Core document detection & scanning
  ├── image_processor.py  - Image enhancement algorithms
  ├── utils.py           - Utility functions
  └── constants.py       - Configuration constants

gui/
  └── main_window.py     - Main application window

tests/
  └── test_scanner.py    - Unit tests
```

## Key Algorithms

### Document Detection

1. **Preprocessing**
   - Resize for performance
   - Convert to grayscale
   - Apply Gaussian blur
   - Edge detection (Canny)

2. **Contour Detection**
   - Find all contours
   - Sort by area (largest first)
   - Approximate polygons
   - Filter for quadrilaterals

3. **Validation**
   - Check for 4 corners
   - Verify minimum area
   - Validate aspect ratio

### Perspective Transformation

1. **Corner Ordering**
   - Order points: TL, TR, BR, BL
   - Use sum and difference of coordinates

2. **Dimension Calculation**
   - Calculate document width and height
   - Determine output dimensions

3. **Transformation**
   - Build perspective matrix
   - Apply warp transformation

## Adding New Features

### Example: Adding a New Enhancement Filter

```python
# In src/image_processor.py

@staticmethod
def your_new_filter(image: np.ndarray, parameter: float = 1.0) -> np.ndarray:
    """
    Your filter description.
    
    Args:
        image: Input image
        parameter: Filter parameter
        
    Returns:
        Filtered image
    """
    # Your implementation
    result = image.copy()
    # ... processing ...
    return result
```

### Example: Adding a GUI Control

```python
# In gui/main_window.py, in create_control_panel()

# Add a new button
self.btn_your_feature = QPushButton("Your Feature")
self.btn_your_feature.clicked.connect(self.your_feature_handler)
layout.addWidget(self.btn_your_feature)

# Add handler method
def your_feature_handler(self):
    """Handle your feature button click"""
    if self.scanned_image is None:
        return
    
    # Process image
    result = self.processor.your_new_filter(self.scanned_image)
    self.display_image(result, self.label_processed)
```

## Testing

### Writing Tests

```python
# In tests/test_scanner.py

def test_your_feature(self):
    """Test your new feature"""
    # Setup
    image = self.create_test_image()
    
    # Execute
    result = your_function(image)
    
    # Assert
    assert result is not None
    assert result.shape == expected_shape
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_scanner.py

# Run with coverage
pytest --cov=src --cov=gui tests/

# Run with verbose output
pytest -v
```

## Code Style

### Follow PEP 8

```bash
# Format code
black src/ gui/ tests/

# Check style
flake8 src/ gui/ tests/

# Type checking
mypy src/
```

### Docstring Format

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
```

## Performance Optimization

### Image Processing

- Use `numpy` operations instead of loops
- Downsample large images for preview
- Cache processed results
- Use threading for long operations

### GUI Responsiveness

- Use `QThread` for processing
- Implement progress indicators
- Update UI incrementally

## Debugging

### Common Issues

1. **Import Errors**
   - Check Python path
   - Verify virtual environment is activated

2. **OpenCV Issues**
   - Ensure opencv-python is installed
   - Check image format compatibility

3. **GUI Not Responding**
   - Use threading for heavy operations
   - Call `QApplication.processEvents()`

### Debugging Tools

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# OpenCV visualization
cv2.imshow("Debug", image)
cv2.waitKey(0)

# Print image info
print(f"Shape: {image.shape}, dtype: {image.dtype}")
print(f"Min: {image.min()}, Max: {image.max()}")
```

## Contributing

### Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure tests pass
6. Format code
7. Submit pull request

### Pull Request Guidelines

- Clear description of changes
- Include tests for new features
- Update documentation
- Follow existing code style
- One feature per PR

## Roadmap Implementation

### Phase 2 Features (Next)

- Camera integration with live preview
- Batch processing support
- Manual corner adjustment
- Advanced enhancement options

### Phase 3 Features (Future)

- OCR integration
- Multi-page PDF support
- Cloud storage integration
- Document organization

## Resources

### OpenCV
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Image Processing](https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html)

### PyQt5
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html)

### Computer Vision
- [Digital Image Processing](https://en.wikipedia.org/wiki/Digital_image_processing)
- [Document Scanning Techniques](https://www.sciencedirect.com/topics/computer-science/document-scanning)

## Contact

For questions or discussions:
- Open an issue on GitHub
- Join our discussions
- Email: your.email@example.com

---

Happy coding! 🚀
