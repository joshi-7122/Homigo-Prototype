import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# Set page configuration
st.set_page_config(page_title="Homigo: Home Service on the Go", layout="centered")

# Custom Title and Tagline
st.title("🏠 Homigo")
st.subheader("Home service on the go")
st.markdown("---")

# Navigation Sidebar
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to:", ["My Unified Shield", "Guardian Predictive Alerts", "Visual Diagnostics"])

# ----------------------------------------
# PAGE 1: The Brand-Agnostic Dashboard
# ----------------------------------------
if menu == "My Unified Shield":
    st.header("🛡️ My Covered Ecosystem")
    st.success("Subscription Status: ACTIVE (All-Appliance AMC)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("❄️ **LG Refrigerator**")
        st.caption("Health: 98% (Optimal)")
    with col2:
        st.warning("💨 **Daikin AC**")
        st.caption("Health: 72% (Warning)")
    with col3:
        st.info("🚗 **Honda City**")
        st.caption("Health: 89% (Good)")

# ----------------------------------------
# PAGE 2: Predictive Maintenance (PdM)
# ----------------------------------------
elif menu == "Guardian Predictive Alerts":
    st.header("🛡️ Guardian Smart Monitor")
    st.write("Analyzing IoT sensors for fault propagation...")
    
    with st.spinner("Guardian is checking frequencies..."):
        time.sleep(1.5)
        
    st.error("🚨 **CRITICAL PREDICTIVE ALERT**")
    st.write("**Device:** Daikin Air Conditioner")
    st.write("**Anomaly:** Abnormal Compressor Vibration.")
    st.info("🔧 Suggestion: Schedule preventative service now (Free under Homigo Shield).")
    
    if st.button("Accept & Dispatch Technician"):
        st.success("Technician dispatched! Arriving tomorrow at 10:00 AM.")
        st.balloons()

# ----------------------------------------
# PAGE 3: Visual Diagnostics (REAL OPENCV INTEGRATION)
# ----------------------------------------
elif menu == "Visual Diagnostics":
    st.header("📷 AI Visual Diagnostics (Powered by OpenCV)")
    st.write("Upload a photo of the damaged part to identify the fault pattern.")
    
    uploaded_file = st.file_uploader("Upload Image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Convert the file to an image that OpenCV can read
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB) # Convert BGR to RGB for Streamlit
        
        col_orig, col_proc = st.columns(2)
        
        with col_orig:
            st.image(opencv_image, caption="Uploaded Original", use_container_width=True)
            
        with col_proc:
            # REAL OPENCV PROCESSING: Edge Detection
            # This demonstrates "Scanning" for cracks or structural issues
            with st.spinner("OpenCV is analyzing fault patterns..."):
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 100, 200) # Edge detection
                st.image(edges, caption="Homigo AI Scan (OpenCV Edges)", use_container_width=True)
        
        st.success("Diagnostic Complete!")
        st.markdown("""
        **🔍 Homigo Analysis Summary:**
        * **Detected Component:** Mechanical Housing
        * **AI Confidence:** 91.4%
        * **Recommendation:** Structural integrity check required.
        """)
        st.button("Connect with Homigo Expert")
