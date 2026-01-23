# New Features Added - January 23, 2026

## 🎉 Three Major Features Implemented

### 1. ✂️ Manual Edge Adjustment

**Description**: Interactive corner adjustment for perfect document detection

**How to Use**:
1. Load an image
2. Click "Adjust Edges Manually" button
3. A new window opens showing your image with corner handles
4. Drag the corner handles (TL, TR, BR, BL) to match document edges precisely
5. Click "Apply" to scan with adjusted edges
6. Click "Reset" to restore auto-detected corners

**Features**:
- Visual feedback with colored handles
- Real-time preview of edge positions
- Smooth dragging with mouse
- Corner labels for easy identification
- Works even when auto-detection fails

**Use Cases**:
- Documents with poor contrast
- Complex backgrounds
- Partial documents in frame
- Fine-tuning auto-detected edges

---

### 2. 🔄 Image Rotation

**Description**: Rotate scanned documents in 90° increments

**How to Use**:
1. Scan a document first
2. Use rotation buttons in the Enhancement section:
   - **⟲ 90°**: Rotate counter-clockwise
   - **⟳ 90°**: Rotate clockwise
3. Rotation applies immediately to the scanned image
4. All enhancements (brightness, contrast, color mode) are preserved

**Features**:
- Quick 90° incremental rotation
- Maintains image quality
- Preserves current enhancements
- Visual feedback in status bar

**Use Cases**:
- Incorrectly oriented documents
- Landscape vs portrait orientation
- Multi-page documents with mixed orientations

---

### 3. 📚 Batch Processing

**Description**: Process multiple documents from a folder automatically

**How to Use**:
1. Click "Batch Process Folder" button
2. Select folder containing images to scan
3. Select output folder for processed documents
4. All current settings are applied:
   - Color mode (B&W, Grayscale, Color)
   - Output format (PDF, JPG, PNG, TIFF)
   - Brightness and contrast adjustments
5. Progress dialog shows processing status
6. Results summary shows success/failure counts

**Features**:
- Process entire folders at once
- Progress tracking with cancellation option
- Applies current enhancement settings to all images
- Automatic timestamp in output filenames
- Detailed error reporting for failed scans
- Preserves original filenames

**Settings Applied**:
- Color mode selection
- Output format
- Brightness adjustment
- Contrast adjustment
- Auto-enhancement (if enabled)

**Use Cases**:
- Scanning multiple receipts
- Processing document archives
- Batch converting photos to PDFs
- Standardizing document formats

**Output Format**:
- Filename: `{original_name}_scanned_{timestamp}.{format}`
- Example: `receipt_001_scanned_20260123_143052.pdf`

---

## Technical Implementation

### Files Created:
- `gui/edge_adjuster.py` - Interactive edge adjustment widget and dialog
- `src/batch_processor.py` - Batch processing engine

### Files Modified:
- `gui/main_window.py` - Added UI controls and methods for all features
- `src/image_processor.py` - Added rotation function

### New Methods:
- `ImageProcessor.rotate_image()` - Rotate by 90°, 180°, or 270°
- `MainWindow.adjust_edges_manually()` - Open edge adjustment dialog
- `MainWindow.rotate_image()` - Rotate scanned image
- `MainWindow.batch_process()` - Batch process folder
- `BatchProcessor.process_folder()` - Process all images in folder
- `BatchProcessor.process_single_image()` - Process one image
- `EdgeAdjusterWidget` - Interactive corner dragging widget
- `EdgeAdjusterDialog` - Dialog wrapper for edge adjustment

---

## UI Changes

### New Buttons:
1. **Input Section**:
   - "Batch Process Folder" - Triggers batch processing

2. **Scan Section**:
   - "Adjust Edges Manually" - Opens edge adjustment dialog

3. **Enhancement Section**:
   - "⟲ 90°" - Rotate counter-clockwise
   - "⟳ 90°" - Rotate clockwise

### Button States:
- Edge adjustment enabled when image is loaded
- Rotation buttons enabled after successful scan
- All buttons properly disabled/enabled based on application state

---

## Usage Tips

### Manual Edge Adjustment:
- Start with auto-detection, then fine-tune if needed
- Drag corners from center of the handle
- Zoom in browser if corners are too close
- Use Reset button to start over

### Batch Processing:
- Organize images in a dedicated input folder
- Ensure all images are in supported formats
- Set desired settings BEFORE starting batch
- Monitor progress dialog for any failures
- Check output folder for results

### Rotation:
- Rotate immediately after scanning for best results
- Multiple rotations are cumulative
- Re-scan if rotation quality degrades

---

## Future Enhancements

Potential improvements for these features:

1. **Edge Adjustment**:
   - Zoom controls for precise placement
   - Snap-to-edge functionality
   - Keyboard shortcuts for corner selection

2. **Rotation**:
   - Arbitrary angle rotation (e.g., 45°)
   - Auto-rotation based on text detection
   - Flip horizontal/vertical

3. **Batch Processing**:
   - Multi-page PDF compilation
   - Resume interrupted batches
   - Preview before processing
   - Custom naming templates
   - Parallel processing for speed

---

## Error Handling

All features include robust error handling:
- Clear error messages in dialogs
- Status updates in status bar
- Graceful failure handling
- Cancellation support for batch operations

---

## Performance Notes

- **Edge Adjustment**: Real-time performance with smooth dragging
- **Rotation**: Instant for 90° increments
- **Batch Processing**: Processes sequentially (1-2 seconds per image typically)

---

*These features significantly enhance the document scanner's capabilities and user experience!*
