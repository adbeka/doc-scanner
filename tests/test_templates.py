"""Tests for document templates"""

import unittest
import numpy as np
import cv2
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.templates import TemplateManager, DocumentTemplate


class TestDocumentTemplates(unittest.TestCase):
    """Test document template functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test image (white image with some noise)
        self.test_image = np.ones((500, 500, 3), dtype=np.uint8) * 255
        # Add some random noise
        noise = np.random.randint(0, 50, (500, 500, 3), dtype=np.uint8)
        self.test_image = cv2.subtract(self.test_image, noise)
    
    def test_get_template_names(self):
        """Test getting available template names"""
        names = TemplateManager.get_template_names()
        self.assertIsInstance(names, list)
        self.assertGreater(len(names), 0)
        self.assertIn('receipt', names)
        self.assertIn('business_card', names)
        self.assertIn('id_card', names)
        self.assertIn('text_document', names)
    
    def test_get_template(self):
        """Test retrieving a template"""
        template = TemplateManager.get_template('receipt')
        self.assertIsInstance(template, DocumentTemplate)
        self.assertEqual(template.name, 'Receipt')
    
    def test_get_invalid_template(self):
        """Test retrieving an invalid template raises error"""
        with self.assertRaises(ValueError):
            TemplateManager.get_template('nonexistent_template')
    
    def test_apply_template_receipt(self):
        """Test applying receipt template"""
        result = TemplateManager.apply_template(self.test_image, 'receipt')
        self.assertIsInstance(result, np.ndarray)
        # Receipt should be B&W
        self.assertEqual(len(result.shape), 2)
        # Should be resized to receipt dimensions
        self.assertEqual(result.shape, (1200, 800))
    
    def test_apply_template_business_card(self):
        """Test applying business card template"""
        result = TemplateManager.apply_template(self.test_image, 'business_card')
        self.assertIsInstance(result, np.ndarray)
        # Business card should be in color
        self.assertEqual(len(result.shape), 3)
        # Should be resized to business card dimensions
        self.assertEqual(result.shape, (600, 1050, 3))
    
    def test_apply_template_text_document(self):
        """Test applying text document template"""
        result = TemplateManager.apply_template(self.test_image, 'text_document')
        self.assertIsInstance(result, np.ndarray)
        # Text document should be B&W
        self.assertEqual(len(result.shape), 2)
    
    def test_apply_template_whiteboard(self):
        """Test applying whiteboard template"""
        result = TemplateManager.apply_template(self.test_image, 'whiteboard')
        self.assertIsInstance(result, np.ndarray)
        # Whiteboard should be B&W
        self.assertEqual(len(result.shape), 2)
    
    def test_create_custom_template(self):
        """Test creating a custom template"""
        custom_template = TemplateManager.create_custom_template(
            name='custom_doc',
            size=(1000, 1000),
            settings={
                'color_mode': 'grayscale',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.0
            }
        )
        self.assertIsInstance(custom_template, DocumentTemplate)
        self.assertEqual(custom_template.name, 'custom_doc')
        self.assertEqual(custom_template.size, (1000, 1000))
    
    def test_apply_custom_template(self):
        """Test applying a custom template"""
        custom_template = TemplateManager.create_custom_template(
            name='test_template',
            size=(400, 400),
            settings={
                'color_mode': 'color',
                'resize': True,
                'brightness': 10
            }
        )
        result = custom_template.apply(self.test_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[:2], (400, 400))
    
    def test_template_settings(self):
        """Test that template settings are properly stored"""
        template = TemplateManager.get_template('invoice')
        self.assertIsInstance(template.settings, dict)
        self.assertIn('color_mode', template.settings)
        self.assertIn('enhance_contrast', template.settings)


if __name__ == '__main__':
    unittest.main()
