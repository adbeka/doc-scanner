"""Image processing and enhancement functions"""

import cv2
import numpy as np
from typing import Optional, Tuple
from . import constants


class ImageProcessor:
    """Image enhancement and processing utilities"""
    
    @staticmethod
    def rotate_image(image: np.ndarray, angle: int) -> np.ndarray:
        """
        Rotate image by specified angle.
        
        Args:
            image: Input image
            angle: Rotation angle (90, 180, 270, or -90)
            
        Returns:
            Rotated image
        """
        if angle == 90 or angle == -270:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180 or angle == -180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270 or angle == -90:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            # For arbitrary angles, use getRotationMatrix2D
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(image, M, (w, h), 
                                 flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(255, 255, 255))
    
    @staticmethod
    def convert_to_bw(image: np.ndarray, threshold_method: str = 'adaptive') -> np.ndarray:
        """
        Convert image to black and white.
        
        Args:
            image: Input image
            threshold_method: 'adaptive' or 'otsu'
            
        Returns:
            Black and white image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        if threshold_method == 'adaptive':
            # Adaptive thresholding works better for varying lighting
            bw = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )
        else:
            # Otsu's thresholding
            _, bw = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        
        return bw
    
    @staticmethod
    def enhance_contrast(image: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
        """
        Enhance image contrast using CLAHE.
        
        Args:
            image: Input image
            clip_limit: Contrast limiting threshold
            
        Returns:
            Enhanced image
        """
        # Convert to LAB color space
        if len(image.shape) == 3:
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
        else:
            l = image.copy()
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels back
        if len(image.shape) == 3:
            enhanced = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        else:
            enhanced = l
        
        return enhanced
    
    @staticmethod
    def adjust_brightness_contrast(
        image: np.ndarray,
        brightness: int = 0,
        contrast: int = 0
    ) -> np.ndarray:
        """
        Adjust brightness and contrast.
        
        Args:
            image: Input image
            brightness: Brightness adjustment (-100 to 100)
            contrast: Contrast adjustment (-100 to 100)
            
        Returns:
            Adjusted image
        """
        # Normalize contrast value
        contrast_factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
        
        # Apply adjustments
        adjusted = cv2.convertScaleAbs(
            image,
            alpha=1 + contrast / 100.0,
            beta=brightness
        )
        
        return adjusted
    
    @staticmethod
    def remove_noise(image: np.ndarray, strength: int = 5) -> np.ndarray:
        """
        Remove noise from image.
        
        Args:
            image: Input image
            strength: Denoising strength (1-10)
            
        Returns:
            Denoised image
        """
        if len(image.shape) == 3:
            denoised = cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h=strength,
                hColor=strength,
                templateWindowSize=7,
                searchWindowSize=21
            )
        else:
            denoised = cv2.fastNlMeansDenoising(
                image,
                None,
                h=strength,
                templateWindowSize=7,
                searchWindowSize=21
            )
        
        return denoised
    
    @staticmethod
    def sharpen_image(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """
        Sharpen image.
        
        Args:
            image: Input image
            strength: Sharpening strength (0.5-2.0)
            
        Returns:
            Sharpened image
        """
        # Create sharpening kernel
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], dtype=np.float32)
        
        # Scale kernel by strength
        kernel = kernel * strength
        kernel[1, 1] = 1 + 4 * strength
        
        # Apply kernel
        sharpened = cv2.filter2D(image, -1, kernel)
        
        return sharpened
    
    @staticmethod
    def deskew_image(image: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Correct image skew/rotation.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (deskewed image, rotation angle)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        if lines is None:
            return image, 0.0
        
        # Calculate average angle
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            if -45 < angle < 45:
                angles.append(angle)
        
        if not angles:
            return image, 0.0
        
        median_angle = np.median(angles)
        
        # Rotate image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(
            image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated, median_angle
    
    @staticmethod
    def remove_shadows(image: np.ndarray) -> np.ndarray:
        """
        Remove shadows from image.
        
        Args:
            image: Input image (color)
            
        Returns:
            Shadow-removed image
        """
        if len(image.shape) != 3:
            return image
        
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply morphological operations to L channel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
        bg = cv2.morphologyEx(l, cv2.MORPH_CLOSE, kernel)
        
        # Calculate difference
        diff = cv2.subtract(bg, l)
        
        # Normalize
        norm = cv2.normalize(
            diff,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX
        )
        
        # Merge back
        lab = cv2.merge([norm, a, b])
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return result
    
    @staticmethod
    def auto_enhance(image: np.ndarray, mode: str = 'document') -> np.ndarray:
        """
        Automatically enhance image for document scanning.
        
        Args:
            image: Input image
            mode: Enhancement mode ('document', 'photo')
            
        Returns:
            Enhanced image
        """
        result = image.copy()
        
        if mode == 'document':
            # Enhance contrast
            result = ImageProcessor.enhance_contrast(result, clip_limit=2.0)
            
            # Convert to grayscale
            if len(result.shape) == 3:
                result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            
            # Apply adaptive thresholding
            result = ImageProcessor.convert_to_bw(result, 'adaptive')
            
            # Light denoising
            result = cv2.medianBlur(result, 3)
        
        else:  # photo mode
            # Remove noise
            result = ImageProcessor.remove_noise(result, strength=3)
            
            # Enhance contrast
            result = ImageProcessor.enhance_contrast(result, clip_limit=1.5)
            
            # Slight sharpening
            result = ImageProcessor.sharpen_image(result, strength=0.5)
        
        return result
    
    @staticmethod
    def resize_to_standard(
        image: np.ndarray,
        size: str = 'A4',
        dpi: int = 300
    ) -> np.ndarray:
        """
        Resize image to standard document size.
        
        Args:
            image: Input image
            size: Document size ('A4', 'LETTER', etc.)
            dpi: Resolution in DPI
            
        Returns:
            Resized image
        """
        if size in constants.DOCUMENT_SIZES:
            target_size = constants.DOCUMENT_SIZES[size]
            resized = cv2.resize(
                image,
                target_size,
                interpolation=cv2.INTER_CUBIC
            )
            return resized
        
        return image
