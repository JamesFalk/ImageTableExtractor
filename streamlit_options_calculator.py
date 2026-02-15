import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image
import cv2
import numpy as np
import re
from io import BytesIO

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="Options Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile optimization
st.markdown("""
    <style>
    /* Mobile-friendly styles */
    .main {
        padding: 1rem;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
    }
    
    .import-calls-btn {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    
    .import-puts-btn {
        background-color: #f44336 !important;
        color: white !important;
    }
    
    .calculate-btn {
        background-color: #2196F3 !important;
        color: white !important;
    }
    
    /* Make data editor more mobile friendly */
    .stDataFrame {
        font-size: 14px;
    }
    
    /* Results box */
    .results-box {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin: 20px 0;
        text-align: center;
    }
    
    .results-title {
        font-size: 20px;
        font-weight: bold;
        color: #2e7d32;
    }
    
    .results-amount {
        font-size: 32px;
        font-weight: bold;
        color: #1b5e20;
        margin-top: 10px;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    
    /* Header */
    h1 {
        text-align: center;
        color: #1976d2;
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)


class OptionsChainExtractor:
    """Extract options data from screenshots"""
    
    @staticmethod
    def preprocess_image(image_array):
        """Preprocess image for better OCR"""
        # Convert PIL to OpenCV format
        img_cv = cv2.cvtColor(np.array(image_array), cv2.COLOR_RGB2BGR)
        
        # Grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        processed = cv2.fastNlMeansDenoising(thresh)
        
        return processed
    
    @staticmethod
    def extract_options_data(image, option_type='calls'):
        """Extract structured options data from image"""
        try:
            # Preprocess
            processed = OptionsChainExtractor.preprocess_image(image)
            
            # OCR
            custom_config = r'--oem 3 --psm 6'
            data = pytesseract.image_to_data(processed, 
                                           output_type=pytesseract.Output.DICT,
                                           config=custom_config)
            
            # Group by rows
            rows = {}
            tolerance = 20
            
            for i, text in enumerate(data['text']):
                if text.strip() and data['conf'][i] > 30:
                    y = data['top'][i]
                    x = data['left'][i]
                    
                    # Find or create row
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
            options_data = {}
            
            for row_y in sorted(rows.keys()):
                row_items = sorted(rows[row_y], key=lambda x: x['x'])
                row_text = [item['text'] for item in row_items]
                
                # Extract strike, volume, and OI
                strike = None
                volume = None
                oi = None
                
                # Look for strike price
                for text in row_text:
                    if '$' in text or OptionsChainExtractor.looks_like_strike(text):
                        cleaned = re.sub(r'[^\d.]', '', text)
                        try:
                            strike = float(cleaned)
                            break
                        except:
                            pass
                
                # Extract numbers (volume and OI are typically the last two large numbers)
                numbers = []
                for text in row_text:
                    cleaned = re.sub(r'[^\d]', '', text)
                    if cleaned and len(cleaned) >= 1:
                        try:
                            numbers.append(int(cleaned))
                        except:
                            pass
                
                if len(numbers) >= 2:
                    volume = numbers[-2]
                    oi = numbers[-1]
                
                if strike and volume is not None and oi is not None:
                    options_data[strike] = {'volume': volume, 'oi': oi}
            
            return options_data
            
        except Exception as e:
            st.error(f"OCR Error: {str(e)}")
            return {}
    
    @staticmethod
    def looks_like_strike(text):
        """Check if text looks like a strike price"""
        cleaned = re.sub(r'[^\d.]', '', text)
        try:
            value = float(cleaned)
            return 1 <= value <= 1000
        except:
            return False


def initialize_session_state():
    """Initialize session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'Strike': [0.0] * 10,
            'Type': ['Both'] * 10,
            'Call Bid': [0.0] * 10,
            'Call Ask': [0.0] * 10,
            'Call Volume': [0] * 10,
            'Call OI': [0] * 10,
            'Put Bid': [0.0] * 10,
            'Put Ask': [0.0] * 10,
            'Put Volume': [0] * 10,
            'Put OI': [0] * 10,
        })
    
    if 'stock_price' not in st.session_state:
        st.session_state.stock_price = 8.46
    
    if 'contracts' not in st.session_state:
        st.session_state.contracts = 1
    
    if 'total_cost' not in st.session_state:
        st.session_state.total_cost = 0.0


