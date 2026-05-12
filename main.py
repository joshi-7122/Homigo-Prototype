import streamlit as st
import cv2
import numpy as np
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. STATE INITIALIZATION ---
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 'selection'
if 'subscription_data' not in st.session_state:
    st.session_state.subscription_data = {}

st.set_page_config(page_title="Homigo | Smart Hub", layout="centered")

# --- 2. SIDEBAR STATUS ---
st.sidebar.title("🏠 Homigo")
if st.session_state.is_subscribed:
    st.sidebar.success(f"🛡️ Shield Active: {st.session_state.subscription_data['brand']} {st.session_state.subscription_data['appliance']}")
    st.sidebar.caption(f"Valid Until: {st.session_state.subscription_data['expiry']}")
else:
    st.sidebar.warning("🛡️ Status: No Active Plan")

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["🏠 Home / AMC Hub", "🛡️ Guardian Live Feed", "📷 AI Diagnostics"])

# ----------------------------------------
# PAGE 1: HOME / AMC HUB
# ----------------------------------------
if menu == "🏠 Home / AMC Hub":
    st.title("🏠 Homigo")
    st.subheader("Home service on the go")
    st.markdown("---")

    # VIEW A: THE ACTIVE DASHBOARD
    if st.session_state.is_subscribed and st.session_state.checkout_step == 'selection':
        data = st.session_state.subscription_data
        st.header(f"Account: {data['name']}")
        st.info("🛡️ Active Shield Subscription")
        
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**Appliance:** {data['brand']} {data['appliance']}")
                st.write(f"**Age Bracket:** {data['timeline']}")
                st.write(f"**Contract:** {data['duration']}")
                st.write(f"**Valid Until:** :green[{data['expiry']}]") 
                st.write(f"**Reference ID:** #HMGO-{data['order_id']}")
            with col2:
                # Engineering Health Metric
                st.metric("Unit Health", "94%", delta="Optimal")
        
        st.markdown("---")
        if st.button("+ Add New Appliance"):
            st.session_state.is_subscribed = False
            st.session_state.checkout_step = 'selection'
            st.rerun()
    
    # VIEW B: THE CHECKOUT FLOW
    else:
        # STEP 1: PLAN SELECTION
        if st.session_state.checkout_step == 'selection':
            st.header("🛡️ Service Plan Selection")
            app_type = st.selectbox("Select Appliances:", ["Air Conditioner (AC)", "Refrigerator", "Washing Machine", "RO Purifier", "Microwave Oven"])
            
            brands = {"Air Conditioner (AC)": ["Daikin", "Voltas", "LG", "Blue Star", "Samsung"], 
                      "Refrigerator": ["Samsung", "LG", "Whirlpool"], 
                      "Washing Machine": ["IFB", "LG", "Samsung"], 
                      "RO Purifier": ["Kent", "Aquaguard"], 
                      "Microwave Oven": ["Samsung", "LG"]}
            brand_name = st.selectbox("Select Brand:", brands[app_type])
            
            timeline_options = ["2000-2005", "2006-2010", "2011-2015", "2016-2020", "2021-Present"]
            selected_timeline = st.selectbox("In which time period does your appliance fall?", timeline_options, index=3)
            
            duration = st.radio("Contract Period:", ["6 Months", "9 Months", "1.5 Years", "2 Years", "3 Years"], horizontal=True)
            
            # Pricing Calculation
            pricing_matrix = {"Air Conditioner (AC)": 1800, "Refrigerator": 1400, "Washing Machine": 1200, "RO Purifier": 1100, "Microwave Oven": 700}
            age_multiplier = {"2000-2005": 1.6, "2006-2010": 1.4, "2011-2015": 1.2, "2016-2020": 1.0, "2021-Present": 0.9}
            dur_map = {"6 Months": 0.6, "9 Months": 0.8, "1.5 Years": 1.4, "2 Years": 1.8, "3 Years": 2.5}
            final_price = int(pricing_matrix[app_type] * age_multiplier[selected_timeline] * dur_map[duration])
            
            st.metric("Total Payable (Inc. Taxes)", f"₹{final_price}")
            if st.button("Proceed to Checkout"):
                st.session_state.temp_data = {"app": app_type, "brand": brand_name, "timeline": selected_timeline, "price": final_price, "duration": duration}
                st.session_state.checkout_step = 'details'
                st.rerun()

        # STEP 2: BILLING DETAILS (WITH VALIDATION)
        elif st.session_state.checkout_step == 'details':
            st.header("📋 Billing Details")
            with st.form("details_form"):
                u_name = st.text_input("Full Name")
                u_email = st.text_input("Email ID")
                u_mobile = st.text_input("Mobile Number")
                u_addr = st.text_area("Full Installation Address")
                
                submit_details = st.form_submit_button("Proceed to Payment")
                
                if submit_details:
                    # VALIDATION GATE: Ensure no field is empty
                    if u_name and u_email and u_mobile and u_addr:
                        st.session_state.temp_name = u_name
                        st.session_state.checkout_step = 'payment'
                        st.rerun()
                    else:
                        st.error("⚠️ Error: All fields are mandatory. Please fill in your details to continue.")

        # STEP 3: PAYMENT
        elif st.session_state.checkout_step == 'payment':
            st.header("💳 Secure Payment")
            st.write(f"Authorized Amount: **₹{st.session_state.temp_data['price']}**")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Homigo", width=150)
            if st.button("Verify & Pay"):
                with st.spinner("Processing..."): 
                    time.sleep(1)
                st.session_state.checkout_step = 'success'
                st.rerun()

        # STEP 4: SUCCESS & EXPIRY CALCULATION
       elif st.session_state.checkout_step == 'success':
            st.balloons()
            st.header("✅ Payment Confirmed")
            if st.button("Go to Home"):
                # --- IMPROVED HUMAN-LOGIC DATE CALCULATION ---
                # We calculate by adding months instead of just total days
                dur_str = st.session_state.temp_data['duration']
                months_map = {
                    "6 Months": 6, 
                    "9 Months": 9, 
                    "1.5 Years": 18, 
                    "2 Years": 24, 
                    "3 Years": 36
                }
                
                # Get the number of months to add
                add_months = months_map[dur_str]
                
                # Calculate the new date
                now = datetime.now()
                # Simple logic: Add years and months
                new_month = (now.month + add_months - 1) % 12 + 1
                new_year = now.year + (now.month + add_months - 1) // 12
                expiry_date = now.replace(year=new_year, month=new_month).strftime("%d %b %Y")
                
                # Save the data
                st.session_state.is_subscribed = True
                st.session_state.subscription_data = {
                    "name": st.session_state.temp_name, 
                    "appliance": st.session_state.temp_data['app'], 
                    "brand": st.session_state.temp_data['brand'], 
                    "timeline": st.session_state.temp_data['timeline'], 
                    "duration": st.session_state.temp_data['duration'], 
                    "expiry": expiry_date,
                    "order_id": np.random.randint(1000, 9999)
                }
                st.session_state.checkout_step = 'selection'
                st.rerun()
