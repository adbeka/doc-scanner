# Document Templates and Filters

## Overview

The doc-scanner application now includes powerful document templates and image filters to help you process and enhance your scanned documents.

## Document Templates

Document templates are predefined processing profiles optimized for different document types. Each template automatically adjusts size, color mode, contrast, sharpness, and other parameters for optimal results.

### Available Templates

#### Document Templates
- **Text Document** (A4, 300 DPI)
  - Optimized for text-heavy documents
  - Black & white with adaptive thresholding
  - High brightness and contrast for clear text

- **Invoice** (A4, 300 DPI)
  - Professional document scanning
  - Otsu thresholding for crisp text
  - Enhanced for tabular data

- **Book Page** (5.5" x 8.5", 300 DPI)
  - Ideal for scanning book pages
  - Preserves text clarity
  - Minimal noise for clean reading

#### ID/Card Templates
- **ID Card** (1280x810)
  - Full color preservation
  - Enhanced for photos and text
  - Optimal for government IDs

- **Business Card** (1050x600)
  - Standard business card dimensions
  - Color mode for logos and designs
  - Sharp text rendering

- **Passport** (Standard passport size)
  - Full color for official documents
  - High quality for photos
  - Detail preservation

#### Specialized Templates
- **Receipt** (800x1200)
  - Optimized for thermal paper receipts
  - High contrast black & white
  - Enhanced readability for faded receipts

- **Whiteboard** (1920x1080)
  - Removes background tones
  - High contrast for marker text
  - Enhanced for photos of whiteboards

- **Photo Document** (A4, 300 DPI)
  - Preserves color and detail
  - Balanced enhancement
  - Ideal for mixed photo/text documents

- **Magazine** (Letter size, 300 DPI)
  - Full color preservation
  - Enhanced for glossy photos
  - Balanced saturation

### Using Templates

#### In the GUI
1. Load and scan your document
2. Select a template from the "Document Templates" dropdown
3. Click "Apply Template"
4. The template settings will be automatically applied

#### In Code
```python
from src.templates import TemplateManager

# Apply a template
result = TemplateManager.apply_template(image, 'receipt')

# Get available templates
templates = TemplateManager.get_template_names()

# Create custom template
custom = TemplateManager.create_custom_template(
    name='my_template',
    size=(1000, 1000),
    settings={
        'color_mode': 'bw',
        'enhance_contrast': True,
        'sharpen': True
    }
)
```

## Image Filters

Image filters apply visual effects and enhancements to your documents. Filters can be combined with templates for powerful processing workflows.

### Available Filters

#### Artistic Filters
- **Sepia** - Classic brownish vintage tone
- **Vintage** - Aged photograph effect with vignette
- **Sketch** - Pencil sketch drawing effect
- **Oil Painting** - Painterly artistic effect
- **Cartoon** - Comic book style rendering

#### Color Filters
- **Invert** - Negative image effect
- **Warm** - Add warm tones (red/yellow)
- **Cool** - Add cool tones (blue/cyan)
- **High Contrast B&W** - Pure black and white

#### Effect Filters
- **Emboss** - 3D embossed effect
- **Posterize** - Reduce color levels
- **Pixelate** - Retro pixel art effect
- **Vignette** - Darkened edges spotlight effect
- **Edge Enhance** - Sharpen edges and details

#### Blur Filters
- **Blur** - Artistic Gaussian blur
- **Motion Blur** - Directional motion effect

#### Document Filters
- **Document Scan** - Specialized document enhancement
  - Combines denoising, contrast enhancement, and thresholding
  - Optimized for maximum text clarity

### Using Filters

#### In the GUI
1. After scanning your document
2. Select a filter from the "Image Filters" dropdown
3. Click "Apply Filter"
4. Multiple filters can be applied sequentially

#### In Code
```python
from src.filters import FilterManager

# Apply a single filter
result = FilterManager.apply_filter(image, 'sepia')

# Apply filter with parameters
result = FilterManager.apply_filter(
    image, 
    'warm', 
    intensity=0.5
)

# Apply multiple filters
filters = [
    ('blur', {'sigma': 3}),
    ('edge_enhance', {'strength': 1.5}),
    ('sepia', {})
]
result = FilterManager.apply_multiple_filters(image, filters)

# Get available filters
filters = FilterManager.get_filter_names()
```

