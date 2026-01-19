# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-19

### Added - MVP Release
- Automatic document detection using edge detection and contour analysis
- Perspective correction for transforming angled photos to flat scans
- PyQt5-based graphical user interface
- Image enhancement features:
  - Black & White conversion with adaptive thresholding
  - Grayscale mode
  - Color preservation mode
  - Auto-enhancement
  - Brightness and contrast adjustment
- File input support for JPG, PNG, BMP, TIFF formats
- Save functionality with multiple output formats (PDF, JPG, PNG, TIFF)
- Real-time preview of original and processed images
- Detection visualization (corner markers on original image)
- Comprehensive test suite
- Full documentation (README, QUICKSTART, DEVELOPMENT guides)
- Setup scripts for easy installation (Linux/macOS/Windows)
- Configuration file (config.yaml) for customization

### Core Modules
- `scanner.py` - Document detection and scanning logic
- `image_processor.py` - Image enhancement algorithms
- `utils.py` - Utility functions
- `constants.py` - Configuration constants
- `main_window.py` - GUI implementation

### Documentation
- README.md - Project overview and installation guide
- QUICKSTART.md - 5-minute getting started guide
- DEVELOPMENT.md - Developer documentation
- License (MIT)

## [Unreleased]

### Planned for v1.1.0 (Phase 2)
- [ ] Camera integration with live preview
- [ ] Real-time document detection overlay
- [ ] Batch processing for multiple files
- [ ] Manual corner adjustment mode
- [ ] Additional enhancement options:
  - Deskew correction
  - Shadow removal
  - Color correction
  - Sharpness adjustment
- [ ] Multi-page PDF support
- [ ] Recent files list
- [ ] Settings persistence
- [ ] Keyboard shortcuts
- [ ] Dark theme support

### Planned for v2.0.0 (Phase 3)
- [ ] OCR text extraction
- [ ] Searchable PDF creation
- [ ] Cloud storage integration (Google Drive, Dropbox, OneDrive)
- [ ] Direct email functionality
- [ ] Document organization and tagging system
- [ ] Advanced search functionality
- [ ] User authentication for enterprise features
- [ ] Mobile app version (Android/iOS)

### Under Consideration
- Watch folder automation
- Scheduled scanning
- Custom processing pipelines
- Plugin system for extensions
- API for programmatic access
- Command-line interface

## Version History

### [1.0.0] - 2026-01-19
**First stable release** - MVP with core scanning functionality and GUI

---

## Contributing

See [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines on contributing to this project.

## Questions?

- Check the [README](README.md) for general information
- See [QUICKSTART](QUICKSTART.md) for usage examples
- Open an issue for bugs or feature requests
