"""Image filters for document processing and enhancement"""

import cv2
import numpy as np
from typing import Optional, Tuple


class ImageFilters:
    """Collection of image filters for document processing"""
    
    @staticmethod
    def sepia(image: np.ndarray) -> np.ndarray:
        """
        Apply sepia tone filter.
        
        Args:
            image: Input image (BGR)
            
        Returns:
            Sepia toned image
        """
        if len(image.shape) == 2:
            # Convert grayscale to BGR first
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Sepia transformation matrix
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        
        sepia = cv2.transform(image, kernel)
        sepia = np.clip(sepia, 0, 255)
        
        return sepia.astype(np.uint8)
    
    @staticmethod
    def invert(image: np.ndarray) -> np.ndarray:
        """
        Invert image colors.
        
        Args:
            image: Input image
            
        Returns:
            Inverted image
        """
        return cv2.bitwise_not(image)
    
    @staticmethod
    def posterize(image: np.ndarray, levels: int = 4) -> np.ndarray:
        """
        Reduce the number of colors (posterize effect).
        
        Args:
            image: Input image
            levels: Number of color levels (2-8)
            
        Returns:
            Posterized image
        """
        levels = max(2, min(8, levels))
        indices = np.arange(0, 256)
        divider = np.linspace(0, 255, levels + 1)[1]
        quantiz = np.int32(np.linspace(0, 255, levels))
        color_levels = np.clip(np.int32(indices / divider), 0, levels - 1)
        palette = quantiz[color_levels]
        
        return palette[image]
    
    @staticmethod
    def sketch(image: np.ndarray) -> np.ndarray:
        """
        Apply pencil sketch filter.
        
        Args:
            image: Input image
            
        Returns:
            Sketch image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Invert the grayscale image
        inverted = 255 - gray
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        
        # Invert blurred image
        inverted_blur = 255 - blurred
        
        # Create sketch
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)
        
        return sketch
    
    @staticmethod
    def edge_enhance(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
        """
        Enhance edges in the image.
        
        Args:
            image: Input image
            strength: Edge enhancement strength (0.5-3.0)
            
        Returns:
            Edge enhanced image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            is_color = True
        else:
            gray = image.copy()
            is_color = False
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.GaussianBlur(edges, (3, 3), 0)
        
        # Combine with original
        if is_color:
            edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            result = cv2.addWeighted(image, 1.0, edges_color, strength, 0)
        else:
            result = cv2.addWeighted(image, 1.0, edges, strength, 0)
        
        return result
    
    @staticmethod
    def emboss(image: np.ndarray) -> np.ndarray:
        """
        Apply emboss filter.
        
        Args:
            image: Input image
            
        Returns:
            Embossed image
        """
        kernel = np.array([[-2, -1, 0],
                          [-1,  1, 1],
                          [ 0,  1, 2]])
        
        embossed = cv2.filter2D(image, -1, kernel)
        embossed = cv2.normalize(embossed, None, 0, 255, cv2.NORM_MINMAX)
        
        return embossed.astype(np.uint8)
    
    @staticmethod
    def oil_painting(image: np.ndarray, size: int = 5, dynRatio: int = 1) -> np.ndarray:
        """
        Apply oil painting filter.
        
        Args:
            image: Input image
            size: Size of the filter (3-9)
            dynRatio: Dynamic ratio (1-3)
            
        Returns:
            Oil painting styled image
        """
        # OpenCV's oil painting effect (if available)
        try:
            result = cv2.xphoto.oilPainting(image, size, dynRatio)
            return result
        except AttributeError:
            # Fallback: apply bilateral filter for similar effect
            result = cv2.bilateralFilter(image, 9, 75, 75)
            return result
    
    @staticmethod
    def vintage(image: np.ndarray) -> np.ndarray:
        """
        Apply vintage filter.
        
        Args:
            image: Input image
            
        Returns:
            Vintage styled image
        """
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Apply sepia tone
        sepia = ImageFilters.sepia(image)
        
        # Add vignette effect
        rows, cols = sepia.shape[:2]
        
        # Generate vignette mask
        X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 2)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 2)
        kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = kernel / kernel.max()
        
        # Apply vignette
        vintage = sepia.copy()
        for i in range(3):
            vintage[:, :, i] = vintage[:, :, i] * mask
        
        # Reduce saturation slightly
        hsv = cv2.cvtColor(vintage, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = hsv[:, :, 1] * 0.7
        vintage = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return vintage
    
    @staticmethod
    def warm_filter(image: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """
        Apply warm color filter.
        
        Args:
            image: Input image
            intensity: Warmth intensity (0.0-1.0)
            
        Returns:
            Warmed image
        """
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Increase red and decrease blue
        warm = image.copy().astype(np.float32)
        warm[:, :, 2] = np.clip(warm[:, :, 2] * (1 + intensity), 0, 255)  # Red
        warm[:, :, 1] = np.clip(warm[:, :, 1] * (1 + intensity * 0.5), 0, 255)  # Green
        warm[:, :, 0] = np.clip(warm[:, :, 0] * (1 - intensity * 0.3), 0, 255)  # Blue
        
        return warm.astype(np.uint8)
    
    @staticmethod
    def cool_filter(image: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """
        Apply cool color filter.
        
        Args:
            image: Input image
            intensity: Coolness intensity (0.0-1.0)
            
        Returns:
            Cooled image
        """
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        # Increase blue and decrease red
        cool = image.copy().astype(np.float32)
        cool[:, :, 0] = np.clip(cool[:, :, 0] * (1 + intensity), 0, 255)  # Blue
        cool[:, :, 1] = np.clip(cool[:, :, 1] * (1 + intensity * 0.3), 0, 255)  # Green
        cool[:, :, 2] = np.clip(cool[:, :, 2] * (1 - intensity * 0.3), 0, 255)  # Red
        
        return cool.astype(np.uint8)
    
    @staticmethod
    def blur_artistic(image: np.ndarray, sigma: int = 5) -> np.ndarray:
        """
        Apply artistic blur filter.
        
        Args:
            image: Input image
            sigma: Blur strength (1-15)
            
        Returns:
            Blurred image
        """
        sigma = max(1, min(15, sigma))
        ksize = (sigma * 2 + 1, sigma * 2 + 1)
        return cv2.GaussianBlur(image, ksize, 0)
    
    @staticmethod
    def motion_blur(image: np.ndarray, size: int = 15, angle: int = 45) -> np.ndarray:
        """
        Apply motion blur filter.
        
        Args:
            image: Input image
            size: Blur size (5-30)
            angle: Blur angle in degrees
            
        Returns:
            Motion blurred image
        """
        size = max(5, min(30, size))
        kernel = np.zeros((size, size))
        kernel[int((size - 1) / 2), :] = np.ones(size)
        kernel = kernel / size
        
        # Rotate kernel
        center = (size // 2, size // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        kernel = cv2.warpAffine(kernel, M, (size, size))
        
        return cv2.filter2D(image, -1, kernel)
    
    @staticmethod
    def pixelate(image: np.ndarray, pixel_size: int = 10) -> np.ndarray:
        """
        Apply pixelation effect.
        
        Args:
            image: Input image
            pixel_size: Size of pixels (5-50)
            
        Returns:
            Pixelated image
        """
        height, width = image.shape[:2]
        
        # Resize down
        small = cv2.resize(
            image,
            (width // pixel_size, height // pixel_size),
            interpolation=cv2.INTER_LINEAR
        )
        
        # Resize back up
        pixelated = cv2.resize(
            small,
            (width, height),
            interpolation=cv2.INTER_NEAREST
        )
        
        return pixelated
    
    @staticmethod
    def vignette(image: np.ndarray, intensity: float = 0.5) -> np.ndarray:
        """
        Apply vignette effect.
        
        Args:
            image: Input image
            intensity: Vignette intensity (0.0-1.0)
            
        Returns:
            Image with vignette
        """
        rows, cols = image.shape[:2]
        
        # Generate vignette mask
        X_resultant_kernel = cv2.getGaussianKernel(cols, cols / 2)
        Y_resultant_kernel = cv2.getGaussianKernel(rows, rows / 2)
        kernel = Y_resultant_kernel * X_resultant_kernel.T
        mask = kernel / kernel.max()
        
        # Apply intensity
        mask = 1 - (1 - mask) * intensity
        
        # Apply vignette
        result = image.copy()
        if len(image.shape) == 3:
            for i in range(3):
                result[:, :, i] = result[:, :, i] * mask
        else:
            result = result * mask
        
        return result.astype(np.uint8)
    
    @staticmethod
    def cartoon(image: np.ndarray) -> np.ndarray:
        """
        Apply cartoon filter.
        
        Args:
            image: Input image
            
        Returns:
            Cartoonized image
        """
        # Reduce colors using bilateral filter
        color = cv2.bilateralFilter(image, 9, 300, 300)
        
        # Convert to grayscale for edge detection
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply median blur
        gray = cv2.medianBlur(gray, 7)
        
        # Detect edges
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9, 2
        )
        
        # Combine color and edges
        if len(image.shape) == 3:
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            cartoon = cv2.bitwise_and(color, edges)
        else:
            cartoon = cv2.bitwise_and(color, edges)
        
        return cartoon
    
    @staticmethod
    def high_contrast_bw(image: np.ndarray, threshold: int = 128) -> np.ndarray:
        """
        Apply high contrast black and white filter.
        
        Args:
            image: Input image
            threshold: Threshold value (0-255)
            
        Returns:
            High contrast B&W image
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        
        return bw
    
    @staticmethod
    def document_scan_filter(image: np.ndarray) -> np.ndarray:
        """
        Specialized filter for document scanning.
        Combines multiple techniques for optimal document clarity.
        
        Args:
            image: Input image
            
        Returns:
            Processed document image
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, None, h=10)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            enhanced, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        
        return thresh


class FilterManager:
    """Manager for applying filters to images"""
    
    FILTER_FUNCTIONS = {
        'sepia': ImageFilters.sepia,
        'invert': ImageFilters.invert,
        'sketch': ImageFilters.sketch,
        'edge_enhance': ImageFilters.edge_enhance,
        'emboss': ImageFilters.emboss,
        'vintage': ImageFilters.vintage,
        'warm': ImageFilters.warm_filter,
        'cool': ImageFilters.cool_filter,
        'cartoon': ImageFilters.cartoon,
        'vignette': ImageFilters.vignette,
        'posterize': ImageFilters.posterize,
        'blur': ImageFilters.blur_artistic,
        'motion_blur': ImageFilters.motion_blur,
        'pixelate': ImageFilters.pixelate,
        'high_contrast_bw': ImageFilters.high_contrast_bw,
        'document_scan': ImageFilters.document_scan_filter,
        'oil_painting': ImageFilters.oil_painting,
    }
    
    @classmethod
    def get_filter_names(cls) -> list:
        """
        Get list of available filter names.
        
        Returns:
            List of filter names
        """
        return list(cls.FILTER_FUNCTIONS.keys())
    
    @classmethod
    def apply_filter(cls, image: np.ndarray, filter_name: str, **kwargs) -> np.ndarray:
        """
        Apply a filter to an image.
        
        Args:
            image: Input image
            filter_name: Name of the filter to apply
            **kwargs: Additional filter parameters
            
        Returns:
            Filtered image
            
        Raises:
            ValueError: If filter not found
        """
        if filter_name not in cls.FILTER_FUNCTIONS:
            raise ValueError(f"Filter '{filter_name}' not found")
        
        filter_func = cls.FILTER_FUNCTIONS[filter_name]
        return filter_func(image, **kwargs)
    
    @classmethod
    def apply_multiple_filters(cls, image: np.ndarray, filters: list) -> np.ndarray:
        """
        Apply multiple filters in sequence.
        
        Args:
            image: Input image
            filters: List of tuples (filter_name, kwargs_dict)
            
        Returns:
            Filtered image
        """
        result = image.copy()
        for filter_name, kwargs in filters:
            result = cls.apply_filter(result, filter_name, **kwargs)
        return result
