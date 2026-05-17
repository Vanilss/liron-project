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
                "findings": "",
                "conclusions": "סוג הסקטור הוא הגורם המשפיע ביותר על הצמיחה, כשהטכנולוגיה והפיננסים מובילים."
            },
            "שאלת תת חקר 2": {
                "findings": "גרף הפיזור מציג פיזור רחב וקיצוני בחברות קטנות, לעומת יציבות יחסית בקרב חברות הענק, שווי השוק בגרף נמדד בטריליונים דולר, וקצב הצמיחה נמדד לי העמודה  renvenue growth in month. קו המגמה השטוח בגרף מוכיח באופן ויזואלי כי אין קשר ישיר או עקבי בין גודל החברה לקצב צמיחתה. הממצאים מראים שווי שוק גבוה אינו מבטיח צמיחה מהירה, וכי אין מתאם ליניארי חיובי חזק בין המשתנים ב-S&P 500. ",
                "conclusions": "אין קשר חיובי חזק בין גודל החברה לקצב צמיחתה ולכן שווי שוק לא בהכרח מנבא תשואה גבוהה."
            },
            "שאלת תת חקר 3": {
                "findings": "מבחינת פיזור הנתונים בגרף, כל נקודה על הגרף מתארת חברה שוק במדד מול הנתונים שמוצבים, ניתן לראות כי קיים קשר חיובי בין שווי השוק של הסקטור לבין קצב הצמיחה שלו, אך קשר זה אינו אחיד לכל אורך הציר. בסקטורים בעלי שווי שוק נמוך (החלק השמאלי של הגרף), קיימת תנודתיות גבוהה מאוד: חלקם מציגים את הצמיחה המהירה ביותר במדד , בעוד שאחרים מציגים צמיחה שלילית.",
                "conclusions": "אמנם הסקטורים בעלי שווי גבוה ביותר מציגים צמיחה חזקה ויציבה יותר בממוצע (כפי שמעיד קו המגמה העולה), אך שיאי הצמיחה נמצאים דווקא אצל סקטורים קטנים יותר. בשורה התחתונה: השוק הנוכחי מתגמל גודל ביציבות, אך פוטנציאל הצמיחה הקיצוני ביותר עדיין קיים עבור מניות יותר קטנות הגודל,הגודל מהווה יתרון, אך הקטנים מובילים בעלי יותר פונטציאל"
            },
            "שאלת תת חקר 4": {
                "findings": "ממצאי שאלת החקר מעלה כי השפעת גודל החברה על קצב הצמיחה אינה אחידה ומשתנה באופן גדול בין ענפי המשק השונים. במדגם נמצא כי בחלק מהסקטורים הגודל מהווה יתרון משמעותי המאפשר לחברות הגדולות להוביל את השוק עם קצבי צמיחה גבוהים יותר, בעוד שבסקטורים אחרים חברות קטנות יותר הן אלו שמציגות את הביצועים הטובים ביותר.. הגרף מציג ממוצע של הצמיחה בכל סקטור שבתוך זה זה מחולק לחברות הקטנות יותר באותו הסקטור ולחברות הגדולות לפי שווי שוק החברה, וגובה העמודה מציג את ממוצע הגדילה של כל עמודה למשל עבור עמודה כתומה זה יראה את ממוצע הצמיחה של כל החברות הגדולות באותו הסקטורציר הX מייצג את הסקטורים וציר הY לממוצע הצמיחה",
                "conclusions": "המסקנה הסופית לסיכום, ניתן לקבוע כי הגודל אינו מבטיח צמיחה באופן אוטומטי, אלא משמש כמנוע או כמשקולת בהתאם לדינמיקה הספציפית של הענף. בעוד שבתחומים מסוימים הגודל מתפקד כמכפיל כוח המאיץ את ההתרחבות, בענפים אחרים הוא עלול לסרבל את הפעילות ולהעניק יתרון תחרותי דווקא לחברות קטנות וגמישות המגיבות מהר יותר לשינויים. המדגם מוכיח כי השוק פועל לפי מערכת חוקים משתנה, שבה יתרון הגודל בא לידי ביטוי בעיקר בסביבות עסקיות המאפשרות ניצול יתרונות לגודל ושליטה רחבה בשוק."
            }
        }

        chart_files = ["chart1.png", "chart2.png", "chart3.png", "chart4.png"]
        all_tab_names = list(st.session_state.all_sheets.keys()) + ["מסקנות"]
        tabs = st.tabs(all_tab_names)

        for index, (sheet_name, df) in enumerate(st.session_state.all_sheets.items()):
            with tabs[index]:
                txt = manual_content.get(sheet_name,
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
            st.markdown('<div class="conclusion-box">', unsafe_allow_html=True)
            st.write("סיכום מסקנה שאלת חקר.")
            st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("S&P 500 Pro Board | 2026")