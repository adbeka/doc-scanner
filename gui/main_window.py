"""Main GUI window for document scanner application"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QComboBox, QSlider, QGroupBox, QMessageBox,
    QSplitter, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np

# Import scanner modules
sys.path.append(str(Path(__file__).parent.parent))
from src.scanner import DocumentScanner
from src.image_processor import ImageProcessor
from src import constants


class ScannerThread(QThread):
    """Worker thread for scanning operations"""
    finished = pyqtSignal(np.ndarray)
    error = pyqtSignal(str)
    
    def __init__(self, scanner, image):
        super().__init__()
        self.scanner = scanner
        self.image = image
    
    def run(self):
        try:
            result = self.scanner.scan_document(self.image)
            if result is not None:
                self.finished.emit(result)
            else:
                self.error.emit("Could not detect document")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.scanner = DocumentScanner()
        self.processor = ImageProcessor()
        self.current_image = None
        self.scanned_image = None
        self.output_folder = "data/output"
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Document Scanner")
        self.setGeometry(100, 100, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Image display
        right_panel = self.create_image_panel()
        splitter.addWidget(right_panel)
        
        # Set initial sizes
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
    
    def create_control_panel(self):
        """Create the control panel with buttons and settings"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("Document Scanner")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Input group
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()
        
        self.btn_load = QPushButton("Load Image")
        self.btn_load.clicked.connect(self.load_image)
        input_layout.addWidget(self.btn_load)
        
        self.btn_camera = QPushButton("Capture from Camera")
        self.btn_camera.clicked.connect(self.capture_from_camera)
        input_layout.addWidget(self.btn_camera)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Scan group
        scan_group = QGroupBox("Scan")
        scan_layout = QVBoxLayout()
        
        self.btn_scan = QPushButton("Scan Document")
        self.btn_scan.clicked.connect(self.scan_document)
        self.btn_scan.setEnabled(False)
        self.btn_scan.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; }")
        scan_layout.addWidget(self.btn_scan)
        
        scan_group.setLayout(scan_layout)
        layout.addWidget(scan_group)
        
        # Enhancement group
        enhance_group = QGroupBox("Enhancement")
        enhance_layout = QVBoxLayout()
        
        # Color mode selection
        enhance_layout.addWidget(QLabel("Color Mode:"))
        self.combo_color_mode = QComboBox()
        self.combo_color_mode.addItems(["Black & White", "Grayscale", "Color"])
        self.combo_color_mode.currentIndexChanged.connect(self.apply_enhancements)
        enhance_layout.addWidget(self.combo_color_mode)
        
        # Brightness slider
        enhance_layout.addWidget(QLabel("Brightness:"))
        self.slider_brightness = QSlider(Qt.Horizontal)
        self.slider_brightness.setMinimum(-100)
        self.slider_brightness.setMaximum(100)
        self.slider_brightness.setValue(0)
        self.slider_brightness.valueChanged.connect(self.apply_enhancements)
        enhance_layout.addWidget(self.slider_brightness)
        
        # Contrast slider
        enhance_layout.addWidget(QLabel("Contrast:"))
        self.slider_contrast = QSlider(Qt.Horizontal)
        self.slider_contrast.setMinimum(-100)
        self.slider_contrast.setMaximum(100)
        self.slider_contrast.setValue(0)
        self.slider_contrast.valueChanged.connect(self.apply_enhancements)
        enhance_layout.addWidget(self.slider_contrast)
        
        # Auto enhance button
        self.btn_auto_enhance = QPushButton("Auto Enhance")
        self.btn_auto_enhance.clicked.connect(self.auto_enhance)
        self.btn_auto_enhance.setEnabled(False)
        enhance_layout.addWidget(self.btn_auto_enhance)
        
        enhance_group.setLayout(enhance_layout)
        layout.addWidget(enhance_group)
        
        # Output group
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        
        # Output format
        output_layout.addWidget(QLabel("Format:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(["PDF", "JPG", "PNG", "TIFF"])
        output_layout.addWidget(self.combo_format)
        
        self.btn_save = QPushButton("Save Result")
        self.btn_save.clicked.connect(self.save_result)
        self.btn_save.setEnabled(False)
        output_layout.addWidget(self.btn_save)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Reset button at bottom
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset)
        layout.addWidget(self.btn_reset)
        
        return panel
    
    def create_image_panel(self):
        """Create the image display panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Original image
        layout.addWidget(QLabel("Original Image:"))
        self.label_original = QLabel()
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setStyleSheet("border: 2px solid #ccc; background-color: #f5f5f5;")
        self.label_original.setMinimumSize(400, 300)
        self.label_original.setScaledContents(False)
        layout.addWidget(self.label_original)
        
        # Processed image
        layout.addWidget(QLabel("Scanned Document:"))
        self.label_processed = QLabel()
        self.label_processed.setAlignment(Qt.AlignCenter)
        self.label_processed.setStyleSheet("border: 2px solid #ccc; background-color: #f5f5f5;")
        self.label_processed.setMinimumSize(400, 300)
        self.label_processed.setScaledContents(False)
        layout.addWidget(self.label_processed)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 10px; font-style: italic;")
        layout.addWidget(self.status_label)
        
        return panel
    
    def load_image(self):
        """Load an image from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.tif)"
        )
        
        if file_path:
            if self.scanner.load_image(file_path):
                self.current_image = self.scanner.original_image.copy()
                self.display_image(self.current_image, self.label_original)
                self.btn_scan.setEnabled(True)
                self.status_label.setText(f"Loaded: {Path(file_path).name}")
            else:
                QMessageBox.critical(self, "Error", "Failed to load image")
    
    def capture_from_camera(self):
        """Capture image from camera"""
        QMessageBox.information(
            self,
            "Camera Capture",
            "Camera capture will be implemented in the next phase.\nFor now, please use 'Load Image'."
        )
    
    def scan_document(self):
        """Scan the document"""
        if self.current_image is None:
            return
        
        self.status_label.setText("Scanning document...")
        self.btn_scan.setEnabled(False)
        QApplication.processEvents()
        
        # Perform scan in thread
        self.scan_thread = ScannerThread(self.scanner, self.current_image)
        self.scan_thread.finished.connect(self.on_scan_finished)
        self.scan_thread.error.connect(self.on_scan_error)
        self.scan_thread.start()
    
    def on_scan_finished(self, result):
        """Handle scan completion"""
        self.scanned_image = result
        self.display_image(result, self.label_processed)
        self.btn_save.setEnabled(True)
        self.btn_auto_enhance.setEnabled(True)
        self.btn_scan.setEnabled(True)
        self.status_label.setText("Document scanned successfully!")
        
        # Show preview with detection
        preview = self.scanner.get_preview_with_detection(self.current_image)
        self.display_image(preview, self.label_original)
    
    def on_scan_error(self, error_msg):
        """Handle scan error"""
        self.btn_scan.setEnabled(True)
        self.status_label.setText("Scan failed")
        QMessageBox.warning(self, "Scan Error", error_msg)
    
    def apply_enhancements(self):
        """Apply enhancement settings to scanned image"""
        if self.scanned_image is None:
            return
        
        result = self.scanned_image.copy()
        
        # Apply brightness/contrast
        brightness = self.slider_brightness.value()
        contrast = self.slider_contrast.value()
        if brightness != 0 or contrast != 0:
            result = self.processor.adjust_brightness_contrast(
                result, brightness, contrast
            )
        
        # Apply color mode
        mode = self.combo_color_mode.currentText()
        if mode == "Black & White":
            result = self.processor.convert_to_bw(result)
        elif mode == "Grayscale":
            if len(result.shape) == 3:
                result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        self.display_image(result, self.label_processed)
    
    def auto_enhance(self):
        """Apply automatic enhancement"""
        if self.scanned_image is None:
            return
        
        result = self.processor.auto_enhance(self.scanned_image, mode='document')
        self.display_image(result, self.label_processed)
        self.status_label.setText("Auto-enhancement applied")
    
    def save_result(self):
        """Save the processed image"""
        if self.scanned_image is None:
            return
        
        # Get current display from processed label
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Scanned Document",
            "scanned_document",
            "PDF Files (*.pdf);;JPG Files (*.jpg);;PNG Files (*.png);;TIFF Files (*.tiff)"
        )
        
        if file_path:
            # Get the currently displayed image
            result = self.scanned_image.copy()
            
            # Apply current enhancements
            brightness = self.slider_brightness.value()
            contrast = self.slider_contrast.value()
            if brightness != 0 or contrast != 0:
                result = self.processor.adjust_brightness_contrast(
                    result, brightness, contrast
                )
            
            # Apply color mode
            mode = self.combo_color_mode.currentText()
            if mode == "Black & White":
                result = self.processor.convert_to_bw(result)
            elif mode == "Grayscale":
                if len(result.shape) == 3:
                    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            
            # Save image
            if cv2.imwrite(file_path, result):
                self.status_label.setText(f"Saved: {Path(file_path).name}")
                QMessageBox.information(self, "Success", "Document saved successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to save document")
    
    def reset(self):
        """Reset the application"""
        self.current_image = None
        self.scanned_image = None
        self.label_original.clear()
        self.label_processed.clear()
        self.btn_scan.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_auto_enhance.setEnabled(False)
        self.slider_brightness.setValue(0)
        self.slider_contrast.setValue(0)
        self.combo_color_mode.setCurrentIndex(0)
        self.status_label.setText("Ready")
    
    def display_image(self, cv_image, label):
        """Display OpenCV image in QLabel"""
        if cv_image is None:
            return
        
        # Convert color space if needed
        if len(cv_image.shape) == 3:
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        else:
            h, w = cv_image.shape
            bytes_per_line = w
            qt_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
        
        # Scale to fit label while maintaining aspect ratio
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        label.setPixmap(scaled_pixmap)


def main():
    """Main entry point for GUI"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
