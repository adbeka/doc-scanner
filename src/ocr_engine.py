"""
OCR (Optical Character Recognition) Engine
Extract text from scanned documents using Tesseract OCR
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from dataclasses import dataclass

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


@dataclass
class OCRResult:
    """Container for OCR results"""
    text: str
    confidence: float
    word_boxes: List[Dict]  # List of {text, confidence, box}
    lines: List[str]
    
    def get_clean_text(self) -> str:
        """Get cleaned text without extra whitespace"""
        return '\n'.join(line.strip() for line in self.lines if line.strip())
    
    def get_words(self) -> List[str]:
        """Get list of all words detected"""
        return [box['text'] for box in self.word_boxes if box['text'].strip()]


class OCREngine:
    """OCR engine for text extraction"""
    
    def __init__(self):
        """Initialize OCR engine"""
        self.available = TESSERACT_AVAILABLE
        
    def is_available(self) -> bool:
        """Check if OCR is available"""
        return self.available
    
    def extract_text(self, image: np.ndarray, lang: str = 'eng', 
                     preprocess: bool = True) -> OCRResult:
        """
        Extract text from image
        
        Args:
            image: Input image (numpy array)
            lang: Language code (e.g., 'eng', 'fra', 'spa')
            preprocess: Apply preprocessing for better OCR
            
        Returns:
            OCRResult object with text and metadata
        """
        if not self.available:
            raise RuntimeError("Tesseract OCR is not installed. Install with: pip install pytesseract")
        
        # Preprocess image if requested
        if preprocess:
            processed = self._preprocess_for_ocr(image)
        else:
            processed = image
        
        # Extract detailed data
        data = pytesseract.image_to_data(processed, lang=lang, output_type=pytesseract.Output.DICT)
        
        # Extract text
        text = pytesseract.image_to_string(processed, lang=lang)
        
        # Parse results
        word_boxes = []
        confidences = []
        lines = []
        current_line = []
        last_block = -1
        
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            confidence = int(data['conf'][i])
            text_item = data['text'][i].strip()
            
            if confidence > 0 and text_item:
                # Get bounding box
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                
                word_boxes.append({
                    'text': text_item,
                    'confidence': confidence,
                    'box': (x, y, w, h)
                })
                confidences.append(confidence)
                
                # Build lines
                block_num = data['block_num'][i]
                if block_num != last_block and current_line:
                    lines.append(' '.join(current_line))
                    current_line = []
                    last_block = block_num
                
                current_line.append(text_item)
        
        # Add last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return OCRResult(
            text=text,
            confidence=avg_confidence,
            word_boxes=word_boxes,
            lines=lines
        )
    
    def extract_text_simple(self, image: np.ndarray, lang: str = 'eng') -> str:
        """
        Extract text from image (simple version)
        
        Args:
            image: Input image
            lang: Language code
            
        Returns:
            Extracted text as string
        """
        if not self.available:
            raise RuntimeError("Tesseract OCR is not installed")
        
        processed = self._preprocess_for_ocr(image)
        return pytesseract.image_to_string(processed, lang=lang)
    
    def detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect regions containing text
        
        Args:
            image: Input image
            
        Returns:
            List of bounding boxes (x, y, w, h)
        """
        if not self.available:
            return []
        
        # Use tesseract to detect text regions
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        boxes = []
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 30:  # Confidence threshold
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                boxes.append((x, y, w, h))
        
        return boxes
    
    def auto_name_from_text(self, text: str, max_length: int = 50) -> str:
        """
        Generate filename from extracted text
        
        Args:
            text: Extracted text
            max_length: Maximum filename length
            
        Returns:
            Suggested filename
        """
        # Get first meaningful line
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            return "untitled"
        
        # Use first line or first few words
        name = lines[0]
        
        # Clean filename
        name = re.sub(r'[^\w\s-]', '', name)  # Remove special chars
        name = re.sub(r'\s+', '_', name)  # Replace spaces with underscore
        name = name[:max_length]  # Truncate
        name = name.strip('_')  # Remove leading/trailing underscores
        
        return name if name else "untitled"
    
    def search_text(self, image: np.ndarray, search_term: str, 
                    case_sensitive: bool = False) -> List[Dict]:
        """
        Search for specific text in image
        
        Args:
            image: Input image
            search_term: Text to search for
            case_sensitive: Whether search is case sensitive
            
        Returns:
            List of matches with bounding boxes
        """
        result = self.extract_text(image)
        matches = []
        
        search_lower = search_term if case_sensitive else search_term.lower()
        
        for box in result.word_boxes:
            text = box['text'] if case_sensitive else box['text'].lower()
            if search_lower in text:
                matches.append(box)
        
        return matches
    
    def _preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Resize if too small
        height, width = gray.shape
        if height < 300 or width < 300:
            scale = max(300 / height, 300 / width)
            gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast = clahe.apply(denoised)
        
        # Threshold
        _, binary = cv2.threshold(contrast, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary
    
    def extract_metadata(self, image: np.ndarray) -> Dict:
        """
        Extract common metadata patterns from text
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with detected metadata
        """
        result = self.extract_text(image)
        text = result.text
        
        metadata = {
            'dates': self._extract_dates(text),
            'emails': self._extract_emails(text),
            'phone_numbers': self._extract_phone_numbers(text),
            'urls': self._extract_urls(text),
            'amounts': self._extract_amounts(text)
        }
        
        return metadata
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract date patterns"""
        patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # MM/DD/YYYY
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',     # YYYY-MM-DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        ]
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        return dates
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(pattern, text)
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers"""
        pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\(\d{3}\)\s*\d{3}[-.]?\d{4}'
        return re.findall(pattern, text)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs"""
        pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(pattern, text)
    
    def _extract_amounts(self, text: str) -> List[str]:
        """Extract monetary amounts"""
        pattern = r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:USD|EUR|GBP)'
        return re.findall(pattern, text)
