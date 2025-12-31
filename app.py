import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (High Contrast Force-Light Theme) ---
st.markdown("""
<style>
    /* 1. FORCE LIGHT THEME (Fixes the "Unreadable Text" issue) */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa; /* Light Grey Background */
    }
    
    /* Force all text to be Dark Grey/Black */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li {
        color: #212529 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main { 
        direction: rtl; 
        text-align: right; 
    }

    /* 2. Cards Styling */
    .pro-card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
    }

    /* 3. Stats Boxes */
    .stat-box {
        background: #e9ecef; /* Darker grey for contrast */
        border-radius: 8px; 
        padding: 15px; 
        text-align: center; 
        border: 1px solid #ced4da;
    }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: #0d6efd !important; } /* Bright Blue */
    .stat-lbl { font-size: 0.9rem; color: #495057 !important; font-weight: 700; }

    /* 4. Input Fields (Force White Background + Black Text) */
    .stTextInput input { 
        background-color: #ffffff !important;
        color: #000000 !important;
        text-align: center; 
        border-radius: 8px; 
        border: 2px solid #ced4da; 
        padding: 10px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    /* 5. Buttons */
    .stButton button { 
        width: 100%; 
        background-color: #0d6efd !important; /* Bootstrap Blue */
        color: white !important; 
        font-size: 18px; 
        border-radius: 8px; 
        padding: 12px 0;
        border: none;
        font-weight: 700;
    }
    .stButton button:hover { background-color: #0b5ed7 !important; }

    /* 6. Progress Bars */
    .bar-label { display: flex; justify-content: space-between; font-weight: 700; color: #343a40 !important; margin-bottom: 5px; }
    .bar-bg { background-color: #dee2e6; border-radius: 6px; height: 12px; width: 100%; overflow: hidden; border: 1px solid #ced4da; }
    .bar-fill { height: 100%; }

    /* 7. Calculator Table (High Contrast) */
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 15px; }
    .calc-table th { background-color: #e9ecef; color: #212529 !important; font-weight: 800; padding: 12px; border-bottom: 2px solid #dee2e6; }
    .calc-table td { padding: 12px; border-bottom: 1px solid #dee2e6; color: #212529 !important; font-weight: 600; }
    
</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 24, 'color': '#212529', 'family': 'Segoe UI'}}, # Force Dark Text
        number = {'font': {'color': '#212529', 'size': 40}}, # Force Dark Number
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#343a40'},
            'bar': {'color': "#343a40"}, # Dark Grey Needle
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#dee2e6",
            'steps': [
                {'range': [0, 25], 'color': '#ffccd5'}, # High Contrast Red
                {'range': [25, 40], 'color': '#fff3cd'}, # High Contrast Yellow
                {'range': [40, 50], 'color': '#d1e7dd'}  # High Contrast Green
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Segoe UI'})
    return fig

def progress_html(label, value, max_val, color_hex):
    try: val_float = float(value)
    except: val_float = 0.0
    percent = (val_float / max_val) * 100
    
    return f"""
    <div style="margin-bottom: 15px;">
        <div class="bar-label">
            <span>{label}</span>
            <span>{val_float:g} / {max_val}</span>
        </div>
        <div class="bar-bg">
            <div class="bar-fill" style="width: {percent}%; background-color: {color_hex};"></div>
        </div>
    </div>
    """

def main():
    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
        df['السعي النهائي (50)'] = pd.to_numeric(df['السعي النهائي (50)'], errors='coerce').fillna(0)
    except FileNotFoundError:
        st.error("❌ Database missing.")
        return

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # --- LOGIN ---
    if not st.session_state.logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""
            <div class="pro-card" style="text-align: center; border-top: 5px solid #0d6efd;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🎓</div>
                <h2 style="font-size: 1.8rem;">بوابة النتائج</h2>
                <p style="font-weight: 600;">يرجى إدخال الرمز السري</p>
            </div>
            """, unsafe_allow_html=True)
            
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="أدخل الرمز هنا")
            
            if st.button("تسجيل الدخول"):
                if key:
                    record = df[df['رمز_الدخول'] == key]
                    if not record.empty:
                        st.session_state.logged_in = True
                        st.session_state.student = record.iloc[0]
                        st.rerun()
                    else:
                        st.error("❌ الرمز غير صحيح")
                else:
                    st.warning("⚠️ أدخل الرمز")

    # --- DASHBOARD ---
    else:
        row = st.session_state.student
        total = float(row['السعي النهائي (50)'])

        # Badge Logic (High Contrast Colors)
        if total >= 40: badge, b_bg, b_txt = "🌟 ممتاز", "#d1e7dd", "#0f5132"
        elif total >= 30: badge, b_bg, b_txt = "✅ جيد جداً", "#cfe2ff", "#084298"
        elif total >= 25: badge, b_bg, b_txt = "⚖️ متوسط", "#fff3cd", "#664d03"
        else: badge, b_bg, b_txt = "⚠️ تنبيه", "#f8d7da", "#842029"

        # 1. HEADER
        st.markdown(f"""
        <div class="pro-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: right;">
                <h2 style="font-size: 1.6rem; color: #212529;">{row['اسم الطالب']}</h2>
                <p style="margin:0; font-weight: bold; color: #6c757d;">السجل الأكاديمي</p>
            </div>
            <div style="background-color:{b_bg}; color:{b_txt}; padding:8px 20px; border-radius:30px; font-weight:800; border: 1px solid {b_txt};">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. VISUALS
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown('<div class="pro-card" style="height: 100%; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="pro-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;'>📊 تفاصيل الدرجات</h4>", unsafe_allow_html=True)
            # High Contrast Bar Colors
            st.markdown(progress_html("الامتحان النصفي", row['الامتحان النصفي'], 15, "#fd7e14"), unsafe_allow_html=True) # Orange
            st.markdown(progress_html("السعي التكويني", row['السعي التكويني (40)'], 40, "#0d6efd"), unsafe_allow_html=True) # Blue
            st.markdown(progress_html("↳ التقرير", row['التقرير (10)'], 10, "#6f42c1"), unsafe_allow_html=True) # Purple
            st.markdown(progress_html("↳ المناقشة", row['المناقشة (10)'], 10, "#198754"), unsafe_allow_html=True) # Green
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. STATS
        total_col = 'السعي النهائي (50)'
        avg = df[total_col].mean()
        high = df[total_col].max()
        df_sort = df.sort_values(by=total_col, ascending=False).reset_index()
        rank = df_sort[df_sort['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1

        s1, s2, s3 = st.columns(3)
        s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        # 4. CALCULATOR
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:15px;'>🧮 حاسبة الامتحان النهائي (من 50)</h4>", unsafe_allow_html=True)
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0:
                # Green Background, Dark Green Text
                rows += f"<tr><td>{lbl}</td><td style='background-color:#d1e7dd; color:#0f5132; font-weight:bold; border-radius:5px;'>✅ ناجح مسبقاً</td></tr>"
            elif req > 50:
                # Red Background, Dark Red Text
                rows += f"<tr><td>{lbl}</td><td style='background-color:#f8d7da; color:#842029; border-radius:5px; opacity:0.9;'>❌ غير ممكن</td></tr>"
            else:
                rows += f"<tr><td>{lbl}</td><td style='color:#212529; font-weight:bold;'>تحتاج <b>{int(req)}</b></td></tr>"
            
        st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير المطلوب</th><th>المطلوب في الفاينل</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
