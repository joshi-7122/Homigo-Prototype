import streamlit as st
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
        st.caption("Last Serviced: Jan 2026")
        
    with col2:
        st.warning("💨 **Daikin AC**")
        st.caption("Health: 72% (Warning)")
        st.caption("Last Serviced: Aug 2025")
        
    with col3:
        st.info("🚗 **Honda City**")
        st.caption("Health: 89% (Good)")
        st.caption("Next Service: 5,000 km")

    st.markdown("---")
    st.write("**Total Estimated Savings vs Reactive Repair:** ₹12,500/year")

# ----------------------------------------
# PAGE 2: Predictive Maintenance (PdM) - GUARDIAN
# ----------------------------------------
elif menu == "Guardian Predictive Alerts":
    st.header("🛡️ Guardian Smart Monitor")
    st.write("Analyzing IoT sensors across your digital twin network...")
    
    # Simulate a scanning effect
    with st.spinner("Guardian is checking component frequencies..."):
        time.sleep(2)
        
    st.error("🚨 **CRITICAL PREDICTIVE ALERT**")
    st.write("**Device:** Daikin Air Conditioner (Master Bedroom)")
    st.write("**Anomaly:** Abnormal Compressor Vibration detected.")
    st.write("**Prediction:** Mechanical failure likely within 14 days.")
    
    st.markdown("### Suggested Action:")
    st.info("🔧 Dispatch Technician for Preventative Alignment")
    st.write("**Cost:** ₹0.00 (Covered under Homigo Shield)")
    
    if st.button("Accept & Dispatch Technician"):
        st.success("Technician 'Ramesh K.' has been dispatched! Arriving tomorrow at 10:00 AM.")
        st.balloons()

# ----------------------------------------
# PAGE 3: Visual Diagnostic (AI Mockup)
# ----------------------------------------
elif menu == "Visual Diagnostics":
    st.header("📷 AI Visual Diagnostics")
    st.write("Upload a photo of the damaged appliance to instantly identify the issue.")
    
    uploaded_file = st.file_uploader("Upload Image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        st.write("Homigo AI is scanning image using CNN models...")
        
        # Simulate ML processing delay
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
            
        st.success("Diagnostic Complete!")
        st.write("🔍 **Identified:** Front-Load Washing Machine")
        st.write("🛠️ **Fault:** Clogged Water Inlet Filter (Confidence: 94%)")
        st.button("Request Homigo Expert")
