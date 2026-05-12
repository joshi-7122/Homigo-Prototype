import streamlit as st
import cv2
import numpy as np
import time
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SESSION STATE INITIALIZATION ---
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
if 'checkout_step' not in st.session_state:
    st.session_state.checkout_step = 'selection'
if 'subscription_data' not in st.session_state:
    st.session_state.subscription_data = {}

st.set_page_config(page_title="Homigo | Smart Hub", layout="centered")

# --- 2. SIDEBAR STATUS & NAVIGATION ---
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

    # VIEW A: DASHBOARD (Shown after purchase)
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
                st.metric("Unit Health", "94%", delta="Optimal")
        
        st.markdown("---")
        if st.button("+ Add New Appliance"):
            st.session_state.is_subscribed = False
            st.session_state.checkout_step = 'selection'
            st.rerun()

    # VIEW B: THE CHECKOUT FLOW
    else:
        # STEP 1: Selection
        if st.session_state.checkout_step == 'selection':
            st.header("🛡️ Service Plan Selection")
            app_type = st.selectbox("Select Appliances:", ["Air Conditioner (AC)", "Refrigerator", "Washing Machine", "RO Purifier", "Microwave Oven"])
            
            brands = {
                "Air Conditioner (AC)": ["Daikin", "Voltas", "LG", "Blue Star", "Samsung"], 
                "Refrigerator": ["Samsung", "LG", "Whirlpool"], 
                "Washing Machine": ["IFB", "LG", "Samsung"], 
                "RO Purifier": ["Kent", "Aquaguard"], 
                "Microwave Oven": ["Samsung", "LG"]
            }
            brand_name = st.selectbox("Select Brand:", brands[app_type])
            
            timeline_options = ["2000-2005", "2006-2010", "2011-2015", "2016-2020", "2021-Present"]
            selected_timeline = st.selectbox("In which time period does your appliance fall?", timeline_options, index=3)
            
            duration = st.radio("Contract Period:", ["6 Months", "9 Months", "1.5 Years", "2 Years", "3 Years"], horizontal=True)
            
            # Pricing Engine
            pricing_matrix = {"Air Conditioner (AC)": 1800, "Refrigerator": 1400, "Washing Machine": 1200, "RO Purifier": 1100, "Microwave Oven": 700}
            age_multiplier = {"2000-2005": 1.6, "2006-2010": 1.4, "2011-2015": 1.2, "2016-2020": 1.0, "2021-Present": 0.9}
            dur_map = {"6 Months": 0.6, "9 Months": 0.8, "1.5 Years": 1.4, "2 Years": 1.8, "3 Years": 2.5}
            final_price = int(pricing_matrix[app_type] * age_multiplier[selected_timeline] * dur_map[duration])
            
            st.metric("Total Payable (Inc. Taxes)", f"₹{final_price}")
            if st.button("Proceed to Checkout"):
                st.session_state.temp_data = {"app": app_type, "brand": brand_name, "timeline": selected_timeline, "price": final_price, "duration": duration}
                st.session_state.checkout_step = 'details'
                st.rerun()

        # STEP 2: Details (With Validation)
        elif st.session_state.checkout_step == 'details':
            st.header("📋 Billing Details")
            with st.form("details_form"):
                u_name = st.text_input("Name")
                u_email = st.text_input("Email")
                u_mobile = st.text_input("Mobile")
                u_addr = st.text_area("Address")
                
                if st.form_submit_button("Proceed to Payment"):
                    if u_name and u_email and u_mobile and u_addr:
                        st.session_state.temp_name = u_name
                        st.session_state.checkout_step = 'payment'
                        st.rerun()
                    else:
                        st.error("⚠️ All fields are mandatory to proceed.")

        # STEP 3: Payment
        elif st.session_state.checkout_step == 'payment':
            st.header("💳 Secure Payment")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Homigo", width=150)
            if st.button("Verify & Pay"):
                with st.spinner("Processing..."): 
                    time.sleep(1)
                st.session_state.checkout_step = 'success'
                st.rerun()

        # STEP 4: Success & Human-Logic Expiry
        elif st.session_state.checkout_step == 'success':
            st.balloons()
            st.header("✅ Payment Confirmed")
            if st.button("Go to Home"):
                # CALCULATION: Adding months so the day remains the same
                dur_str = st.session_state.temp_data['duration']
                months_map = {"6 Months": 6, "9 Months": 9, "1.5 Years": 18, "2 Years": 24, "3 Years": 36}
                add_months = months_map[dur_str]
                
                now = datetime.now()
                new_month = (now.month + add_months - 1) % 12 + 1
                new_year = now.year + (now.month + add_months - 1) // 12
                # Note: Handling potential February 29th or 31st issues
                try:
                    expiry_date = now.replace(year=new_year, month=new_month).strftime("%d %b %Y")
                except ValueError:
                    # If the day doesn't exist in that month (like 31st June), use last day of month
                    expiry_date = (now.replace(year=new_year, month=new_month, day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
                    expiry_date = expiry_date.strftime("%d %b %Y")
                
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
            for i in range(30):
                v = round(0.42 + np.random.normal(0, 0.04), 3)
                t = round(28.5 + np.random.normal(0, 0.6), 1)
                c = round(4.8 + np.random.normal(0, 0.1), 2)
                v1.metric("Vibration (mm/s)", f"{v}")
                v2.metric("Core Temp (°C)", f"{t}")
                v3.metric("Current (Amps)", f"{c}")
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
    st.write("Scan your appliance components for structural health verification.")
    up = st.file_uploader("Upload Component Image...", type=["jpg", "png", "jpeg"])
    
    if up:
        img = cv2.imdecode(np.asarray(bytearray(up.read()), dtype=np.uint8), 1)
        with st.spinner("AI analyzing structural patterns..."):
            time.sleep(1.2)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            density = np.sum(edges == 255) / edges.size
        
        c1, c2 = st.columns(2)
        c1.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Input Feed", use_container_width=True)
        c2.image(edges, caption="AI Edge Mapping", use_container_width=True)
        
        st.markdown("### 🔍 Homigo Diagnostic Report")
        if density > 0.05:
            st.error("**Finding: CRITICAL FAULT DETECTED**")
            st.markdown("1. **Immediate Shutdown Required.**\n2. **Technician Visit:** Covered under Shield.")
            st.markdown("---")
            st.subheader("📅 Book Your Service Slot")
            with st.form("service_booking"):
                day = st.selectbox("Select Preferred Day:", ["Today", "Tomorrow", "Monday", "Tuesday"])
                slot = st.selectbox("Select Time Slot:", ["Morning", "Afternoon", "Evening"])
                if st.form_submit_button("Confirm Slot & Book Technician"):
                    st.success(f"✅ Technician Booked for {day} during the {slot}!")
                    st.balloons()
        else:
            st.success("**Finding: HEALTHY COMPONENT**")
            st.write("Proceed with routine quarterly maintenance.")
        st.metric("AI Confidence", f"{round(92 + (density * 10), 2)}%")
