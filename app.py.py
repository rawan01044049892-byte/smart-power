import streamlit as st
import pandas as pd
import numpy as np
import random

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Smart Power", layout="wide")

# --- 2. إدارة الحالة (اللغة والصفحات) ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

# --- 3. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    /* خلفية صفحة الترحيب كحلي سادة */
    .welcome-bg {
        background-color: #001f3f;
        color: white;
        padding: 100px;
        border-radius: 25px;
        text-align: center;
        border: 2px solid #29b5e8;
    }
    /* جعل زر الإضافة أخضر */
    .green-btn button {
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px !important;
        width: 100%;
    }
    /* تنسيق كروت الأجهزة */
    .device-box {
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة الترحيب (Welcome Screen) ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="welcome-bg">
            <h1 style='color: #29b5e8; font-size: 60px;'>⚡ SMART POWER</h1>
            <p style='font-size: 24px;'>Full Home Energy Control System</p>
            <hr style='border-color: #0074D9;'>
            <h2 style='color: #2ECC40;'>Developed by: Rawan Essam El_sayed</h2>
            <p style='margin-top: 20px;'>Monitor your appliances and save energy today.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("ENTER DASHBOARD 🚀", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()

# --- 5. لوحة التحكم (Dashboard) ---
else:
    # القائمة الجانبية
    with st.sidebar:
        st.title("⚙️ Control")
        st.session_state.lang = st.radio("Language / اللغة", ["Arabic", "English"])
        st.divider()
        st.write(f"👤 **Dev:** Rawan Essam")
        if st.button("Logout"):
            st.session_state.page = 'welcome'
            st.rerun()

    is_ar = st.session_state.lang == "Arabic"
    st.title("💡 Smart Power Dashboard" if not is_ar else "💡 لوحة تحكم Smart Power")
    st.write(f"**Developer:** Rawan Essam El_sayed")
    st.markdown("---")

    # --- الجزء الأول: ملخص الاستهلاك (Metrics) ---
    watt_now = 2450 # مجموع استهلاك الأجهزة الشغالة
    cost_now = round(watt_now * 0.015, 2)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="الاستهلاك اللحظي" if is_ar else "Current Usage", value=f"{watt_now} W", delta="1.8%")
    with m2:
        st.metric(label="التكلفة التقديرية" if is_ar else "Estimated Cost", value=f"{cost_now} EGP/hr")
    with m3:
        st.metric(label="عدد الأجهزة النشطة" if is_ar else "Active Devices", value="10")

    st.divider()

    # --- الجزء الثاني: قائمة أجهزة المنزل كاملة ---
    st.subheader("🏠 Home Appliances List" if not is_ar else "🏠 قائمة أجهزة المنزل")
    
    # مصفوفة البيانات (الجهاز، الاستهلاك، الحالة واللون)
    devices = [
        ("Refrigerator" if not is_ar else "الثلاجة", "250W", "🟢 ON", "success"),
        ("Air Conditioner" if not is_ar else "التكييف", "1500W", "🟢 ON", "success"),
        ("Electric Oven" if not is_ar else "الفرن الكهربائي", "0W", "🔴 OFF", "error"),
        ("Washing Machine" if not is_ar else "الغسالة", "0W", "🔴 OFF", "error"),
        ("Smart TV" if not is_ar else "الشاشة الذكية", "120W", "🟢 ON", "success"),
        ("Microwave" if not is_ar else "الميكروويف", "0W", "🔴 OFF", "error"),
        ("Water Heater" if not is_ar else "السخان", "2000W", "🟢 ON", "success"),
        ("WiFi Router" if not is_ar else "الراوتر", "15W", "🔵 Standby", "info"),
        ("Laptop" if not is_ar else "اللابتوب", "65W", "🟢 ON", "success"),
        ("Room Lighting" if not is_ar else "إضاءة الغرف", "100W", "🟢 ON", "success"),
        ("Mobile Charger" if not is_ar else "شاحن الموبايل", "0.7W", "🔵 Warning", "info"),
        ("Electric Iron" if not is_ar else "المكواة", "0W", "🔴 OFF", "error"),
    ]

    # عرض الأجهزة في قائمة (كل جهاز في صف)
    for name, power, status, color in devices:
        col_n, col_p, col_s = st.columns([2, 1, 1])
        with col_n:
            st.write(f"**{name}**")
        with col_p:
            st.write(f"Consumption: {power}" if not is_ar else f"الاستهلاك: {power}")
        with col_s:
            if color == "success": st.success(status)
            elif color == "error": st.error(status)
            else: st.info(status)

    st.divider()

    # --- الجزء الثالث: إضافة جهاز جديد (الزر الأخضر) ---
    st.subheader("➕ Add New Device" if not is_ar else "➕ إضافة جهاز جديد")
    d_input = st.text_input("Enter device name" if not is_ar else "أدخل اسم الجهاز")
    
    st.markdown('<div class="green-btn">', unsafe_allow_html=True)
    if st.button("Save Device" if not is_ar else "حفظ الجهاز"):
        if d_input:
            st.success(f"Device '{d_input}' added to the list!" if not is_ar else f"تم إضافة '{d_input}' للقائمة!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    # الرسم البياني
    st.subheader("📈 Energy Usage Curve" if not is_ar else "📈 منحنى استهلاك الطاقة")
    st.area_chart(pd.DataFrame(np.random.randint(500, 4000, size=24), columns=['Watts']))
    
    st.caption(f"Smart Power System © 2026 | Designed by Rawan Essam El_sayed")