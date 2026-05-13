import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Homigo Pulse | Circuit Monitor", layout="wide")

# --- CUSTOM CSS FOR INDUSTRIAL LOOK ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: HARDWARE STATUS ---
st.sidebar.title("🔌 Hardware Node: 047")
st.sidebar.info("Location: Server Room / Unit 12B")
st.sidebar.markdown("---")
st.sidebar.write("**Gateway Status:** Connected")
st.sidebar.write("**Signal Strength:** -67dBm")
st.sidebar.write("**Firmware:** v2.4.1-Stable")

# --- HEADER ---
st.title("📟 Homigo Pulse")
st.subheader("Industrial IoT Circuit Telemetry Dashboard")
st.markdown("---")

# --- 1. REAL-TIME METRIC PLACEHOLDERS ---
m1, m2, m3, m4 = st.columns(4)
volt_metric = m1.empty()
curr_metric = m2.empty()
pf_metric = m3.empty()
temp_metric = m4.empty()

# --- 2. LIVE OSCILLOSCOPE (CHART) ---
st.markdown("### 📊 Phase Vibration & Power Oscilloscope")
chart_placeholder = st.empty()

# --- 3. LOG & DIAGNOSTICS ---
st.markdown("---")
col_log, col_stat = st.columns([2, 1])

with col_stat:
    st.write("🔍 **Node Health Check**")
    st.progress(98, text="Relay Health: 98%")
    st.progress(100, text="Fuse Status: Normal")
    st.progress(85, text="Storage: 85%")

with col_log:
    st.write("📋 **System Log (Live)**")
    log_placeholder = st.empty()

# --- SIMULATION ENGINE ---
if st.button("Initialize Live Stream"):
    # Buffers for history
    v_history = []
    p_history = []
    logs = ["Checking connectivity...", "Handshake successful.", "Fetching phase data..."]
    
    for i in range(100): # Run for 100 cycles
        # Simulated Electrical Logic
        v = round(230 + np.random.normal(0, 2), 1)     # Voltage (India Std 230V)
        a = round(5.5 + np.random.normal(0, 0.3), 2)   # Amps
        pf = round(0.92 + np.random.normal(0, 0.01), 2) # Power Factor
        t = round(32 + (i * 0.1) + np.random.normal(0, 0.2), 1) # Rising temp simulation
        
        # Update Metrics
        volt_metric.metric("Voltage (V)", f"{v}V", delta="0.2V")
        curr_metric.metric("Load (A)", f"{a}A", delta="-0.05A")
        pf_metric.metric("Power Factor", f"{pf}", delta="Optimal")
        temp_metric.metric("Node Temp", f"{t}°C", delta="Rising" if i > 50 else "Stable")
        
        # Update Chart (Simulating a sine wave-ish vibration)
        v_history.append(v)
        p_history.append(a * 10) # Scaling for visibility
        chart_data = pd.DataFrame({
            "Voltage Baseline": v_history[-30:],
            "Load Intensity": p_history[-30:]
        })
        chart_placeholder.line_chart(chart_data)
        
        # Dynamic Logging
        if v > 235:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] WARNING: Voltage surge detected.")
        if i % 10 == 0:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Heartbeat sent to Homigo Cloud.")
        
        log_placeholder.code("\n".join(logs[-6:])) # Show last 6 logs
        
        time.sleep(0.5)

    st.success("Monitoring session completed. Data logged to secure buffer.")
