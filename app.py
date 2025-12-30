import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="نظام نتائج الطلاب", page_icon="🎓", layout="centered")

# --- CUSTOM CSS (Modern UI) ---
st.markdown("""
<style>
    /* Global Font & Direction */
    .main { direction: rtl; text-align: right; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Login Card Styling */
    .login-container {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 50px;
    }
    
    /* Stats Cards */
    .stat-card {
        background-color: white; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .stat-card:hover { transform: translateY(-5px); }
    .stat-value { font-size: 2rem; font-weight: bold; color: #1E88E5; }
    .stat-label { font-size: 0.9rem; color: #888; margin-top: 5px;}

    /* Inputs & Buttons */
    .stTextInput > label { direction: rtl; text-align: right; width: 100%; }
    .stTextInput input { text-align: center; border-radius: 10px; }
    .stButton button { 
        width: 100%; 
        background-color: #1E88E5; 
        color: white; 
        font-size: 16px; 
        border-radius: 10px; 
        padding: 10px;
        border: none;
    }
    .stButton button:hover { background-color: #1565C0; }

    /* Progress Bar Labels */
    .progress-label { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px; color: #555; }
    
    /* Calculator Table */
    .calc-table { width: 100%; border-collapse: separate; border-spacing: 0; direction: rtl; border: 1px solid #eee; border-radius: 10px; overflow: hidden; }
    .calc-table td, .calc-table th { padding: 12px; text-align: center; border-bottom: 1px solid #eee; }
    .calc-table th { background-color: #f8f9fa; color: #444; font-weight: bold; }
    .calc-row-pass { background-color: #e8f5e9; color: #2e7d32; font-weight: bold; }
    .calc-row-hard { background-color: #ffebee; color: #c62828; }
</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 18, 'color': '#555'}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#ffebee'},
                {'range': [25, 40], 'color': '#fff8e1'},
                {'range': [40, 50], 'color': '#e8f5e9'}
            ],
        }
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20))
    return fig

# Helper to make HTML Progress Bars
def progress_bar_html(label, value, max_val, color="#1E88E5"):
    percentage = (value / max_val) * 100
    return f"""
    <div style="margin-bottom: 12px;">
        <div class="progress-label">
            <span>{label}</span>
            <span style="font-weight:bold;">{value}/{max_val}</span>
        </div>
        <div style="background-color: #eef2f6; border-radius: 8px; height: 10px; width: 100%; overflow: hidden;">
            <div style="background-color: {color}; width: {percentage}%; height: 100%; border-radius: 8px;"></div>
        </div>
    </div>
    """

def main():
    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
    except FileNotFoundError:
        st.error("عذراً، لم يتم العثور على ملف الدرجات.")
        return

    # --- Login Section ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Centered Login Card
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="login-container">
                <h1 style="margin:0;">🔐</h1>
                <h3 style="color:#333; margin-top:10px;">بوابة النتائج</h3>
                <p style="color:#777; font-size:0.9rem;">أدخل الرمز السري لعرض نتيجتك</p>
            </div>
            """, unsafe_allow_html=True)
            
            key_input = st.text_input("رمز الدخول", type="password", label_visibility="collapsed", placeholder="أدخل الرمز هنا")
            
            if st.button("دخول"):
                if key_input:
                    student_record = df[df['رمز_الدخول'] == key_input]
                    if not student_record.empty:
                        st.session_state.logged_in = True
                        st.session_state.student = student_record.iloc[0]
                        st.rerun()
                    else:
                        st.error("❌ رمز غير صحيح")
                else:
                    st.warning("يرجى إدخال الرمز")

    # --- Dashboard Section ---
    else:
        row = st.session_state.student
        total_score = row['السعي النهائي (50)']
        
        # Determine Status Badge
        if total_score >= 40:
            badge = "🌟 مميز"
            badge_color = "#e8f5e9" # Light Green
            text_color = "#2e7d32"
        elif total_score >= 25:
            badge = "✅ جيد"
            badge_color = "#fff8e1" # Light Yellow
            text_color = "#f57f17"
        else:
            badge = "⚠️ يحتاج متابعة"
            badge_color = "#ffebee" # Light Red
            text_color = "#c62828"

        # 1. Header with Badge
        st.markdown(f"""
        <div style="background-color:white; padding:20px; border-radius:15px; margin-bottom:20px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee;">
            <h2 style="color:#333; margin:0;">{row['اسم الطالب']}</h2>
            <div style="margin-top:10px;">
                <span style="background-color:{badge_color}; color:{text_color}; padding:5px 15px; border-radius:20px; font-weight:bold; font-size:0.9rem;">{badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Main Visuals
        col_gauge, col_details = st.columns([1, 1])
        
        with col_gauge:
            st.plotly_chart(create_gauge(total_score), use_container_width=True)

        with col_details:
            st.markdown("#### 📊 تفاصيل الدرجات")
            st.markdown("<div style='background-color:white; padding:15px; border-radius:15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee;'>", unsafe_allow_html=True)
            
            # Progress Bars
            st.markdown(progress_bar_html("الامتحان النصفي", row['الامتحان النصفي'], 15, "#1E88E5"), unsafe_allow_html=True)
            st.markdown(progress_bar_html("السعي التكويني", row['السعي التكويني (40)'], 40, "#43A047"), unsafe_allow_html=True)
            st.markdown(progress_bar_html("↳ التقرير", row['التقرير (10)'], 10, "#FB8C00"), unsafe_allow_html=True)
            st.markdown(progress_bar_html("↳ المناقشة", row['المناقشة (10)'], 10, "#FB8C00"), unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Class Stats
        st.markdown("### 📈 مستواك مقارنة بالدفعة")
        total_grade_col = 'السعي النهائي (50)'
        class_avg = df[total_grade_col].mean()
        class_max = df[total_grade_col].max()
        df_sorted = df.sort_values(by=total_grade_col, ascending=False).reset_index()
        rank = df_sorted[df_sorted['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1

        m1, m2, m3 = st.columns(3)
        with m3:
            st.markdown(f"""<div class="stat-card"><div class="stat-value">#{rank}</div><div class="stat-label">الترتيب</div></div>""", unsafe_allow_html=True)
        with m2:
             st.markdown(f"""<div class="stat-card"><div class="stat-value">{class_avg:.1f}</div><div class="stat-label">المعدل العام</div></div>""", unsafe_allow_html=True)
        with m1:
            st.markdown(f"""<div class="stat-card"><div class="stat-value">{class_max}</div><div class="stat-label">أعلى درجة</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Calculator
        st.markdown("### 🧮 ماذا تحتاج في النهائي؟")
        
        targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
        html_rows = ""
        
        for label, target in targets.items():
            required = target - total_score
            if required <= 0:
                status = "✅ ناجح"
                color_class = "calc-row-pass"
            elif required > 50:
                status = "❌ غير ممكن"
                color_class = "calc-row-hard"
            else:
                status = f"تحتاج <b>{required}</b>"
                color_class = ""
            html_rows += f"<tr class='{color_class}'><td>{label}</td><td>{status}</td></tr>"

        st.markdown(f"""
        <table class="calc-table">
            <tr><th>التقدير المطلوب</th><th>المطلوب في النهائي (من 50)</th></tr>
            {html_rows}
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
