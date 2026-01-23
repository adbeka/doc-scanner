# Quick Start Guide - New Features

## 🚀 Three Powerful New Features Added!

---

## 1️⃣ Manual Edge Adjustment

**When to use**: Auto-detection missed the document edges or needs fine-tuning

### Steps:
```
1. Load Image  →  2. Click "Adjust Edges Manually"  →  3. Drag corners  →  4. Apply
```

### What you'll see:
- Interactive window with your image
- 4 colored corner handles (TL, TR, BR, BL)
- Green lines connecting corners
- Red highlight when dragging

### Tips:
✅ Drag from center of corner handle
✅ Use "Reset" button if you make a mistake
✅ Works even when auto-scan fails completely

---

## 2️⃣ Image Rotation

**When to use**: Document came out sideways or upside down

### Steps:
```
1. Scan Document  →  2. Look at Enhancement section  →  3. Click ⟲ or ⟳
```

### Buttons:
- **⟲ 90°** = Rotate counter-clockwise (left)
- **⟳ 90°** = Rotate clockwise (right)

### Tips:
✅ Click multiple times to rotate more
✅ All adjustments (brightness, contrast) are kept
✅ Works on already enhanced images

---

## 3️⃣ Batch Processing

**When to use**: You have multiple documents to scan at once

### Steps:
```
1. Organize images in folder
2. Click "Batch Process Folder"
3. Select input folder
4. Select output folder
5. Wait for processing
6. Check results!
```

### Settings Applied:
- ✓ Color Mode (B&W / Grayscale / Color)
- ✓ Output Format (PDF / JPG / PNG / TIFF)
- ✓ Brightness adjustment
- ✓ Contrast adjustment

### What happens:
```
Input:   photo_001.jpg, photo_002.jpg, photo_003.jpg
         ↓ ↓ ↓
Output:  photo_001_scanned_20260123_143052.pdf
         photo_002_scanned_20260123_143053.pdf
         photo_003_scanned_20260123_143054.pdf
```

### Tips:
✅ Set all settings BEFORE batch processing
✅ Progress bar shows which file is processing
✅ Can cancel anytime
✅ Results dialog shows success/failure count

---

## 📋 Complete Workflow Examples

### Example 1: Single Document with Manual Adjustment
```
Load Image
   ↓
Adjust Edges Manually (drag corners)
   ↓
Apply
   ↓
Rotate if needed (⟲ or ⟳)
   ↓
Adjust brightness/contrast
   ↓
Select color mode
   ↓
Save Result
```

### Example 2: Batch Process 50 Receipts
```
Put all receipt photos in folder
   ↓
Set: Color Mode = B&W
Set: Format = PDF
Set: Brightness = +20
   ↓
Click "Batch Process Folder"
   ↓
Select input folder
Select output folder
   ↓
Wait (shows "Processing 1/50: receipt_001.jpg")
   ↓
Done! 50 scanned PDFs ready
```

### Example 3: Fix Upside-Down Scan
```
Load Image
   ↓
Scan Document
   ↓
Oh no, it's upside down!
   ↓
Click ⟳ twice (rotate 180°)
   ↓
Perfect! Save Result
```

---

## 🎯 UI Layout Changes

```
┌─────────────────────────────────────────────────┐
│           DOCUMENT SCANNER                      │
├─────────────┬───────────────────────────────────┤
│  CONTROLS   │  IMAGE DISPLAY                    │
├─────────────┤                                   │
│ INPUT       │  ┌──────────────────────┐        │
│ [Load Image]│  │  Original Image      │        │
│ [Batch...] ← NEW │                      │        │
│ [Camera]    │  └──────────────────────┘        │
│             │                                   │
│ SCAN        │  ┌──────────────────────┐        │
│ [Scan Doc]  │  │  Scanned Document    │        │
│ [Adjust]   ← NEW │                      │        │
│             │  └──────────────────────┘        │
│ ENHANCE     │                                   │
│ Color: [▼]  │                                   │
│ Bright: [-] │                                   │
│ Contrast:[-]│                                   │
│ [Auto Enh]  │                                   │
│ Rotate:     │                                   │
│ [⟲][⟳]    ← NEW                               │
│             │                                   │
│ OUTPUT      │                                   │
│ Format:[▼]  │                                   │
│ [Save]      │                                   │
│             │                                   │
│ [Reset]     │                                   │
└─────────────┴───────────────────────────────────┘
```

---

## ⚡ Keyboard Shortcuts (Future Enhancement)

Currently, all operations require button clicks.
Future versions may include:
- `Ctrl+O` - Load Image
- `Ctrl+S` - Save Result
- `Ctrl+E` - Adjust Edges
- `Ctrl+R` - Rotate Right
- `Ctrl+Shift+R` - Rotate Left
- `Ctrl+B` - Batch Process

---

## 🐛 Troubleshooting

### Edge Adjustment Won't Open
**Problem**: Button is disabled
**Solution**: Load an image first

### Rotation Buttons Disabled
**Problem**: Not enabled
**Solution**: Scan a document first

### Batch Processing Fails
**Problem**: Some images don't process
**Solution**: Check error details in results dialog
- Ensure images contain visible documents
- Check image format is supported
- Verify document has clear edges

### Manual Corners Not Working
**Problem**: Can't drag corners
**Solution**: Click and hold on the colored circles

---

## 📊 Performance Expectations

| Feature | Speed | Notes |
|---------|-------|-------|
| Manual Edge Adjustment | Instant | Real-time dragging |
| Rotation | < 1 second | Very fast |
| Batch Processing | 1-2 sec/image | Depends on image size |

---

## 💡 Pro Tips

1. **Set settings before batch processing** - Can't change mid-batch
2. **Use manual edges for tricky documents** - Better than re-scanning
3. **Rotate before enhancing** - Saves time
4. **Organize input folders** - Makes batch processing easier
5. **Check progress** - Cancel if something looks wrong

---

*Happy scanning! 📄✨*
