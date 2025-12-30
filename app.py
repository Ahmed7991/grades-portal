import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (Navy & Slate Theme) ---
st.markdown("""
<style>
    /* 1. Global Background */
    .stApp {
        background-color: #f1f5f9; /* Slate-100 */
    }
    .main { 
        direction: rtl; 
        text-align: right; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        color: #1e293b; /* Slate-800 */
    }
    
    /* 2. Cards */
    .pro-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        padding: 24px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
    }

    /* 3. Typography */
    h1, h2, h3, h4 { color: #0f172a; margin: 0; font-weight: 700; } /* Slate-900 */
    p { color: #64748b; font-size: 0.95rem; } /* Slate-500 */
    
    /* 4. Stats Boxes */
    .stat-box {
        background: #f8fafc; 
        border-radius: 8px; 
        padding: 12px; 
        text-align: center; 
        border: 1px solid #e2e8f0;
    }
    .stat-val { font-size: 1.6rem; font-weight: 800; color: #334155; }
    .stat-lbl { font-size: 0.8rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

    /* 5. Inputs & Buttons */
    .stTextInput input { 
        text-align: center; 
        border-radius: 8px; 
        border: 1px solid #cbd5e1; 
        padding: 10px;
        font-size: 1.1rem;
        color: #334155;
    }
    .stButton button { 
        width: 100%; 
        background-color: #334155; /* Slate-700 */
        color: white; 
        font-size: 16px; 
        border-radius: 8px; 
        padding: 12px 0;
        border: none;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton button:hover { background-color: #1e293b; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }

    /* 6. Progress Bars styling container */
    .bar-container {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }
    .bar-label { flex: 1; font-size: 0.9rem; font-weight: 600; color: #475569; }
    .bar-val { font-size: 0.85rem; font-weight: bold; color: #64748b; margin-left: 10px; min-width: 40px; text-align: left; }

    /* 7. Calculator Table */
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 15px; }
    .calc-table th { text-align: right; color: #64748b; font-size: 0.85rem; padding: 10px; border-bottom: 2px solid #f1f5f9; }
    .calc-table td { padding: 12px 10px; border-bottom: 1px solid #f1f5f9; color: #334155; font-weight: 500; }

</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 18, 'color': '#475569'}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#cbd5e1'},
            'bar': {'color': "#475569"}, # Dark Slate needle
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#fee2e2'}, # Soft Red
                {'range': [25, 40], 'color': '#fef3c7'}, # Soft Amber
                {'range': [40, 50], 'color': '#d1fae5'}  # Soft Emerald
            ],
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Segoe UI'})
    return fig

def progress_html(label, value, max_val):
    try: val_float = float(value)
    except: val_float = 0.0
    percent = (val_float / max_val) * 100
    
    # Cohesive Color (Slate Blue)
    color = "#64748b" 
    
    return f"""
    <div style="margin-bottom: 10px;">
        <div style="display:flex; justify-content:space-between; font-size:0.9rem; color:#475569; margin-bottom:4px; font-weight:600;">
            <span>{label}</span>
            <span>{val_float:g} / {max_val}</span>
        </div>
        <div style="background-color:#f1f5f9; border-radius:6px; height:8px; width:100%; overflow:hidden;">
            <div style="background-color:{color}; width:{percent}%; height:100%; border-radius:6px;"></div>
        </div>
    </div>
    """

def main():
    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
        # Force numeric conversion for calculation
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
            <div class="pro-card" style="text-align: center; border-top: 4px solid #334155;">
                <div style="font-size: 3rem; margin-bottom: 15px;">🏛️</div>
                <h2 style="color:#1e293b;">بوابة النتائج</h2>
                <p style="margin-top:5px;">النظام الأكاديمي للطلاب</p>
            </div>
            """, unsafe_allow_html=True)
            
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="أدخل رمز الدخول")
            
            if st.button("تسجيل الدخول"):
                if key:
                    record = df[df['رمز_الدخول'] == key]
                    if not record.empty:
                        st.session_state.logged_in = True
                        st.session_state.student = record.iloc[0]
                        st.rerun()
                    else:
                        st.error("❌ الرمز غير موجود")
                else:
                    st.warning("يرجى إدخال الرمز")

    # --- DASHBOARD ---
    else:
        row = st.session_state.student
        total = float(row['السعي النهائي (50)'])

        # Badge Logic (Soft Pastels)
        if total >= 40: badge, b_bg, b_txt = "🌟 ممتاز", "#dcfce7", "#166534"
        elif total >= 30: badge, b_bg, b_txt = "✅ جيد جداً", "#e0f2fe", "#075985"
        elif total >= 25: badge, b_bg, b_txt = "⚖️ متوسط", "#fef9c3", "#854d0e"
        else: badge, b_bg, b_txt = "⚠️ تنبيه", "#fee2e2", "#991b1b"

        # 1. Header
        st.markdown(f"""
        <div class="pro-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: right;">
                <h2 style="font-size: 1.4rem;">{row['اسم الطالب']}</h2>
                <p style="margin:0;">السجل الأكاديمي</p>
            </div>
            <div style="background-color:{b_bg}; color:{b_txt}; padding:5px 15px; border-radius:20px; font-weight:bold; font-size:0.85rem;">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Main Visuals
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown('<div class="pro-card" style="height: 100%; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="pro-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:20px; color:#475569;'>📊 تفاصيل الدرجات</h4>", unsafe_allow_html=True)
            st.markdown(progress_html("الامتحان النصفي", row['الامتحان النصفي'], 15), unsafe_allow_html=True)
            st.markdown(progress_html("السعي التكويني", row['السعي التكويني (40)'], 40), unsafe_allow_html=True)
            st.markdown(progress_html("↳ التقرير", row['التقرير (10)'], 10), unsafe_allow_html=True)
            st.markdown(progress_html("↳ المناقشة", row['المناقشة (10)'], 10), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 3. Stats
        total_col = 'السعي النهائي (50)'
        avg = df[total_col].mean()
        high = df[total_col].max()
        df_sort = df.sort_values(by=total_col, ascending=False).reset_index()
        rank = df_sort[df_sort['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1

        s1, s2, s3 = st.columns(3)
        s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        # 4. Calculator
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:10px;'>🧮 حاسبة الامتحان النهائي (Final Exam)</h4>", unsafe_allow_html=True)
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0:
                # Green styling (Inline for reliability)
                rows += f"<tr><td>{lbl}</td><td style='color:#166534; font-weight:bold; background-color:#f0fdf4; border-radius:6px;'>✅ ناجح مسبقاً</td></tr>"
            elif req > 50:
                # Red styling (Inline)
                rows += f"<tr><td>{lbl}</td><td style='color:#991b1b; background-color:#fef2f2; border-radius:6px; opacity:0.8;'>❌ غير ممكن</td></tr>"
            else:
                # Normal
                rows += f"<tr><td>{lbl}</td><td style='color:#1e293b; font-weight:600;'>تحتاج <b>{int(req)}</b> / 50</td></tr>"
            
        st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير المطلوب</th><th>المطلوب في الفاينل</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
