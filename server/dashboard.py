import streamlit as st
import sqlite3
import pandas as pd
import time
import plotly.express as px

st.set_page_config(page_title="Giám sát Bảo mật IoT", layout="wide")

st.title("Hệ thống Giám sát Mã hóa IoT - Database Edition")
st.subheader("Bảo mật tầng ứng dụng cho thiết bị tài nguyên hạn chế")

DB_NAME = 'iot_security.db'

def get_data():
    conn = sqlite3.connect(DB_NAME)
    df_telemetry = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 100", conn)
    df_stats = pd.read_sql_query("SELECT status, count(*) as count FROM telemetry GROUP BY status", conn)
    conn.close()
    return df_telemetry, df_stats

# Placeholder để cập nhật dữ liệu thời gian thực
placeholder = st.empty()

while True:
    df, stats = get_data()
    
    with placeholder.container():
        # 1. Thong ke nhanh dang the (Metrics)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tong ban tin", len(df))
        with col2:
            safe_count = stats[stats['status'] == 'An toan']['count'].sum() if not stats.empty else 0
            st.metric("Ban tin an toan", int(safe_count))
        with col3:
            alert_count = stats[stats['status'] == 'Canh bao bao mat']['count'].sum() if not stats.empty else 0
            st.metric("Canh bao tan cong", int(alert_count), delta_color="inverse")

        # 2. Bieu do thoi gian thuc
        st.write("### Bieu do du lieu cam bien")
        if not df.empty and df['temperature'].notnull().any():
            # Chi lay du lieu "An toan" de ve bieu do
            df_safe = df[df['status'] == 'An toan'].copy()
            if not df_safe.empty:
                df_safe['timestamp'] = pd.to_datetime(df_safe['timestamp'])
                fig = px.line(df_safe, x='timestamp', y=['temperature', 'humidity'], 
                              title='Dien bien Nhiet do va Do am',
                              labels={'value': 'Gia tri', 'timestamp': 'Thoi gian'})
                st.plotly_chart(fig, use_container_width=True)
        
        # 3. Nhat ky va Bieu do tron
        col_list, col_pie = st.columns([2, 1])
        
        with col_list:
            st.write("### Nhat ky he thong (Moi nhat)")
            st.dataframe(df[['timestamp', 'device_id', 'temperature', 'humidity', 'status', 'error_msg']].head(10), 
                         use_container_width=True)
            
        with col_pie:
            st.write("### Ty le an ninh")
            if not stats.empty:
                fig_pie = px.pie(stats, values='count', names='status', 
                                 color='status',
                                 color_discrete_map={'An toàn':'green', 'Cảnh báo bảo mật':'red'})
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu thống kê")
            
    time.sleep(2) # Cập nhật mỗi 2 giây
