import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="بوابة الطالب", page_icon="🎓", layout="centered")

# --- THEME & CSS ---
PRIMARY_COLOR = "#2563eb"
TEXT_COLOR = "#1e293b"
FONT_URL = "https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap"

def load_css():
    st.markdown(f"""
    <style>
        @import url('{FONT_URL}');

        html, body, [class*="css"] {{
            font-family: 'Cairo', sans-serif;
            color: {TEXT_COLOR};
        }}

        /* Background */
        .stApp {{
            background-color: #f8fafc;
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 24px 24px;
        }}

        /* RTL Layout */
        .main {{ direction: rtl; }}

        /* Clean Card (Custom HTML version for Header) */
        .clean-card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid #e2e8f0;
        }}

        /* Overwriting Streamlit's Bordered Container to look like a Card */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
            padding: 20px;
            margin-bottom: 20px;
        }}

        h1, h2, h3, h4 {{ color: #0f172a; margin: 0; }}
        p {{ color: #64748b; }}

        /* Stats Box */
        .stat-box {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            border: 1px solid #bfdbfe;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.05);
            margin-bottom: 10px;
            min-height: 100px;
            display: flex; flex-direction: column; justify-content: center;
        }}
        .stat-val {{ font-size: 1.8rem; font-weight: 700; color: {PRIMARY_COLOR}; }}
        .stat-lbl {{ font-size: 0.85rem; color: #475569; font-weight: 600; margin-top: 4px; }}

        /* Inputs & Buttons */
        .stTextInput input {{
            text-align: center; border-radius: 12px; border: 2px solid #e2e8f0; padding: 10px; font-size: 1.1rem;
        }}
        .stButton button {{
            background-color: {PRIMARY_COLOR}; color: white; border-radius: 12px; padding: 10px; border: none; font-weight: 600;
        }}

        /* Progress Bars */
        .prog-container {{ margin-bottom: 12px; }}
        .prog-header {{
            display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 6px; font-weight: 600; color: #334155;
        }}
        .prog-bg {{
            background-color: #f1f5f9; border-radius: 99px; height: 8px; width: 100%; overflow: hidden;
        }}
        .prog-fill {{ height: 100%; border-radius: 99px; }}

        /* Calculator Table */
        .calc-table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 10px; font-size: 0.9rem; }}
        .calc-table th {{ background: #f8fafc; color: #475569; padding: 10px; text-align: right; border-bottom: 2px solid #e2e8f0; }}
        .calc-table td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; color: #334155; }}
        .row-pass {{ background: #dcfce7; color: #166534; font-weight: 700; }}
        .row-fail {{ background: #fee2e2; color: #991b1b; }}
    </style>
    """, unsafe_allow_html=True)

