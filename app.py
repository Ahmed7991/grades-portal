import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CONFIGURATION: DEFINE YOUR SUBJECTS HERE ---
# Format: "Subject Name": "filename.csv."
SUBJECTS_CONFIG = {
    "المادة الأساسية": "grades.csv",
    # To add more subjects, upload the CSV to GitHub and add a line here:
    # "الرياضيات": "math.csv",
    # "الفيزياء": "physics.csv",
}

# --- CUSTOM CSS (High Contrast & Clean) ---
st.markdown("""
<style>
    /* 1. Global Settings */
    [data-testid="stAppViewContainer"] { background-color: #f8f9fa; }
    .main { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, sans-serif; }
    h1, h2, h3, h4, p, div, span, label { color: #212529 !important; }

    /* 2. Subject Selector Styling */
    .subject-box {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 2px solid #dee2e6;
        text-align: center;
    }

    /* 3. Cards */
    .pro-card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
    }

    /* 4. Stats */
    .stat-box {
        background: #e9ecef;
        border-radius: 8px; 
        padding: 15px; 
        text-align: center; 
        border: 1px solid #ced4da;
    }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: #0d6efd !important; }
    .stat-lbl { font-size: 0.9rem; font-weight: 700; color: #495057 !important; }

    /* 5. Inputs & Buttons */
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
    .stButton button { 
        width: 100%; 
        background-color: #0d6efd !important; 
        color: white !important; 
        font-size: 18px; 
        border-radius: 8px; 
        padding: 12px 0;
        border: none;
        font-weight: 700;
    }
    .stButton button:hover { background-color: #0b5ed7 !important; }

    /* 6. Progress Bars */
    .bar-label { display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 5px; }
    .bar-bg { background-color: #dee2e6; border-radius: 6px; height: 12px; width: 100%; overflow: hidden; border: 1px solid #ced4da; }
    .bar-fill { height: 100%; }

    /* 7. Calculator Table */
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 15px; }
    .calc-table th { background-color: #e9ecef; padding: 12px; border-bottom: 2px solid #dee2e6; font-weight: 800; }
    .calc-table td { padding: 12px; border-bottom: 1px solid #dee2e6; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

def load_all_data():
    """Loads all configured CSV files into a dictionary"""
    datasets = {}
    for subject, filepath in SUBJECTS_CONFIG.items():
        try:
            df = pd.read_csv(filepath, dtype={'رمز_الدخول': str})
            # Ensure numeric column
            if 'السعي النهائي (50)' in df.columns:
                df['السعي النهائي (50)'] = pd.to_numeric(df['السعي النهائي (50)'], errors='coerce').fillna(0)
            datasets[subject] = df
        except FileNotFoundError:
            # We don't stop the app, just skip the missing file
            continue
    return datasets

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 24, 'color': '#212529', 'family': 'Segoe UI'}},
        number = {'font': {'color': '#212529', 'size': 40}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#343a40'},
            'bar': {'color': "#343a40"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#dee2e6",
            'steps': [
                {'range': [0, 25], 'color': '#ffccd5'},
                {'range': [25, 40], 'color': '#fff3cd'},
                {'range': [40, 50], 'color': '#d1e7dd'}
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
    # Load Data
    all_data = load_all_data()
    
    if not all_data:
        st.error("❌ No grade files found. Please check SUBJECTS_CONFIG.")
        return

    # Initialize Session
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_key = ""

    # --- LOGIN SCREEN ---
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
                # Check if key exists in ANY subject file
                found_name = None
                for subj, df in all_data.items():
                    record = df[df['رمز_الدخول'] == key]
                    if not record.empty:
                        found_name = record.iloc[0]['اسم الطالب']
                        break
                
                if found_name:
                    st.session_state.logged_in = True
                    st.session_state.student_key = key
                    st.session_state.student_name = found_name
                    st.rerun()
                else:
                    st.error("❌ الرمز غير صحيح")

    # --- DASHBOARD SCREEN ---
    else:
        # 1. Subject Selector
        st.markdown(f"""
        <div class="pro-card" style="display: flex; justify-content: space-between; align-items: center; padding: 15px;">
            <div style="text-align: right;">
                <h3 style="margin:0;">👤 {st.session_state.student_name}</h3>
            </div>
            <div>
               <span style="font-weight:bold; color:#0d6efd;">اختر المادة أدناه 👇</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected_subject = st.selectbox("اختر المادة لعرض الدرجات:", list(all_data.keys()))

        # 2. Load Data for Selected Subject
        df = all_data[selected_subject]
        key = st.session_state.student_key
        record = df[df['رمز_الدخول'] == key]

        if record.empty:
            st.warning(f"⚠️ عذراً، لم يتم العثور على درجة للطالب في مادة: **{selected_subject}**")
            if st.button("تسجيل خروج"):
                st.session_state.logged_in = False
                st.rerun()
            return

        row = record.iloc[0]
        total = float(row['السعي النهائي (50)'])

        # 3. Badge Logic
        if total >= 40: badge, b_bg, b_txt = "🌟 ممتاز", "#d1e7dd", "#0f5132"
        elif total >= 30: badge, b_bg, b_txt = "✅ جيد جداً", "#cfe2ff", "#084298"
        elif total >= 25: badge, b_bg, b_txt = "⚖️ متوسط", "#fff3cd", "#664d03"
        else: badge, b_bg, b_txt = "⚠️ تنبيه", "#f8d7da", "#842029"

        # 4. Display Header
        st.markdown(f"""
        <div class="pro-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div><h3 style="margin:0;">{selected_subject}</h3></div>
            <div style="background-color:{b_bg}; color:{b_txt}; padding:5px 15px; border-radius:20px; font-weight:800; border:1px solid {b_txt};">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

        # 5. Visuals
        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.markdown('<div class="pro-card" style="height: 100%; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
            st.plotly_chart(create_gauge(total), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_right:
            st.markdown('<div class="pro-card" style="height: 100%;">', unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom:20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;'>📊 التفاصيل</h4>", unsafe_allow_html=True)
            
            # Safe Get for columns (in case other subjects have different columns)
            mid = row.get('الامتحان النصفي', 0)
            formative = row.get('السعي التكويني (40)', 0)
            rep = row.get('التقرير (10)', 0)
            disc = row.get('المناقشة (10)', 0)

            st.markdown(progress_html("الامتحان النصفي", mid, 15, "#fd7e14"), unsafe_allow_html=True)
            st.markdown(progress_html("السعي التكويني", formative, 40, "#0d6efd"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ التقرير", rep, 10, "#6f42c1"), unsafe_allow_html=True)
            st.markdown(progress_html("↳ المناقشة", disc, 10, "#198754"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # 6. Stats & Calculator
        total_col = 'السعي النهائي (50)'
        avg = df[total_col].mean()
        high = df[total_col].max()
        df_sort = df.sort_values(by=total_col, ascending=False).reset_index()
        # Find rank safely
        try:
            rank = df_sort[df_sort['رمز_الدخول'] == key].index[0] + 1
        except:
            rank = "-"

        s1, s2, s3 = st.columns(3)
        s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='margin-bottom:15px;'>🧮 حاسبة الامتحان النهائي (من 50)</h4>", unsafe_allow_html=True)
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        rows = ""
        for lbl, tgt in targets.items():
            req = tgt - total
            if req <= 0:
                rows += f"<tr><td>{lbl}</td><td style='background-color:#d1e7dd; color:#0f5132; font-weight:bold; border-radius:5px;'>✅ ناجح مسبقاً</td></tr>"
            elif req > 50:
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

