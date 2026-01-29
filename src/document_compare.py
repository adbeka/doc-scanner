"""
Document Comparison Module
Compare two versions of a document and highlight differences
"""

import cv2
import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class DifferenceType(Enum):
    """Types of differences"""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


@dataclass
class Difference:
    """Container for difference data"""
    type: DifferenceType
    region: Tuple[int, int, int, int]  # x, y, width, height
    confidence: float
    description: str = ""


class DocumentComparator:
    """Compare two document images"""
    
    def __init__(self):
        """Initialize document comparator"""
        self.threshold_sensitivity = 30  # Difference sensitivity (0-255)
        self.min_contour_area = 100  # Minimum area for difference region
    
    def compare_documents(self, doc1: np.ndarray, doc2: np.ndarray,
                         highlight_color: Tuple[int, int, int] = (0, 0, 255)) -> Tuple[np.ndarray, List[Difference]]:
        """
        Compare two document images and highlight differences
        
        Args:
            doc1: First document (original)
            doc2: Second document (modified)
            highlight_color: Color for highlighting differences (BGR)
            
        Returns:
            Tuple of (comparison image, list of differences)
        """
        # Align documents first
        doc2_aligned = self._align_documents(doc1, doc2)
        
        # Resize to match if needed
        if doc1.shape != doc2_aligned.shape:
            doc2_aligned = cv2.resize(doc2_aligned, (doc1.shape[1], doc1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(doc1, cv2.COLOR_BGR2GRAY) if len(doc1.shape) == 3 else doc1
        gray2 = cv2.cvtColor(doc2_aligned, cv2.COLOR_BGR2GRAY) if len(doc2_aligned.shape) == 3 else doc2_aligned
        
        # Calculate difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Threshold to find significant differences
        _, thresh = cv2.threshold(diff, self.threshold_sensitivity, 255, cv2.THRESH_BINARY)
        
        # Find contours of differences
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create comparison image
        comparison = doc2_aligned.copy()
        if len(comparison.shape) == 2:
            comparison = cv2.cvtColor(comparison, cv2.COLOR_GRAY2BGR)
        
        differences = []
        
        # Highlight differences
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Draw rectangle around difference
                cv2.rectangle(comparison, (x, y), (x + w, y + h), highlight_color, 2)
                
                # Calculate confidence (based on difference intensity)
                roi_diff = diff[y:y+h, x:x+w]
                confidence = np.mean(roi_diff) / 255.0
                
                # Determine type of difference
                diff_type = self._classify_difference(gray1[y:y+h, x:x+w], gray2[y:y+h, x:x+w])
                
                differences.append(Difference(
                    type=diff_type,
                    region=(x, y, w, h),
                    confidence=confidence,
                    description=f"{diff_type.value.capitalize()} content at ({x}, {y})"
                ))
        
        return comparison, differences
    
    def compare_side_by_side(self, doc1: np.ndarray, doc2: np.ndarray,
                            label1: str = "Original",
                            label2: str = "Modified") -> np.ndarray:
        """
        Create side-by-side comparison
        
        Args:
            doc1: First document
            doc2: Second document
            label1: Label for first document
            label2: Label for second document
            
        Returns:
            Side-by-side comparison image
        """
        # Resize to same height
        h1, w1 = doc1.shape[:2]
        h2, w2 = doc2.shape[:2]
        
        target_height = max(h1, h2)
        
        if h1 != target_height:
            scale = target_height / h1
            doc1 = cv2.resize(doc1, None, fx=scale, fy=scale)
            w1 = int(w1 * scale)
        
        if h2 != target_height:
            scale = target_height / h2
            doc2 = cv2.resize(doc2, None, fx=scale, fy=scale)
            w2 = int(w2 * scale)
        
        # Convert to BGR if grayscale
        if len(doc1.shape) == 2:
            doc1 = cv2.cvtColor(doc1, cv2.COLOR_GRAY2BGR)
        if len(doc2.shape) == 2:
            doc2 = cv2.cvtColor(doc2, cv2.COLOR_GRAY2BGR)
        
        # Add labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        label_height = 40
        
        # Create labeled images
        labeled1 = np.ones((target_height + label_height, w1, 3), dtype=np.uint8) * 255
        labeled2 = np.ones((target_height + label_height, w2, 3), dtype=np.uint8) * 255
        
        labeled1[label_height:, :] = doc1
        labeled2[label_height:, :] = doc2
        
        # Add text labels
        cv2.putText(labeled1, label1, (10, 25), font, 0.8, (0, 0, 0), 2)
        cv2.putText(labeled2, label2, (10, 25), font, 0.8, (0, 0, 0), 2)
        
        # Add dividing line
        divider = np.ones((target_height + label_height, 2, 3), dtype=np.uint8) * 128
        
        # Concatenate
        result = np.hstack([labeled1, divider, labeled2])
        
        return result
    
    def create_diff_map(self, doc1: np.ndarray, doc2: np.ndarray,
                       colormap: int = cv2.COLORMAP_JET) -> np.ndarray:
        """
        Create color-coded difference map
        
        Args:
            doc1: First document
            doc2: Second document
            colormap: OpenCV colormap to use
            
        Returns:
            Difference map image
        """
        # Align documents
        doc2_aligned = self._align_documents(doc1, doc2)
        
        # Resize to match
        if doc1.shape != doc2_aligned.shape:
            doc2_aligned = cv2.resize(doc2_aligned, (doc1.shape[1], doc1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(doc1, cv2.COLOR_BGR2GRAY) if len(doc1.shape) == 3 else doc1
        gray2 = cv2.cvtColor(doc2_aligned, cv2.COLOR_BGR2GRAY) if len(doc2_aligned.shape) == 3 else doc2_aligned
        
        # Calculate absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Apply colormap
        diff_colored = cv2.applyColorMap(diff, colormap)
        
        return diff_colored
    
    def calculate_similarity(self, doc1: np.ndarray, doc2: np.ndarray) -> float:
        """
        Calculate similarity percentage between two documents
        
        Args:
            doc1: First document
            doc2: Second document
            
        Returns:
            Similarity percentage (0.0 to 100.0)
        """
        # Align and resize
        doc2_aligned = self._align_documents(doc1, doc2)
        if doc1.shape != doc2_aligned.shape:
            doc2_aligned = cv2.resize(doc2_aligned, (doc1.shape[1], doc1.shape[0]))
        
        # Convert to grayscale
        gray1 = cv2.cvtColor(doc1, cv2.COLOR_BGR2GRAY) if len(doc1.shape) == 3 else doc1
        gray2 = cv2.cvtColor(doc2_aligned, cv2.COLOR_BGR2GRAY) if len(doc2_aligned.shape) == 3 else doc2_aligned
        
        # Calculate SSIM (Structural Similarity Index)
        from skimage.metrics import structural_similarity as ssim
        similarity = ssim(gray1, gray2)
        
        return similarity * 100.0
    
    def get_difference_summary(self, differences: List[Difference]) -> Dict:
        """
        Get summary statistics for differences
        
        Args:
            differences: List of differences
            
        Returns:
            Dictionary with summary statistics
        """
        if not differences:
            return {
                'total': 0,
                'added': 0,
                'removed': 0,
                'modified': 0,
                'avg_confidence': 0.0
            }
        
        summary = {
            'total': len(differences),
            'added': sum(1 for d in differences if d.type == DifferenceType.ADDED),
            'removed': sum(1 for d in differences if d.type == DifferenceType.REMOVED),
            'modified': sum(1 for d in differences if d.type == DifferenceType.MODIFIED),
            'avg_confidence': sum(d.confidence for d in differences) / len(differences)
        }
        
        return summary
    
    def highlight_specific_differences(self, image: np.ndarray,
                                      differences: List[Difference],
                                      diff_type: Optional[DifferenceType] = None,
                                      color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        Highlight only specific types of differences
        
        Args:
            image: Input image
            differences: List of all differences
            diff_type: Type to highlight (None for all)
            color: Highlight color
            
        Returns:
            Image with highlighted differences
        """
        result = image.copy()
        
        for diff in differences:
            if diff_type is None or diff.type == diff_type:
                x, y, w, h = diff.region
                cv2.rectangle(result, (x, y), (x + w, y + h), color, 2)
                
                # Add label
                label = diff.type.value[:3].upper()
                cv2.putText(result, label, (x, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return result
    
    def create_blink_comparison(self, doc1: np.ndarray, doc2: np.ndarray) -> List[np.ndarray]:
        """
        Create frames for blink comparison (alternating between documents)
        
        Args:
            doc1: First document
            doc2: Second document
            
        Returns:
            List of frames [doc1, doc2, doc1, doc2, ...]
        """
        # Align and resize
        doc2_aligned = self._align_documents(doc1, doc2)
        if doc1.shape != doc2_aligned.shape:
            doc2_aligned = cv2.resize(doc2_aligned, (doc1.shape[1], doc1.shape[0]))
        
        # Create 10 alternating frames
        frames = []
        for i in range(10):
            frames.append(doc1 if i % 2 == 0 else doc2_aligned)
        
        return frames
    
    def _align_documents(self, doc1: np.ndarray, doc2: np.ndarray) -> np.ndarray:
        """
        Align doc2 to match doc1 using feature matching
        
        Args:
            doc1: Reference document
            doc2: Document to align
            
        Returns:
            Aligned document
        """
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(doc1, cv2.COLOR_BGR2GRAY) if len(doc1.shape) == 3 else doc1
            gray2 = cv2.cvtColor(doc2, cv2.COLOR_BGR2GRAY) if len(doc2.shape) == 3 else doc2
            
            # Detect ORB features
            orb = cv2.ORB_create(5000)
            kp1, des1 = orb.detectAndCompute(gray1, None)
            kp2, des2 = orb.detectAndCompute(gray2, None)
            
            if des1 is None or des2 is None:
                return doc2
            
            # Match features
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            
            if len(matches) < 10:
                return doc2
            
            # Sort matches by distance
            matches = sorted(matches, key=lambda x: x.distance)
            
            # Extract matched keypoints
            src_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:100]]).reshape(-1, 1, 2)
            
            # Find homography
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            if M is None:
                return doc2
            
            # Warp document
            h, w = doc1.shape[:2]
            aligned = cv2.warpPerspective(doc2, M, (w, h))
            
            return aligned
            
        except Exception:
            # If alignment fails, return original
            return doc2
    
    def _classify_difference(self, region1: np.ndarray, region2: np.ndarray) -> DifferenceType:
        """
        Classify type of difference in region
        
        Args:
            region1: Region from first document
            region2: Region from second document
            
        Returns:
            Type of difference
        """
        mean1 = np.mean(region1)
        mean2 = np.mean(region2)
        
        # Simple classification based on brightness
        if mean1 > 200 and mean2 < 100:
            return DifferenceType.ADDED
        elif mean1 < 100 and mean2 > 200:
            return DifferenceType.REMOVED
        else:
            return DifferenceType.MODIFIED
    
    def generate_comparison_report(self, doc1: np.ndarray, doc2: np.ndarray,
                                   differences: List[Difference]) -> str:
        """
        Generate text report of comparison
        
        Args:
            doc1: First document
            doc2: Second document
            differences: List of differences
            
        Returns:
            Formatted report string
        """
        summary = self.get_difference_summary(differences)
        similarity = self.calculate_similarity(doc1, doc2)
        
        report = f"""
Document Comparison Report
==========================

Similarity: {similarity:.2f}%
Total Differences: {summary['total']}

Breakdown:
- Added: {summary['added']}
- Removed: {summary['removed']}
- Modified: {summary['modified']}

Average Confidence: {summary['avg_confidence']:.2f}

Detailed Differences:
"""
        
        for i, diff in enumerate(differences[:20], 1):  # Limit to first 20
            report += f"\n{i}. {diff.description} (confidence: {diff.confidence:.2f})"
        
        if len(differences) > 20:
            report += f"\n... and {len(differences) - 20} more differences"
        
        return report
