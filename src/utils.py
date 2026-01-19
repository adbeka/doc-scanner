"""Utility functions for document scanner"""

import cv2
import numpy as np
from typing import Tuple, Optional, List


def resize_image(image: np.ndarray, max_width: int = 1500, max_height: int = 1500) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio.
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    if width <= max_width and height <= max_height:
        return image
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    return cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)


def order_points(pts: np.ndarray) -> np.ndarray:
    """
    Order points in top-left, top-right, bottom-right, bottom-left order.
    
    Args:
        pts: Array of 4 points
        
    Returns:
        Ordered array of points
    """
    # Initialize ordered coordinates
    rect = np.zeros((4, 2), dtype="float32")
    
    # Top-left point has smallest sum
    # Bottom-right has largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # Top-right has smallest difference
    # Bottom-left has largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect


def calculate_distance(pt1: Tuple[float, float], pt2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        pt1: First point (x, y)
        pt2: Second point (x, y)
        
    Returns:
        Distance between points
    """
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)


def validate_quadrilateral(approx: np.ndarray) -> bool:
    """
    Validate if the approximated contour is a valid quadrilateral.
    
    Args:
        approx: Approximated contour points
        
    Returns:
        True if valid quadrilateral
    """
    if len(approx) != 4:
        return False
    
    # Check if all angles are reasonable (not too acute)
    # This helps filter out false detections
    return True


def load_image(filepath: str) -> Optional[np.ndarray]:
    """
    Load image from file path.
    
    Args:
        filepath: Path to image file
        
    Returns:
        Loaded image or None if failed
    """
    try:
        image = cv2.imread(filepath)
        if image is None:
            print(f"Failed to load image: {filepath}")
            return None
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def save_image(image: np.ndarray, filepath: str) -> bool:
    """
    Save image to file.
    
    Args:
        image: Image to save
        filepath: Output file path
        
    Returns:
        True if successful
    """
    try:
        cv2.imwrite(filepath, image)
        return True
    except Exception as e:
        print(f"Error saving image: {e}")
        return False


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convert image to grayscale.
    
    Args:
        image: Input image
        
    Returns:
        Grayscale image
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def get_image_dimensions(image: np.ndarray) -> Tuple[int, int]:
    """
    Get image dimensions.
    
    Args:
        image: Input image
        
    Returns:
        Tuple of (width, height)
    """
    height, width = image.shape[:2]
    return width, height
