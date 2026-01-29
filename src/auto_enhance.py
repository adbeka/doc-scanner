"""
Auto Enhancement Module
Automatic cropping, deskewing, and image enhancement
"""

import cv2
import numpy as np
from typing import Tuple, Optional
from scipy import ndimage


class AutoEnhancer:
    """Automatic image enhancement and correction"""
    
    def __init__(self):
        """Initialize auto enhancer"""
        pass
    
    def auto_crop(self, image: np.ndarray, padding: int = 10) -> np.ndarray:
        """
        Automatically crop image to remove borders and unnecessary margins
        
        Args:
            image: Input image
            padding: Padding to add around cropped region
            
        Returns:
            Cropped image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Threshold to find content
        _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return image
        
        # Find bounding box of all contours
        x_min, y_min = image.shape[1], image.shape[0]
        x_max, y_max = 0, 0
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)
        
        # Add padding
        h, w = image.shape[:2]
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)
        
        # Crop
        cropped = image[y_min:y_max, x_min:x_max]
        
        return cropped if cropped.size > 0 else image
    
    def auto_deskew(self, image: np.ndarray, max_angle: float = 10.0) -> Tuple[np.ndarray, float]:
        """
        Automatically detect and correct skew angle
        
        Args:
            image: Input image
            max_angle: Maximum expected skew angle in degrees
            
        Returns:
            Tuple of (deskewed image, detected angle)
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Detect angle using multiple methods and average
        angle1 = self._detect_angle_hough(gray)
        angle2 = self._detect_angle_projection(gray)
        
        # Average the angles
        angles = [a for a in [angle1, angle2] if a is not None]
        if not angles:
            return image, 0.0
        
        angle = np.mean(angles)
        
        # Limit to max angle
        if abs(angle) > max_angle:
            angle = max_angle if angle > 0 else -max_angle
        
        # Rotate image
        if abs(angle) > 0.1:  # Only rotate if angle is significant
            deskewed = self._rotate_image(image, angle)
            return deskewed, angle
        
        return image, 0.0
    
    def _detect_angle_hough(self, gray: np.ndarray) -> Optional[float]:
        """Detect skew angle using Hough line transform"""
        # Edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect lines
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)
        
        if lines is None:
            return None
        
        # Calculate angles
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            # Only consider nearly horizontal lines
            if -45 < angle < 45:
                angles.append(angle)
        
        if not angles:
            return None
        
        # Return median angle
        return np.median(angles)
    
    def _detect_angle_projection(self, gray: np.ndarray) -> Optional[float]:
        """Detect skew angle using projection profile"""
        # Threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        binary = 255 - binary  # Invert
        
        # Try different angles
        angles = np.arange(-5, 5, 0.5)
        scores = []
        
        for angle in angles:
            rotated = ndimage.rotate(binary, angle, reshape=False)
            
            # Calculate horizontal projection
            projection = np.sum(rotated, axis=1)
            
            # Score is variance of projection (higher = better alignment)
            score = np.var(projection)
            scores.append(score)
        
        # Find angle with maximum score
        best_idx = np.argmax(scores)
        return angles[best_idx]
    
    def _rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """Rotate image by given angle"""
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Calculate new bounding dimensions
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        
        # Adjust rotation matrix for new center
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        
        # Rotate with white background
        if len(image.shape) == 3:
            rotated = cv2.warpAffine(image, M, (new_w, new_h), 
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(255, 255, 255))
        else:
            rotated = cv2.warpAffine(image, M, (new_w, new_h),
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=255)
        
        return rotated
    
    def auto_straighten(self, image: np.ndarray) -> np.ndarray:
        """
        Automatically straighten document (crop + deskew)
        
        Args:
            image: Input image
            
        Returns:
            Straightened and cropped image
        """
        # First deskew
        deskewed, angle = self.auto_deskew(image)
        
        # Then crop
        cropped = self.auto_crop(deskewed)
        
        return cropped
    
    def remove_shadows(self, image: np.ndarray) -> np.ndarray:
        """
        Remove shadows from image
        
        Args:
            image: Input image (BGR)
            
        Returns:
            Image with reduced shadows
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels
        lab = cv2.merge([l, a, b])
        
        # Convert back to BGR
        result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return result
    
    def auto_white_balance(self, image: np.ndarray) -> np.ndarray:
        """
        Automatically adjust white balance
        
        Args:
            image: Input image (BGR)
            
        Returns:
            White balanced image
        """
        # Calculate average for each channel
        avg = [np.mean(image[:, :, i]) for i in range(3)]
        
        # Calculate gain for each channel
        avg_gray = np.mean(avg)
        gain = [avg_gray / a for a in avg]
        
        # Apply gain
        result = image.copy().astype(np.float32)
        for i in range(3):
            result[:, :, i] = np.clip(result[:, :, i] * gain[i], 0, 255)
        
        return result.astype(np.uint8)
    
    def auto_contrast(self, image: np.ndarray, clip_percent: float = 1.0) -> np.ndarray:
        """
        Automatically adjust contrast
        
        Args:
            image: Input image
            clip_percent: Percentage of pixels to clip at extremes
            
        Returns:
            Contrast-adjusted image
        """
        if len(image.shape) == 3:
            # Process each channel
            result = np.zeros_like(image)
            for i in range(3):
                result[:, :, i] = self._auto_contrast_channel(image[:, :, i], clip_percent)
            return result
        else:
            return self._auto_contrast_channel(image, clip_percent)
    
    def _auto_contrast_channel(self, channel: np.ndarray, clip_percent: float) -> np.ndarray:
        """Auto contrast for single channel"""
        # Calculate histogram
        hist, bins = np.histogram(channel.flatten(), 256, [0, 256])
        
        # Calculate cumulative distribution
        cdf = hist.cumsum()
        cdf_normalized = cdf / cdf[-1]
        
        # Find clip values
        clip_low = clip_percent / 100.0
        clip_high = 1.0 - clip_percent / 100.0
        
        low_val = np.searchsorted(cdf_normalized, clip_low)
        high_val = np.searchsorted(cdf_normalized, clip_high)
        
        # Stretch histogram
        if high_val > low_val:
            result = np.clip((channel.astype(np.float32) - low_val) * (255.0 / (high_val - low_val)), 0, 255)
            return result.astype(np.uint8)
        
        return channel
    
    def auto_sharpen(self, image: np.ndarray, amount: float = 1.0) -> np.ndarray:
        """
        Automatically sharpen image
        
        Args:
            image: Input image
            amount: Sharpening amount (0.0 to 2.0)
            
        Returns:
            Sharpened image
        """
        # Create sharpening kernel
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]]) * amount / 9.0
        kernel[1, 1] = 1 + (8 * amount / 9.0)
        
        # Apply kernel
        sharpened = cv2.filter2D(image, -1, kernel)
        
        return sharpened
    
    def enhance_document(self, image: np.ndarray, 
                        deskew: bool = True,
                        crop: bool = True,
                        white_balance: bool = True,
                        remove_shadow: bool = True,
                        auto_contrast: bool = True,
                        sharpen: bool = True) -> np.ndarray:
        """
        Apply full automatic enhancement pipeline
        
        Args:
            image: Input image
            deskew: Apply deskewing
            crop: Apply auto-cropping
            white_balance: Apply white balance
            remove_shadow: Remove shadows
            auto_contrast: Apply auto contrast
            sharpen: Apply sharpening
            
        Returns:
            Enhanced image
        """
        result = image.copy()
        
        # Deskew first
        if deskew:
            result, _ = self.auto_deskew(result)
        
        # Crop
        if crop:
            result = self.auto_crop(result)
        
        # Color corrections
        if len(result.shape) == 3:
            if white_balance:
                result = self.auto_white_balance(result)
            
            if remove_shadow:
                result = self.remove_shadows(result)
        
        # Contrast
        if auto_contrast:
            result = self.auto_contrast(result)
        
        # Sharpen
        if sharpen:
            result = self.auto_sharpen(result, amount=0.5)
        
        return result