# ----------------------------------------
# PAGE 2: GUARDIAN LIVE FEED
# ----------------------------------------
elif menu == "🛡️ Guardian Live Feed":
    st.header("🛡️ Guardian Live IoT Monitoring")
    if st.session_state.is_subscribed:
        data = st.session_state.subscription_data
        st.subheader(f"Telemetry Stream: {data['brand']} {data['appliance']}")
        m1, m2, m3 = st.columns(3)
        v1 = m1.empty(); v2 = m2.empty(); v3 = m3.empty()
        chart_space = st.empty()
        
        if st.button("Start Live Monitoring"):
            pulse = pd.DataFrame(np.random.randn(20, 1), columns=['Vibration Pulse'])
            for i in range(25):
                v = round(0.42 + np.random.normal(0, 0.04), 3)
                t = round(28.5 + np.random.normal(0, 0.6), 1)
                curr = round(4.8 + np.random.normal(0, 0.1), 2)
                v1.metric("Vibration (mm/s)", f"{v}")
                v2.metric("Core Temp (°C)", f"{t}")
                v3.metric("Current (Amps)", f"{curr}")
                pulse = pd.concat([pulse, pd.DataFrame([[v]], columns=['Vibration Pulse'])], ignore_index=True)
                chart_space.line_chart(pulse.tail(20))
                time.sleep(0.4)
    else:
        st.warning("Please activate a Homigo Shield to access the Guardian Live Feed.")

# ----------------------------------------
# PAGE 3: AI DIAGNOSTICS
# ----------------------------------------
elif menu == "📷 AI Diagnostics":
    st.header("📷 AI Diagnostics")
    up = st.file_uploader("Upload Component Image...", type=["jpg", "png", "jpeg"])
    
    if up:
        img = cv2.imdecode(np.asarray(bytearray(up.read()), dtype=np.uint8), 1)
        with st.spinner("AI Analysis in progress..."):
            time.sleep(1.2)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            density = np.sum(edges == 255) / edges.size
        
        c1, c2 = st.columns(2)
        c1.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Input Feed")
        c2.image(edges, caption="AI Edge Mapping")
        
        st.markdown("### 🔍 Homigo Diagnostic Report")
        if density > 0.05:
            st.error("**Finding: CRITICAL FAULT DETECTED**")
            st.markdown("1. **Immediate Shutdown Required.**\n2. **Technician Visit:** Covered under Shield.")
            st.markdown("---")
            st.subheader("📅 Book Your Service Slot")
            with st.form("service_booking"):
                day = st.selectbox("Select Day:", ["Today", "Tomorrow", "Monday"])
                slot = st.selectbox("Select Slot:", ["Morning", "Afternoon", "Evening"])
                if st.form_submit_button("Confirm Booking"):
                    st.success(f"✅ Expert scheduled for {day} ({slot}).")
                    st.balloons()
        else:
            st.success("**Finding: HEALTHY COMPONENT**")
            st.write("Proceed with routine quarterly maintenance.")
        st.metric("AI Confidence", f"{round(92 + (density * 10), 2)}%")
