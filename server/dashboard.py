import streamlit as st
import sqlite3
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="He quan tri an ninh IoT", layout="wide")

DB_NAME = 'iot_security.db'

def get_db_connection():
    return sqlite3.connect(DB_NAME)

# --- HAM TIEN ICH ---
def load_telemetry():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def load_attack_logs():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM attack_logs ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def load_devices():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM devices", conn)
    conn.close()
    return df

# --- GIAO DIEN ---
st.title("He thong Quan tri va Giam sat An ninh IoT")

tabs = st.tabs(["Giam sat thoi gian thuc", "Nhat ky an ninh", "Quan ly thiet bi", "Bao cao thong ke"])

# --- TAB 1: GIAM SAT THOI GIAN THUC ---
with tabs[0]:
    placeholder = st.empty()
    while True:
        df_telemetry = load_telemetry()
        df_safe = df_telemetry[df_telemetry['status'] == 'An toan'].head(50)
        
        with placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Do tre trung binh (s)", f"{df_safe['latency'].mean():.4f}" if not df_safe.empty else "0")
            col2.metric("Ban tin hop le", len(df_telemetry[df_telemetry['status'] == 'An toan']))
            col3.metric("Canh bao an ninh", len(df_telemetry[df_telemetry['status'] != 'An toan']))

            if not df_safe.empty:
                fig = px.line(df_safe, x='timestamp', y=['temperature', 'humidity'], title="Dien bien du lieu cam bien (50 ban tin gan nhat)")
                st.plotly_chart(fig, use_container_width=True)
                
                fig_lat = px.area(df_safe, x='timestamp', y='latency', title="Phan tich do tre xu ly (Latency)")
                st.plotly_chart(fig_lat, use_container_width=True)
        
        time.sleep(5) # Cap nhat moi 5 giay trong tab nay
        if st.session_state.get('stop_refresh'): break

# --- TAB 2: NHAT KY AN NINH ---
with tabs[1]:
    st.header("Danh sach cac no luc truy cap bat thuong")
    df_attacks = load_attack_logs()
    st.dataframe(df_attacks, use_container_width=True)
    
    if not df_attacks.empty:
        fig_pie = px.pie(df_attacks, names='attack_type', title="Phan loai cac kieu tan cong")
        st.plotly_chart(fig_pie)

# --- TAB 3: QUAN LY THIET BI (CRUD) ---
with tabs[2]:
    st.header("Danh sach thiet bi trong he thong")
    df_devs = load_devices()
    st.table(df_devs[['device_id', 'status', 'description']])
    
    with st.expander("Them thiet bi moi"):
        new_id = st.text_input("Device ID")
        new_node_key = st.text_input("Node Key (16 bytes)")
        new_gw_key = st.text_input("Gateway Key")
        new_desc = st.text_area("Mo ta")
        if st.button("Luu thiet bi"):
            conn = get_db_connection()
            conn.execute("INSERT INTO devices (device_id, node_key, gateway_key, description) VALUES (?,?,?,?)",
                         (new_id, new_node_key, new_gw_key, new_desc))
            conn.commit()
            conn.close()
            st.success("Da them thiet bi thanh cong")
            st.rerun()

    with st.expander("Mo khoa / Chan thiet bi"):
        target_id = st.selectbox("Chon thiet bi", df_devs['device_id'])
        action = st.radio("Hanh dong", ["active", "blocked"])
        if st.button("Cap nhat trang thai"):
            conn = get_db_connection()
            conn.execute("UPDATE devices SET status = ? WHERE device_id = ?", (action, target_id))
            conn.commit()
            conn.close()
            st.success(f"Da cap nhat trang thai {target_id} sang {action}")
            st.rerun()

# --- TAB 4: BAO CAO THONG KE ---
with tabs[3]:
    st.header("Xuat du lieu he thong")
    df_all = load_telemetry()
    
    csv = df_all.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Tai ve du lieu Telemetry (CSV)",
        data=csv,
        file_name=f"telemetry_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
    
    st.write("### Tom tat hoat dong")
    st.write(df_all.describe())
