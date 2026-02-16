import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

# Page config
st.set_page_config(
    page_title="Options Extractor",
    page_icon="📊",
    layout="centered"
)

# Minimal CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    h1 {
        text-align: center;
        color: #1976d2;
        margin-bottom: 2rem;
    }
    
    .upload-section {
        background-color: #f5f5f5;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    .success-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 20px 0;
    }
    
    .data-preview {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 14px;
        white-space: pre;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)


def preprocess_image(image_array):
    """Preprocess image for OCR"""
    img_cv = cv2.cvtColor(np.array(image_array), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed = cv2.fastNlMeansDenoising(thresh)
    return processed


def extract_options_data(image):
    """Extract options data from screenshot"""
    try:
        processed = preprocess_image(image)
        
        custom_config = r'--oem 3 --psm 6'
        data = pytesseract.image_to_data(processed, 
                                       output_type=pytesseract.Output.DICT,
                                       config=custom_config)
        
        # Group by rows
        rows = {}
        tolerance = 35  # Increased tolerance for better row detection
        
        for i, text in enumerate(data['text']):
            # Lower confidence threshold to catch zeros and small numbers
            if text.strip() and data['conf'][i] > 0:
                y = data['top'][i]
                x = data['left'][i]
                
                row_key = None
                for existing_y in rows.keys():
                    if abs(y - existing_y) < tolerance:
                        row_key = existing_y
                        break
                
                if row_key is None:
                    row_key = y
                    rows[row_key] = []
                
                rows[row_key].append({'text': text, 'x': x})
        
        # Parse rows
        options_data = []
        
        for row_y in sorted(rows.keys()):
            row_items = sorted(rows[row_y], key=lambda x: x['x'])
            row_text = [item['text'] for item in row_items]
            
            # Find numbers (volume and OI) - simplified
            numbers = []
            for text in row_text:
                # Remove commas and check if it's a number
                cleaned = text.replace(',', '').strip()
                if cleaned.isdigit():
                    numbers.append(int(cleaned))
            
            # Take last 2 numbers as volume and OI
            if len(numbers) >= 2:
                volume = numbers[-2]
                oi = numbers[-1]
                options_data.append({
                    'Volume': volume,
                    'OI': oi
                })
        
        return options_data
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def looks_like_strike(text):
    """Check if text looks like strike price"""
    cleaned = re.sub(r'[^\d.]', '', text)
    try:
        value = float(cleaned)
        return 1 <= value <= 1000
    except:
        return False


def format_for_clipboard(data):
    """Format data as (volume, oi) pairs"""
    if not data:
        return ""
    
    # Create pairs format: (vol, oi) (vol, oi) ...
    pairs = [f"({row['Volume']}, {row['OI']})" for row in data]
    return " ".join(pairs)


# Main app
st.title("📊 Options Data Extractor")

st.markdown("""
<div class="upload-section">
    <h3>📸 Upload Options Screenshot</h3>
    <p>Upload a clear screenshot of your options chain</p>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=['png', 'jpg', 'jpeg'],
    label_visibility="collapsed"
)

if uploaded_file:
    # Show image
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    # Extract button
    if st.button("🔍 EXTRACT DATA", type="primary"):
        with st.spinner('Extracting data...'):
            extracted_data = extract_options_data(image)
        
        if extracted_data:
            st.markdown("""
            <div class="success-box">
                <h4>✅ Extraction Complete!</h4>
                <p>Found <strong>{}</strong> rows of data</p>
            </div>
            """.format(len(extracted_data)), unsafe_allow_html=True)
            
            # Store in session state
            st.session_state.extracted_data = extracted_data
            st.session_state.clipboard_text = format_for_clipboard(extracted_data)
            
            # Show data preview
            st.markdown("### 📋 Extracted Data:")
            df = pd.DataFrame(extracted_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Copy button
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Show formatted text
            st.text_area(
                "Copy this data:",
                value=st.session_state.clipboard_text,
                height=100,
                help="Select all and copy (Ctrl+A, Ctrl+C)"
            )
            
            st.info("💡 **Tip:** Select the text above and copy it (Ctrl+A then Ctrl+C on desktop, long-press and Copy on mobile)")
            
        else:
            st.warning("⚠️ Could not extract data. Try a clearer screenshot.")

# Instructions at bottom
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <h4>How to use:</h4>
    <p>1. Upload screenshot of options chain<br>
    2. Click "Extract Data"<br>
    3. Copy the extracted data</p>
    <br>
    <small>Works best with clear screenshots showing Volume and OI columns</small>
</div>
""", unsafe_allow_html=True)
