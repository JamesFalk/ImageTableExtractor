# 📱 Quick Mobile Guide

## 🚀 Getting Started (5 Minutes)

### 1. Deploy Your App (Choose ONE):

**Easiest**: Streamlit Cloud
- Create GitHub account
- Upload 3 files to new repo
- Deploy on share.streamlit.io
- Get your app URL

**Alternative**: Hugging Face Spaces
- Similar process, different platform

### 2. Access on Phone:
- Open app URL in browser
- Add to Home Screen
- Use like a native app!

---

## 📸 How to Use

### Step 1: Setup
```
Open sidebar (☰) → Enter stock price & contracts
```

### Step 2: Import CALLS
```
Sidebar → "Import CALLS" → Select screenshot → Extract
```

### Step 3: Import PUTS
```
Sidebar → "Import PUTS" → Select screenshot → Extract
```

### Step 4: Fill Data
```
Main table → Enter strike prices & bid/ask values
Choose strategy type for each row
```

### Step 5: Calculate
```
Tap blue "CALCULATE" button → See total cost
```

---

## 📷 Screenshot Tips

✅ **DO**:
- Clear, bright screenshots
- Full options table visible
- Strike, Volume, OI columns shown
- No overlapping UI elements

❌ **DON'T**:
- Blurry or dark images
- Cropped too tight
- Notifications/pop-ups in frame
- Low resolution

---

## 💡 Pro Tips

1. **Enter strikes FIRST** before importing screenshots
2. **Import CALLS and PUTS separately**
3. **Double-check extracted values** (OCR 90-95% accurate)
4. **Manual entry always available** as backup
5. **Bookmark app URL** for quick access

---

## 🎯 Strategy Types

| Type | What It Does |
|------|-------------|
| **Both** | Buys call AND put (general) |
| **Call Only** | Only buy call option |
| **Put Only** | Only buy put option |
| **Straddle** | ATM call + put (neutral strategy) |
| **Strangle** | OTM call + put (wider strikes) |

---

## ⚡ Keyboard Shortcuts (Desktop)

- `Tab` - Move between cells
- `Enter` - Edit cell
- `Esc` - Stop editing
- `Ctrl/Cmd + Enter` - Calculate (if focused)

---

## 🐛 Troubleshooting

### OCR Not Working?
- Check screenshot quality
- Verify strikes entered first
- Try manual entry
- Check app logs (cloud version)

### App Slow?
- First load takes ~30 seconds (cloud wakes up)
- OCR takes 5-10 seconds
- Refreshing may help

### Can't Upload?
- File size under 5MB
- PNG or JPEG only
- Try compressing image

---

## 📊 Example Workflow

```
1. Open Robinhood → Options chain
2. Screenshot CALLS table
3. Screenshot PUTS table
4. Open calculator app
5. Enter: Stock price $8.46, 1 contract
6. Add strikes: 8, 8.5, 9, 9.5, 10
7. Import CALLS screenshot
8. Import PUTS screenshot
9. Enter bid/ask prices manually
10. Choose strategy (e.g., "Straddle")
11. Calculate → See total: $1,250.00
```

---

## 🆓 Costs

- **App**: 100% FREE
- **Hosting**: FREE (Streamlit Cloud/HF Spaces)
- **Usage**: Unlimited (with free tier limits)
- **No credit card needed**

---

## 📞 Quick Help

**Won't deploy?**
→ Check you uploaded all 3 files

**OCR fails?**
→ Verify Tesseract in packages.txt

**Slow on phone?**
→ Normal for first load, then faster

**Lost data?**
→ App doesn't save between sessions (by design)

---

## 🎯 One-Page Checklist

Deploy:
- [ ] GitHub/HF account created
- [ ] Repository created  
- [ ] 3 files uploaded
- [ ] App deployed
- [ ] URL bookmarked on phone

Use:
- [ ] Enter stock price & contracts
- [ ] Enter strike prices
- [ ] Upload CALLS screenshot
- [ ] Upload PUTS screenshot  
- [ ] Enter bid/ask manually
- [ ] Select strategy types
- [ ] Calculate total cost

---

**You're ready to trade smarter! 🚀**