def create_gauge(score, max_score=50):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "الدرجة النهائية", 'font': {'size': 18, 'color': '#475569', 'family': 'Cairo'}},
        gauge = {
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': '#9ca3af'},
            'bar': {'color': "#2563eb", 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 25], 'color': '#fee2e2'},
                {'range': [25, 40], 'color': '#fef3c7'},
                {'range': [40, 50], 'color': '#dcfce7'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', font={'family': 'Cairo'})
    return fig

def create_distribution_chart(df, student_score, total_col):
    fig = px.histogram(
        df, x=total_col, nbins=15,
        title="توزيع درجات الصف",
        color_discrete_sequence=['#93c5fd'],
        opacity=0.7
    )
    fig.add_vline(x=student_score, line_width=3, line_dash="dash", line_color="#ef4444")
    fig.add_annotation(
        x=student_score, y=0, text="درجتك",
        showarrow=True, arrowhead=2, ax=0, ay=-40,
        font=dict(color="#ef4444", size=14, family="Cairo", weight="bold")
    )
    fig.update_layout(
        xaxis_title="الدرجة", yaxis_title="عدد الطلاب",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        font={'family': 'Cairo', 'color': '#475569'}, bargap=0.1
    )
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f1f5f9')
    return fig

def progress_html(label, value, max_val, color):
    try: val_float = float(value)
    except: val_float = 0.0
    percent = min((val_float / max_val) * 100, 100)
    return f"""
    <div class="prog-container">
        <div class="prog-header">
            <span>{label}</span>
            <span style="color: {color}">{val_float} / {max_val}</span>
        </div>
        <div class="prog-bg">
            <div class="prog-fill" style="width: {percent}%; background-color: {color};"></div>
        </div>
    </div>
    """

def main():
    load_css()

    try:
        df = pd.read_csv("grades.csv", dtype={'رمز_الدخول': str})
        total_col = 'السعي النهائي (50)'
        df[total_col] = pd.to_numeric(df[total_col], errors='coerce').fillna(0)
    except FileNotFoundError:
        st.error("❌ قاعدة البيانات غير موجودة")
        return

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("""
            <div class="clean-card" style="text-align: center; padding: 40px 20px;">
                <div style="font-size: 4rem; margin-bottom: 15px;">🎓</div>
                <h2 style="margin-bottom: 10px;">بوابة النتائج</h2>
                <p style="margin-bottom: 20px;">أدخل الرمز السري الخاص بك</p>
            </div>
            """, unsafe_allow_html=True)
            key = st.text_input("Key", type="password", label_visibility="collapsed", placeholder="🔒 رمز الدخول")
            if st.button("تسجيل الدخول"):
                if key:
                    record = df[df['رمز_الدخول'] == key]
                    if not record.empty:
                        st.session_state.logged_in = True
                        st.session_state.student = record.iloc[0]
                        st.rerun()
                    else: st.error("❌ الرمز غير صحيح")
                else: st.warning("يرجى إدخال الرمز")

    else:
        row = st.session_state.student
        total = float(row[total_col])

        # Badge
        if total >= 40: badge, b_col, t_col = "🌟 ممتاز", "#dcfce7", "#166534"
        elif total >= 30: badge, b_col, t_col = "✅ جيد جداً", "#e0f2fe", "#0369a1"
        elif total >= 25: badge, b_col, t_col = "⚖️ متوسط", "#fef9c3", "#854d0e"
        else: badge, b_col, t_col = "⚠️ يحتاج متابعة", "#fee2e2", "#991b1b"

        # 1. Header (Custom HTML)
        st.markdown(f"""
        <div class="clean-card" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="font-size: 1.8rem; font-weight: 700; color: #0f172a;">{row['اسم الطالب']}</h2>
                <p style="margin-top: 5px;">📍 لوحة النتائج الشاملة</p>
            </div>
            <div style="background-color:{b_col}; color:{t_col}; padding: 8px 20px; border-radius: 99px; font-weight:bold; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Main Grid
        c_left, c_right = st.columns([1, 1.2])

        with c_left:
            with st.container(border=True):
                st.plotly_chart(create_gauge(total), use_container_width=True)

        with c_right:
            with st.container(border=True):
                st.markdown("<h3 style='margin-bottom:20px; font-size:1.2rem;'>📊 تفاصيل الدرجات</h3>", unsafe_allow_html=True)
                st.markdown(progress_html("📝 الامتحان النصفي", row['الامتحان النصفي'], 15, "#f97316"), unsafe_allow_html=True)
                st.markdown(progress_html("🏗️ السعي التكويني", row['السعي التكويني (40)'], 40, "#3b82f6"), unsafe_allow_html=True)
                st.markdown(progress_html("📄 التقرير", row['التقرير (10)'], 10, "#8b5cf6"), unsafe_allow_html=True)
                st.markdown(progress_html("🗣️ المناقشة", row['المناقشة (10)'], 10, "#10b981"), unsafe_allow_html=True)

        # 3. Stats Row
        avg = df[total_col].mean()
        high = df[total_col].max()
        df_sort = df.sort_values(by=total_col, ascending=False).reset_index()
        rank = df_sort[df_sort['رمز_الدخول'] == row['رمز_الدخول']].index[0] + 1

        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f'<div class="stat-box"><div class="stat-val">#{rank}</div><div class="stat-lbl">الترتيب</div></div>', unsafe_allow_html=True)
        with s2: st.markdown(f'<div class="stat-box"><div class="stat-val">{avg:.1f}</div><div class="stat-lbl">المعدل</div></div>', unsafe_allow_html=True)
        with s3: st.markdown(f'<div class="stat-box"><div class="stat-val">{high}</div><div class="stat-lbl">الأعلى</div></div>', unsafe_allow_html=True)

        # 4. Distribution & Calculator
        st.markdown("<br>", unsafe_allow_html=True)
        c_calc, c_dist = st.columns([1, 1])

        with c_dist:
            with st.container(border=True):
                st.markdown("<h3 style='margin-bottom:15px; font-size:1.1rem;'>📈 موقعك في الدفعة</h3>", unsafe_allow_html=True)
                st.plotly_chart(create_distribution_chart(df, total, total_col), use_container_width=True)

        with c_calc:
            with st.container(border=True):
                st.markdown("<h3 style='margin-bottom:10px; font-size:1.1rem;'>🧮 حاسبة الفاينل</h3>", unsafe_allow_html=True)
                st.caption("الدرجة المطلوبة في النهائي (من 50):")

                targets = {"مقبول (50)": 50, "متوسط (60)": 60, "جيد (70)": 70, "جيد جداً (80)": 80, "امتياز (90)": 90}
                rows = ""
                for lbl, tgt in targets.items():
                    req = tgt - total
                    if req <= 0: rows += f"<tr class='row-pass'><td>{lbl}</td><td>✅ ناجح مسبقاً</td></tr>"
                    elif req > 50: rows += f"<tr class='row-fail'><td>{lbl}</td><td>❌ غير ممكن ({int(req)})</td></tr>"
                    else: rows += f"<tr><td>{lbl}</td><td>تحتاج <b>{int(req)}</b> / 50</td></tr>"

                st.markdown(f"<table class='calc-table'><thead><tr><th>التقدير</th><th>المطلوب</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

        if st.button("تسجيل الخروج"):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
