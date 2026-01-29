# Quick Reference: New Features

## 🔤 OCR (Text Recognition)

### Extract Text
**Button**: 📝 Extract Text  
**What it does**: Extracts all text from your scanned document  
**When to use**: When you need to copy text, search content, or convert to digital text

**Steps**:
1. Scan your document first
2. Click "Extract Text"
3. View text in dialog window
4. Click "Copy to Clipboard" if needed

### Auto-Name File
**Button**: 🏷️ Auto-Name File  
**What it does**: Suggests filename based on document content  
**When to use**: When organizing many scanned documents

**Steps**:
1. Scan your document first
2. Click "Auto-Name File"
3. Review/edit suggested name
4. File is automatically saved with that name

---

## ✨ Auto Enhancement

### Auto Deskew
**Button**: 📐 Auto Deskew  
**What it does**: Automatically straightens tilted documents (up to 10°)  
**When to use**: When document photo is at an angle

### Auto Crop  
**Button**: ✂️ Auto Crop  
**What it does**: Removes white borders and unnecessary margins  
**When to use**: When scan has extra whitespace around it

### Full Auto Enhancement
**Button**: ✨ Full Auto Enhancement  
**What it does**: Complete optimization pipeline:
- Straightens document
- Crops borders
- Fixes white balance
- Removes shadows
- Enhances contrast
- Sharpens image

**When to use**: For quick, professional results in one click

---

## 📝 Annotations

**Dropdown**: Select annotation type  
**Button**: ➕ Add Annotation  
**Button**: Clear Annotations

### Available Annotations

| Annotation | Use Case | Example |
|------------|----------|---------|
| **Add Text** | Add notes or labels | "Please review section 3" |
| **Add Rectangle** | Highlight areas | Draw box around important section |
| **Add Highlight** | Emphasize text | Yellow highlight over key points |
| **Add Arrow** | Point to specific areas | Arrow pointing to signature line |
| **Add Stamp** | Official markings | APPROVED, CONFIDENTIAL, DRAFT |
| **Add Date** | Timestamp document | Current date/time stamp |

### Stamps Available
- APPROVED ✅
- REJECTED ❌
- CONFIDENTIAL 🔒
- DRAFT 📝
- URGENT ⚡
- COPY 📄
- VOID ⭕
- RECEIVED 📨

---

## 🔍 Document Comparison

### Load Comparison Document
**Button**: 📊 Load Document to Compare  
**What it does**: Loads a second version of the document  
**When to use**: When you want to compare two versions

### Compare Documents
**Button**: 🔍 Compare Documents  
**What it does**: 
- Shows side-by-side comparison
- Highlights differences in red boxes
- Calculates similarity percentage
- Generates detailed report

**When to use**: 
- Quality assurance
- Version control
- Proofreading edits
- Detecting changes

**Report includes**:
- Similarity percentage
- Number of differences
- Types of changes (added/removed/modified)
- Location of each difference

---

## 📋 Workflows

### Workflow 1: Quick Professional Scan
```
1. Load Image
2. Scan Document
3. Full Auto Enhancement ← ONE CLICK!
4. Save Result
```

### Workflow 2: Scan & Digitize Text
```
1. Load Image
2. Scan Document
3. Extract Text
4. Copy to Clipboard
5. Use in other applications
```

### Workflow 3: Review & Annotate
```
1. Load Image
2. Scan Document
3. Add annotations (text, highlights, stamps)
4. Save annotated version
```

### Workflow 4: Compare Versions
```
1. Load & scan first version
2. Load Document to Compare
3. Compare Documents
4. Review differences report
5. Save comparison view
```

### Workflow 5: Organize Documents
```
1. Load Image
2. Scan Document
3. Auto-Name File ← Auto-names based on content!
4. Repeat for multiple documents
```

---

## 💡 Pro Tips

### OCR Tips
- ✅ Use high-resolution scans for best results
- ✅ Ensure good lighting (no shadows)
- ✅ Black text on white background works best
- ❌ Avoid cursive or handwritten text (lower accuracy)

### Auto Enhancement Tips
- ✅ Start with Full Auto Enhancement
- ✅ Use manual adjustments only if needed
- ✅ Auto Deskew works up to 10° tilt
- ✅ Auto Crop requires clear borders

### Annotation Tips
- ✅ Add annotations AFTER scanning
- ✅ Use stamps for professional workflows
- ✅ Highlights work great for PDFs
- ✅ Clear annotations to start over

### Comparison Tips
- ✅ Documents should be similar size
- ✅ Automatic alignment handles small differences
- ✅ Use same scan settings for both documents
- ✅ Side-by-side view shows both versions

---

## ⚙️ Settings

### OCR Languages
Currently supports: English (default)  
**Future**: Language selection in GUI

### Enhancement Sensitivity
Currently: Automatic  
**Customization**: Use manual controls after auto-enhancement

### Annotation Colors
Currently: Default colors (red, yellow, black)  
**Future**: Color picker

---

## ❓ Troubleshooting

### "OCR Not Available"
**Problem**: Tesseract not installed  
**Solution**: 
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

### Poor OCR Accuracy
**Problem**: Text not extracted correctly  
**Solutions**:
- Use higher resolution scan
- Ensure better lighting
- Try black & white mode first
- Make sure text is clear and not blurry

### Auto Deskew Not Working
**Problem**: Document still tilted  
**Solutions**:
- Tilt must be less than 10°
- Ensure document has clear edges
- Try manual rotation first

### Annotations in Wrong Position
**Problem**: Annotation not where expected  
**Note**: Current version uses predefined positions  
**Workaround**: Multiple clicks will add multiple annotations

### Comparison Shows Too Many Differences
**Problem**: Documents are too different  
**Solutions**:
- Ensure both are same document type
- Use same scan settings
- Check if documents are properly aligned
- Adjust sensitivity if option available

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open/Load Image |
| Ctrl+S | Save Result |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

*Note: New features don't have shortcuts yet - use mouse/buttons*

---

## 📊 Feature Availability

| Feature | Status | Requires |
|---------|--------|----------|
| OCR Text Extraction | ✅ Ready | Tesseract installed |
| Auto-Name Files | ✅ Ready | Tesseract installed |
| Auto Deskew | ✅ Ready | Nothing |
| Auto Crop | ✅ Ready | Nothing |
| Full Enhancement | ✅ Ready | Nothing |
| Annotations | ✅ Ready | Nothing |
| Document Compare | ✅ Ready | Nothing |

---

## 🆘 Need Help?

1. Check [README.md](README.md) for detailed documentation
2. See [NEW_FEATURES_2026.md](NEW_FEATURES_2026.md) for technical details
3. Run tests: `python test_new_features.py`
4. Check GitHub issues: https://github.com/adbeka/doc-scanner

---

**Last Updated**: January 29, 2026  
**Version**: 2.0 (with advanced features)
