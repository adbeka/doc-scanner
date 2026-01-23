"""Batch processing functionality for multiple documents"""

import os
from pathlib import Path
from typing import List, Optional, Callable, Dict
import cv2
import numpy as np
from datetime import datetime


class BatchProcessor:
    """Handle batch processing of multiple documents"""
    
    def __init__(self, scanner, image_processor):
        """
        Initialize batch processor.
        
        Args:
            scanner: DocumentScanner instance
            image_processor: ImageProcessor instance
        """
        self.scanner = scanner
        self.processor = image_processor
        self.results = []
        
    def process_folder(
        self,
        input_folder: str,
        output_folder: str,
        color_mode: str = 'color',
        output_format: str = 'pdf',
        progress_callback: Optional[Callable] = None,
        auto_enhance: bool = False,
        brightness: int = 0,
        contrast: int = 0
    ) -> Dict:
        """
        Process all images in a folder.
        
        Args:
            input_folder: Path to folder containing images
            output_folder: Path to save processed images
            color_mode: 'bw', 'grayscale', or 'color'
            output_format: Output format ('pdf', 'jpg', 'png', 'tiff')
            progress_callback: Function to call with progress updates (current, total, filename)
            auto_enhance: Apply auto enhancement
            brightness: Brightness adjustment (-100 to 100)
            contrast: Contrast adjustment (-100 to 100)
            
        Returns:
            Dictionary with success/failure counts and details
        """
        # Get all image files
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')
        image_files = []
        
        for file in os.listdir(input_folder):
            if file.lower().endswith(image_extensions):
                image_files.append(os.path.join(input_folder, file))
        
        if not image_files:
            return {
                'success': 0,
                'failed': 0,
                'total': 0,
                'details': [],
                'message': 'No image files found in folder'
            }
        
        # Create output folder if needed
        os.makedirs(output_folder, exist_ok=True)
        
        # Process each image
        results = {
            'success': 0,
            'failed': 0,
            'total': len(image_files),
            'details': []
        }
        
        for i, image_path in enumerate(image_files):
            filename = os.path.basename(image_path)
            
            # Update progress
            if progress_callback:
                progress_callback(i + 1, len(image_files), filename)
            
            try:
                # Process single image
                result = self.process_single_image(
                    image_path,
                    output_folder,
                    color_mode,
                    output_format,
                    auto_enhance,
                    brightness,
                    contrast
                )
                
                if result['success']:
                    results['success'] += 1
                    results['details'].append({
                        'filename': filename,
                        'status': 'success',
                        'output': result['output_path']
                    })
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'filename': filename,
                        'status': 'failed',
                        'error': result.get('error', 'Unknown error')
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['details'].append({
                    'filename': filename,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    def process_single_image(
        self,
        image_path: str,
        output_folder: str,
        color_mode: str = 'color',
        output_format: str = 'pdf',
        auto_enhance: bool = False,
        brightness: int = 0,
        contrast: int = 0
    ) -> Dict:
        """
        Process a single image.
        
        Args:
            image_path: Path to image file
            output_folder: Output directory
            color_mode: 'bw', 'grayscale', or 'color'
            output_format: Output format
            auto_enhance: Apply auto enhancement
            brightness: Brightness adjustment
            contrast: Contrast adjustment
            
        Returns:
            Dictionary with processing result
        """
        try:
            # Load image
            if not self.scanner.load_image(image_path):
                return {
                    'success': False,
                    'error': 'Failed to load image'
                }
            
            # Scan document
            scanned = self.scanner.scan_document()
            
            if scanned is None:
                return {
                    'success': False,
                    'error': 'Could not detect document'
                }
            
            # Apply enhancements
            result = scanned.copy()
            
            # Auto enhance
            if auto_enhance:
                result = self.processor.auto_enhance(result, mode='document')
            
            # Brightness/Contrast
            if brightness != 0 or contrast != 0:
                result = self.processor.adjust_brightness_contrast(
                    result, brightness, contrast
                )
            
            # Color mode
            if color_mode == 'bw':
                result = self.processor.convert_to_bw(result)
            elif color_mode == 'grayscale':
                if len(result.shape) == 3:
                    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            
            # Generate output filename
            input_filename = Path(image_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{input_filename}_scanned_{timestamp}.{output_format}"
            output_path = os.path.join(output_folder, output_filename)
            
            # Save result
            if cv2.imwrite(output_path, result):
                return {
                    'success': True,
                    'output_path': output_path
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to save image'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_multiple_files(
        self,
        image_paths: List[str],
        output_folder: str,
        color_mode: str = 'color',
        output_format: str = 'pdf',
        progress_callback: Optional[Callable] = None,
        auto_enhance: bool = False,
        brightness: int = 0,
        contrast: int = 0,
        combine_pdf: bool = False
    ) -> Dict:
        """
        Process multiple selected images.
        
        Args:
            image_paths: List of image file paths
            output_folder: Output directory
            color_mode: Color mode
            output_format: Output format
            progress_callback: Progress callback function
            auto_enhance: Apply auto enhancement
            brightness: Brightness adjustment
            contrast: Contrast adjustment
            combine_pdf: Combine all into single PDF (only if format is pdf)
            
        Returns:
            Dictionary with processing results
        """
        os.makedirs(output_folder, exist_ok=True)
        
        results = {
            'success': 0,
            'failed': 0,
            'total': len(image_paths),
            'details': [],
            'combined_pdf': None
        }
        
        processed_images = []
        
        for i, image_path in enumerate(image_paths):
            filename = os.path.basename(image_path)
            
            if progress_callback:
                progress_callback(i + 1, len(image_paths), filename)
            
            try:
                result = self.process_single_image(
                    image_path,
                    output_folder,
                    color_mode,
                    output_format,
                    auto_enhance,
                    brightness,
                    contrast
                )
                
                if result['success']:
                    results['success'] += 1
                    results['details'].append({
                        'filename': filename,
                        'status': 'success',
                        'output': result['output_path']
                    })
                    
                    if combine_pdf and output_format.lower() == 'pdf':
                        # Store for combining later
                        processed_images.append(result['output_path'])
                else:
                    results['failed'] += 1
                    results['details'].append({
                        'filename': filename,
                        'status': 'failed',
                        'error': result.get('error', 'Unknown error')
                    })
                    
            except Exception as e:
                results['failed'] += 1
                results['details'].append({
                    'filename': filename,
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Combine PDFs if requested (note: basic implementation, may need PyPDF2 for full support)
        if combine_pdf and processed_images and output_format.lower() == 'pdf':
            combined_path = os.path.join(
                output_folder,
                f"combined_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            results['combined_pdf'] = combined_path
            # Note: Actual PDF combination would require PyPDF2 or similar library
            # For now, we just note the intention
        
        return results