def process_uploaded_image(uploaded_file, option_type):
    """Process uploaded screenshot and extract data"""
    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        
        # Show preview
        st.image(image, caption=f"{option_type.upper()} Screenshot", use_container_width=True)
        
        # Extract data
        with st.spinner(f'Extracting {option_type} data...'):
            extracted_data = OptionsChainExtractor.extract_options_data(image, option_type)
        
        if extracted_data:
            # Update dataframe
            updated_count = 0
            for idx, row in st.session_state.data.iterrows():
                strike = row['Strike']
                if strike > 0 and strike in extracted_data:
                    if option_type == 'calls':
                        st.session_state.data.at[idx, 'Call Volume'] = extracted_data[strike]['volume']
                        st.session_state.data.at[idx, 'Call OI'] = extracted_data[strike]['oi']
                    else:  # puts
                        st.session_state.data.at[idx, 'Put Volume'] = extracted_data[strike]['volume']
                        st.session_state.data.at[idx, 'Put OI'] = extracted_data[strike]['oi']
                    updated_count += 1
            
            st.success(f"✅ Successfully extracted data for {updated_count} strikes!")
            
            # Show extracted data
            with st.expander("View Extracted Data"):
                extracted_df = pd.DataFrame([
                    {'Strike': f'${k}', 'Volume': v['volume'], 'OI': v['oi']}
                    for k, v in sorted(extracted_data.items())
                ])
                st.dataframe(extracted_df, use_container_width=True)
        else:
            st.warning("⚠️ No data extracted. Please ensure the screenshot is clear and contains a visible options chain table.")


