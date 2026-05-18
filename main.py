import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="S&P 500 Elite Analytics", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f8fafc;
    }
    .conclusion-box {
        background: rgba(56, 189, 248, 0.1);
        border-right: 4px solid #38bdf8;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;

        /* כאן אתה משנה! מ-1.25 למספר גבוה יותר כמו 1.5 או 1.8 */
        font-size: 1.5rem; 

        line-height: 1.6;
        color: #f8fafc;
    }

    h4 {
        /* גם כאן, אם הכותרת קטנה מדי, תעלה מ-1.6 ל-2.0 למשל */
        font-size: 2.0rem !important; 

        color: #38bdf8 !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(56, 189, 248, 0.2) !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

if "all_sheets" not in st.session_state:
    st.session_state.all_sheets = {}

st.sidebar.markdown("# 🔧 סרגל כלים")
page = st.sidebar.radio("ניווט:", ["🏠 דף הבית", "📊 S&P 500 - מרכז הניתוח", "⚙️ ניהול נתונים"])

if page == "🏠 דף הבית":
    st.markdown("<h1 style='text-align: center; font-size: 4.5rem;'>S&P 500 INSIGHTS</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.6rem; color: #94a3b8;'>מערכת חקר נתונים מתקדמת | 2026</p>",
        unsafe_allow_html=True)
    st.write("---")

    if st.session_state.all_sheets:
        st.markdown("### 💎 מדדי מפתח למדד")
        c1, c2, c3 = st.columns(3)
        c1.metric("שווי שוק ממוצע", "$11.6B", "+3.2%")
        c2.metric("כמות סקטורים", "11", "מלא")
        c3.metric("עלייה שנתית", "14.2%", "+1.5%")
        st.write("---")
    else:
        st.info("אנא העלה את קובץ הנתונים בלשונית 'ניהול נתונים'.")

    st.image("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=1200",
             use_container_width=True)

elif page == "⚙️ ניהול נתונים":
    st.title("📂 טעינת מסד נתונים")
    uploaded_file = st.file_uploader("העלה קובץ אקסל (XLSX)", type=["xlsx"])

    if uploaded_file is not None:
        try:
            all_sheets_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
            valid_sheets = {}
            for sheet_name, df in all_sheets_data.items():
                if not df.empty:
                    df.columns = [str(c).strip() for c in df.columns]
                    valid_sheets[sheet_name] = df

            if valid_sheets:
                st.session_state.all_sheets = valid_sheets
                st.success("🎯 מסד הנתונים נטען בהצלחה!")
                st.balloons()
        except Exception as e:
            st.error(f"שגיאה בטעינה: {str(e)}")

elif page == "📊 S&P 500 - מרכז הניתוח":
    if not st.session_state.all_sheets:
        st.warning("אין נתונים. יש להעלות קובץ בניהול נתונים.")
    else:
        st.markdown("## 📈 ניתוח אוטומטי לפי תתי-שאלות")


        manual_content = {
            "שאלת תת חקר 1": {
                "findings": "בגרף רואים שסקטורי הפיננסים והטכנולוגיה מובילים עם צמיחה של כ־12%, בעוד שסקטור חומרי הגלם נמצא בירידה. רוב הסקטורים מציגים צמיחה חיובית של כ־4%–8%, מה שמראה על מגמת צמיחה כללית בשוק. הנתונים מראים שסוג הסקטור משפיע על פוטנציאל הצמיחה של החברה.",
                "conclusions": "סוג הסקטור הוא גורם מרכזי שמשפיע על רמת הצמיחה, כאשר טכנולוגיה ופיננסים מובילים את השוק."
            },
            "שאלת תת חקר 2": {
                "findings": "הגרף פיזור מציג פיזור גדול יותר בחברות קטנות לעומת יציבות יחסית בחברות גדולות. שווי השוק נמדד בטריליוני דולרים, וקצב הצמיחה לפי Revenue Growth. קו המגמה השטוח ומקדם פירסון 0.1529 מראים שאין קשר חזק בין גודל החברה לקצב הצמיחה, ולכן שווי שוק גבוה לא מבטיח צמיחה מהירה.",
                "conclusions": "אין קשר חזק בין גודל החברה לקצב הצמיחה, ולכן שווי שוק גבוה לא מנבא בהכרח צמיחה גבוהה.",
            },
            "שאלת תת חקר 3": {
                "findings": "בגרף פיזור כל נקודה מייצגת חברה לפי שווי השוק וקצב הצמיחה שלה. ניתן לראות קשר חיובי חלש בין שווי השוק לצמיחה, אבל הוא לא עקבי. בחברות עם שווי שוק נמוך יש תנודתיות גבוהה חלקן צומחות מהר מאוד וחלקן שליליות.",
                "conclusions": "סקטורים גדולים יותר מציגים בממוצע צמיחה יציבה וחזקה יותר, אך שיאי הצמיחה נמצאים גם בסקטורים קטנים בין אם זה חיובי או שלילי לפי דילמן החדשן. לכן גודל הסקטור משפיע על יציבות יותר מאשר על פוטנציאל הצמיחה.",
            },
            "שאלת תת חקר 4": {
                "findings": "בגרף העמודות הנתונים מראים שגודל החברה משפיע בצורה שונה בכל סקטור. יש סקטורים שבהם חברות גדולות צומחות יותר, ויש סקטורים שבהם דווקא חברות קטנות צומחות יותר. בגרף רואים את ממוצע הצמיחה של חברות גדולות וקטנות בכל סקטור.  ציר ה־X מראה את הסקטורים, וציר ה־Y מראה את ממוצע הצמיחה.",
                "conclusions": "השפעת גודל החברה משתנה בין סקטורים, לעיתים חברות גדולות מובילות בצמיחה באותו סקטור שזה מה שמוסבר , ולעיתים דווקא קטנות, ולכן אין קשר מדוייק לגודל בתוך כל סקטור.",
            }
        }

        chart_files = ["chart1.png", "chart2.png", "chart3.png", "chart4.png"]
        all_tab_names = list(st.session_state.all_sheets.keys()) + ["מסקנות"]
        tabs = st.tabs(all_tab_names)

        # ניקוי רווחים מיותרים משמות הגיליונות למניעת אי-התאמות
        clean_manual_content = {k.strip(): v for k, v in manual_content.items()}

        for index, (sheet_name, df) in enumerate(st.session_state.all_sheets.items()):
            with tabs[index]:
                txt = clean_manual_content.get(sheet_name.strip(),
                                         {"findings": "ממצאים טרם הוזנו", "conclusions": "מסקנות טרם הוזנו"})

                if index == 0:
                    st.markdown(f"### Analysis: {sheet_name}")
                    st.markdown("<p style='color: #94a3b8; margin-top: -15px;'>חלוקה לפי exchange</p>",
                                unsafe_allow_html=True)

                    x_col = df.columns[0]
                    num_cols = df.select_dtypes(include=['number']).columns.tolist()
                    y_col = num_cols[-1] if num_cols else df.columns[-1]

                    df_plot = df[df[x_col] != "Exchange"]
                    color_col = df_plot.columns[1] if len(df_plot.columns) > 1 else df_plot.columns[0]

                    fig = px.bar(df_plot, x=x_col, y=y_col, color=color_col, template="plotly_dark")
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis_title="",
                        yaxis_title="",
                        legend_title_text="Symbol"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.markdown(f"### 📄 נושא: {sheet_name}")

                    st.markdown("#### 📊 גרף ניתוח (מתוך אקסל)")

                    image_index = index - 1
                    if image_index < len(chart_files):
                        img_path = chart_files[image_index]
                        if os.path.exists(img_path):
                            st.image(img_path, use_container_width=True, caption=f"גרף עבור {sheet_name}")
                        else:
                            st.error(f"הקובץ {img_path} לא נמצא.")
                    else:
                        st.info("לא הוגדרה תמונה.")

                    st.markdown("#### 🔍 ממצאים")
                    st.markdown(
                        f'<div class="conclusion-box"><ul><li>{txt["findings"]}</li></ul></div>',
                        unsafe_allow_html=True)

                    st.markdown("#### 💡 מסקנות")
                    st.markdown(
                        f'<div class="conclusion-box"><ul><li>{txt["conclusions"]}</li></ul></div>',
                        unsafe_allow_html=True)

                st.markdown("#### 📋 טבלת נתונים מלאה")
                st.dataframe(df, use_container_width=True)

        with tabs[-1]:
            st.markdown("## 🎯 סיכום ומסקנות סופיות של המחקר")
            
            st.markdown("#### ❓ שאלת החקר")
            st.markdown(
                '<div class="conclusion-box"><ul><li>השאלה: מהו הקשר בין הסקטור לבין קצב הצמיחה, והאם סקטורים עם שווי שוק גבוה יותר הם גם אלו שצומחים מהר יותר?</li></ul></div>',
                unsafe_allow_html=True)
                
            st.markdown("#### 🔍 מה השאלה בודקת")
            st.markdown(
                '<div class="conclusion-box"><ul><li>מחקר זה בוחן את היחס בין שני משתנים מרכזיים, סקטור הפעילות לבין קצב הצמיחה שלה בפועל. השאלה המרכזית הנבחנת היא האם קיימת חוקיות בין סוג הסקטור לבין מהירות הצמיחה, וספציפית האם סקטורים המאופיינים בשווי שוק גבוה יותר הם אלו המציגים את קצבי הצמיחה המהירים ביותר במסד הנתונים. המחקר ינתח את הנתונים באופן מעשי כדי לקבוע האם שווי שוק גבוה מהווה מדד לצמיחה מואצת, או שקצב הצמיחה מוכתב בעיקר על ידי שיוך הסקטור ללא תלות בשווי השוק.</li></ul></div>',
                unsafe_allow_html=True)
                
            st.markdown("#### 💡 מסקנות משאלת החקר")
            st.markdown(
                '<div class="conclusion-box"><ul><li>על בסיס ממצאי המחקר, הבנו כי הקשר בין סקטור הפעילות לקצב הצמיחה הוא המשפיע ביותר בהחלטת ביצועי החברה, כאשר סקטור הוא הכי משפיע על הצמיחה. סקטורים טכנולוגים ופיננסים מובילים את השוק בגודל צמיחה של14%, מה שמעיד כי להשקיע יותר בחדשנות ויעילות הון מראה בסיס חזק להגדלת הכנסות, ללא קשר ישיר לגודל הפיזי של החברות הפועלות בהם.<br><br>בשאלת  החקר הקשר בין שווי השוק לקצב הצמיחה, הממצאים מראים כי שווי שוק גבוה אינו בהכרח אומר צמיחה מהירה יותר, ולמעשה אין קשר חזק בין שני המשתנים. עם זאת, הגודל קובע המון באופי הצמיחה: בעוד שחברות וסקטורים בעלי שווי שוק נמוך מציגים בלאגן ותנודתיות גבוהה, חברות הענק נשארות יחסית יציבות . השוק הנוכחי תורם גודל ביציבות ובעוצמה, אך פוטנציאל הצמיחה הקיצוני ביותר נשאר אצל  החברות קטנות וגמישות יותר,</li></ul></div>',
                unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("S&P 500 Pro Board | 2026")