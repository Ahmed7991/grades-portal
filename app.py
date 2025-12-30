import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="نظام نتائج الطلاب", page_icon="🎓")

# Custom CSS for Full Arabic (RTL) Support
st.markdown("""
<style>
    /* Force the main container to be Right-to-Left */
    .main {
        direction: rtl;
        text-align: right;
    }
    .stTextInput > label {
        direction: rtl; 
        text-align: right;
        font-size: 1.2rem;
        font-weight: bold;
        display: block;
        width: 100%;
    }
    .stTextInput input {
        direction: ltr; /* Keep numbers LTR for easier typing */
        text-align: center;
    }
    .stButton button {
        width: 100%;
        background-color: #4CAF50; /* Green color */
        color: white;
        font-size: 18px;
    }
    .student-card {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: right;
        direction: rtl;
    }
    .grade-box {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .grade-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }
    .grade-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    h1, h2, h3, p, div {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title aligned to the right
    st.markdown("<h1 style='text-align: right; color: #1E88E5;'>🎓 بوابة نتائج الطلاب</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right;'>الرجاء إدخال رمز الدخول الخاص بك لعرض النتيجة التفصيلية.</p>", unsafe_allow_html=True)
    
    # 1. Load the data
    try:
        # Read CSV. Make sure encoding handles Arabic if needed, but utf-8 is standard.
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
    except FileNotFoundError:
        st.error("عذراً، لم يتم العثور على ملف الدرجات (grades.csv).")
        return

    # 2. Input Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        key_input = st.text_input("رمز الدخول", type="password", help="أدخل الرمز المكون من 5 أرقام")
        submit_btn = st.button("عرض النتيجة")

    # 3. Validation Logic
    if submit_btn:
        if key_input:
            # Filter logic
            student_record = df[df['رمز_الدخول'] == key_input]

            if not student_record.empty:
                row = student_record.iloc[0]
                
                # --- SUCCESS DISPLAY ---
                st.markdown(f"""
                <div class="student-card">
                    <h2 style="color: #2E7D32;">✅ أهلاً بك، {row['اسم الطالب']}</h2>
                    <hr>
                </div>
                """, unsafe_allow_html=True)

                # Create columns for grades (Right to Left logic usually requires reversing lists in some frameworks, 
                # but in Streamlit we just place them 3-2-1 visually or rely on the RTL CSS)
                
                # Row 1: The Main Result (Total)
                st.markdown("<h4 style='text-align: right; margin-top: 20px;'>النتيجة النهائية</h4>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns([1,1,1])
                
                with m3: # Rightmost column in LTR grid, becomes first in RTL visual check
                    st.markdown(f"""
                    <div class="grade-box" style="border: 2px solid #1E88E5;">
                        <div class="grade-label">السعي النهائي (50)</div>
                        <div class="grade-value">{row['السعي النهائي (50)']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with m2:
                    st.markdown(f"""
                    <div class="grade-box">
                        <div class="grade-label">الامتحان النصفي</div>
                        <div class="grade-value">{row['الامتحان النصفي']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with m1:
                    st.markdown(f"""
                    <div class="grade-box">
                        <div class="grade-label">السعي التكويني (40)</div>
                        <div class="grade-value">{row['السعي التكويني (40)']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Row 2: Details
                st.markdown("<h4 style='text-align: right; margin-top: 20px;'>تفاصيل السعي التكويني</h4>", unsafe_allow_html=True)
                d1, d2, d3, d4 = st.columns(4)
                
                # Displaying Report and Discussion
                with d4:
                    st.markdown(f"""
                    <div class="grade-box">
                        <div class="grade-label">المناقشة (10)</div>
                        <div class="grade-value">{row['المناقشة (10)']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with d3:
                    st.markdown(f"""
                    <div class="grade-box">
                        <div class="grade-label">التقرير (10)</div>
                        <div class="grade-value">{row['التقرير (10)']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Placeholder for other components if you add them later
                with d2:
                    st.write("") 
                with d1:
                    st.write("")

            else:
                st.error("❌ رمز الدخول غير صحيح. يرجى التأكد والمحاولة مرة أخرى.")
        else:
            st.warning("يرجى إدخال الرمز أولاً.")

if __name__ == "__main__":
    main()