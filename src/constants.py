"""Configuration constants for the document scanner"""

# Standard document sizes (in pixels at 300 DPI)
DOCUMENT_SIZES = {
    'A4': (2480, 3508),
    'LETTER': (2550, 3300),
    'LEGAL': (2550, 4200),
    'A3': (3508, 4961),
}

# Image processing parameters
DEFAULT_BLUR_KERNEL = (5, 5)
DEFAULT_CANNY_THRESHOLD1 = 50
DEFAULT_CANNY_THRESHOLD2 = 150
MIN_DOCUMENT_AREA = 10000
APPROX_EPSILON_FACTOR = 0.02

# Resize settings for preview
MAX_PREVIEW_WIDTH = 800
MAX_PREVIEW_HEIGHT = 600

# Color modes
COLOR_MODE_BW = 'bw'
COLOR_MODE_GRAYSCALE = 'grayscale'
COLOR_MODE_COLOR = 'color'

# Output formats
FORMAT_PDF = 'pdf'
FORMAT_JPG = 'jpg'
FORMAT_PNG = 'png'
FORMAT_TIFF = 'tiff'

# File extensions
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']

# GUI constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
