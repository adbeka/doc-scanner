# Quick Reference: Templates and Filters

## Templates Quick List

| Template | Size | Mode | Best For |
|----------|------|------|----------|
| Text Document | A4 (2480x3508) | B&W | Letters, contracts, forms |
| Receipt | 800x1200 | B&W | Receipts, tickets |
| Business Card | 1050x600 | Color | Business cards |
| ID Card | 1280x810 | Color | ID cards, driver's licenses |
| Invoice | A4 (2480x3508) | B&W | Invoices, bills |
| Whiteboard | 1920x1080 | B&W | Whiteboard photos |
| Book Page | 5.5"x8.5" | B&W | Book scanning |
| Magazine | Letter (2550x3300) | Color | Magazines, brochures |
| Passport | 1398x1960 | Color | Passports, official docs |
| Photo Document | A4 (2480x3508) | Color | Mixed text/photos |

## Filters Quick List

| Category | Filters | Description |
|----------|---------|-------------|
| **Artistic** | Sepia | Classic vintage brown tone |
| | Vintage | Aged photo with vignette |
| | Sketch | Pencil drawing effect |
| | Oil Painting | Painterly artistic effect |
| | Cartoon | Comic book style |
| **Color** | Warm | Add red/yellow warm tones |
| | Cool | Add blue/cyan cool tones |
| | Invert | Negative image |
| | High Contrast B&W | Pure black & white |
| **Effects** | Emboss | 3D embossed relief |
| | Posterize | Reduce color levels |
| | Pixelate | Retro pixel art |
| | Vignette | Darkened edges |
| | Edge Enhance | Sharpen edges |
| **Blur** | Blur | Gaussian blur |
| | Motion Blur | Directional motion |
| **Document** | Document Scan | Optimized for documents |

## Common Combinations

### High Contrast Documents
1. Template: Text Document
2. Filter: High Contrast B&W

### Professional Receipts
1. Template: Receipt
2. Filter: Document Scan

### Artistic Business Cards
1. Template: Business Card
2. Filter: Vintage or Sepia

### Whiteboard Enhancement
1. Template: Whiteboard
2. Filter: Edge Enhance

### Old Document Style
1. Template: Text Document
2. Filter: Sepia or Vintage

## Code Snippets

### Apply Template
```python
from src.templates import TemplateManager

result = TemplateManager.apply_template(image, 'receipt')
```

### Apply Filter
```python
from src.filters import FilterManager

result = FilterManager.apply_filter(image, 'sepia')
```

### Apply Both
```python
# Template first
result = TemplateManager.apply_template(image, 'business_card')
# Then filter
result = FilterManager.apply_filter(result, 'vintage')
```

### Custom Template
```python
custom = TemplateManager.create_custom_template(
    name='my_template',
    size=(1000, 1000),
    settings={
        'color_mode': 'bw',
        'enhance_contrast': True,
        'sharpen': True,
        'brightness': 10
    }
)
result = custom.apply(image)
```

### Multiple Filters
```python
filters = [
    ('blur', {'sigma': 3}),
    ('sepia', {}),
    ('vignette', {'intensity': 0.5})
]
result = FilterManager.apply_multiple_filters(image, filters)
```

## Performance Tips

- ✅ Templates resize images (can be slow for large images)
- ✅ Lightweight filters: invert, blur, sepia, warm, cool
- ⚠️ Medium filters: edge_enhance, emboss, sketch
- ⚠️ Heavy filters: cartoon, oil_painting (1-3 seconds)
- ✅ Document scan filter is optimized for speed

## Batch Processing

Apply templates/filters to multiple images:

```python
from src.batch_processor import BatchProcessor

processor = BatchProcessor(scanner, image_processor)

# Process folder with template
processor.process_folder(
    input_folder='images/',
    output_folder='output/',
    template='receipt'
)
```

## GUI Keyboard Shortcuts (Planned)

- `Ctrl+T` - Apply Template
- `Ctrl+F` - Apply Filter
- `Ctrl+Z` - Undo
- `Ctrl+S` - Save Result

## File Locations

- Templates: `src/templates.py`
- Filters: `src/filters.py`
- Tests: `tests/test_templates.py`, `tests/test_filters.py`
- Demo: `demo_features.py`
- Documentation: `TEMPLATES_AND_FILTERS.md`
- Generated demos: `data/output/*_demos/`

## Getting Help

- Full documentation: [TEMPLATES_AND_FILTERS.md](TEMPLATES_AND_FILTERS.md)
- Run demo: `python demo_features.py`
- Run tests: `pytest tests/test_templates.py tests/test_filters.py`
- Issues: Create an issue on GitHub

## Version Info

- Templates: 10 built-in + custom support
- Filters: 17 built-in
- Total combinations: 170+
- Tests: 31 (all passing ✅)
- Python: 3.8+
- Dependencies: OpenCV, NumPy
