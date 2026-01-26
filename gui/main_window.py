"""Main GUI window for document scanner application"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QComboBox, QSlider, QGroupBox, QMessageBox,
    QSplitter, QApplication, QProgressDialog, QShortcut, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
import cv2
import numpy as np

# Import scanner modules
sys.path.append(str(Path(__file__).parent.parent))
from src.scanner import DocumentScanner
from src.image_processor import ImageProcessor
from src.batch_processor import BatchProcessor
from src.history_manager import HistoryManager
from src.multi_page_manager import MultiPageManager
from src.templates import TemplateManager
from src.filters import FilterManager
from src import constants
from gui.edge_adjuster import EdgeAdjusterDialog
from gui.page_thumbnails import PageThumbnailsWidget


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
        self.batch_processor = BatchProcessor(self.scanner, self.processor)
        self.history = HistoryManager(max_history=20)
        self.multi_page = MultiPageManager()
        self.current_image = None
        self.scanned_image = None
        self.rotation_angle = 0
        self.output_folder = "data/output"
        
        self.init_ui()
        self.setup_shortcuts()
    
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
        
        self.btn_batch = QPushButton("Batch Process Folder")
        self.btn_batch.clicked.connect(self.batch_process)
        input_layout.addWidget(self.btn_batch)
        
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
        
        self.btn_adjust_edges = QPushButton("Adjust Edges Manually")
        self.btn_adjust_edges.clicked.connect(self.adjust_edges_manually)
        self.btn_adjust_edges.setEnabled(False)
        scan_layout.addWidget(self.btn_adjust_edges)
        
        scan_group.setLayout(scan_layout)
        layout.addWidget(scan_group)
        
        # Undo/Redo group
        history_group = QGroupBox("History")
        history_layout = QHBoxLayout()
        
        self.btn_undo = QPushButton("↶ Undo")
        self.btn_undo.clicked.connect(self.undo)
        self.btn_undo.setEnabled(False)
        self.btn_undo.setToolTip("Ctrl+Z")
        history_layout.addWidget(self.btn_undo)
        
        self.btn_redo = QPushButton("↷ Redo")
        self.btn_redo.clicked.connect(self.redo)
        self.btn_redo.setEnabled(False)
        self.btn_redo.setToolTip("Ctrl+Y")
        history_layout.addWidget(self.btn_redo)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Multi-Page group
        multipage_group = QGroupBox("Multi-Page PDF")
        multipage_layout = QVBoxLayout()
        
        self.btn_add_page = QPushButton("➕ Add to Pages")
        self.btn_add_page.clicked.connect(self.add_to_pages)
        self.btn_add_page.setEnabled(False)
        multipage_layout.addWidget(self.btn_add_page)
        
        self.btn_export_pdf = QPushButton("📄 Export Multi-Page PDF")
        self.btn_export_pdf.clicked.connect(self.export_multipage_pdf)
        self.btn_export_pdf.setEnabled(False)
        multipage_layout.addWidget(self.btn_export_pdf)
        
        self.btn_clear_pages = QPushButton("Clear All Pages")
        self.btn_clear_pages.clicked.connect(self.clear_all_pages)
        self.btn_clear_pages.setEnabled(False)
        multipage_layout.addWidget(self.btn_clear_pages)
        
        multipage_group.setLayout(multipage_layout)
        layout.addWidget(multipage_group)
        
        # Templates group
        template_group = QGroupBox("Document Templates")
        template_layout = QVBoxLayout()
        
        template_layout.addWidget(QLabel("Template:"))
        self.combo_template = QComboBox()
        self.combo_template.addItem("None (Manual)")
        template_names = TemplateManager.get_template_names()
        for name in sorted(template_names):
            display_name = name.replace('_', ' ').title()
            self.combo_template.addItem(display_name, name)
        template_layout.addWidget(self.combo_template)
        
        self.btn_apply_template = QPushButton("Apply Template")
        self.btn_apply_template.clicked.connect(self.apply_template)
        self.btn_apply_template.setEnabled(False)
        template_layout.addWidget(self.btn_apply_template)
        
        template_group.setLayout(template_layout)
        layout.addWidget(template_group)
        
        # Filters group
        filter_group = QGroupBox("Image Filters")
        filter_layout = QVBoxLayout()
        
        filter_layout.addWidget(QLabel("Filter:"))
        self.combo_filter = QComboBox()
        self.combo_filter.addItem("None")
        filter_names = FilterManager.get_filter_names()
        for name in sorted(filter_names):
            display_name = name.replace('_', ' ').title()
            self.combo_filter.addItem(display_name, name)
        filter_layout.addWidget(self.combo_filter)
        
        self.btn_apply_filter = QPushButton("Apply Filter")
        self.btn_apply_filter.clicked.connect(self.apply_filter)
        self.btn_apply_filter.setEnabled(False)
        filter_layout.addWidget(self.btn_apply_filter)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
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
        
        # Rotation controls
        enhance_layout.addWidget(QLabel("Rotate:"))
        rotation_layout = QHBoxLayout()
        self.btn_rotate_left = QPushButton("⟲ 90°")
        self.btn_rotate_left.clicked.connect(lambda: self.rotate_image(-90))
        self.btn_rotate_left.setEnabled(False)
        rotation_layout.addWidget(self.btn_rotate_left)
        
        self.btn_rotate_right = QPushButton("⟳ 90°")
        self.btn_rotate_right.clicked.connect(lambda: self.rotate_image(90))
        self.btn_rotate_right.setEnabled(False)
        rotation_layout.addWidget(self.btn_rotate_right)
        enhance_layout.addLayout(rotation_layout)
        
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
        # Create main splitter for image area and page thumbnails
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - images
        image_widget = QWidget()
        layout = QVBoxLayout(image_widget)
        
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
        
        splitter.addWidget(image_widget)
        
        # Right side - page thumbnails
        self.page_thumbnails = PageThumbnailsWidget()
        self.page_thumbnails.page_selected.connect(self.on_page_selected)
        self.page_thumbnails.page_deleted.connect(self.on_page_deleted)
        self.page_thumbnails.setMaximumWidth(180)
        splitter.addWidget(self.page_thumbnails)
        
        # Set initial sizes (images larger than thumbnails)
        splitter.setSizes([800, 180])
        
        return splitter
    
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
                self.btn_adjust_edges.setEnabled(True)
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
        self.btn_rotate_left.setEnabled(True)
        self.btn_rotate_right.setEnabled(True)
        self.btn_add_page.setEnabled(True)
        self.btn_scan.setEnabled(True)
        self.btn_apply_template.setEnabled(True)
        self.btn_apply_filter.setEnabled(True)
        self.status_label.setText("Document scanned successfully!")
        
        # Add to history
        self.history.clear()  # Clear old history on new scan
        self.add_history_state("Initial scan")
        
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
        self.rotation_angle = 0
        self.history.clear()
        self.label_original.clear()
        self.label_processed.clear()
        self.btn_scan.setEnabled(False)
        self.btn_adjust_edges.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_auto_enhance.setEnabled(False)
        self.btn_rotate_left.setEnabled(False)
        self.btn_rotate_right.setEnabled(False)
        self.btn_add_page.setEnabled(False)
        self.btn_apply_template.setEnabled(False)
        self.btn_apply_filter.setEnabled(False)
        self.update_history_buttons()
        self.slider_brightness.setValue(0)
        self.slider_contrast.setValue(0)
        self.combo_color_mode.setCurrentIndex(0)
        self.combo_template.setCurrentIndex(0)
        self.combo_filter.setCurrentIndex(0)
        self.status_label.setText("Ready")
    
    def adjust_edges_manually(self):
        """Open manual edge adjustment dialog"""
        if self.current_image is None:
            return
        
        # First detect document to get initial corners
        corners = self.scanner.detect_document(self.current_image)
        
        if corners is None:
            # If auto-detection fails, provide default corners
            h, w = self.current_image.shape[:2]
            margin = 50
            corners = np.array([
                [margin, margin],
                [w - margin, margin],
                [w - margin, h - margin],
                [margin, h - margin]
            ], dtype=np.float32)
            QMessageBox.information(
                self,
                "Auto-detection Failed",
                "Could not automatically detect document edges.\n"
                "Default corners have been set. Please adjust them manually."
            )
        
        # Show edge adjustment dialog
        adjusted_corners = EdgeAdjusterDialog.adjust_edges(
            self.current_image,
            corners,
            self
        )
        
        if adjusted_corners is not None:
            # Scan with manual corners
            self.status_label.setText("Scanning with manual edges...")
            QApplication.processEvents()
            
            result = self.scanner.scan_document(
                self.current_image,
                manual_corners=adjusted_corners
            )
            
            if result is not None:
                self.scanned_image = result
                self.display_image(result, self.label_processed)
                self.btn_save.setEnabled(True)
                self.btn_auto_enhance.setEnabled(True)
                self.btn_rotate_left.setEnabled(True)
                self.btn_rotate_right.setEnabled(True)
                self.btn_add_page.setEnabled(True)
                self.btn_apply_template.setEnabled(True)
                self.btn_apply_filter.setEnabled(True)
                self.status_label.setText("Document scanned with manual edges!")
                
                # Add to history
                self.history.clear()
                self.add_history_state("Manual edge adjustment")
            else:
                QMessageBox.warning(self, "Error", "Failed to scan with adjusted edges")
    
    def apply_template(self):
        """Apply selected document template"""
        if self.scanned_image is None:
            return
        
        template_index = self.combo_template.currentIndex()
        if template_index == 0:  # "None (Manual)"
            return
        
        template_name = self.combo_template.currentData()
        
        try:
            self.status_label.setText(f"Applying template: {template_name}...")
            QApplication.processEvents()
            
            result = TemplateManager.apply_template(self.scanned_image, template_name)
            self.scanned_image = result
            self.display_image(result, self.label_processed)
            
            template_display = template_name.replace('_', ' ').title()
            self.status_label.setText(f"Template '{template_display}' applied")
            self.add_history_state(f"Apply template: {template_display}")
        except Exception as e:
            QMessageBox.critical(self, "Template Error", f"Failed to apply template: {str(e)}")
            self.status_label.setText("Template application failed")
    
    def apply_filter(self):
        """Apply selected image filter"""
        if self.scanned_image is None:
            return
        
        filter_index = self.combo_filter.currentIndex()
        if filter_index == 0:  # "None"
            return
        
        filter_name = self.combo_filter.currentData()
        
        try:
            self.status_label.setText(f"Applying filter: {filter_name}...")
            QApplication.processEvents()
            
            result = FilterManager.apply_filter(self.scanned_image, filter_name)
            self.scanned_image = result
            self.display_image(result, self.label_processed)
            
            filter_display = filter_name.replace('_', ' ').title()
            self.status_label.setText(f"Filter '{filter_display}' applied")
            self.add_history_state(f"Apply filter: {filter_display}")
        except Exception as e:
            QMessageBox.critical(self, "Filter Error", f"Failed to apply filter: {str(e)}")
            self.status_label.setText("Filter application failed")
    
    def rotate_image(self, angle):
        """Rotate the scanned image"""
        if self.scanned_image is None:
            return
        
        self.rotation_angle = (self.rotation_angle + angle) % 360
        rotated = self.processor.rotate_image(self.scanned_image, angle)
        self.scanned_image = rotated
        
        # Reapply current enhancements
        self.apply_enhancements()
        self.status_label.setText(f"Rotated {angle}\u00b0")
        self.add_history_state(f"Rotate {angle}°")
    
    def batch_process(self):
        """Process multiple images from a folder"""
        # Select input folder
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder with Images to Scan",
            ""
        )
        
        if not folder:
            return
        
        # Select output folder
        output_folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            "data/output"
        )
        
        if not output_folder:
            return
        
        # Get current settings
        color_mode_map = {
            "Black & White": "bw",
            "Grayscale": "grayscale",
            "Color": "color"
        }
        color_mode = color_mode_map[self.combo_color_mode.currentText()]
        output_format = self.combo_format.currentText().lower()
        brightness = self.slider_brightness.value()
        contrast = self.slider_contrast.value()
        
        # Create progress dialog
        progress = QProgressDialog("Processing images...", "Cancel", 0, 100, self)
        progress.setWindowTitle("Batch Processing")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        
        def update_progress(current, total, filename):
            progress.setValue(int((current / total) * 100))
            progress.setLabelText(f"Processing {current}/{total}: {filename}")
            QApplication.processEvents()
            
            if progress.wasCanceled():
                raise Exception("Cancelled by user")
        
        try:
            # Process folder
            results = self.batch_processor.process_folder(
                folder,
                output_folder,
                color_mode=color_mode,
                output_format=output_format,
                progress_callback=update_progress,
                brightness=brightness,
                contrast=contrast
            )
            
            progress.close()
            
            # Show results
            message = (
                f"Batch Processing Complete!\n\n"
                f"Total: {results['total']}\n"
                f"Success: {results['success']}\n"
                f"Failed: {results['failed']}\n\n"
                f"Output folder: {output_folder}"
            )
            
            if results['failed'] > 0:
                message += "\n\nFailed files:\n"
                for detail in results['details']:
                    if detail['status'] == 'failed':
                        message += f"- {detail['filename']}: {detail.get('error', 'Unknown')}\n"
            
            QMessageBox.information(self, "Batch Processing Results", message)
            self.status_label.setText(
                f"Batch processing complete: {results['success']}/{results['total']} successful"
            )
            
        except Exception as e:
            progress.close()
            if "Cancelled" not in str(e):
                QMessageBox.critical(self, "Batch Processing Error", str(e))
            else:
                self.status_label.setText("Batch processing cancelled")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Undo/Redo shortcuts
        QShortcut(QKeySequence.Undo, self, self.undo)
        QShortcut(QKeySequence.Redo, self, self.redo)
        
        # Save shortcut
        QShortcut(QKeySequence.Save, self, self.save_result)
        
        # Open shortcut
        QShortcut(QKeySequence.Open, self, self.load_image)
    
    def add_history_state(self, description: str = ""):
        """Add current state to history"""
        if self.scanned_image is not None:
            settings = {
                'brightness': self.slider_brightness.value(),
                'contrast': self.slider_contrast.value(),
                'color_mode': self.combo_color_mode.currentIndex(),
                'rotation': self.rotation_angle
            }
            self.history.add_state(self.scanned_image, description, settings)
            self.update_history_buttons()
    
    def update_history_buttons(self):
        """Update undo/redo button states"""
        self.btn_undo.setEnabled(self.history.can_undo())
        self.btn_redo.setEnabled(self.history.can_redo())
    
    def undo(self):
        """Undo to previous state"""
        state = self.history.undo()
        if state:
            self.scanned_image = state.get_image()
            
            # Restore settings
            settings = state.settings
            if settings:
                self.slider_brightness.setValue(settings.get('brightness', 0))
                self.slider_contrast.setValue(settings.get('contrast', 0))
                self.combo_color_mode.setCurrentIndex(settings.get('color_mode', 0))
                self.rotation_angle = settings.get('rotation', 0)
            
            self.display_image(self.scanned_image, self.label_processed)
            self.status_label.setText(f"Undo: {state.description}")
            self.update_history_buttons()
    
    def redo(self):
        """Redo to next state"""
        state = self.history.redo()
        if state:
            self.scanned_image = state.get_image()
            
            # Restore settings
            settings = state.settings
            if settings:
                self.slider_brightness.setValue(settings.get('brightness', 0))
                self.slider_contrast.setValue(settings.get('contrast', 0))
                self.combo_color_mode.setCurrentIndex(settings.get('color_mode', 0))
                self.rotation_angle = settings.get('rotation', 0)
            
            self.display_image(self.scanned_image, self.label_processed)
            self.status_label.setText(f"Redo: {state.description}")
            self.update_history_buttons()
    
    def add_to_pages(self):
        """Add current scanned image to multi-page document"""
        if self.scanned_image is None:
            return
        
        # Get page name
        page_num = self.multi_page.get_page_count() + 1
        name, ok = QInputDialog.getText(
            self,
            "Add Page",
            "Page name:",
            text=f"Page {page_num}"
        )
        
        if ok:
            # Get current processed image with all enhancements
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
            
            # Add to multi-page manager
            self.multi_page.add_page(result, name)
            
            # Add thumbnail
            self.page_thumbnails.add_page(result, name)
            
            # Enable export button
            self.btn_export_pdf.setEnabled(True)
            self.btn_clear_pages.setEnabled(True)
            
            self.status_label.setText(f"Added: {name} ({self.multi_page.get_page_count()} pages total)")
    
    def on_page_selected(self, index: int):
        """Handle page selection from thumbnails"""
        page = self.multi_page.get_page(index)
        if page:
            self.display_image(page.get_image(), self.label_processed)
            self.status_label.setText(f"Viewing: {page.name}")
    
    def on_page_deleted(self, index: int):
        """Handle page deletion"""
        reply = QMessageBox.question(
            self,
            "Delete Page",
            f"Delete page {index + 1}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            page = self.multi_page.get_page(index)
            if page:
                page_name = page.name
                self.multi_page.remove_page(index)
                self.page_thumbnails.remove_page(index)
                self.status_label.setText(f"Deleted: {page_name}")
                
                # Disable export if no pages left
                if self.multi_page.get_page_count() == 0:
                    self.btn_export_pdf.setEnabled(False)
                    self.btn_clear_pages.setEnabled(False)
    
    def export_multipage_pdf(self):
        """Export all pages as a multi-page PDF"""
        if self.multi_page.get_page_count() == 0:
            QMessageBox.warning(self, "No Pages", "No pages to export")
            return
        
        # Get output file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Multi-Page PDF",
            "multipage_document.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            # Ensure .pdf extension
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'
            
            # Export
            success = self.multi_page.export_to_pdf(file_path, page_size='A4')
            
            if success:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Exported {self.multi_page.get_page_count()}-page PDF:\n{file_path}"
                )
                self.status_label.setText(f"Exported {self.multi_page.get_page_count()} pages to PDF")
            else:
                QMessageBox.critical(self, "Error", "Failed to export PDF")
    
    def clear_all_pages(self):
        """Clear all pages from multi-page document"""
        reply = QMessageBox.question(
            self,
            "Clear All Pages",
            f"Delete all {self.multi_page.get_page_count()} pages?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.multi_page.clear_all()
            self.page_thumbnails.clear_all()
            self.btn_export_pdf.setEnabled(False)
            self.btn_clear_pages.setEnabled(False)
            self.status_label.setText("All pages cleared")
    
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
