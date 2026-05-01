import streamlit as st
import json
import os
import time

st.set_page_config(page_title="Giám sát Bảo mật IoT", layout="wide")

st.title("Hệ thống Giám sát Mã hóa IoT")
st.subheader("Bảo mật tầng ứng dụng cho thiết bị tài nguyên hạn chế")

# Placeholder để cập nhật dữ liệu thời gian thực
placeholder = st.empty()

LOG_FILE = 'data_log.json'

while True:
    with placeholder.container():
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                except:
                    logs = []
            
            # Chia màn hình làm 2 cột
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("### 📜 Nhật ký nhận tin (Thời gian thực)")
                for entry in logs:
                    if entry['status'] == "An toàn":
                        st.success(f"**[HỢP LỆ]** {entry['data']}")
                    else:
                        st.error(f"**[CẢNH BÁO]** {entry['data']}")
            
            with col2:
                st.write("### 📊 Thống kê nhanh")
                success_count = sum(1 for e in logs if e['status'] == "An toàn")
                alert_count = sum(1 for e in logs if e['status'] == "Cảnh báo bảo mật")
                
                st.metric("Bản tin an toàn", f"{success_count}")
                st.metric("Cảnh báo tấn công", f"{alert_count}", delta_color="inverse")
        else:
            st.info("Đang chờ dữ liệu đầu tiên từ Server...")
            
    time.sleep(1) # Cập nhật mỗi giây
