import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="نظام نتائج الطلاب", page_icon="🎓", layout="centered")

# Custom CSS for Full Arabic (RTL) Support & Card Styling
st.markdown("""
<style>
    .main { direction: rtl; text-align: right; }
    .stTextInput > label {
        direction: rtl; text-align: right; font-size: 1.2rem; font-weight: bold; display: block; width: 100%;
    }
    .stTextInput input { direction: ltr; text-align: center; }
    .stButton button { width: 100%; background-color: #1E88E5; color: white; font-size: 18px; border-radius: 8px; }
    
    /* Stats Cards */
    .stat-card {
        background-color: #f8f9fa; border-radius: 10px; padding: 15px; 
        text-align: center; border: 1px solid #e0e0e0; margin-bottom: 10px;
    }
    .stat-value { font-size: 1.8rem; font-weight: bold; color: #1E88E5; }
    .stat-label { font-size: 0.9rem; color: #666; }

    /* Calculator Table */
    .calc-table { width: 100%; border-collapse: collapse; direction: rtl; }
    .calc-table td, .calc-table th { border: 1px solid #ddd; padding: 8px; text-align: center; }
    .calc-table th { background-color: #1E88E5; color: white; }
    .calc-row-pass { background-color: #e8f5e9; } /* Green tint */
    .calc-row-hard { background-color: #ffebee; } /* Red tint */
</style>
""", unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    """Creates a speedometer chart using Plotly"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "السعي النهائي (50)", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': '#ffcdd2'},  # Red zone
                {'range': [25, 40], 'color': '#fff9c4'}, # Yellow zone
                {'range': [40, 50], 'color': '#c8e6c9'}  # Green zone
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    return fig

def main():
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🎓 بوابة نتائج الطلاب</h1>", unsafe_allow_html=True)
    
    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
    except FileNotFoundError:
        st.error("عذراً، لم يتم العثور على ملف الدرجات.")
        return

    # --- Login Section ---
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### تسجيل الدخول")
            key_input = st.text_input("رمز الدخول", type="password", help="أدخل الرمز المكون من 5 أرقام")
            if st.button("عرض النتيجة"):
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

    # --- Dashboard Section (After Login) ---
    else:
        row = st.session_state.student
        
        # 1. Header & Welcome
        st.markdown(f"""
        <div style="background-color:#e3f2fd; padding:15px; border-radius:10px; margin-bottom:20px; text-align:center;">
            <h2 style="color:#1565C0; margin:0;">أهلاً بك، {row['اسم الطالب']}</h2>
        </div>
        """, unsafe_allow_html=True)

        # 2. Top Row: Gauge & Detailed Grades
        col_gauge, col_details = st.columns([1, 1])
        
        with col_gauge:
            # FEATURE 1: Visual Gauge
            current_score = row['السعي النهائي (50)']
            st.plotly_chart(create_gauge(current_score), use_container_width=True)

        with col_details:
            st.markdown("#### 📄 تفاصيل الدرجات")
            st.markdown(f"""
            <ul style="list-style-type:none; padding:0; font-size:1.1rem; line-height:2.2;">
                <li><b>الامتحان النصفي:</b> {row['الامتحان النصفي']}</li>
                <li><b>السعي التكويني (40):</b> {row['السعي التكويني (40)']}</li>
                <li>&nbsp;&nbsp;↳ التقرير: {row['التقرير (10)']}</li>
                <li>&nbsp;&nbsp;↳ المناقشة: {row['المناقشة (10)']}</li>
            </ul>
            """, unsafe_allow_html=True)

        st.divider()

        # 3. FEATURE 2: "Where Do I Stand?" (Class Stats)
        st.markdown("### 📊 مستواك مقارنة بالدفعة")
        
        # Calculate Stats
        total_grade_col = 'السعي النهائي (50)'
        class_avg = df[total_grade_col].mean()
        class_max = df[total_grade_col].max()
        
        # Calculate Rank
        df_sorted = df.sort_values(by=total_grade_col, ascending=False).reset_index()
        rank = df_sorted[df_sorted['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1
        total_students = len(df)

        m1, m2, m3 = st.columns(3)
        with m3:
            st.markdown(f"""<div class="stat-card"><div class="stat-value">#{rank}</div><div class="stat-label">ترتيبك على الدفعة</div></div>""", unsafe_allow_html=True)
        with m2:
             st.markdown(f"""<div class="stat-card"><div class="stat-value">{class_avg:.1f}</div><div class="stat-label">معدل الدفعة</div></div>""", unsafe_allow_html=True)
        with m1:
            st.markdown(f"""<div class="stat-card"><div class="stat-value">{class_max}</div><div class="stat-label">أعلى درجة</div></div>""", unsafe_allow_html=True)

        st.divider()

        # 4. FEATURE 3: Final Exam Calculator
        st.markdown("### 🧮 حاسبة الامتحان النهائي")
        st.write("كم تحتاج في الامتحان النهائي (من 50) للوصول إلى تقدير معين؟")

        targets = {
            "مقبول (50)": 50,
            "متوسط (60)": 60,
            "جيد (70)": 70,
            "جيد جداً (80)": 80,
            "امتياز (90)": 90
        }

        html_rows = ""
        for label, target in targets.items():
            required = target - current_score
            
            if required <= 0:
                status = "🎉 ناجح مسبقاً"
                color_class = "calc-row-pass"
            elif required > 50:
                status = "❌ غير ممكن نظرياً"
                color_class = "calc-row-hard"
            else:
                status = f"تحتاج <b>{required}</b> / 50"
                color_class = ""
            
            html_rows += f"<tr class='{color_class}'><td>{label}</td><td>{status}</td></tr>"

        st.markdown(f"""
        <table class="calc-table">
            <tr><th>التقدير المطلوب (المجموع من 100)</th><th>الدرجة المطلوبة في النهائي</th></tr>
            {html_rows}
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("تسجيل خروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
