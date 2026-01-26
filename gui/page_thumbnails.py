"""Page thumbnails widget for multi-page document management"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel,
    QPushButton, QFrame, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor
import cv2
import numpy as np


class PageThumbnail(QFrame):
    """Single page thumbnail widget"""
    
    clicked = pyqtSignal(int)  # Emits page index
    delete_requested = pyqtSignal(int)  # Emits page index
    
    def __init__(self, index: int, image: np.ndarray, name: str, parent=None):
        """
        Initialize page thumbnail.
        
        Args:
            index: Page index
            image: Page image
            name: Page name
            parent: Parent widget
        """
        super().__init__(parent)
        self.index = index
        self.is_selected = False
        
        self.init_ui(image, name)
        
    def init_ui(self, image: np.ndarray, name: str):
        """Initialize UI"""
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(2)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Thumbnail image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(120, 160)
        self.image_label.setStyleSheet("background-color: #f0f0f0;")
        
        # Set thumbnail
        self.set_thumbnail(image)
        
        layout.addWidget(self.image_label)
        
        # Page info
        info_layout = QVBoxLayout()
        
        # Page name
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 10px;")
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        
        # Delete button
        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.index))
        
        # Center delete button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(delete_btn)
        btn_layout.addStretch()
        info_layout.addLayout(btn_layout)
        
        layout.addLayout(info_layout)
        
        self.update_style()
        
    def set_thumbnail(self, image: np.ndarray):
        """Set thumbnail image"""
        if image is None:
            return
        
        # Convert to QPixmap
        if len(image.shape) == 3:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        else:
            h, w = image.shape
            bytes_per_line = w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            110, 150,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        self.update_style()
    
    def update_style(self):
        """Update widget style based on selection"""
        if self.is_selected:
            self.setStyleSheet("""
                PageThumbnail {
                    border: 2px solid #2196F3;
                    background-color: #E3F2FD;
                }
            """)
        else:
            self.setStyleSheet("""
                PageThumbnail {
                    border: 2px solid #cccccc;
                    background-color: white;
                }
                PageThumbnail:hover {
                    border: 2px solid #999999;
                    background-color: #f5f5f5;
                }
            """)
    
    def mousePressEvent(self, event):
        """Handle mouse click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)


class PageThumbnailsWidget(QWidget):
    """Widget displaying all page thumbnails"""
    
    page_selected = pyqtSignal(int)  # Emits selected page index
    page_deleted = pyqtSignal(int)  # Emits deleted page index
    
    def __init__(self, parent=None):
        """Initialize page thumbnails widget"""
        super().__init__(parent)
        self.thumbnails = []
        self.current_selection = -1
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("Pages")
        title.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        layout.addWidget(title)
        
        # Scroll area for thumbnails
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for thumbnails
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignTop)
        self.container_layout.setSpacing(10)
        
        scroll.setWidget(self.container)
        layout.addWidget(scroll)
        
        # Info label
        self.info_label = QLabel("No pages")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(self.info_label)
        
    def add_page(self, image: np.ndarray, name: str) -> int:
        """
        Add a page thumbnail.
        
        Args:
            image: Page image
            name: Page name
            
        Returns:
            Page index
        """
        # Get thumbnail
        thumbnail_img = self._create_thumbnail(image)
        
        index = len(self.thumbnails)
        thumbnail = PageThumbnail(index, thumbnail_img, name)
        thumbnail.clicked.connect(self._on_thumbnail_clicked)
        thumbnail.delete_requested.connect(self._on_delete_requested)
        
        self.thumbnails.append(thumbnail)
        self.container_layout.addWidget(thumbnail)
        
        self.update_info_label()
        
        # Select the new page
        self.select_page(index)
        
        return index
    
    def remove_page(self, index: int):
        """Remove a page thumbnail"""
        if 0 <= index < len(self.thumbnails):
            thumbnail = self.thumbnails.pop(index)
            self.container_layout.removeWidget(thumbnail)
            thumbnail.deleteLater()
            
            # Update indices for remaining thumbnails
            for i, thumb in enumerate(self.thumbnails):
                thumb.index = i
            
            self.update_info_label()
            
            # Adjust selection
            if self.current_selection == index:
                if self.thumbnails:
                    new_selection = min(index, len(self.thumbnails) - 1)
                    self.select_page(new_selection)
                else:
                    self.current_selection = -1
            elif self.current_selection > index:
                self.current_selection -= 1
    
    def clear_all(self):
        """Remove all thumbnails"""
        while self.thumbnails:
            self.remove_page(0)
        self.current_selection = -1
        self.update_info_label()
    
    def select_page(self, index: int):
        """Select a page"""
        if 0 <= index < len(self.thumbnails):
            # Deselect previous
            if 0 <= self.current_selection < len(self.thumbnails):
                self.thumbnails[self.current_selection].set_selected(False)
            
            # Select new
            self.current_selection = index
            self.thumbnails[index].set_selected(True)
            self.page_selected.emit(index)
    
    def update_page_thumbnail(self, index: int, image: np.ndarray):
        """Update thumbnail image"""
        if 0 <= index < len(self.thumbnails):
            thumbnail_img = self._create_thumbnail(image)
            self.thumbnails[index].set_thumbnail(thumbnail_img)
    
    def get_page_count(self) -> int:
        """Get number of pages"""
        return len(self.thumbnails)
    
    def _create_thumbnail(self, image: np.ndarray) -> np.ndarray:
        """Create thumbnail from image"""
        if image is None:
            return None
        
        # Calculate thumbnail size
        h, w = image.shape[:2]
        max_dim = 150
        
        if h > w:
            new_h = max_dim
            new_w = int(w * max_dim / h)
        else:
            new_w = max_dim
            new_h = int(h * max_dim / w)
        
        thumbnail = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return thumbnail
    
    def _on_thumbnail_clicked(self, index: int):
        """Handle thumbnail click"""
        self.select_page(index)
    
    def _on_delete_requested(self, index: int):
        """Handle delete request"""
        self.page_deleted.emit(index)
    
    def update_info_label(self):
        """Update info label"""
        count = len(self.thumbnails)
        if count == 0:
            self.info_label.setText("No pages")
        elif count == 1:
            self.info_label.setText("1 page")
        else:
            self.info_label.setText(f"{count} pages")
