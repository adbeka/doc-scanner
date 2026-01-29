"""
Annotation Tools
Add text, shapes, highlights, and stamps to documents
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum
import datetime


class AnnotationType(Enum):
    """Types of annotations"""
    TEXT = "text"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ARROW = "arrow"
    HIGHLIGHT = "highlight"
    LINE = "line"
    STAMP = "stamp"
    FREEHAND = "freehand"


@dataclass
class Annotation:
    """Container for annotation data"""
    type: AnnotationType
    position: Tuple[int, int]  # (x, y) or start point
    data: dict  # Type-specific data
    color: Tuple[int, int, int] = (0, 0, 255)  # BGR color
    thickness: int = 2
    
    def to_dict(self):
        """Convert to dictionary for saving"""
        return {
            'type': self.type.value,
            'position': self.position,
            'data': self.data,
            'color': self.color,
            'thickness': self.thickness
        }


class AnnotationTools:
    """Tools for annotating documents"""
    
    def __init__(self):
        """Initialize annotation tools"""
        self.annotations: List[Annotation] = []
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    
    def add_text(self, image: np.ndarray, text: str, 
                 position: Tuple[int, int],
                 font_scale: float = 1.0,
                 color: Tuple[int, int, int] = (0, 0, 255),
                 thickness: int = 2,
                 background: bool = False) -> np.ndarray:
        """
        Add text annotation
        
        Args:
            image: Input image
            text: Text to add
            position: (x, y) position
            font_scale: Font size scale
            color: Text color (BGR)
            thickness: Text thickness
            background: Add background behind text
            
        Returns:
            Image with text
        """
        result = image.copy()
        
        # Get text size
        (text_width, text_height), baseline = cv2.getTextSize(
            text, self.font, font_scale, thickness
        )
        
        # Draw background if requested
        if background:
            x, y = position
            padding = 5
            cv2.rectangle(
                result,
                (x - padding, y - text_height - padding),
                (x + text_width + padding, y + baseline + padding),
                (255, 255, 255),
                -1
            )
            cv2.rectangle(
                result,
                (x - padding, y - text_height - padding),
                (x + text_width + padding, y + baseline + padding),
                color,
                1
            )
        
        # Draw text
        cv2.putText(result, text, position, self.font, font_scale, 
                   color, thickness, cv2.LINE_AA)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.TEXT,
            position=position,
            data={'text': text, 'font_scale': font_scale, 'background': background},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def add_rectangle(self, image: np.ndarray,
                     top_left: Tuple[int, int],
                     bottom_right: Tuple[int, int],
                     color: Tuple[int, int, int] = (0, 0, 255),
                     thickness: int = 2,
                     filled: bool = False) -> np.ndarray:
        """
        Add rectangle annotation
        
        Args:
            image: Input image
            top_left: Top-left corner (x, y)
            bottom_right: Bottom-right corner (x, y)
            color: Rectangle color (BGR)
            thickness: Line thickness (-1 for filled)
            filled: Whether to fill rectangle
            
        Returns:
            Image with rectangle
        """
        result = image.copy()
        
        thick = -1 if filled else thickness
        cv2.rectangle(result, top_left, bottom_right, color, thick)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.RECTANGLE,
            position=top_left,
            data={'bottom_right': bottom_right, 'filled': filled},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def add_circle(self, image: np.ndarray,
                  center: Tuple[int, int],
                  radius: int,
                  color: Tuple[int, int, int] = (0, 0, 255),
                  thickness: int = 2,
                  filled: bool = False) -> np.ndarray:
        """
        Add circle annotation
        
        Args:
            image: Input image
            center: Center point (x, y)
            radius: Circle radius
            color: Circle color (BGR)
            thickness: Line thickness
            filled: Whether to fill circle
            
        Returns:
            Image with circle
        """
        result = image.copy()
        
        thick = -1 if filled else thickness
        cv2.circle(result, center, radius, color, thick)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.CIRCLE,
            position=center,
            data={'radius': radius, 'filled': filled},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def add_arrow(self, image: np.ndarray,
                 start: Tuple[int, int],
                 end: Tuple[int, int],
                 color: Tuple[int, int, int] = (0, 0, 255),
                 thickness: int = 2,
                 tip_length: float = 0.2) -> np.ndarray:
        """
        Add arrow annotation
        
        Args:
            image: Input image
            start: Start point (x, y)
            end: End point (x, y)
            color: Arrow color (BGR)
            thickness: Line thickness
            tip_length: Arrow tip length ratio
            
        Returns:
            Image with arrow
        """
        result = image.copy()
        
        cv2.arrowedLine(result, start, end, color, thickness, 
                       tipLength=tip_length)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.ARROW,
            position=start,
            data={'end': end, 'tip_length': tip_length},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def add_highlight(self, image: np.ndarray,
                     region: Tuple[int, int, int, int],
                     color: Tuple[int, int, int] = (0, 255, 255),
                     alpha: float = 0.3) -> np.ndarray:
        """
        Add semi-transparent highlight
        
        Args:
            image: Input image
            region: Region to highlight (x, y, width, height)
            color: Highlight color (BGR)
            alpha: Transparency (0.0 to 1.0)
            
        Returns:
            Image with highlight
        """
        result = image.copy()
        x, y, w, h = region
        
        # Create overlay
        overlay = result.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
        
        # Blend
        cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0, result)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.HIGHLIGHT,
            position=(x, y),
            data={'width': w, 'height': h, 'alpha': alpha},
            color=color,
            thickness=0
        ))
        
        return result
    
    def add_line(self, image: np.ndarray,
                start: Tuple[int, int],
                end: Tuple[int, int],
                color: Tuple[int, int, int] = (0, 0, 255),
                thickness: int = 2,
                line_type: str = 'solid') -> np.ndarray:
        """
        Add line annotation
        
        Args:
            image: Input image
            start: Start point (x, y)
            end: End point (x, y)
            color: Line color (BGR)
            thickness: Line thickness
            line_type: 'solid' or 'dashed'
            
        Returns:
            Image with line
        """
        result = image.copy()
        
        if line_type == 'dashed':
            self._draw_dashed_line(result, start, end, color, thickness)
        else:
            cv2.line(result, start, end, color, thickness)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.LINE,
            position=start,
            data={'end': end, 'line_type': line_type},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def _draw_dashed_line(self, image: np.ndarray, 
                         start: Tuple[int, int],
                         end: Tuple[int, int],
                         color: Tuple[int, int, int],
                         thickness: int,
                         dash_length: int = 10):
        """Draw dashed line"""
        x1, y1 = start
        x2, y2 = end
        
        # Calculate line length
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # Calculate number of dashes
        num_dashes = int(length / (2 * dash_length))
        
        for i in range(num_dashes):
            # Calculate dash start and end
            t1 = (2 * i * dash_length) / length
            t2 = ((2 * i + 1) * dash_length) / length
            
            dash_start = (int(x1 + t1 * (x2 - x1)), int(y1 + t1 * (y2 - y1)))
            dash_end = (int(x1 + t2 * (x2 - x1)), int(y1 + t2 * (y2 - y1)))
            
            cv2.line(image, dash_start, dash_end, color, thickness)
    
    def add_stamp(self, image: np.ndarray,
                 stamp_type: str,
                 position: Tuple[int, int],
                 color: Tuple[int, int, int] = (255, 0, 0),
                 size: int = 100) -> np.ndarray:
        """
        Add stamp annotation (APPROVED, CONFIDENTIAL, etc.)
        
        Args:
            image: Input image
            stamp_type: Type of stamp ('approved', 'confidential', 'draft', 'urgent')
            position: Center position (x, y)
            color: Stamp color (BGR)
            size: Stamp size
            
        Returns:
            Image with stamp
        """
        result = image.copy()
        
        # Stamp text
        stamps = {
            'approved': 'APPROVED',
            'rejected': 'REJECTED',
            'confidential': 'CONFIDENTIAL',
            'draft': 'DRAFT',
            'urgent': 'URGENT',
            'copy': 'COPY',
            'void': 'VOID',
            'received': 'RECEIVED'
        }
        
        text = stamps.get(stamp_type.lower(), stamp_type.upper())
        
        # Create stamp overlay
        overlay = result.copy()
        
        # Draw circle border
        cv2.circle(overlay, position, size, color, 3)
        
        # Add text
        font_scale = size / 100.0
        (text_width, text_height), _ = cv2.getTextSize(
            text, self.font, font_scale, 2
        )
        
        text_pos = (position[0] - text_width // 2, position[1] + text_height // 2)
        cv2.putText(overlay, text, text_pos, self.font, font_scale, 
                   color, 2, cv2.LINE_AA)
        
        # Blend with transparency
        cv2.addWeighted(overlay, 0.7, result, 0.3, 0, result)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.STAMP,
            position=position,
            data={'stamp_type': stamp_type, 'size': size},
            color=color,
            thickness=3
        ))
        
        return result
    
    def add_signature_placeholder(self, image: np.ndarray,
                                  position: Tuple[int, int],
                                  width: int = 200,
                                  label: str = "Signature") -> np.ndarray:
        """
        Add signature placeholder line
        
        Args:
            image: Input image
            position: Start position (x, y)
            width: Width of signature line
            label: Label text
            
        Returns:
            Image with signature placeholder
        """
        result = image.copy()
        x, y = position
        
        # Draw line
        cv2.line(result, (x, y), (x + width, y), (0, 0, 0), 2)
        
        # Add label below
        label_pos = (x, y + 20)
        cv2.putText(result, label, label_pos, self.font, 0.5, 
                   (0, 0, 0), 1, cv2.LINE_AA)
        
        return result
    
    def add_date_stamp(self, image: np.ndarray,
                      position: Tuple[int, int],
                      color: Tuple[int, int, int] = (0, 0, 0),
                      font_scale: float = 0.7) -> np.ndarray:
        """
        Add current date stamp
        
        Args:
            image: Input image
            position: Position (x, y)
            color: Text color (BGR)
            font_scale: Font size
            
        Returns:
            Image with date stamp
        """
        # Get current date
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        return self.add_text(image, date_str, position, font_scale, color, 
                           thickness=1, background=True)
    
    def draw_freehand(self, image: np.ndarray,
                     points: List[Tuple[int, int]],
                     color: Tuple[int, int, int] = (0, 0, 255),
                     thickness: int = 2) -> np.ndarray:
        """
        Draw freehand annotation
        
        Args:
            image: Input image
            points: List of points (x, y)
            color: Line color (BGR)
            thickness: Line thickness
            
        Returns:
            Image with freehand drawing
        """
        result = image.copy()
        
        if len(points) < 2:
            return result
        
        # Draw lines between consecutive points
        for i in range(len(points) - 1):
            cv2.line(result, points[i], points[i + 1], color, thickness)
        
        # Store annotation
        self.annotations.append(Annotation(
            type=AnnotationType.FREEHAND,
            position=points[0],
            data={'points': points},
            color=color,
            thickness=thickness
        ))
        
        return result
    
    def clear_annotations(self):
        """Clear all stored annotations"""
        self.annotations.clear()
    
    def get_annotations(self) -> List[Annotation]:
        """Get all annotations"""
        return self.annotations.copy()
    
    def apply_all_annotations(self, image: np.ndarray) -> np.ndarray:
        """
        Apply all stored annotations to image
        
        Args:
            image: Input image
            
        Returns:
            Image with all annotations
        """
        result = image.copy()
        
        for ann in self.annotations:
            if ann.type == AnnotationType.TEXT:
                result = self.add_text(
                    result, ann.data['text'], ann.position,
                    ann.data['font_scale'], ann.color, ann.thickness,
                    ann.data.get('background', False)
                )
            elif ann.type == AnnotationType.RECTANGLE:
                result = self.add_rectangle(
                    result, ann.position, ann.data['bottom_right'],
                    ann.color, ann.thickness, ann.data.get('filled', False)
                )
            elif ann.type == AnnotationType.CIRCLE:
                result = self.add_circle(
                    result, ann.position, ann.data['radius'],
                    ann.color, ann.thickness, ann.data.get('filled', False)
                )
            elif ann.type == AnnotationType.ARROW:
                result = self.add_arrow(
                    result, ann.position, ann.data['end'],
                    ann.color, ann.thickness, ann.data.get('tip_length', 0.2)
                )
            elif ann.type == AnnotationType.HIGHLIGHT:
                region = (ann.position[0], ann.position[1], 
                         ann.data['width'], ann.data['height'])
                result = self.add_highlight(
                    result, region, ann.color, ann.data.get('alpha', 0.3)
                )
            elif ann.type == AnnotationType.LINE:
                result = self.add_line(
                    result, ann.position, ann.data['end'],
                    ann.color, ann.thickness, ann.data.get('line_type', 'solid')
                )
            elif ann.type == AnnotationType.STAMP:
                result = self.add_stamp(
                    result, ann.data['stamp_type'], ann.position,
                    ann.color, ann.data.get('size', 100)
                )
            elif ann.type == AnnotationType.FREEHAND:
                result = self.draw_freehand(
                    result, ann.data['points'], ann.color, ann.thickness
                )
        
        return result
