#!/usr/bin/env python3
"""
Demonstration script for document templates and filters
Shows various templates and filters applied to sample images
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.templates import TemplateManager
from src.filters import FilterManager


def create_demo_image():
    """Create a demo document image for testing"""
    # Create a white background
    img = np.ones((1000, 800, 3), dtype=np.uint8) * 255
    
    # Add some text-like patterns
    for i in range(20, 900, 40):
        cv2.line(img, (50, i), (750, i), (0, 0, 0), 2)
    
    # Add a colored box (like a logo or image)
    img[100:200, 600:750] = [200, 150, 100]
    
    return img


def demonstrate_templates():
    """Demonstrate all available document templates"""
    print("=" * 60)
    print("DOCUMENT TEMPLATES DEMONSTRATION")
    print("=" * 60)
    
    # Create demo image
    demo_image = create_demo_image()
    
    # Get all available templates
    template_names = TemplateManager.get_template_names()
    
    print(f"\nAvailable templates ({len(template_names)}):")
    for i, name in enumerate(sorted(template_names), 1):
        display_name = name.replace('_', ' ').title()
        template = TemplateManager.get_template(name)
        print(f"  {i}. {display_name} - Size: {template.size}, "
              f"Mode: {template.settings.get('color_mode', 'N/A')}")
    
    print("\nApplying templates to demo image...")
    
    # Apply each template
    output_dir = Path("data/output/template_demos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for name in sorted(template_names):
        try:
            result = TemplateManager.apply_template(demo_image, name)
            output_path = output_dir / f"template_{name}.png"
            cv2.imwrite(str(output_path), result)
            print(f"  ✓ {name.replace('_', ' ').title()} -> {output_path}")
        except Exception as e:
            print(f"  ✗ {name}: {str(e)}")
    
    print(f"\nTemplate demos saved to: {output_dir}")


def demonstrate_filters():
    """Demonstrate all available image filters"""
    print("\n" + "=" * 60)
    print("IMAGE FILTERS DEMONSTRATION")
    print("=" * 60)
    
    # Create a more colorful demo image
    demo_image = np.zeros((400, 600, 3), dtype=np.uint8)
    
    # Add some colorful elements
    cv2.rectangle(demo_image, (50, 50), (200, 150), (255, 0, 0), -1)  # Blue
    cv2.rectangle(demo_image, (250, 50), (400, 150), (0, 255, 0), -1)  # Green
    cv2.rectangle(demo_image, (450, 50), (550, 150), (0, 0, 255), -1)  # Red
    cv2.circle(demo_image, (300, 250), 80, (255, 255, 0), -1)  # Cyan
    cv2.putText(demo_image, "FILTERS", (150, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    # Get all available filters
    filter_names = FilterManager.get_filter_names()
    
    print(f"\nAvailable filters ({len(filter_names)}):")
    for i, name in enumerate(sorted(filter_names), 1):
        display_name = name.replace('_', ' ').title()
        print(f"  {i}. {display_name}")
    
    print("\nApplying filters to demo image...")
    
    # Apply each filter
    output_dir = Path("data/output/filter_demos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save original
    cv2.imwrite(str(output_dir / "00_original.png"), demo_image)
    print(f"  ✓ Original -> {output_dir / '00_original.png'}")
    
    for name in sorted(filter_names):
        try:
            # Apply filter
            result = FilterManager.apply_filter(demo_image, name)
            output_path = output_dir / f"filter_{name}.png"
            cv2.imwrite(str(output_path), result)
            print(f"  ✓ {name.replace('_', ' ').title()} -> {output_path}")
        except Exception as e:
            print(f"  ✗ {name}: {str(e)}")
    
    print(f"\nFilter demos saved to: {output_dir}")


def demonstrate_combinations():
    """Demonstrate combining templates with filters"""
    print("\n" + "=" * 60)
    print("TEMPLATE + FILTER COMBINATIONS")
    print("=" * 60)
    
    demo_image = create_demo_image()
    output_dir = Path("data/output/combo_demos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Try some interesting combinations
    combinations = [
        ('text_document', 'document_scan'),
        ('receipt', 'high_contrast_bw'),
        ('business_card', 'vintage'),
        ('whiteboard', 'edge_enhance'),
        ('photo_document', 'sepia'),
    ]
    
    print("\nApplying template + filter combinations...")
    
    for template_name, filter_name in combinations:
        try:
            # Apply template first
            result = TemplateManager.apply_template(demo_image, template_name)
            # Then apply filter
            result = FilterManager.apply_filter(result, filter_name)
            
            output_path = output_dir / f"combo_{template_name}_{filter_name}.png"
            cv2.imwrite(str(output_path), result)
            
            template_display = template_name.replace('_', ' ').title()
            filter_display = filter_name.replace('_', ' ').title()
            print(f"  ✓ {template_display} + {filter_display} -> {output_path}")
        except Exception as e:
            print(f"  ✗ {template_name} + {filter_name}: {str(e)}")
    
    print(f"\nCombination demos saved to: {output_dir}")


def show_statistics():
    """Show statistics about available features"""
    print("\n" + "=" * 60)
    print("FEATURE STATISTICS")
    print("=" * 60)
    
    template_count = len(TemplateManager.get_template_names())
    filter_count = len(FilterManager.get_filter_names())
    
    print(f"\nTotal document templates: {template_count}")
    print(f"Total image filters: {filter_count}")
    print(f"Total combinations possible: {template_count * filter_count}")
    
    # Template categories
    templates = TemplateManager.get_template_names()
    doc_templates = [t for t in templates if any(x in t for x in ['text', 'invoice', 'book'])]
    id_templates = [t for t in templates if any(x in t for x in ['id', 'card', 'passport'])]
    
    print(f"\nTemplate categories:")
    print(f"  - Document templates: {len(doc_templates)}")
    print(f"  - ID/Card templates: {len(id_templates)}")
    print(f"  - Other templates: {len(templates) - len(doc_templates) - len(id_templates)}")
    
    # Filter categories
    filters = FilterManager.get_filter_names()
    artistic_filters = [f for f in filters if any(x in f for x in ['sepia', 'vintage', 'sketch', 'cartoon', 'oil'])]
    color_filters = [f for f in filters if any(x in f for x in ['warm', 'cool', 'invert'])]
    effect_filters = [f for f in filters if any(x in f for x in ['blur', 'pixelate', 'vignette', 'emboss'])]
    
    print(f"\nFilter categories:")
    print(f"  - Artistic filters: {len(artistic_filters)}")
    print(f"  - Color filters: {len(color_filters)}")
    print(f"  - Effect filters: {len(effect_filters)}")
    print(f"  - Document filters: {len([f for f in filters if 'document' in f])}")


def main():
    """Main demonstration function"""
    print("\n" + "=" * 60)
    print("DOC-SCANNER: TEMPLATES & FILTERS DEMONSTRATION")
    print("=" * 60)
    print("\nThis script demonstrates the new document templates and")
    print("image filters features added to the document scanner.\n")
    
    try:
        # Show statistics
        show_statistics()
        
        # Demonstrate templates
        demonstrate_templates()
        
        # Demonstrate filters
        demonstrate_filters()
        
        # Demonstrate combinations
        demonstrate_combinations()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("\nAll demo images have been saved to data/output/")
        print("You can view them to see the effects of templates and filters.")
        print("\nTo use these features in the GUI:")
        print("  1. Run: python main.py")
        print("  2. Load an image")
        print("  3. Scan the document")
        print("  4. Select a template from the 'Document Templates' section")
        print("  5. Apply filters from the 'Image Filters' section")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
