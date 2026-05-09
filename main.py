import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import random

# Set page configuration
st.set_page_config(page_title="Homigo: Home Service on the Go", layout="centered")

# Custom Title and Tagline
st.title("🏠 Homigo")
st.subheader("Home service on the go")
st.markdown("---")

# Navigation Sidebar
st.sidebar.header("Navigation")
menu = st.sidebar.radio("Go to:", ["AMC Package Builder", "Guardian Predictive Alerts", "Visual Diagnostics"])

# ----------------------------------------
# PAGE 1: AMC PACKAGE BUILDER (The Subscription Logic)
# ----------------------------------------
if menu == "AMC Package Builder":
    st.header("🛡️ Homigo Shield Subscription")
    st.write("Secure your appliances with our brand-agnostic protection plans.")

    # 1. Select Timeline
    st.markdown("### **1. Select Purchase Timeline**")
    year_range = st.select_slider(
        "When was your appliance purchased?",
        options=[str(y) for y in range(1998, 2030)],
        value="2018"
    )
    appliance_year = int(year_range)

    # 2. Select Appliances
    st.markdown("### **2. Select Appliance**")
    appliance_type = st.selectbox(
        "Choose the appliance to cover:",
        ["Refrigerator", "Air Conditioner (AC)", "RO Water Purifier", "Microwave Oven", "Washing Machine"]
    )

    # Logic to determine Plan Type based on Age
    current_year = 2026
    age = current_year - appliance_year

    if age > 12:
        plan_name = "Vintage Support Plan"
        base_rate = 3500
        benefits = ["Component restoration", "Hard-to-find part sourcing", "24/7 Priority Support"]
    elif 5 <= age <= 12:
        plan_name = "Standard Performance Plan"
        base_rate = 2200
        benefits = ["Bi-annual deep cleaning", "Wear & tear coverage", "Unlimited technician visits"]
    else:
        plan_name = "Premium Smart Shield"
        base_rate = 1200
        benefits = ["IoT Sensor Integration", "Predictive failure alerts", "Free spare parts up to ₹5000"]

    # 3. Select Package Duration
    st.markdown("---")
    st.markdown(f"### **3. Choose Package for your {appliance_type}**")
    
    duration = st.radio(
        "How long would you like the protection?",
        ["6 Months", "1 Year (Recommended)", "1.5 Years"],
        horizontal=True
    )

    # Calculate Price
    multipliers = {"6 Months": 0.6, "1 Year (Recommended)": 1.0, "1.5 Years": 1.4}
    total_price = int(base_rate * multipliers[duration])

    # Show the Package Card
    st.info(f"**Recommended Plan:** {plan_name}")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Plan Includes:**")
        for b in benefits:
            st.write(f"- {b}")
    with c2:
        st.metric("Total Subscription Cost", f"₹{total_price}")
        if st.button("Subscribe to Homigo Shield"):
            st.success("Successfully enrolled! Your technician will arrive for the initial inspection shortly.")
            st.balloons()

# ----------------------------------------
# PAGE 2: GUARDIAN PREDICTIVE ALERTS (IoT Logic)
# ----------------------------------------
elif menu == "Guardian Predictive Alerts":
    st.header("🛡️ Guardian Smart Monitor")
    st.write("Analyzing IoT sensors for fault propagation...")
    
    with st.spinner("Guardian is checking frequencies..."):
        time.sleep(1.5)
        
    st.error("🚨 **CRITICAL PREDICTIVE ALERT**")
    st.write("**Device:** Daikin Air Conditioner")
    st.write("**Anomaly:** Abnormal Compressor Vibration detected via IoT Node #721.")
    st.info("🔧 Suggestion: Schedule preventative service now (Free under your Homigo Shield).")
    
    if st.button("Dispatch Expert Under AMC"):
        st.success("Technician dispatched! Arriving tomorrow at 10:00 AM.")

# ----------------------------------------
# PAGE 3: VISUAL DIAGNOSTICS (YOUR CV2 CODE)
# ----------------------------------------
elif menu == "Visual Diagnostics":
    st.header("📷 AI Visual Diagnostics (Powered by OpenCV)")
    st.write("Upload a photo of the damaged part to identify the fault pattern.")
    
    uploaded_file = st.file_uploader("Upload Image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Convert the file to an image that OpenCV can read
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB) 
        
        col_orig, col_proc = st.columns(2)
        
        with col_orig:
            st.image(opencv_image, caption="Uploaded Original", use_container_width=True)
            
        with col_proc:
            with st.spinner("OpenCV is analyzing fault patterns..."):
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 100, 200) 
                st.image(edges, caption="Homigo AI Scan (OpenCV Edges)", use_container_width=True)
        
        st.success("Diagnostic Complete!")
        st.markdown("""
        **🔍 Homigo Analysis Summary:**
        * **Detected Component:** Mechanical Housing
        * **AI Confidence:** 91.4%
        * **Recommendation:** Structural integrity check required. Claimable under your active AMC.
        """)
