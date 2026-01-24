"""Document templates and presets for common document types"""

import cv2
import numpy as np
from typing import Tuple, Dict, Any
from .image_processor import ImageProcessor


class DocumentTemplate:
    """Base class for document templates"""
    
    def __init__(self, name: str, size: Tuple[int, int], settings: Dict[str, Any]):
        """
        Initialize a document template.
        
        Args:
            name: Template name
            size: Target size (width, height) in pixels
            settings: Processing settings dictionary
        """
        self.name = name
        self.size = size
        self.settings = settings
    
    def apply(self, image: np.ndarray) -> np.ndarray:
        """
        Apply template processing to image.
        
        Args:
            image: Input image
            
        Returns:
            Processed image
        """
        result = image.copy()
        
        # Resize to template size
        if self.settings.get('resize', True):
            result = cv2.resize(result, self.size, interpolation=cv2.INTER_CUBIC)
        
        # Apply color mode
        color_mode = self.settings.get('color_mode', 'color')
        if color_mode == 'bw':
            result = ImageProcessor.convert_to_bw(
                result,
                threshold_method=self.settings.get('threshold_method', 'adaptive')
            )
        elif color_mode == 'grayscale':
            if len(result.shape) == 3:
                result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        # Apply contrast enhancement
        if self.settings.get('enhance_contrast', False):
            clip_limit = self.settings.get('contrast_clip_limit', 2.0)
            result = ImageProcessor.enhance_contrast(result, clip_limit=clip_limit)
        
        # Apply sharpening
        if self.settings.get('sharpen', False):
            strength = self.settings.get('sharpen_strength', 1.0)
            result = ImageProcessor.sharpen_image(result, strength=strength)
        
        # Apply denoising
        if self.settings.get('denoise', False):
            strength = self.settings.get('denoise_strength', 5)
            result = ImageProcessor.remove_noise(result, strength=strength)
        
        # Apply brightness/contrast adjustments
        brightness = self.settings.get('brightness', 0)
        contrast = self.settings.get('contrast', 0)
        if brightness != 0 or contrast != 0:
            result = ImageProcessor.adjust_brightness_contrast(
                result, brightness=brightness, contrast=contrast
            )
        
        return result


class TemplateManager:
    """Manager for document templates"""
    
    # Predefined templates
    TEMPLATES = {
        'receipt': DocumentTemplate(
            name='Receipt',
            size=(800, 1200),
            settings={
                'color_mode': 'bw',
                'threshold_method': 'adaptive',
                'enhance_contrast': True,
                'contrast_clip_limit': 3.0,
                'sharpen': True,
                'sharpen_strength': 1.2,
                'denoise': True,
                'denoise_strength': 3,
                'brightness': 10,
                'contrast': 15
            }
        ),
        'business_card': DocumentTemplate(
            name='Business Card',
            size=(1050, 600),
            settings={
                'color_mode': 'color',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.0,
                'sharpen': True,
                'sharpen_strength': 1.5,
                'denoise': True,
                'denoise_strength': 4,
                'brightness': 5,
                'contrast': 10
            }
        ),
        'id_card': DocumentTemplate(
            name='ID Card',
            size=(1280, 810),
            settings={
                'color_mode': 'color',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.5,
                'sharpen': True,
                'sharpen_strength': 1.3,
                'denoise': True,
                'denoise_strength': 5,
                'brightness': 0,
                'contrast': 10
            }
        ),
        'text_document': DocumentTemplate(
            name='Text Document',
            size=(2480, 3508),  # A4 at 300 DPI
            settings={
                'color_mode': 'bw',
                'threshold_method': 'adaptive',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.5,
                'sharpen': False,
                'denoise': True,
                'denoise_strength': 2,
                'brightness': 15,
                'contrast': 20
            }
        ),
        'photo_document': DocumentTemplate(
            name='Photo Document',
            size=(2480, 3508),  # A4 at 300 DPI
            settings={
                'color_mode': 'color',
                'enhance_contrast': True,
                'contrast_clip_limit': 1.5,
                'sharpen': True,
                'sharpen_strength': 0.8,
                'denoise': True,
                'denoise_strength': 4,
                'brightness': 0,
                'contrast': 5
            }
        ),
        'whiteboard': DocumentTemplate(
            name='Whiteboard',
            size=(1920, 1080),
            settings={
                'color_mode': 'bw',
                'threshold_method': 'adaptive',
                'enhance_contrast': True,
                'contrast_clip_limit': 3.5,
                'sharpen': True,
                'sharpen_strength': 1.5,
                'denoise': True,
                'denoise_strength': 6,
                'brightness': 20,
                'contrast': 30
            }
        ),
        'book_page': DocumentTemplate(
            name='Book Page',
            size=(1654, 2339),  # 5.5" x 8.5" at 300 DPI
            settings={
                'color_mode': 'bw',
                'threshold_method': 'adaptive',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.0,
                'sharpen': False,
                'denoise': True,
                'denoise_strength': 3,
                'brightness': 10,
                'contrast': 15
            }
        ),
        'invoice': DocumentTemplate(
            name='Invoice',
            size=(2480, 3508),  # A4 at 300 DPI
            settings={
                'color_mode': 'bw',
                'threshold_method': 'otsu',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.5,
                'sharpen': True,
                'sharpen_strength': 1.0,
                'denoise': True,
                'denoise_strength': 2,
                'brightness': 12,
                'contrast': 18
            }
        ),
        'magazine': DocumentTemplate(
            name='Magazine',
            size=(2550, 3300),  # Letter at 300 DPI
            settings={
                'color_mode': 'color',
                'enhance_contrast': True,
                'contrast_clip_limit': 1.8,
                'sharpen': True,
                'sharpen_strength': 1.0,
                'denoise': True,
                'denoise_strength': 3,
                'brightness': 0,
                'contrast': 8
            }
        ),
        'passport': DocumentTemplate(
            name='Passport',
            size=(1398, 1960),  # Standard passport size
            settings={
                'color_mode': 'color',
                'enhance_contrast': True,
                'contrast_clip_limit': 2.0,
                'sharpen': True,
                'sharpen_strength': 1.2,
                'denoise': True,
                'denoise_strength': 5,
                'brightness': 5,
                'contrast': 10
            }
        ),
    }
    
    @classmethod
    def get_template(cls, template_name: str) -> DocumentTemplate:
        """
        Get a template by name.
        
        Args:
            template_name: Name of the template
            
        Returns:
            DocumentTemplate instance
            
        Raises:
            ValueError: If template not found
        """
        if template_name not in cls.TEMPLATES:
            raise ValueError(f"Template '{template_name}' not found")
        return cls.TEMPLATES[template_name]
    
    @classmethod
    def get_template_names(cls) -> list:
        """
        Get list of available template names.
        
        Returns:
            List of template names
        """
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def apply_template(cls, image: np.ndarray, template_name: str) -> np.ndarray:
        """
        Apply a template to an image.
        
        Args:
            image: Input image
            template_name: Name of the template to apply
            
        Returns:
            Processed image
        """
        template = cls.get_template(template_name)
        return template.apply(image)
    
    @classmethod
    def create_custom_template(
        cls,
        name: str,
        size: Tuple[int, int],
        settings: Dict[str, Any]
    ) -> DocumentTemplate:
        """
        Create a custom template.
        
        Args:
            name: Template name
            size: Target size (width, height)
            settings: Processing settings
            
        Returns:
            New DocumentTemplate instance
        """
        return DocumentTemplate(name, size, settings)
