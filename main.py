#!/usr/bin/env python3
"""
Document Scanner Application
Main entry point for the document scanner application.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import main

if __name__ == '__main__':
    main()
