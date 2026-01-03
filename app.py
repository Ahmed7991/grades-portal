import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CONFIGURATION ---
KEYS_FILE = "students.csv"  # File containing Name + Key
SUBJECTS_CONFIG = {
    "برمجة الالعاب": "game_programming.csv",
    "معمارية الحاسوب": "computer_architecture.csv",
    # To add more subjects, upload the CSV to GitHub and add a line here:
    # "الرياضيات": "math.csv",
    # "الفيزياء": "physics.csv",
}

# --- CUSTOM CSS (Professional Theme) ---
st.markdown("""
<style>
    /* Global Settings */
    [data-testid="stAppViewContainer"] { background-color: #f1f5f9; }
    .main { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
    h1, h2, h3, h4, p, div, span, label { color: #1e293b !important; }

    /* Cards */
    .pro-card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    /* Stats */
    .stat-box {
        background: #f8fafc;
        border-radius: 8px; 
        padding: 15px; 
        text-align: center; 
        border: 1px solid #e2e8f0;
    }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: #334155 !important; }
    .stat-lbl { font-size: 0.9rem; font-weight: 700; color: #64748b !important; }

    /* Inputs & Buttons */
    .stTextInput input { 
        background-color: #ffffff !important;
        color: #334155 !important;
        text-align: center; 
        border-radius: 8px; 
        border: 1px solid #cbd5e1; 
        padding: 10px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .stButton button { 
        width: 100%; 
        background-color: #334155 !important; 
        color: white !important; 
        font-size: 18px; 
        border-radius: 8px; 
        padding: 12px 0;
        border: none;
        font-weight: 700;
    }
    .stButton button:hover { background-color: #1e293b !important; }

    /* Progress Bars */
    .bar-label { display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 5px; color: #475569 !important; }
    .bar-bg { background-color: #f1f5f9; border-radius: 6px; height: 12px; width: 100%; overflow: hidden; border: 1px solid #e2e8f0; }
    .bar-fill { height: 100%; }

    /* Calculator Table */
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 15px; }
    .calc-table th { background-color: #f8fafc; padding: 12px; border-bottom: 2px solid #e2e8f0; font-weight: 800; color: #64748b !important; }
    .calc-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-weight: 600; color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

def load_keys():
    """Loads the student keys database"""
    try:
        # Force key to string to preserve leading zeros
        df = pd.read_csv(KEYS_FILE, dtype={'رمز_الدخول': str})
        return df
    except FileNotFoundError:
        return None

def load_subject_data(filename):
    """Loads a specific subject grade file"""
    try:
        df = pd.read_csv(filename)
        # Ensure numeric calculation
        if 'السعي النهائي (50)' in df.columns:
            df['السعي النهائي (50)'] = pd.to_numeric(df['السعي النهائي (50)'], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        return None

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 20, 'color': '#475569', 'family': 'Segoe UI'}},
        number = {'font': {'color': '#334155', 'size': 40}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#cbd5e1'},
            'bar': {'color': "#475569"},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#fee2e2'},
                {'range': [25, 40], 'color': '#fef3c7'},
                {'range': [40, 50], 'color': '#d1fae5'}
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
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_name = ""

    # --- LOGIN SCREEN ---
    if not st.session_state.logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""
            <div class="pro-card" style="text-align: center; border-top: 5px solid #334155;">
                <div style="font-size: 3.5rem; margin-bottom: 10px;">🏛️</div>
                <h2 style="font-size: 1.8rem;">بوابة النتائج</h2>
                <p style="font-weight: 600;">يرجى إدخال رمز الدخول</p>
            </div>
            """, unsafe_allow_html=True)
            
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="أدخل الرمز هنا")
            
            if st.button("تسجيل الدخول"):
                keys_df = load_keys()
                if keys_df is None:
                    st.error("❌ ملف الطلاب (students.csv) مفقود!")
                else:
                    # Look for key in students.csv
                    student_record = keys_df[keys_df['رمز_الدخول'] == key]
                    
                    if not student_record.empty:
                        # KEY FOUND -> Login Success
                        st.session_state.logged_in = True
                        st.session_state.student_name = student_record.iloc[0]['اسم الطالب']
                        st.rerun()
                    else:
                        st.error("❌ الرمز غير صحيح")

    # --- DASHBOARD SCREEN ---
    else:
        student_name = st.session_state.student_name

        # 1. Subject Selector
        st.markdown(f"""
        <div class="pro-card" style="display: flex; justify-content: space-between; align-items: center; padding: 15px;">
            <div style="text-align: right;">
                <h3 style="margin:0; font-size:1.2rem;">👤 {student_name}</h3>
            </div>
            <div>
               <span style="font-weight:bold; color:#334155; font-size:0.9rem;">اختر المادة 👇</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected_subject = st.selectbox("اختر المادة لعرض الدرجات:", list(SUBJECTS_CONFIG.keys()))

        # 2. Load Grade Data
        filename = SUBJECTS_CONFIG[selected_subject]
        grades_df = load_subject_data(filename)

        if grades_df is None:
            st.warning("⚠️ ملف الدرجات لهذه المادة غير موجود.")
            if st.button("تسجيل خروج"):
                st.session_state.logged_in = False
                st.rerun()
            return

        # 3. Find Student in Grades File by NAME
        # Note: We strip whitespace to ensure 'Ahmed ' matches 'Ahmed'
        record = grades_df[grades_df['اسم الطالب'].str.strip() == student_name.strip()]

        if record.empty:
            st.warning(f"⚠️ عذراً، لم يتم العثور على درجة للطالب **{student_name}** في مادة: **{selected_subject}**")
            st.caption("يرجى التأكد من أن الاسم في ملف الدرجات يطابق الاسم في ملف الرموز تماماً.")
            if st.button("تسجيل خروج"):
                st.session_state.logged_in = False
                st.rerun()
            return

        row = record.iloc[0]
        total = float(row['السعي النهائي (50)'])

        # 4. Badge Logic
        if total >= 40: badge, b_bg, b_txt = "🌟 ممتاز", "#d1e7dd", "#0f5132"
        elif total >= 30: badge, b_bg, b_txt = "✅ جيد جداً", "#cfe2ff", "#084298"
        elif total >= 25: badge, b_bg, b_txt = "⚖️ متوسط", "#fff3cd", "#664d03"
        else: badge, b_bg, b_txt = "⚠️ تنبيه", "#f8d7da", "#842029"

        # 5. Header
        st.markdown(f"""
        <div class="pro-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div><h3 style="margin:0;">{selected_subject}</h3></div>
            <div style="background-color:{b_bg}; color:{b_txt}; padding:5px 15px; border-radius:20px; font-weight:800; border:1px solid {b_txt}; font-size:0.85rem;">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

        # 6. Visuals
        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.markdown('<div class="pro-card" style="height: 100%; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="pro-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:20px; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; color:#475569;'>📊 التفاصيل</h4>", unsafe_allow_html=True)
            
            # Safe Get
            mid = row.get('الامتحان النصفي', 0)
            formative = row.get('السعي التكويني (40)', 0)
            rep = row.get('التقرير (10)', 0)
            disc = row.get('المناقشة (10)', 0)

            st.markdown(progress_html("الامتحان النصفي", mid, 15, "#fd7e14"), unsafe_allow_html=True)
            st.markdown(progress_html("السعي التكويني", formative, 40, "#0d6efd"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ التقرير", rep, 10, "#6f42c1"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ المناقشة", disc, 10, "#198754"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 7. Stats & Calculator
        total_col = 'السعي النهائي (50)'
        avg = grades_df[total_col].mean()
        high = grades_df[total_col].max()
        df_sort = grades_df.sort_values(by=total_col, ascending=False).reset_index()
        
        try:
            # We must find the rank by NAME now, not Key
            rank_idx = df_sort[df_sort['اسم الطالب'].str.strip() == student_name.strip()].index[0] + 1
        except:
            rank_idx = "-"

        s1, s2, s3 = st.columns(3)
        s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank_idx}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:15px; color:#334155;'>🧮 حاسبة الامتحان النهائي (من 50)</h4>", unsafe_allow_html=True)
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0:
                rows += f"<tr><td>{lbl}</td><td style='background-color:#d1e7dd; color:#0f5132; font-weight:bold; border-radius:5px;'>✅ ناجح مسبقاً</td></tr>"
            elif req > 50:
                rows += f"<tr><td>{lbl}</td><td style='background-color:#f8d7da; color:#842029; border-radius:5px; opacity:0.9;'>❌ غير ممكن</td></tr>"
            else:
                rows += f"<tr><td>{lbl}</td><td style='color:#334155; font-weight:bold;'>تحتاج <b>{int(req)}</b></td></tr>"
            
        st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير المطلوب</th><th>المطلوب في الفاينل</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
