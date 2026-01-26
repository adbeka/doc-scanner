"""Multi-page document manager for creating multi-page PDFs"""

import numpy as np
from typing import List, Optional, Dict
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import cv2


class Page:
    """Represents a single page in a multi-page document"""
    
    def __init__(self, image: np.ndarray, name: str = "", page_number: int = 1):
        """
        Initialize a page.
        
        Args:
            image: Page image
            name: Page name/description
            page_number: Page number
        """
        self.image = image.copy() if image is not None else None
        self.name = name or f"Page {page_number}"
        self.page_number = page_number
        self.timestamp = datetime.now()
        
    def get_image(self) -> Optional[np.ndarray]:
        """Get image copy"""
        return self.image.copy() if self.image is not None else None
    
    def get_thumbnail(self, size: tuple = (150, 200)) -> Optional[np.ndarray]:
        """
        Get thumbnail version of page.
        
        Args:
            size: Thumbnail size (width, height)
            
        Returns:
            Thumbnail image
        """
        if self.image is None:
            return None
        
        # Calculate aspect ratio
        h, w = self.image.shape[:2]
        aspect = w / h
        
        if aspect > size[0] / size[1]:
            # Width is limiting
            new_w = size[0]
            new_h = int(new_w / aspect)
        else:
            # Height is limiting
            new_h = size[1]
            new_w = int(new_h * aspect)
        
        thumbnail = cv2.resize(self.image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return thumbnail


class MultiPageManager:
    """Manages multiple pages for multi-page PDF creation"""
    
    def __init__(self):
        """Initialize multi-page manager"""
        self.pages: List[Page] = []
        self.current_page_index = -1
        
    def add_page(self, image: np.ndarray, name: str = "") -> int:
        """
        Add a new page.
        
        Args:
            image: Page image
            name: Optional page name
            
        Returns:
            Index of added page
        """
        page_number = len(self.pages) + 1
        page = Page(image, name or f"Page {page_number}", page_number)
        self.pages.append(page)
        self.current_page_index = len(self.pages) - 1
        return self.current_page_index
    
    def remove_page(self, index: int) -> bool:
        """
        Remove a page.
        
        Args:
            index: Page index to remove
            
        Returns:
            True if successful
        """
        if 0 <= index < len(self.pages):
            self.pages.pop(index)
            # Update page numbers
            for i, page in enumerate(self.pages):
                page.page_number = i + 1
                if not page.name.startswith("Page "):
                    # Keep custom names
                    pass
                else:
                    page.name = f"Page {i + 1}"
            
            # Adjust current index
            if self.current_page_index >= len(self.pages):
                self.current_page_index = len(self.pages) - 1
            
            return True
        return False
    
    def move_page(self, from_index: int, to_index: int) -> bool:
        """
        Move a page to a new position.
        
        Args:
            from_index: Source index
            to_index: Destination index
            
        Returns:
            True if successful
        """
        if 0 <= from_index < len(self.pages) and 0 <= to_index < len(self.pages):
            page = self.pages.pop(from_index)
            self.pages.insert(to_index, page)
            
            # Update page numbers
            for i, p in enumerate(self.pages):
                p.page_number = i + 1
            
            self.current_page_index = to_index
            return True
        return False
    
    def get_page(self, index: int) -> Optional[Page]:
        """Get page at index"""
        if 0 <= index < len(self.pages):
            return self.pages[index]
        return None
    
    def get_current_page(self) -> Optional[Page]:
        """Get currently selected page"""
        return self.get_page(self.current_page_index)
    
    def set_current_page(self, index: int):
        """Set current page index"""
        if 0 <= index < len(self.pages):
            self.current_page_index = index
    
    def get_page_count(self) -> int:
        """Get total number of pages"""
        return len(self.pages)
    
    def clear_all(self):
        """Remove all pages"""
        self.pages = []
        self.current_page_index = -1
    
    def update_page_image(self, index: int, image: np.ndarray) -> bool:
        """
        Update image for a specific page.
        
        Args:
            index: Page index
            image: New image
            
        Returns:
            True if successful
        """
        if 0 <= index < len(self.pages):
            self.pages[index].image = image.copy()
            return True
        return False
    
    def export_to_pdf(self, output_path: str, page_size: str = 'A4') -> bool:
        """
        Export all pages to a multi-page PDF.
        
        Args:
            output_path: Output PDF file path
            page_size: Page size ('A4' or 'Letter')
            
        Returns:
            True if successful
        """
        if not self.pages:
            return False
        
        try:
            # Set page size
            if page_size.upper() == 'A4':
                ps = A4
            else:
                ps = letter
            
            # Create PDF canvas
            c = canvas.Canvas(output_path, pagesize=ps)
            page_width, page_height = ps
            
            for page in self.pages:
                if page.image is None:
                    continue
                
                # Convert OpenCV image to PIL Image
                if len(page.image.shape) == 3:
                    # BGR to RGB
                    rgb_image = cv2.cvtColor(page.image, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_image)
                else:
                    # Grayscale
                    pil_image = Image.fromarray(page.image)
                
                # Calculate image dimensions to fit page
                img_width, img_height = pil_image.size
                aspect = img_width / img_height
                
                # Add margins
                margin = 36  # 0.5 inch margins
                available_width = page_width - 2 * margin
                available_height = page_height - 2 * margin
                
                # Calculate size to fit
                if aspect > available_width / available_height:
                    # Width is limiting
                    draw_width = available_width
                    draw_height = available_width / aspect
                else:
                    # Height is limiting
                    draw_height = available_height
                    draw_width = available_height * aspect
                
                # Center image on page
                x = (page_width - draw_width) / 2
                y = (page_height - draw_height) / 2
                
                # Draw image
                c.drawImage(ImageReader(pil_image), x, y, 
                           width=draw_width, height=draw_height)
                
                # Add page number at bottom
                c.setFont("Helvetica", 10)
                c.drawCentredString(page_width / 2, 20, 
                                   f"Page {page.page_number} of {len(self.pages)}")
                
                # Create new page for next image
                c.showPage()
            
            # Save PDF
            c.save()
            return True
            
        except Exception as e:
            print(f"Error exporting PDF: {e}")
            return False
    
    def export_pages_as_images(self, output_folder: str, format: str = 'png') -> Dict:
        """
        Export all pages as individual images.
        
        Args:
            output_folder: Output folder path
            format: Image format ('png', 'jpg', 'tiff')
            
        Returns:
            Dictionary with results
        """
        os.makedirs(output_folder, exist_ok=True)
        
        results = {
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for i, page in enumerate(self.pages):
            if page.image is None:
                results['failed'] += 1
                continue
            
            filename = f"page_{i+1:03d}.{format}"
            filepath = os.path.join(output_folder, filename)
            
            try:
                cv2.imwrite(filepath, page.image)
                results['success'] += 1
                results['files'].append(filepath)
            except Exception as e:
                print(f"Error saving page {i+1}: {e}")
                results['failed'] += 1
        
        return results
    
    def get_page_info(self) -> List[Dict]:
        """
        Get information about all pages.
        
        Returns:
            List of page info dictionaries
        """
        info = []
        for i, page in enumerate(self.pages):
            info.append({
                'index': i,
                'number': page.page_number,
                'name': page.name,
                'timestamp': page.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'has_image': page.image is not None,
                'size': page.image.shape if page.image is not None else None
            })
        return info
