import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (Modern Glassmorphism UI) ---
st.markdown("""
<style>
    /* 1. Global Background Gradient */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* 2. Global Font & Direction */
    .main { 
        direction: rtl; 
        text-align: right; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    /* 3. Glassmorphism Card (Login & Dashboard) */
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 30px;
        margin-bottom: 20px;
        text-align: center;
    }

    /* 4. Stats Cards (Inside Dashboard) */
    .stat-box {
        background: white; 
        border-radius: 15px; 
        padding: 15px; 
        text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .stat-box:hover { transform: translateY(-5px); }
    .stat-val { font-size: 1.8rem; font-weight: bold; color: #1E88E5; }
    .stat-lbl { font-size: 0.85rem; color: #666; }

    /* 5. Inputs & Buttons */
    .stTextInput > label { display: none; } /* Hide default label */
    .stTextInput input { 
        text-align: center; 
        border-radius: 15px; 
        border: 2px solid #eee; 
        padding: 10px;
        font-size: 1.2rem;
        background: rgba(255, 255, 255, 0.9);
    }
    .stButton button { 
        width: 100%; 
        background: linear-gradient(90deg, #1E88E5, #42A5F5); 
        color: white; 
        font-size: 18px; 
        border-radius: 15px; 
        padding: 10px; 
        border: none;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
        transition: all 0.3s;
    }
    .stButton button:hover { 
        transform: scale(1.02); 
        box-shadow: 0 6px 20px rgba(30, 136, 229, 0.4); 
    }

    /* 6. Progress Bars */
    .progress-wrapper { text-align: right; margin-bottom: 15px; }
    .progress-header { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px; color: #444; font-weight: 600; }
    .progress-bg { background-color: #e0e0e0; border-radius: 10px; height: 12px; width: 100%; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 10px; transition: width 1s ease-in-out; }

    /* 7. Calculator Table */
    .calc-table { width: 100%; direction: rtl; border-collapse: separate; border-spacing: 0 8px; }
    .calc-table td { background: white; padding: 12px; border-radius: 0; border: 1px solid #eee; border-width: 1px 0; }
    .calc-table tr td:first-child { border-radius: 0 10px 10px 0; border-left: none; border-right: 1px solid #eee; }
    .calc-table tr td:last-child { border-radius: 10px 0 0 10px; border-right: none; border-left: 1px solid #eee; }
    .pass-row td { background-color: #e8f5e9; color: #2e7d32; font-weight: bold; border-color: #c8e6c9; }
    .hard-row td { background-color: #ffebee; color: #c62828; border-color: #ffcdd2; }

</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "النتيجة النهائية", 'font': {'size': 20, 'color': '#333'}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#ffebee'},
                {'range': [25, 40], 'color': '#fff3e0'},
                {'range': [40, 50], 'color': '#e8f5e9'}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Segoe UI'})
    return fig

def progress_html(label, value, max_val, color):
    percent = (value / max_val) * 100
    return f"""
    <div class="progress-wrapper">
        <div class="progress-header">
            <span>{label}</span>
            <span>{value} / {max_val}</span>
        </div>
        <div class="progress-bg">
            <div class="progress-fill" style="width: {percent}%; background-color: {color};"></div>
        </div>
    </div>
    """

def main():
    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
    except FileNotFoundError:
        st.error("❌ Database missing.")
        return

    # --- Login Logic ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Spacer
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Center Column
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            # GLASSMORPHISM LOGIN CARD
            st.markdown("""
            <div class="glass-card">
                <div style="font-size: 4rem; margin-bottom: 10px;">🔐</div>
                <h2 style="color:#333; margin:0;">بوابة الطلاب</h2>
                <p style="color:#555;">أدخل الرمز السري لعرض النتيجة</p>
            </div>
            """, unsafe_allow_html=True)
            
            key = st.text_input("Key", type="password", placeholder="-----", label_visibility="collapsed")
            
            if st.button("دخول"):
                if key:
                    record = df[df['رمز_الدخول'] == key]
                    if not record.empty:
                        st.session_state.logged_in = True
                        st.session_state.student = record.iloc[0]
                        st.rerun()
                    else:
                        st.error("❌ الرمز غير صحيح")
                else:
                    st.warning("يرجى كتابة الرمز")

    # --- Dashboard Logic ---
    else:
        row = st.session_state.student
        total = row['السعي النهائي (50)']

        # Badge Logic
        if total >= 40: badge, b_col, t_col = "🌟 ممتاز", "#e8f5e9", "#2e7d32"
        elif total >= 30: badge, b_col, t_col = "✅ جيد جداً", "#e3f2fd", "#1565C0"
        elif total >= 25: badge, b_col, t_col = "⚖️ متوسط", "#fff8e1", "#f57f17"
        else: badge, b_col, t_col = "⚠️ يحتاج متابعة", "#ffebee", "#c62828"

        # 1. HEADER CARD
        st.markdown(f"""
        <div class="glass-card" style="padding: 20px; text-align: right; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin:0; color:#333;">{row['اسم الطالب']}</h2>
                <p style="margin:0; color:#666; font-size:0.9rem;">المرحلة الدراسية الحالية</p>
            </div>
            <div style="background-color:{b_col}; color:{t_col}; padding:8px 20px; border-radius:30px; font-weight:bold;">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. GAUGE & DETAILS
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="glass-card" style="text-align:right;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#333; margin-bottom:20px;'>📊 التفاصيل</h4>", unsafe_allow_html=True)
            
            # Progress Bars
            st.markdown(progress_html("الامتحان النصفي", row['الامتحان النصفي'], 15, "#FF7043"), unsafe_allow_html=True)
            st.markdown(progress_html("السعي التكويني", row['السعي التكويني (40)'], 40, "#42A5F5"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ التقرير", row['التقرير (10)'], 10, "#FFA726"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ المناقشة", row['المناقشة (10)'], 10, "#66BB6A"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. STATS ROW
        total_col = 'السعي النهائي (50)'
        avg = df[total_col].mean()
        high = df[total_col].max()
        df_sort = df.sort_values(by=total_col, ascending=False).reset_index()
        rank = df_sort[df_sort['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1

        s1, s2, s3 = st.columns(3)
        s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. CALCULATOR
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align:right; color:#333;'>🧮 حاسبة الفاينل (Final Exam)</h4>", unsafe_allow_html=True)
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0: style, txt = "pass-row", "✅ ناجح"
            elif req > 50: style, txt = "hard-row", "❌ غير ممكن"
            else: style, txt = "", f"تحتاج <b>{req}</b>"
            rows += f"<tr class='{style}'><td>{lbl}</td><td>{txt}</td></tr>"
            
        st.markdown(f"<table class='calc-table'>{rows}</table>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
