import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import cv2
import numpy as np

st.set_page_config(
    page_title="Options Extractor",
    page_icon="📊",
    layout="centered"
)

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
    </style>
""", unsafe_allow_html=True)


def preprocess_image(image_array):
    """Preprocess image for OCR"""
    img_cv = cv2.cvtColor(np.array(image_array), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    mean_val = np.mean(gray)
    if mean_val < 127:
        gray = cv2.bitwise_not(gray)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    processed = cv2.fastNlMeansDenoising(thresh)
    
    return processed


def extract_options_data(image):
    """Extract all numbers and pair them sequentially"""
    try:
        processed = preprocess_image(image)
        
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,'
        text = pytesseract.image_to_string(processed, config=custom_config)
        
        numbers = []
        for line in text.split('\n'):
            line = line.strip().replace(',', '')
            if line.isdigit():
                numbers.append(int(line))
        
        options_data = []
        for i in range(0, len(numbers)-1, 2):
            volume = numbers[i]
            oi = numbers[i+1]
            options_data.append({
                'Volume': volume,
                'OI': oi
            })
        
        return options_data
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def format_for_clipboard(data):
    """Format data as (volume, oi) pairs"""
    if not data:
        return ""
    
    pairs = [f"({row['Volume']}, {row['OI']})" for row in data]
    return " ".join(pairs)


st.title("📊 Options Data Extractor")

st.markdown("""
<div class="upload-section">
    <h3>📸 Upload Options Screenshot</h3>
    <p>Upload a clear screenshot of your options chain</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=['png', 'jpg', 'jpeg'],
    label_visibility="collapsed"
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
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
            
            st.session_state.extracted_data = extracted_data
            st.session_state.clipboard_text = format_for_clipboard(extracted_data)
            
            st.markdown("### 📋 Extracted Data:")
            df = pd.DataFrame(extracted_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.text_area(
                "Copy this data:",
                value=st.session_state.clipboard_text,
                height=100,
                help="Select all and copy"
            )
            
            st.info("💡 Select the text above and copy it")
            
        else:
            st.warning("⚠️ Could not extract data. Try a clearer screenshot.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <h4>How to use:</h4>
    <p>1. Upload screenshot of options chain<br>
    2. Click Extract Data<br>
    3. Copy the extracted data</p>
    <br>
    <small>Works best with clear screenshots showing Volume and OI columns</small>
</div>
""", unsafe_allow_html=True)
