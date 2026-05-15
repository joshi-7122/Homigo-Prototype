import streamlit as st
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Homigo Expert | Pro App", layout="centered")

# --- 1. SIMULATED "EXCEL" DATABASE ---
if 'jobs_db' not in st.session_state:
    # This acts as your backend Excel Sheet
    st.session_state.jobs_db = pd.DataFrame({
        "Job_ID": ["#HM-101", "#HM-102"],
        "Customer": ["Aryan Joshi", "Dr. Sharma"],
        "Appliance": ["IFB Washing Machine", "Samsung AC"],
        "Slot": ["10:00 AM - 1:00 PM", "2:00 PM - 5:00 PM"],
        "Status": ["Scheduled", "Scheduled"],
        "Start_Time": ["--", "--"],
        "End_Time": ["--", "--"],
        "Payment": ["Pending", "Pending"],
        "Rating": ["--", "--"]
    })

if 'active_job' not in st.session_state:
    st.session_state.active_job = None

# --- UI BRANDING ---
st.title("🛠️ Homigo Expert")
st.write("Welcome, **Tech. Rahul Kumar** | ID: 9022")
st.markdown("---")

# --- 2. THE MASTER DASHBOARD (The "Excel" View) ---
st.subheader("📋 Today's Master Itinerary")
st.dataframe(st.session_state.jobs_db, use_container_width=True, hide_index=True)
st.markdown("---")

# --- 3. JOB EXECUTION WORKFLOW ---
st.subheader("📱 Active Job Terminal")

# Job Selector
job_list = st.session_state.jobs_db[st.session_state.jobs_db['Status'] != "Completed"]['Job_ID'].tolist()

if not job_list:
    st.success("🎉 All jobs completed for today! Time to head home.")
else:
    selected_job = st.selectbox("Select Next Job to Execute:", job_list)
    
    # Get current job details
    job_idx = st.session_state.jobs_db.index[st.session_state.jobs_db['Job_ID'] == selected_job][0]
    job_status = st.session_state.jobs_db.at[job_idx, 'Status']
    
    st.info(f"**Target:** {st.session_state.jobs_db.at[job_idx, 'Customer']} | **Task:** {st.session_state.jobs_db.at[job_idx, 'Appliance']}")

    # --- PHASE 1: REACHED & START OTP ---
    if job_status == "Scheduled":
        st.write("📍 **Status: En Route / Arrived**")
        with st.form("start_otp_form"):
            start_otp = st.text_input("Enter 4-Digit Customer OTP to Begin Service:", max_chars=4)
            if st.form_submit_button("Verify & Start Timer"):
                if start_otp == "1234": # Simulated correct OTP
                    st.session_state.jobs_db.at[job_idx, 'Status'] = "In Progress"
                    st.session_state.jobs_db.at[job_idx, 'Start_Time'] = datetime.now().strftime("%H:%M:%S")
                    st.success("✅ OTP Verified! Timer started.")
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Ask the customer for the correct code.")

    # --- PHASE 2: JOB IN PROGRESS & END OTP ---
    elif job_status == "In Progress":
        st.write("⚙️ **Status: Service In Progress**")
        start_t = st.session_state.jobs_db.at[job_idx, 'Start_Time']
        st.caption(f"Job started at: {start_t}")
        
        with st.form("end_job_form"):
            st.write("Service Complete? Verify with Customer.")
            end_otp = st.text_input("Enter 4-Digit Closing OTP:", max_chars=4)
            
            # --- PHASE 3: PAYMENT & REVIEW ---
            st.write("💰 **Payment & Closure**")
            payment_collected = st.checkbox("Payment of ₹450 Collected via UPI/Cash")
            customer_rating = st.slider("Customer Satisfaction Rating (Stars)", 1, 5, 5)
            
            if st.form_submit_button("Finalize & Close Job"):
                if end_otp == "9999": # Simulated closing OTP
                    if payment_collected:
                        # Update "Excel" Data
                        st.session_state.jobs_db.at[job_idx, 'Status'] = "Completed"
                        st.session_state.jobs_db.at[job_idx, 'End_Time'] = datetime.now().strftime("%H:%M:%S")
                        st.session_state.jobs_db.at[job_idx, 'Payment'] = "Collected"
                        st.session_state.jobs_db.at[job_idx, 'Rating'] = "⭐" * customer_rating
                        st.success("✅ Job Officially Closed! Data synced to Homigo Servers.")
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("⚠️ Please confirm payment collection before closing the job.")
                else:
                    st.error("❌ Invalid Closing OTP.")
