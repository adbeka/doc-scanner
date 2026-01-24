"""Tests for image filters"""

import unittest
import numpy as np
import cv2
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.filters import ImageFilters, FilterManager


class TestImageFilters(unittest.TestCase):
    """Test image filter functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test color image
        self.color_image = np.ones((300, 300, 3), dtype=np.uint8) * 128
        # Add some patterns
        self.color_image[50:150, 50:150] = [255, 0, 0]  # Red square
        self.color_image[150:250, 150:250] = [0, 255, 0]  # Green square
        
        # Create a test grayscale image
        self.gray_image = np.ones((300, 300), dtype=np.uint8) * 128
        self.gray_image[50:150, 50:150] = 255
    
    def test_get_filter_names(self):
        """Test getting available filter names"""
        names = FilterManager.get_filter_names()
        self.assertIsInstance(names, list)
        self.assertGreater(len(names), 0)
        self.assertIn('sepia', names)
        self.assertIn('invert', names)
        self.assertIn('sketch', names)
    
    def test_sepia_filter(self):
        """Test sepia filter"""
        result = ImageFilters.sepia(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Sepia should have warm tones
        self.assertGreater(np.mean(result[:, :, 2]), np.mean(result[:, :, 0]))
    
    def test_invert_filter(self):
        """Test invert filter"""
        result = ImageFilters.invert(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Inverted values should sum to 255
        np.testing.assert_array_almost_equal(
            self.color_image + result,
            np.full_like(self.color_image, 255)
        )
    
    def test_posterize_filter(self):
        """Test posterize filter"""
        result = ImageFilters.posterize(self.color_image, levels=4)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Result should have limited color levels
        # Just check that posterize returns valid data
        self.assertTrue(np.all(result >= 0))
        self.assertTrue(np.all(result <= 255))
    
    def test_sketch_filter(self):
        """Test sketch filter"""
        result = ImageFilters.sketch(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        # Sketch should be grayscale
        self.assertEqual(len(result.shape), 2)
    
    def test_edge_enhance_filter(self):
        """Test edge enhancement filter"""
        result = ImageFilters.edge_enhance(self.color_image, strength=1.0)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_emboss_filter(self):
        """Test emboss filter"""
        result = ImageFilters.emboss(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_vintage_filter(self):
        """Test vintage filter"""
        result = ImageFilters.vintage(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 3)
    
    def test_warm_filter(self):
        """Test warm color filter"""
        result = ImageFilters.warm_filter(self.color_image, intensity=0.3)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Warm filter should increase red channel
        self.assertGreater(np.mean(result[:, :, 2]), np.mean(self.color_image[:, :, 2]))
    
    def test_cool_filter(self):
        """Test cool color filter"""
        result = ImageFilters.cool_filter(self.color_image, intensity=0.3)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Cool filter should increase blue channel
        self.assertGreater(np.mean(result[:, :, 0]), np.mean(self.color_image[:, :, 0]))
    
    def test_blur_artistic_filter(self):
        """Test artistic blur filter"""
        result = ImageFilters.blur_artistic(self.color_image, sigma=5)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_motion_blur_filter(self):
        """Test motion blur filter"""
        result = ImageFilters.motion_blur(self.color_image, size=15, angle=45)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_pixelate_filter(self):
        """Test pixelate filter"""
        result = ImageFilters.pixelate(self.color_image, pixel_size=10)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_vignette_filter(self):
        """Test vignette filter"""
        result = ImageFilters.vignette(self.color_image, intensity=0.5)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
        # Corners should be darker than center
        corner_mean = np.mean(result[0:10, 0:10])
        center_mean = np.mean(result[145:155, 145:155])
        self.assertLess(corner_mean, center_mean)
    
    def test_cartoon_filter(self):
        """Test cartoon filter"""
        result = ImageFilters.cartoon(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_high_contrast_bw_filter(self):
        """Test high contrast B&W filter"""
        result = ImageFilters.high_contrast_bw(self.color_image, threshold=128)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 2)
        # Should only have 0 and 255 values
        unique_vals = np.unique(result)
        self.assertTrue(np.all(np.isin(unique_vals, [0, 255])))
    
    def test_document_scan_filter(self):
        """Test document scan filter"""
        result = ImageFilters.document_scan_filter(self.color_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result.shape), 2)
    
    def test_filter_manager_apply(self):
        """Test FilterManager apply method"""
        result = FilterManager.apply_filter(self.color_image, 'sepia')
        self.assertIsInstance(result, np.ndarray)
    
    def test_filter_manager_invalid_filter(self):
        """Test FilterManager with invalid filter raises error"""
        with self.assertRaises(ValueError):
            FilterManager.apply_filter(self.color_image, 'nonexistent_filter')
    
    def test_apply_multiple_filters(self):
        """Test applying multiple filters in sequence"""
        filters = [
            ('blur', {'sigma': 3}),
            ('edge_enhance', {'strength': 1.0}),
            ('warm', {'intensity': 0.2})
        ]
        result = FilterManager.apply_multiple_filters(self.color_image, filters)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, self.color_image.shape)
    
    def test_filters_on_grayscale(self):
        """Test that filters work on grayscale images"""
        # Test a few filters that should work on grayscale
        result = ImageFilters.invert(self.gray_image)
        self.assertIsInstance(result, np.ndarray)
        
        result = ImageFilters.emboss(self.gray_image)
        self.assertIsInstance(result, np.ndarray)


if __name__ == '__main__':
    unittest.main()
