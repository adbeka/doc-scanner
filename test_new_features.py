"""
Quick test script for new features
Tests OCR, Auto Enhancement, Annotations, and Document Comparison
"""

import cv2
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ocr_engine import OCREngine
from src.auto_enhance import AutoEnhancer
from src.annotations import AnnotationTools
from src.document_compare import DocumentComparator


def create_test_image():
    """Create a simple test image with text"""
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Add some text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "INVOICE #12345", (50, 100), font, 2, (0, 0, 0), 3)
    cv2.putText(img, "Date: 2026-01-29", (50, 200), font, 1, (0, 0, 0), 2)
    cv2.putText(img, "Amount: $1,234.56", (50, 300), font, 1, (0, 0, 0), 2)
    cv2.putText(img, "Email: test@example.com", (50, 400), font, 1, (0, 0, 0), 2)
    
    # Add a rectangle for scanning
    cv2.rectangle(img, (40, 50), (760, 550), (0, 0, 0), 2)
    
    return img


def test_ocr():
    """Test OCR functionality"""
    print("\n" + "="*60)
    print("TESTING OCR ENGINE")
    print("="*60)
    
    ocr = OCREngine()
    
    if not ocr.is_available():
        print("❌ OCR not available (Tesseract not installed)")
        print("   Install with: pip install pytesseract")
        print("   And install Tesseract from: https://github.com/tesseract-ocr/tesseract")
        return False
    
    print("✅ OCR engine available")
    
    # Create test image
    img = create_test_image()
    
    # Extract text
    try:
        result = ocr.extract_text_simple(img)
        print(f"\n📝 Extracted text preview:")
        print("-" * 40)
        print(result[:200] if len(result) > 200 else result)
        print("-" * 40)
        
        # Test auto-naming
        name = ocr.auto_name_from_text(result)
        print(f"\n🏷️  Suggested filename: {name}")
        
        # Test metadata extraction
        metadata = ocr.extract_metadata(img)
        print(f"\n📊 Metadata extracted:")
        for key, values in metadata.items():
            if values:
                print(f"   {key}: {values}")
        
        print("✅ OCR tests passed")
        return True
        
    except Exception as e:
        print(f"❌ OCR test failed: {e}")
        return False


def test_auto_enhance():
    """Test auto enhancement features"""
    print("\n" + "="*60)
    print("TESTING AUTO ENHANCEMENT")
    print("="*60)
    
    enhancer = AutoEnhancer()
    
    # Create tilted test image
    img = create_test_image()
    
    # Rotate slightly to test deskew
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), 5, 1.0)  # 5 degree tilt
    tilted = cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))
    
    try:
        # Test deskew
        deskewed, angle = enhancer.auto_deskew(tilted)
        print(f"✅ Deskew: Detected angle = {angle:.2f}°")
        
        # Test crop
        # Add borders
        bordered = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        cropped = enhancer.auto_crop(bordered)
        print(f"✅ Auto crop: {bordered.shape} -> {cropped.shape}")
        
        # Test full enhancement
        enhanced = enhancer.enhance_document(img)
        print(f"✅ Full enhancement: Applied all enhancements")
        
        print("✅ All auto enhancement tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Auto enhancement test failed: {e}")
        return False


def test_annotations():
    """Test annotation tools"""
    print("\n" + "="*60)
    print("TESTING ANNOTATIONS")
    print("="*60)
    
    annotator = AnnotationTools()
    img = create_test_image()
    
    try:
        # Test text annotation
        annotated = annotator.add_text(img, "DRAFT", (600, 100), font_scale=1.5, background=True)
        print("✅ Text annotation added")
        
        # Test rectangle
        annotated = annotator.add_rectangle(annotated, (100, 150), (300, 250), color=(255, 0, 0))
        print("✅ Rectangle annotation added")
        
        # Test highlight
        annotated = annotator.add_highlight(annotated, (50, 350, 400, 50), alpha=0.3)
        print("✅ Highlight annotation added")
        
        # Test stamp
        annotated = annotator.add_stamp(annotated, "approved", (650, 450), size=80)
        print("✅ Stamp annotation added")
        
        # Test date stamp
        annotated = annotator.add_date_stamp(annotated, (50, 550))
        print("✅ Date stamp added")
        
        # Check annotations stored
        annotations = annotator.get_annotations()
        print(f"✅ {len(annotations)} annotations stored")
        
        print("✅ All annotation tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Annotation test failed: {e}")
        return False


def test_comparison():
    """Test document comparison"""
    print("\n" + "="*60)
    print("TESTING DOCUMENT COMPARISON")
    print("="*60)
    
    comparator = DocumentComparator()
    
    # Create two similar images
    img1 = create_test_image()
    img2 = create_test_image()
    
    # Modify img2 slightly
    cv2.putText(img2, "MODIFIED", (400, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.rectangle(img2, (500, 200), (700, 300), (0, 255, 0), 3)
    
    try:
        # Test comparison
        comparison, differences = comparator.compare_documents(img1, img2)
        print(f"✅ Comparison completed: {len(differences)} differences found")
        
        # Test similarity
        similarity = comparator.calculate_similarity(img1, img2)
        print(f"✅ Similarity score: {similarity:.2f}%")
        
        # Test side-by-side
        side_by_side = comparator.compare_side_by_side(img1, img2)
        print(f"✅ Side-by-side view created: {side_by_side.shape}")
        
        # Test summary
        summary = comparator.get_difference_summary(differences)
        print(f"✅ Difference summary: {summary}")
        
        # Test report
        report = comparator.generate_comparison_report(img1, img2, differences)
        print(f"✅ Report generated: {len(report)} characters")
        
        print("✅ All comparison tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("NEW FEATURES TEST SUITE")
    print("="*60)
    
    results = {
        'OCR': test_ocr(),
        'Auto Enhancement': test_auto_enhance(),
        'Annotations': test_annotations(),
        'Document Comparison': test_comparison()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    for feature, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{feature:.<40} {status}")
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Features are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check error messages above.")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
