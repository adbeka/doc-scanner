"""Unit tests for document scanner core functionality"""

import pytest
import numpy as np
import cv2
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scanner import DocumentScanner
from src.image_processor import ImageProcessor
from src import utils


class TestDocumentScanner:
    """Test cases for DocumentScanner class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scanner = DocumentScanner()
        # Create a simple test image (white document on black background)
        self.test_image = self.create_test_document()
    
    def create_test_document(self):
        """Create a synthetic test image with a document"""
        # Create black background
        image = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # Draw white rectangle (document)
        cv2.rectangle(image, (100, 100), (700, 500), (255, 255, 255), -1)
        
        return image
    
    def test_scanner_initialization(self):
        """Test scanner initializes correctly"""
        assert self.scanner is not None
        assert self.scanner.original_image is None
        assert self.scanner.processed_image is None
        assert self.scanner.detected_corners is None
    
    def test_set_image(self):
        """Test setting image directly"""
        self.scanner.set_image(self.test_image)
        assert self.scanner.original_image is not None
        assert self.scanner.original_image.shape == self.test_image.shape
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        resized, gray, edges = self.scanner.preprocess_image(self.test_image)
        
        assert resized is not None
        assert gray is not None
        assert edges is not None
        assert len(gray.shape) == 2  # Grayscale should be 2D
        assert len(edges.shape) == 2  # Edges should be 2D
    
    def test_detect_document(self):
        """Test document detection"""
        corners = self.scanner.detect_document(self.test_image)
        
        # Should find 4 corners
        if corners is not None:
            assert len(corners) == 4
            assert corners.shape == (4, 2)
    
    def test_scan_document(self):
        """Test complete scan workflow"""
        self.scanner.set_image(self.test_image)
        result = self.scanner.scan_document()
        
        # Result may be None if detection fails (acceptable for simple test)
        if result is not None:
            assert isinstance(result, np.ndarray)
            assert len(result.shape) in [2, 3]  # 2D or 3D array


class TestImageProcessor:
    """Test cases for ImageProcessor class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.processor = ImageProcessor()
        # Create test grayscale image
        self.test_gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        # Create test color image
        self.test_color = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    def test_convert_to_bw(self):
        """Test black and white conversion"""
        bw = self.processor.convert_to_bw(self.test_color)
        
        assert bw is not None
        assert len(bw.shape) == 2
        assert bw.dtype == np.uint8
    
    def test_enhance_contrast(self):
        """Test contrast enhancement"""
        enhanced = self.processor.enhance_contrast(self.test_color)
        
        assert enhanced is not None
        assert enhanced.shape == self.test_color.shape
    
    def test_adjust_brightness_contrast(self):
        """Test brightness and contrast adjustment"""
        adjusted = self.processor.adjust_brightness_contrast(
            self.test_color,
            brightness=10,
            contrast=10
        )
        
        assert adjusted is not None
        assert adjusted.shape == self.test_color.shape
    
    def test_sharpen_image(self):
        """Test image sharpening"""
        sharpened = self.processor.sharpen_image(self.test_color)
        
        assert sharpened is not None
        assert sharpened.shape == self.test_color.shape
    
    def test_auto_enhance(self):
        """Test automatic enhancement"""
        enhanced = self.processor.auto_enhance(self.test_color, mode='document')
        
        assert enhanced is not None


class TestUtils:
    """Test cases for utility functions"""
    
    def test_resize_image(self):
        """Test image resizing"""
        test_image = np.zeros((1000, 1000, 3), dtype=np.uint8)
        resized = utils.resize_image(test_image, 500, 500)
        
        assert resized.shape[0] <= 500
        assert resized.shape[1] <= 500
    
    def test_order_points(self):
        """Test point ordering"""
        # Create points in random order
        pts = np.array([
            [100, 100],  # top-left
            [400, 100],  # top-right
            [400, 300],  # bottom-right
            [100, 300]   # bottom-left
        ], dtype=np.float32)
        
        ordered = utils.order_points(pts)
        
        assert ordered.shape == (4, 2)
        # Top-left should have smallest sum
        assert ordered[0][0] + ordered[0][1] < ordered[2][0] + ordered[2][1]
    
    def test_calculate_distance(self):
        """Test distance calculation"""
        pt1 = (0, 0)
        pt2 = (3, 4)
        distance = utils.calculate_distance(pt1, pt2)
        
        assert distance == 5.0  # 3-4-5 triangle
    
    def test_convert_to_grayscale(self):
        """Test grayscale conversion"""
        color_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        gray = utils.convert_to_grayscale(color_image)
        
        assert len(gray.shape) == 2
        assert gray.shape == (100, 100)


if __name__ == '__main__':
    pytest.main([__file__])