## Workflow Examples

### Example 1: Receipt Processing
```python
# Load image
scanner.load_image('receipt.jpg')

# Scan document
scanned = scanner.scan_document()

# Apply receipt template
result = TemplateManager.apply_template(scanned, 'receipt')

# Optional: Additional high contrast
result = FilterManager.apply_filter(result, 'high_contrast_bw')
```

### Example 2: Artistic Document
```python
# Scan document
scanned = scanner.scan_document(image)

# Apply photo document template
result = TemplateManager.apply_template(scanned, 'photo_document')

# Add vintage effect
result = FilterManager.apply_filter(result, 'vintage')

# Add vignette
result = FilterManager.apply_filter(result, 'vignette', intensity=0.6)
```

### Example 3: Whiteboard Enhancement
```python
# Scan whiteboard photo
scanned = scanner.scan_document(whiteboard_image)

# Apply whiteboard template
result = TemplateManager.apply_template(scanned, 'whiteboard')

# Optional: Enhance edges
result = FilterManager.apply_filter(result, 'edge_enhance', strength=1.2)
```

## Customization

### Creating Custom Templates

You can create custom templates for your specific needs:

```python
custom_template = TemplateManager.create_custom_template(
    name='custom_legal_doc',
    size=(2550, 4200),  # Legal size at 300 DPI
    settings={
        'color_mode': 'bw',
        'threshold_method': 'adaptive',
        'enhance_contrast': True,
        'contrast_clip_limit': 2.8,
        'sharpen': True,
        'sharpen_strength': 1.2,
        'denoise': True,
        'denoise_strength': 3,
        'brightness': 15,
        'contrast': 20
    }
)

# Apply your custom template
result = custom_template.apply(image)
```

### Template Settings Reference

Available settings for custom templates:

| Setting | Type | Description |
|---------|------|-------------|
| `resize` | bool | Whether to resize to template size |
| `color_mode` | str | 'color', 'grayscale', or 'bw' |
| `threshold_method` | str | 'adaptive' or 'otsu' (for B&W) |
| `enhance_contrast` | bool | Apply contrast enhancement |
| `contrast_clip_limit` | float | CLAHE clip limit (1.0-4.0) |
| `sharpen` | bool | Apply sharpening |
| `sharpen_strength` | float | Sharpening amount (0.5-2.0) |
| `denoise` | bool | Apply denoising |
| `denoise_strength` | int | Denoising strength (1-10) |
| `brightness` | int | Brightness adjustment (-100 to 100) |
| `contrast` | int | Contrast adjustment (-100 to 100) |

## Performance Considerations

- Templates resize images, which may take time for large images
- Some filters (like oil painting, cartoon) are computationally intensive
- For batch processing, choose lighter filters for faster processing
- Document scan filter is optimized for speed and quality

## Tips and Best Practices

1. **Start with templates** - Templates provide a good baseline for document types
2. **Add filters for style** - Use filters after templates for artistic effects
3. **Experiment with combinations** - Different template+filter combos yield unique results
4. **Use document scan filter** - For maximum text clarity on any document
5. **Save originals** - Always keep a copy of the original scan before applying filters
6. **Batch processing** - Apply the same template+filter to multiple documents at once

## Troubleshooting

### Template Issues
- **Image too large/small**: Templates automatically resize, but check output dimensions
- **Lost details**: Try 'photo_document' template or reduce enhancement settings
- **Too dark/bright**: Adjust brightness slider after applying template

### Filter Issues
- **Unexpected results**: Some filters assume color input, may need color image
- **Slow processing**: Oil painting and cartoon filters are slow on large images
- **Crashes**: Very large images may need to be resized before applying filters

## Command Line Demo

Run the demonstration script to see all templates and filters in action:

```bash
python demo_features.py
```

This will create sample outputs showing all templates and filters applied to demo images.

## Integration with Batch Processing

Templates and filters can be used in batch processing workflows. See the batch processor documentation for details on applying templates and filters to multiple documents.
