import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION ---
# FIXED: Use ONLY the ID, not the full URL
SHEET_ID = "1UhMsdmZeFYQFHIYdPGHNPlos_rC0gJPmpedOu8jyfbU"

SUBJECTS_CONFIG = {
    "تحليل وتصميم الخوارزميات": "analysis_of_algorithms",
    "معمارية الحاسوب": "computer_architecture",
    "برمجة الالعاب": "game_programming"
}

# Page Setup
st.set_page_config(page_title="Student Portal", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (High Contrast) ---
st.markdown("""
<style>
    /* Same professional CSS as before */
    [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
    h1, h2, h3, h4, p, span, div, label { color: #1e293b !important; font-family: 'Segoe UI', Tahoma, sans-serif; }
    .main { direction: rtl; text-align: right; }
    .pro-card { background-color: #ffffff !important; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 24px; margin-bottom: 20px; border: 1px solid #e2e8f0; }
    .stat-box { background-color: #f1f5f9 !important; border-radius: 8px; padding: 15px; text-align: center; border: 1px solid #cbd5e1; }
    .stat-val { font-size: 1.8rem; font-weight: 800; color: #2563eb !important; }
    .stat-lbl { font-size: 0.85rem; font-weight: 700; color: #64748b !important; }
    .stTextInput input { background-color: #ffffff !important; color: #0f172a !important; text-align: center; border: 2px solid #cbd5e1; border-radius: 8px; padding: 12px; font-size: 1.2rem; font-weight: bold; }
    .stButton button { width: 100%; background-color: #1e293b !important; color: #ffffff !important; font-size: 16px; border-radius: 8px; padding: 12px 0; border: none; font-weight: 600; }
    .stButton button:hover { background-color: #0f172a !important; }
    .bar-label { display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 6px; font-size: 0.9rem; }
    .bar-bg { background-color: #e2e8f0; border-radius: 6px; height: 10px; width: 100%; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 6px; }
    .calc-table { width: 100%; direction: rtl; border-collapse: collapse; margin-top: 10px; }
    .calc-table th { background-color: #f1f5f9; padding: 12px; border-bottom: 2px solid #e2e8f0; font-weight: 800; color: #475569 !important; text-align: right; }
    .calc-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-weight: 600; color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS FUNCTIONS ---

@st.cache_data(ttl=600) # Cache data for 10 minutes to be fast
def load_sheet(sheet_name):
    """Loads a specific sheet tab by name"""
    # Now this URL construction will work correctly because SHEET_ID is clean
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url, dtype={'رمز_الدخول': str})
        # Clean up column names (Google sometimes adds extras)
        df = df.dropna(how='all', axis=1) 
        
        # Ensure numeric for total grade
        if 'السعي النهائي (50)' in df.columns:
            df['السعي النهائي (50)'] = pd.to_numeric(df['السعي النهائي (50)'], errors='coerce').fillna(0)
            
        return df
    except Exception as e:
        # It's often good to print the error to console for debugging
        print(f"Error loading sheet {sheet_name}: {e}")
        return None

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 18, 'color': '#475569', 'family': 'Segoe UI'}},
        number = {'font': {'color': '#1e293b', 'size': 36}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#94a3b8'},
            'bar': {'color': "#3b82f6"}, 
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, 25], 'color': '#fee2e2'}, 
                {'range': [25, 40], 'color': '#fef3c7'}, 
                {'range': [40, 50], 'color': '#dcfce7'}  
            ],
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Segoe UI'})
    return fig

def progress_html(label, value, max_val, color):
    try: val = float(value)
    except: val = 0.0
    pct = (val / max_val) * 100
    return f"""<div style="margin-bottom: 12px;"><div class="bar-label"><span style="color:#475569;">{label}</span><span style="color:#1e293b;">{val:g} / {max_val}</span></div><div class="bar-bg"><div class="bar-fill" style="width: {pct}%; background-color: {color};"></div></div></div>"""

# --- MAIN APP ---

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.student_name = ""

    # 1. LOGIN
    if not st.session_state.logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""<div class="pro-card" style="text-align: center; border-top: 4px solid #1e293b;"><div style="font-size: 3rem; margin-bottom: 10px;">🔐</div><h2 style="margin-bottom: 5px;">بوابة الطالب</h2><p style="color:#64748b; font-size: 0.9rem;">أدخل رمز الدخول</p></div>""", unsafe_allow_html=True)
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="أدخل الرمز هنا")
            
            if st.button("دخول"):
                keys_df = load_sheet("students") # Load form Google Sheet
                if keys_df is not None:
                    # Check if key column exists to avoid errors
                    if 'رمز_الدخول' in keys_df.columns:
                        student = keys_df[keys_df['رمز_الدخول'] == key]
                        if not student.empty:
                            st.session_state.logged_in = True
                            st.session_state.student_name = student.iloc[0]['اسم الطالب']
                            st.rerun()
                        else:
                            st.error("❌ الرمز غير صحيح")
                    else:
                        st.error("❌ خطأ في قاعدة البيانات: عمود 'رمز_الدخول' مفقود")
                else:
                    st.error("❌ فشل الاتصال بقاعدة البيانات")

    # 2. DASHBOARD
    else:
        student_name = st.session_state.student_name
        st.markdown(f"""<div class="pro-card" style="display:flex; justify-content:space-between; align-items:center;"><div style="text-align:right;"><h2 style="font-size:1.4rem; margin:0;">{student_name}</h2><p style="margin:0; font-size:0.9rem;">لوحة النتائج</p></div><div style="background:#f1f5f9; padding:8px 12px; border-radius:8px;"><span style="font-size:1.5rem;">👤</span></div></div>""", unsafe_allow_html=True)

        selected_subject = st.selectbox("اختر المادة:", list(SUBJECTS_CONFIG.keys()))
        sheet_name = SUBJECTS_CONFIG[selected_subject]
        grades_df = load_sheet(sheet_name) # Load from Google Sheet

        if grades_df is None:
            # FIXED: Added the missing quote " at the start of the string
            st.warning("⚠️ جاري تحديث البيانات... يرجى المحاولة لاحقاً")
        else:
            record = grades_df[grades_df['اسم الطالب'].str.strip() == student_name.strip()]
            if record.empty:
                st.warning(f"⚠️ لم يتم العثور على درجة للطالب في مادة: {selected_subject}")
            else:
                row = record.iloc[0]
                total = float(row['السعي النهائي (50)'])
                if total >= 40: badge, bg, txt = "🌟 ممتاز", "#dcfce7", "#166534"
                elif total >= 30: badge, bg, txt = "✅ جيد جداً", "#dbeafe", "#1e40af"
                elif total >= 25: badge, bg, txt = "⚖️ متوسط", "#fef9c3", "#854d0e"
                else: badge, bg, txt = "⚠️ تنبيه", "#fee2e2", "#991b1b"

                st.markdown(f"""<div class="subject-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; margin-bottom: 15px;"><h3 style="margin:0;">{selected_subject}</h3><span style="background-color:{bg}; color:{txt}; padding:5px 12px; border-radius:20px; font-weight:bold; font-size:0.85rem;">{badge}</span></div>""", unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown('<div class="pro-card" style="height:100%; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
                    st.plotly_chart(create_gauge(total), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="pro-card" style="height:100%;">', unsafe_allow_html=True)
                    st.markdown("<h4 style='margin-bottom:15px;'>تفاصيل الدرجة</h4>", unsafe_allow_html=True)
                    mid = row.get('الامتحان النصفي', 0)
                    formative = row.get('السعي التكويني (40)', 0)
                    rep = row.get('التقرير (10)', 0)
                    disc = row.get('المناقشة (10)', 0)
                    st.markdown(progress_html("الامتحان النصفي", mid, 15, "#f59e0b"), unsafe_allow_html=True)
                    st.markdown(progress_html("السعي التكويني", formative, 40, "#3b82f6"), unsafe_allow_html=True)
                    st.markdown(progress_html("↳ التقرير", rep, 10, "#8b5cf6"), unsafe_allow_html=True)
                    st.markdown(progress_html("↳ المناقشة", disc, 10, "#10b981"), unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                total_col = 'السعي النهائي (50)'
                avg = grades_df[total_col].mean()
                high = grades_df[total_col].max()
                try: rank = grades_df.sort_values(by=total_col, ascending=False).reset_index()[grades_df.sort_values(by=total_col, ascending=False).reset_index()['اسم الطالب'].str.strip() == student_name.strip()].index[0] + 1
                except: rank = "-"

                s1, s2, s3 = st.columns(3)
                s3.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
                s2.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">معدل الدفعة</div></div>', unsafe_allow_html=True)
                s1.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">أعلى درجة</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="pro-card">', unsafe_allow_html=True)
                st.markdown("<h4 style='margin-bottom:10px;'>🧮 حاسبة الامتحان النهائي (من 50)</h4>", unsafe_allow_html=True)
                targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
                rows = ""
                for lbl, tgt in targets.items():
                    req = tgt - total
                    if req <= 0: rows += f"<tr><td>{lbl}</td><td><span style='background-color:#dcfce7; color:#166534; padding:4px 8px; border-radius:4px;'>✅ ناجح مسبقاً</span></td></tr>"
                    elif req > 50: rows += f"<tr><td>{lbl}</td><td><span style='background-color:#fee2e2; color:#991b1b; padding:4px 8px; border-radius:4px;'>❌ غير ممكن</span></td></tr>"
                    else: rows += f"<tr><td>{lbl}</td><td>تحتاج <b>{int(req)}</b></td></tr>"
                st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير المطلوب</th><th>المطلوب</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()

