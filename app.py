import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (Clean Professional UI) ---
st.markdown("""
<style>
    /* 1. Global Background & Font */
    .stApp {
        background-color: #f4f6f9;
        background-image: radial-gradient(#e3e8ef 1px, transparent 1px);
        background-size: 20px 20px;
    }
    .main { 
        direction: rtl; 
        text-align: right; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        color: #333;
    }
    
    /* 2. Clean Cards */
    .clean-card {
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #e1e4e8;
    }

    /* 3. Header Styling */
    h1, h2, h3, h4 { color: #1f2937; margin: 0; }
    p { color: #6b7280; }

    /* 4. Stats Boxes */
    .stat-box {
        background: #f8fafc; 
        border-radius: 12px; 
        padding: 15px; 
        text-align: center; 
        border: 1px solid #e2e8f0;
    }
    .stat-val { font-size: 1.8rem; font-weight: bold; color: #2563eb; }
    .stat-lbl { font-size: 0.85rem; color: #64748b; font-weight: 600; }

    /* 5. Inputs & Buttons */
    .stTextInput input { 
        text-align: center; 
        border-radius: 10px; 
        border: 1px solid #d1d5db; 
        padding: 10px;
        font-size: 1.1rem;
    }
    .stButton button { 
        width: 100%; 
        background-color: #2563eb; 
        color: white; 
        font-size: 16px; 
        border-radius: 10px; 
        padding: 10px 0;
        border: none;
        font-weight: 600;
        transition: background 0.2s;
    }
    .stButton button:hover { background-color: #1d4ed8; }

    /* 6. Progress Bars */
    .progress-label { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 4px; color: #374151; font-weight: 600; }
    .progress-bg { background-color: #e5e7eb; border-radius: 8px; height: 10px; width: 100%; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 8px; }

    /* 7. Calculator Table (Fixed Colors) */
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 10px; }
    .calc-table td, .calc-table th { padding: 12px; border-bottom: 1px solid #e5e7eb; color: #1f2937; text-align: right; }
    .calc-table th { font-weight: 600; color: #4b5563; background-color: #f9fafb; }
    
    /* Rows Styles */
    .row-pass { color: #166534 !important; font-weight: bold; background-color: #f0fdf4; }
    .row-fail { color: #991b1b !important; background-color: #fef2f2; opacity: 0.7; }
    .row-norm { color: #1f2937; }

</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 18, 'color': '#374151'}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#9ca3af'},
            'bar': {'color': "#2563eb"},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#fecaca'}, # Light Red
                {'range': [25, 40], 'color': '#fde68a'}, # Light Yellow
                {'range': [40, 50], 'color': '#bbf7d0'}  # Light Green
            ],
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Segoe UI'})
    return fig

def progress_html(label, value, max_val, color):
    # Ensure value handles NaN or non-numeric gracefully
    try:
        val_float = float(value)
    except:
        val_float = 0.0
    
    percent = (val_float / max_val) * 100
    return f"""
    <div style="margin-bottom: 12px;">
        <div class="progress-label">
            <span>{label}</span>
            <span>{val_float} / {max_val}</span>
        </div>
        <div class="progress-bg">
            <div class="progress-fill" style="width: {percent}%; background-color: {color};"></div>
        </div>
    </div>
    """

def main():
    try:
        # Force string for key to keep leading zeros
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
        
        # Ensure 'السعي النهائي (50)' is numeric
        # This fixes the calculator if the CSV had weird text formats
        df['السعي النهائي (50)'] = pd.to_numeric(df['السعي النهائي (50)'], errors='coerce').fillna(0)

    except FileNotFoundError:
        st.error("❌ Database missing.")
        return

    # --- Login Logic ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""
            <div class="clean-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 10px;">🔐</div>
                <h2>بوابة الطلاب</h2>
                <p>أدخل الرمز السري</p>
            </div>
            """, unsafe_allow_html=True)
            
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="رمز الدخول")
            
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
        total = float(row['السعي النهائي (50)'])

        # Badge Logic
        if total >= 40: badge, b_col, t_col = "🌟 ممتاز", "#dcfce7", "#166534"
        elif total >= 30: badge, b_col, t_col = "✅ جيد جداً", "#e0f2fe", "#0369a1"
        elif total >= 25: badge, b_col, t_col = "⚖️ متوسط", "#fef9c3", "#854d0e"
        else: badge, b_col, t_col = "⚠️ يحتاج متابعة", "#fee2e2", "#991b1b"

        # 1. HEADER CARD
        st.markdown(f"""
        <div class="clean-card" style="display: flex; justify-content: space-between; align-items: center; padding: 20px;">
            <div style="text-align: right;">
                <h2 style="font-size: 1.5rem; font-weight: bold;">{row['اسم الطالب']}</h2>
                <p style="margin:0; font-size: 0.9rem;">لوحة النتائج</p>
            </div>
            <div style="background-color:{b_col}; color:{t_col}; padding:6px 16px; border-radius:20px; font-weight:bold; font-size:0.9rem;">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. GAUGE & DETAILS
        c_left, c_right = st.columns([1, 1])
        
        with c_left:
            st.markdown('<div class="clean-card" style="height: 100%;">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="clean-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;'>📊 التفاصيل</h4>", unsafe_allow_html=True)
            
            st.markdown(progress_html("الامتحان النصفي", row['الامتحان النصفي'], 15, "#f97316"), unsafe_allow_html=True)
            st.markdown(progress_html("السعي التكويني", row['السعي التكويني (40)'], 40, "#3b82f6"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ التقرير", row['التقرير (10)'], 10, "#8b5cf6"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ المناقشة", row['المناقشة (10)'], 10, "#10b981"), unsafe_allow_html=True)
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

        # 4. CALCULATOR
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:15px;'>🧮 حاسبة الفاينل (Final Exam)</h4>", unsafe_allow_html=True)
        st.caption("كم تحتاج في الامتحان النهائي (من 50) للحصول على التقدير:")

        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0:
                # Already Passed
                rows += f"<tr class='row-pass'><td>{lbl}</td><td>✅ ناجح مسبقاً</td></tr>"
            elif req > 50:
                # Impossible
                rows += f"<tr class='row-fail'><td>{lbl}</td><td>❌ غير ممكن (تحتاج {int(req)})</td></tr>"
            else:
                # Needed
                rows += f"<tr class='row-norm'><td>{lbl}</td><td>تحتاج <b>{int(req)}</b> / 50</td></tr>"
            
        st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير المطلوب</th><th>الدرجة المطلوبة في النهائي</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