def calculate_costs():
    """Calculate total strategy cost"""
    df = st.session_state.data
    stock_price = st.session_state.stock_price
    contracts = st.session_state.contracts
    
    total_cost = 0.0
    costs = []
    
    for idx, row in df.iterrows():
        strike = row['Strike']
        if strike <= 0:
            costs.append(0.0)
            continue
        
        option_type = row['Type']
        row_cost = 0.0
        
        # Calculate based on strategy type
        if option_type in ['Both', 'Call Only', 'Straddle', 'Strangle']:
            call_ask = row['Call Ask']
            if call_ask > 0:
                row_cost += call_ask * 100 * contracts
        
        if option_type in ['Both', 'Put Only', 'Straddle', 'Strangle']:
            put_ask = row['Put Ask']
            if put_ask > 0:
                row_cost += put_ask * 100 * contracts
        
        costs.append(row_cost)
        total_cost += row_cost
    
    # Add cost column to dataframe
    df['Total Cost'] = costs
    st.session_state.total_cost = total_cost
    
    return df, total_cost


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("📊 Options Cost Calculator")
    st.markdown("##### Mobile-Friendly OCR Calculator")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Settings")
        
        st.session_state.stock_price = st.number_input(
            "Current Stock Price",
            min_value=0.01,
            value=st.session_state.stock_price,
            step=0.01,
            format="%.2f"
        )
        
        st.session_state.contracts = st.number_input(
            "Number of Contracts",
            min_value=1,
            value=st.session_state.contracts,
            step=1
        )
        
        st.markdown("---")
        
        st.header("📸 Import Data")
        st.markdown("Upload screenshots to auto-fill Volume & OI")
        
        # Calls upload
        st.markdown("##### 🟢 Import CALLS")
        calls_file = st.file_uploader(
            "Upload CALLS screenshot",
            type=['png', 'jpg', 'jpeg'],
            key='calls_uploader',
            label_visibility="collapsed"
        )
        
        if calls_file:
            if st.button("Extract CALLS Data", key='extract_calls', use_container_width=True):
                process_uploaded_image(calls_file, 'calls')
        
        st.markdown("---")
        
        # Puts upload
        st.markdown("##### 🔴 Import PUTS")
        puts_file = st.file_uploader(
            "Upload PUTS screenshot",
            type=['png', 'jpg', 'jpeg'],
            key='puts_uploader',
            label_visibility="collapsed"
        )
        
        if puts_file:
            if st.button("Extract PUTS Data", key='extract_puts', use_container_width=True):
                process_uploaded_image(puts_file, 'puts')
        
        st.markdown("---")
        
        # Clear data button
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.data = pd.DataFrame({
                'Strike': [0.0] * 10,
                'Type': ['Both'] * 10,
                'Call Bid': [0.0] * 10,
                'Call Ask': [0.0] * 10,
                'Call Volume': [0] * 10,
                'Call OI': [0] * 10,
                'Put Bid': [0.0] * 10,
                'Put Ask': [0.0] * 10,
                'Put Volume': [0] * 10,
                'Put OI': [0] * 10,
            })
            st.session_state.total_cost = 0.0
            st.rerun()
    
    # Main content area
    st.markdown("### 📋 Options Data")
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>📝 How to use:</strong><br>
        1️⃣ Enter strike prices and bid/ask values<br>
        2️⃣ Upload screenshots to auto-fill Volume & OI (optional)<br>
        3️⃣ Select strategy type for each row<br>
        4️⃣ Click Calculate to see total cost
    </div>
    """, unsafe_allow_html=True)
    
    # Data editor
    edited_df = st.data_editor(
        st.session_state.data,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "Strike": st.column_config.NumberColumn("Strike", format="%.2f", min_value=0.0),
            "Type": st.column_config.SelectboxColumn(
                "Type",
                options=['Both', 'Call Only', 'Put Only', 'Straddle', 'Strangle']
            ),
            "Call Bid": st.column_config.NumberColumn("Call Bid", format="%.2f", min_value=0.0),
            "Call Ask": st.column_config.NumberColumn("Call Ask", format="%.2f", min_value=0.0),
            "Call Volume": st.column_config.NumberColumn("Call Vol", format="%d"),
            "Call OI": st.column_config.NumberColumn("Call OI", format="%d"),
            "Put Bid": st.column_config.NumberColumn("Put Bid", format="%.2f", min_value=0.0),
            "Put Ask": st.column_config.NumberColumn("Put Ask", format="%.2f", min_value=0.0),
            "Put Volume": st.column_config.NumberColumn("Put Vol", format="%d"),
            "Put OI": st.column_config.NumberColumn("Put OI", format="%d"),
        },
        hide_index=True,
    )
    
    # Update session state
    st.session_state.data = edited_df
    
    # Calculate button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧮 CALCULATE TOTAL COST", use_container_width=True, type="primary"):
            result_df, total_cost = calculate_costs()
            st.session_state.data = result_df
            st.rerun()
    
    # Show results
    if st.session_state.total_cost > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="results-box">
            <div class="results-title">💰 Total Strategy Cost</div>
            <div class="results-amount">${st.session_state.total_cost:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show breakdown if exists
        if 'Total Cost' in st.session_state.data.columns:
            with st.expander("📊 View Cost Breakdown"):
                breakdown_df = st.session_state.data[st.session_state.data['Strike'] > 0][
                    ['Strike', 'Type', 'Total Cost']
                ].copy()
                breakdown_df['Total Cost'] = breakdown_df['Total Cost'].apply(lambda x: f"${x:,.2f}")
                st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <small>📱 Mobile-Optimized | 🔒 Runs in Browser | ⚡ No Installation Required</small><br>
        <small>Made with ❤️ for options traders</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
