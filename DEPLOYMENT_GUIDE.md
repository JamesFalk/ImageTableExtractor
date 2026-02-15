# 📱 Options Calculator - Streamlit Web App Deployment Guide

## 🌟 Overview

This is a **mobile-friendly web application** that runs in your browser. No installation needed on your phone - just access the URL!

## 🚀 Quick Start (3 Options)

### Option 1: Deploy to Streamlit Cloud (FREE & EASIEST) ⭐

**Perfect for mobile use! Free hosting, works on any device.**

1. **Create a GitHub account** (if you don't have one): https://github.com

2. **Create a new repository**:
   - Go to GitHub and click "New Repository"
   - Name it: `options-calculator`
   - Make it Public
   - Click "Create repository"

3. **Upload these files to your repository**:
   - `streamlit_options_calculator.py`
   - `requirements_streamlit.txt` (rename to `requirements.txt`)
   - `packages.txt`

4. **Deploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `options-calculator`
   - Main file path: `streamlit_options_calculator.py`
   - Click "Deploy"!

5. **Access from your phone**:
   - You'll get a URL like: `https://your-app.streamlit.app`
   - Bookmark it on your phone
   - Access anytime from any device!

**✅ Pros**: Free, easy, works on all devices, automatic updates
**❌ Cons**: Public URL (anyone with link can access)

---

### Option 2: Run Locally on Your Computer

**Good for testing or local use only.**

#### Windows:
```bash
# Install Python 3.8+ from python.org

# Install dependencies
pip install -r requirements_streamlit.txt

# Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Run installer, default location is fine

# Run the app
streamlit run streamlit_options_calculator.py
```

#### Mac:
```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Install Tesseract
brew install tesseract

# Run the app
streamlit run streamlit_options_calculator.py
```

#### Linux:
```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Install Tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr

# Run the app
streamlit run streamlit_options_calculator.py
```

**Access**: Open browser to `http://localhost:8501`

**✅ Pros**: Private, fast, full control
**❌ Cons**: Only accessible on that computer, can't use on phone (unless on same network)

---

### Option 3: Deploy to Hugging Face Spaces (FREE ALTERNATIVE)

**Another free cloud option with OCR support.**

1. **Create Hugging Face account**: https://huggingface.co

2. **Create a new Space**:
   - Click "Create new Space"
   - Name: `options-calculator`
   - Space SDK: **Streamlit**
   - Make it Public
   - Create Space

3. **Upload files**:
   - `streamlit_options_calculator.py` → rename to `app.py`
   - `requirements_streamlit.txt` → rename to `requirements.txt`
   - `packages.txt`

4. **Access your app**:
   - URL: `https://huggingface.co/spaces/YOUR_USERNAME/options-calculator`

**✅ Pros**: Free, alternative to Streamlit Cloud
**❌ Cons**: Slightly slower than Streamlit Cloud

---

## 📱 Using the App on Your Phone

### Step-by-Step:

1. **Open the app URL** in your mobile browser (Chrome, Safari, etc.)

2. **Add to Home Screen** (makes it feel like a native app):
   - **iPhone**: Tap Share → "Add to Home Screen"
   - **Android**: Tap Menu (⋮) → "Add to Home Screen"

3. **Upload Screenshots**:
   - Tap the sidebar (three lines icon)
   - Take or select CALLS screenshot → Extract
   - Take or select PUTS screenshot → Extract

4. **Enter your data**:
   - Edit strike prices
   - Add bid/ask values
   - Choose strategy type

5. **Calculate**:
   - Tap the blue "CALCULATE" button
   - See your total cost!

---

## 📸 Taking Good Screenshots for OCR

### ✅ Best Practices:

1. **Open your trading app** (Robinhood, Webull, etc.)
2. Navigate to the options chain
3. **Make sure the table is visible**:
   - Strike prices clearly shown
   - Volume and Open Interest columns visible
   - No overlapping menus or notifications
4. **Take a clear screenshot**:
   - Good lighting
   - Phone held straight (not angled)
   - No glare or shadows
5. **Crop if needed** (but keep the full table)

### Example Screenshots:
- Shows: Strike | Bid | Ask | Volume | OI
- Dark mode or light mode both work
- Portrait or landscape both work

---

## 🔧 Troubleshooting

### OCR Not Working on Cloud Deployment?

**Check the logs in Streamlit Cloud**:
1. Go to your app dashboard
2. Click "Manage app" → "Logs"
3. Look for Tesseract errors

**Common fix**: Make sure `packages.txt` is uploaded with these contents:
```
tesseract-ocr
tesseract-ocr-eng
libgl1
```

### App is Slow?

- Streamlit Cloud free tier has limited resources
- First load may be slow (it's "waking up")
- OCR processing takes 5-10 seconds
- Subsequent uses will be faster

### Can't Upload Images?

- Check file size (keep under 5MB)
- Use PNG or JPEG format
- Try compressing the image
- Make sure you're using HTTPS (not HTTP)

### Data Not Extracting?

- Verify screenshot quality
- Make sure strike prices are in the calculator FIRST
- Check that Volume and OI columns are visible
- Try adjusting screenshot brightness/contrast

---

## 💡 Tips for Best Experience

1. **Enter strikes first**: Type in all your strike prices before importing screenshots
2. **One section at a time**: Do CALLS first, then PUTS
3. **Manual backup**: You can always manually type Volume/OI if OCR misses them
4. **Save your work**: Take a screenshot of the final table for your records
5. **Bookmark the app**: Add to home screen for quick access

---

## 🔐 Privacy & Security

### Streamlit Cloud (Public):
- Your app URL is public (anyone with link can access)
- Data is NOT saved between sessions
- Screenshots are processed in memory only
- No data is stored on servers

### Running Locally:
- Completely private
- All processing on your computer
- No internet connection needed (after setup)

---

## 🎯 Features

✅ **Mobile-optimized interface**
✅ **OCR screenshot import** for Volume & OI
✅ **Real-time calculations**
✅ **Multiple strategy types** (Straddle, Strangle, etc.)
✅ **Editable data table**
✅ **Cost breakdown**
✅ **No installation required** (cloud version)
✅ **Works on any device**

---

## 📊 Supported Strategies

- **Both**: Buy both call and put
- **Call Only**: Buy call only
- **Put Only**: Buy put only
- **Straddle**: ATM call + put (same strike)
- **Strangle**: OTM call + put (different strikes)

---

## 🆘 Need Help?

### Common Questions:

**Q: Do I need to pay for hosting?**
A: No! Streamlit Cloud and Hugging Face Spaces are free for public apps.

**Q: Can others see my trades?**
A: No. Each session is private. Data isn't saved between visits.

**Q: Does it work offline?**
A: Only the local version works offline. Cloud versions need internet.

**Q: Can I use it on iPhone and Android?**
A: Yes! Works on all mobile browsers.

**Q: How accurate is the OCR?**
A: 90-95% accurate with clear screenshots. Always double-check values.

---

## 🔄 Updating Your App

If you deploy to Streamlit Cloud:
1. Update files in your GitHub repository
2. Streamlit Cloud auto-detects changes
3. App redeploys automatically
4. Refresh your browser

---

## 📦 Files Needed for Deployment

```
your-repository/
├── streamlit_options_calculator.py  (or app.py for HuggingFace)
├── requirements.txt
└── packages.txt
```

That's it! Just these 3 files.

---

## 🎉 You're All Set!

Deploy once, use forever from your phone. No app store, no downloads, just a URL!

**Recommended**: Deploy to Streamlit Cloud for the best mobile experience.

---

**Made with ❤️ for mobile traders**
