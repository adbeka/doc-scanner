"""Interactive edge adjustment widget for manual corner correction"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage
import cv2
import numpy as np


class EdgeAdjusterWidget(QWidget):
    """Interactive widget for adjusting document corners"""
    
    corners_changed = pyqtSignal(np.ndarray)  # Emits updated corners
    
    def __init__(self, image, corners, parent=None):
        """
        Initialize edge adjuster widget.
        
        Args:
            image: Original image (numpy array)
            corners: Initial corner positions (4x2 array)
            parent: Parent widget
        """
        super().__init__(parent)
        self.image = image
        self.corners = corners.copy() if corners is not None else self._get_default_corners()
        self.selected_corner = None
        self.corner_radius = 15
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        self.init_ui()
        
    def _get_default_corners(self):
        """Get default corners if none provided"""
        h, w = self.image.shape[:2]
        margin = 50
        return np.array([
            [margin, margin],
            [w - margin, margin],
            [w - margin, h - margin],
            [margin, h - margin]
        ], dtype=np.float32)
    
    def init_ui(self):
        """Initialize UI"""
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        
        # Calculate scale factor to fit image
        self.update_scale_factor()
    
    def update_scale_factor(self):
        """Calculate scale factor to fit image in widget"""
        if self.image is None:
            return
        
        img_h, img_w = self.image.shape[:2]
        widget_w = self.width()
        widget_h = self.height()
        
        # Calculate scale to fit
        scale_w = widget_w / img_w
        scale_h = widget_h / img_h
        self.scale_factor = min(scale_w, scale_h, 1.0) * 0.9  # 90% of available space
        
        # Calculate offset to center image
        scaled_w = int(img_w * self.scale_factor)
        scaled_h = int(img_h * self.scale_factor)
        self.offset_x = (widget_w - scaled_w) // 2
        self.offset_y = (widget_h - scaled_h) // 2
    
    def resizeEvent(self, event):
        """Handle widget resize"""
        super().resizeEvent(event)
        self.update_scale_factor()
        self.update()
    
    def paintEvent(self, event):
        """Draw the image and corners"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw image
        if self.image is not None:
            # Convert to QPixmap
            if len(self.image.shape) == 3:
                rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            else:
                h, w = self.image.shape
                bytes_per_line = w
                qt_image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                int(w * self.scale_factor),
                int(h * self.scale_factor),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            painter.drawPixmap(self.offset_x, self.offset_y, scaled_pixmap)
        
        # Draw corners and lines
        if self.corners is not None and len(self.corners) == 4:
            # Draw lines connecting corners
            pen = QPen(QColor(0, 255, 0), 3)
            painter.setPen(pen)
            
            scaled_corners = self._scale_corners_to_widget(self.corners)
            for i in range(4):
                p1 = scaled_corners[i]
                p2 = scaled_corners[(i + 1) % 4]
                painter.drawLine(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]))
            
            # Draw corner handles
            for i, corner in enumerate(scaled_corners):
                if i == self.selected_corner:
                    brush = QBrush(QColor(255, 0, 0))
                    radius = self.corner_radius + 3
                else:
                    brush = QBrush(QColor(0, 0, 255))
                    radius = self.corner_radius
                
                painter.setBrush(brush)
                painter.setPen(QPen(QColor(255, 255, 255), 2))
                painter.drawEllipse(
                    QPoint(int(corner[0]), int(corner[1])),
                    radius,
                    radius
                )
                
                # Draw corner labels
                painter.setPen(QPen(QColor(255, 255, 255)))
                labels = ['TL', 'TR', 'BR', 'BL']
                painter.drawText(
                    int(corner[0]) - 10,
                    int(corner[1]) - radius - 5,
                    labels[i]
                )
    
    def _scale_corners_to_widget(self, corners):
        """Scale corner coordinates to widget space"""
        scaled = corners * self.scale_factor
        scaled[:, 0] += self.offset_x
        scaled[:, 1] += self.offset_y
        return scaled
    
    def _scale_point_to_image(self, x, y):
        """Scale widget coordinates to image space"""
        img_x = (x - self.offset_x) / self.scale_factor
        img_y = (y - self.offset_y) / self.scale_factor
        return img_x, img_y
    
    def _get_corner_at_pos(self, x, y):
        """Get corner index at given position or None"""
        scaled_corners = self._scale_corners_to_widget(self.corners)
        
        for i, corner in enumerate(scaled_corners):
            dx = x - corner[0]
            dy = y - corner[1]
            distance = np.sqrt(dx * dx + dy * dy)
            if distance < self.corner_radius:
                return i
        
        return None
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.LeftButton:
            self.selected_corner = self._get_corner_at_pos(event.x(), event.y())
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        if self.selected_corner is not None:
            # Update corner position
            img_x, img_y = self._scale_point_to_image(event.x(), event.y())
            
            # Clamp to image bounds
            h, w = self.image.shape[:2]
            img_x = max(0, min(w, img_x))
            img_y = max(0, min(h, img_y))
            
            self.corners[self.selected_corner] = [img_x, img_y]
            self.update()
        else:
            # Change cursor if hovering over corner
            corner_idx = self._get_corner_at_pos(event.x(), event.y())
            if corner_idx is not None:
                self.setCursor(Qt.PointingHandCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton and self.selected_corner is not None:
            self.selected_corner = None
            self.corners_changed.emit(self.corners.copy())
            self.update()
    
    def get_corners(self):
        """Get current corner positions"""
        return self.corners.copy()
    
    def set_corners(self, corners):
        """Set corner positions"""
        self.corners = corners.copy()
        self.update()


class EdgeAdjusterDialog(QDialog):
    """Dialog for interactive edge adjustment"""
    
    def __init__(self, image, corners, parent=None):
        """
        Initialize dialog.
        
        Args:
            image: Original image
            corners: Initial corners
            parent: Parent widget
        """
        super().__init__(parent)
        self.image = image
        self.initial_corners = corners
        self.final_corners = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Adjust Document Edges")
        self.setModal(True)
        self.resize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Drag the corner handles to adjust document edges.\n"
            "TL = Top Left, TR = Top Right, BR = Bottom Right, BL = Bottom Left"
        )
        instructions.setStyleSheet("padding: 10px; background-color: #e3f2fd; border-radius: 5px;")
        layout.addWidget(instructions)
        
        # Edge adjuster widget
        self.adjuster = EdgeAdjusterWidget(self.image, self.initial_corners)
        layout.addWidget(self.adjuster, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_corners)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)
        apply_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 16px;")
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
    
    def reset_corners(self):
        """Reset corners to initial position"""
        self.adjuster.set_corners(self.initial_corners)
    
    def get_corners(self):
        """Get adjusted corners"""
        return self.adjuster.get_corners()
    
    @staticmethod
    def adjust_edges(image, corners, parent=None):
        """
        Static method to show dialog and get adjusted corners.
        
        Args:
            image: Original image
            corners: Initial corners
            parent: Parent widget
            
        Returns:
            Adjusted corners or None if cancelled
        """
        dialog = EdgeAdjusterDialog(image, corners, parent)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.get_corners()
        return None
