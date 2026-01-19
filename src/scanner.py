"""Core document scanner implementation"""

import cv2
import numpy as np
from typing import Optional, Tuple, List
from . import constants
from . import utils


class DocumentScanner:
    """Core document scanner class for detecting and processing documents"""
    
    def __init__(self):
        """Initialize the document scanner"""
        self.original_image = None
        self.processed_image = None
        self.detected_corners = None
        
    def load_image(self, filepath: str) -> bool:
        """
        Load an image from file path.
        
        Args:
            filepath: Path to image file
            
        Returns:
            True if successful
        """
        self.original_image = utils.load_image(filepath)
        return self.original_image is not None
    
    def set_image(self, image: np.ndarray):
        """
        Set image directly (useful for camera capture).
        
        Args:
            image: Input image array
        """
        self.original_image = image.copy()
    
    def preprocess_image(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Preprocess image for edge detection.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (resized, grayscale, edges)
        """
        # Resize image for faster processing
        resized = utils.resize_image(image, 1500, 1500)
        
        # Convert to grayscale
        gray = utils.convert_to_grayscale(resized)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, constants.DEFAULT_BLUR_KERNEL, 0)
        
        # Perform edge detection
        edges = cv2.Canny(
            blurred,
            constants.DEFAULT_CANNY_THRESHOLD1,
            constants.DEFAULT_CANNY_THRESHOLD2
        )
        
        return resized, gray, edges
    
    def detect_document(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Detect document in the image.
        
        Args:
            image: Input image
            
        Returns:
            Array of 4 corner points or None if not found
        """
        # Preprocess image
        resized, gray, edges = self.preprocess_image(image)
        
        # Find contours
        contours, _ = cv2.findContours(
            edges.copy(),
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Find the largest contour with 4 points
        for contour in contours[:10]:  # Check top 10 largest
            # Calculate perimeter and approximate polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(
                contour,
                constants.APPROX_EPSILON_FACTOR * perimeter,
                True
            )
            
            # If we found a quadrilateral with sufficient area
            if len(approx) == 4:
                area = cv2.contourArea(approx)
                if area > constants.MIN_DOCUMENT_AREA:
                    # Scale points back to original image size
                    scale_x = image.shape[1] / resized.shape[1]
                    scale_y = image.shape[0] / resized.shape[0]
                    
                    corners = approx.reshape(4, 2).astype(np.float32)
                    corners[:, 0] *= scale_x
                    corners[:, 1] *= scale_y
                    
                    self.detected_corners = corners
                    return corners
        
        # No document found
        return None
    
    def apply_perspective_transform(
        self,
        image: np.ndarray,
        corners: np.ndarray,
        output_size: Optional[Tuple[int, int]] = None
    ) -> np.ndarray:
        """
        Apply perspective transformation to get top-down view.
        
        Args:
            image: Input image
            corners: Four corner points
            output_size: Desired output size (width, height)
            
        Returns:
            Warped image
        """
        # Order the corners
        rect = utils.order_points(corners)
        (tl, tr, br, bl) = rect
        
        # Calculate width and height of the document
        width_a = utils.calculate_distance((br[0], br[1]), (bl[0], bl[1]))
        width_b = utils.calculate_distance((tr[0], tr[1]), (tl[0], tl[1]))
        max_width = max(int(width_a), int(width_b))
        
        height_a = utils.calculate_distance((tr[0], tr[1]), (br[0], br[1]))
        height_b = utils.calculate_distance((tl[0], tl[1]), (bl[0], bl[1]))
        max_height = max(int(height_a), int(height_b))
        
        # Use provided output size or calculated dimensions
        if output_size:
            max_width, max_height = output_size
        
        # Define destination points for the perspective transform
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")
        
        # Calculate perspective transform matrix
        M = cv2.getPerspectiveTransform(rect, dst)
        
        # Apply perspective transformation
        warped = cv2.warpPerspective(image, M, (max_width, max_height))
        
        return warped
    
    def scan_document(
        self,
        image: Optional[np.ndarray] = None,
        manual_corners: Optional[np.ndarray] = None
    ) -> Optional[np.ndarray]:
        """
        Complete scan workflow: detect and transform document.
        
        Args:
            image: Input image (uses self.original_image if None)
            manual_corners: Manually specified corners (skips detection)
            
        Returns:
            Scanned document image or None if failed
        """
        if image is None:
            image = self.original_image
            
        if image is None:
            print("No image available")
            return None
        
        # Use manual corners or detect automatically
        if manual_corners is not None:
            corners = manual_corners
        else:
            corners = self.detect_document(image)
            
        if corners is None:
            print("Could not detect document")
            return None
        
        # Apply perspective transform
        scanned = self.apply_perspective_transform(image, corners)
        self.processed_image = scanned
        
        return scanned
    
    def get_preview_with_detection(self, image: np.ndarray) -> np.ndarray:
        """
        Get preview image with detected corners highlighted.
        
        Args:
            image: Input image
            
        Returns:
            Image with corners drawn
        """
        preview = image.copy()
        
        if self.detected_corners is not None:
            # Draw the detected quadrilateral
            corners_int = self.detected_corners.astype(np.int32)
            cv2.drawContours(preview, [corners_int], -1, (0, 255, 0), 3)
            
            # Draw corner circles
            for point in corners_int:
                cv2.circle(preview, tuple(point), 10, (0, 0, 255), -1)
        
        return preview
    
    def save_result(self, filepath: str, image: Optional[np.ndarray] = None) -> bool:
        """
        Save processed image to file.
        
        Args:
            filepath: Output file path
            image: Image to save (uses self.processed_image if None)
            
        Returns:
            True if successful
        """
        if image is None:
            image = self.processed_image
            
        if image is None:
            print("No processed image available")
            return False
        
        return utils.save_image(image, filepath)
