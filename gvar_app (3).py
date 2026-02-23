import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="شرح نموذج GVAR",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cairo:wght@300;400;600;700;900&family=Tajawal:wght@300;400;500;700&display=swap');

/* Base RTL */
html, body, [class*="css"] {
    direction: rtl;
    font-family: 'Cairo', 'Tajawal', sans-serif;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 50%, #fef9f0 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a237e 0%, #283593 40%, #3949ab 100%);
    direction: rtl;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-family: 'Cairo', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 8px 14px;
    margin: 4px 0;
    cursor: pointer;
    transition: background 0.3s;
    display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.25);
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #1565c0 0%, #0288d1 50%, #0097a7 100%);
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(21,101,192,0.35);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    background: rgba(255,255,255,0.07);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Amiri', serif;
    font-size: 3.2em;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 12px 0;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.hero-subtitle {
    font-size: 1.4em;
    color: rgba(255,255,255,0.9);
    margin: 0 0 16px 0;
    font-weight: 300;
}
.hero-en {
    font-size: 1.1em;
    color: rgba(255,255,255,0.75);
    letter-spacing: 2px;
    font-weight: 400;
}
.dev-badge {
    display: inline-block;
    margin-top: 20px;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 30px;
    padding: 8px 24px;
    color: #ffffff;
    font-size: 0.95em;
    backdrop-filter: blur(10px);
}

/* Section Cards */
.section-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 32px 36px;
    margin: 20px 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border-top: 5px solid #1565c0;
    direction: rtl;
}
.section-card-green { border-top-color: #2e7d32; }
.section-card-orange { border-top-color: #e65100; }
.section-card-teal { border-top-color: #00695c; }
.section-card-purple { border-top-color: #6a1b9a; }
.section-card-pink { border-top-color: #ad1457; }
.section-card-indigo { border-top-color: #283593; }

/* Section Titles */
.sec-title {
    font-family: 'Cairo', sans-serif;
    font-size: 1.8em;
    font-weight: 700;
    color: #1a237e;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8eaf6;
}
.sec-subtitle {
    font-size: 1.1em;
    color: #546e7a;
    margin-bottom: 24px;
    line-height: 1.8;
}

/* Info Boxes */
.info-box {
    border-radius: 12px;
    padding: 20px 24px;
    margin: 16px 0;
    direction: rtl;
}
.info-blue   { background: #e3f2fd; border-right: 5px solid #1565c0; }
.info-green  { background: #e8f5e9; border-right: 5px solid #2e7d32; }
.info-orange { background: #fff3e0; border-right: 5px solid #e65100; }
.info-yellow { background: #fffde7; border-right: 5px solid #f9a825; }
.info-teal   { background: #e0f2f1; border-right: 5px solid #00695c; }
.info-pink   { background: #fce4ec; border-right: 5px solid #ad1457; }
.info-purple { background: #f3e5f5; border-right: 5px solid #6a1b9a; }

.info-box p, .info-box li, .info-box span {
    color: #263238;
    font-size: 1.0em;
    line-height: 2.0;
    margin: 0;
}
.info-box strong { color: #1a237e; }

/* Term badges */
.term-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1565c0, #0288d1);
    color: white;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.85em;
    font-weight: 600;
    margin: 4px 3px;
    vertical-align: middle;
}
.term-ar { background: linear-gradient(135deg, #2e7d32, #43a047); }
.term-en { background: linear-gradient(135deg, #e65100, #ef6c00); }

/* Step cards */
.step-card {
    background: linear-gradient(135deg, #e8eaf6, #f3e5f5);
    border-radius: 14px;
    padding: 20px 24px;
    margin: 12px 0;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    direction: rtl;
}
.step-number {
    background: linear-gradient(135deg, #1565c0, #0288d1);
    color: white;
    border-radius: 50%;
    width: 44px; height: 44px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3em; font-weight: 700;
    flex-shrink: 0;
}
.step-content h4 { color: #1a237e; margin: 0 0 6px 0; font-size: 1.1em; }
.step-content p  { color: #455a64; margin: 0; line-height: 1.9; font-size: 0.97em; }

/* Math boxes */
.math-container {
    background: linear-gradient(135deg, #e8eaf6 0%, #f3e5f5 100%);
    border-radius: 14px;
    padding: 24px 28px;
    margin: 16px 0;
    border: 1px solid #c5cae9;
    text-align: center;
}
.math-label {
    font-size: 0.9em;
    color: #5c6bc0;
    font-weight: 600;
    margin-bottom: 10px;
    text-align: right;
}

/* Assumption cards */
.assume-card {
    background: #fafafa;
    border-radius: 12px;
    border: 1px solid #e0e0e0;
    padding: 18px 22px;
    margin: 10px 0;
}
.assume-title { font-weight: 700; color: #1a237e; font-size: 1.05em; margin-bottom: 8px; }
.assume-body  { color: #546e7a; line-height: 1.9; font-size: 0.97em; }

/* Comparison table */
.compare-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.compare-table th {
    background: linear-gradient(135deg, #1565c0, #0288d1);
    color: white;
    padding: 14px 18px;
    text-align: right;
    font-size: 1.0em;
}
.compare-table td {
    padding: 12px 18px;
    border-bottom: 1px solid #e8eaf6;
    color: #37474f;
    line-height: 1.8;
    font-size: 0.97em;
}
.compare-table tr:nth-child(even) td { background: #f8f9ff; }
.compare-table tr:hover td { background: #e8f4fd; }

/* Footer */
.footer-bar {
    background: linear-gradient(135deg, #1a237e, #283593);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    margin-top: 40px;
    color: rgba(255,255,255,0.9);
    font-size: 0.95em;
}

/* Latex wrapper */
.latex-wrapper {
    overflow-x: auto;
    padding: 10px 0;
}

/* highlight text */
.highlight { background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%); padding: 2px 8px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2.8em;'>🌐</div>
        <div style='font-size:1.2em; font-weight:700; margin:8px 0;'>نموذج GVAR</div>
        <div style='font-size:0.85em; opacity:0.8;'>دليلك الشامل خطوة بخطوة</div>
        <hr style='border-color:rgba(255,255,255,0.25); margin:14px 0;'/>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio("", [
        "🏠  الصفحة الرئيسية",
        "📌  ما هو نموذج GVAR؟",
        "⚠️  مشكلة الأبعاد الكبيرة",
        "🔧  الحل: بناء النموذج",
        "🔬  أنواع المتغيرات ومعناها",
        "🗂️  خطوات الباحث التفصيلية",
        "🧮  الاختبارات القبلية",
        "📐  الرياضيات خطوة بخطوة",
        "📋  الافتراضات والشروط",
        "💥  تحليل الصدمات (IRF)",
        "🔮  التنبؤ بالنموذج",
        "📊  العلاقات طويلة الأجل",
        "🌲  نماذج GVAR المختلفة",
        "🌍  التطبيقات العملية",
        "🧪  اختبارات التشخيص",
        "📈  محاكاة تفاعلية",
    ], label_visibility="collapsed")

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.2); margin:16px 0;'/>
    <div style='font-size:0.82em; text-align:center; opacity:0.85; line-height:1.8;'>
        👨‍🏫 المطوّر<br/>
        <strong>Dr. Merwan Roudane</strong><br/>
        <span style='font-size:0.9em;'>د. مروان رودان</span><br/>
        <span style='opacity:0.7; font-size:0.85em;'>اقتصاد قياسي • نماذج عالمية</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO BANNER (shared)
# ─────────────────────────────────────────────
def show_hero():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🌐 نموذج GVAR</div>
        <div class="hero-subtitle">النموذج الشعاعي العالمي الذاتي الانحدار</div>
        <div class="hero-en">Global Vector AutoRegressive Model</div>
        <div class="dev-badge">👨‍🏫 Dr. Merwan Roudane &nbsp;|&nbsp; د. مروان رودان</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PAGE 1 — HOME
# ═══════════════════════════════════════════════════════
if menu == "🏠  الصفحة الرئيسية":
    show_hero()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="section-card">
            <div style='font-size:2.5em; text-align:center;'>📖</div>
            <div class="sec-title" style='text-align:center;'>لمن هذا الدليل؟</div>
            <div class="info-box info-blue">
                <p>هذا الدليل مُصمَّم لك <strong>تمامًا</strong> حتى لو لم تسمع بـ GVAR من قبل. سنبدأ من الصفر ونصل إلى كامل تفاصيل النموذج.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="section-card section-card-green">
            <div style='font-size:2.5em; text-align:center;'>🎯</div>
            <div class="sec-title" style='text-align:center;'>ماذا ستتعلم؟</div>
            <div class="info-box info-green">
                <p>الفكرة الأساسية • الرياضيات بالتفصيل • الافتراضات • كيفية بناء النموذج • التطبيقات الحقيقية</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="section-card section-card-orange">
            <div style='font-size:2.5em; text-align:center;'>⭐</div>
            <div class="sec-title" style='text-align:center;'>لماذا GVAR؟</div>
            <div class="info-box info-orange">
                <p>لأن الاقتصادات العالمية مترابطة! ما يحدث في أمريكا يؤثر في الجزائر والصين وأوروبا. GVAR يُمثّل هذا التشابك بدقة.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🗺️ خريطة الدراسة</div>
        <div class="sec-subtitle">إليك ترتيب الموضوعات الموصى به للفهم الكامل:</div>
    """, unsafe_allow_html=True)

    steps_home = [
        ("📌", "ما هو GVAR؟", "الفكرة الكبيرة والتعريف والتاريخ"),
        ("⚠️", "مشكلة الأبعاد", "لماذا نحتاج إلى GVAR أصلاً؟"),
        ("🔧", "بناء النموذج", "الخطوتان الرئيسيتان للبناء"),
        ("🔬", "أنواع المتغيرات", "المحلية، النجمية، المشتركة — التفصيل الكامل"),
        ("🗂️", "خطوات الباحث", "ما يفعله الباحث فعلياً من أول خطوة حتى آخرها"),
        ("🧮", "الاختبارات القبلية", "جذر الوحدة، التكامل المشترك، الخارجية الضعيفة"),
        ("📐", "الرياضيات", "المعادلات والمصطلحات بالتفصيل"),
        ("📋", "الافتراضات", "الشروط اللازمة لصحة النموذج"),
        ("💥", "تحليل الصدمات", "كيف نقيس أثر حدث ما؟"),
        ("🔮", "التنبؤ", "كيف يتنبأ النموذج بالمستقبل؟"),
        ("📊", "العلاقات طويلة الأجل", "التكامل المشترك والاستقرار"),
        ("🌲", "نماذج GVAR المختلفة", "الأساسي، البيزي، الانتقالي، الأوزان المتغيرة..."),
        ("🌍", "التطبيقات", "أمثلة حقيقية من العالم"),
        ("📈", "محاكاة تفاعلية", "جرّب بنفسك!"),
    ]
    for i, (icon, title, desc) in enumerate(steps_home):
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number">{i+1}</div>
            <div class="step-content">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Quick Stats
    st.markdown("<div class='section-card section-card-teal'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>📊 أرقام مهمة عن GVAR</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("2004", "سنة الاختراع", "#1565c0"),
        ("33+", "دولة في النموذج الأصلي", "#2e7d32"),
        ("100+", "ورقة بحثية تطبيقية", "#e65100"),
        ("3", "بدائل حل مشكلة الأبعاد", "#6a1b9a"),
    ]
    for col, (val, lbl, clr) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f"""
            <div style='background:{clr}; border-radius:14px; padding:22px; text-align:center; color:white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='font-size:2.4em; font-weight:900;'>{val}</div>
                <div style='font-size:0.9em; opacity:0.9; margin-top:6px;'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  PAGE 2 — WHAT IS GVAR
# ═══════════════════════════════════════════════════════
elif menu == "📌  ما هو نموذج GVAR؟":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">📌 التعريف البسيط أولاً</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-blue">
        <p>تخيّل أنك تريد دراسة <strong>الاقتصاد العالمي</strong> كله في آنٍ واحد. كيف تؤثر صدمة في الاقتصاد الأمريكي على الاقتصاد الجزائري أو الصيني؟ هذا بالضبط ما يفعله <span class="highlight">GVAR</span>.</p>
    </div>
    <div class="info-box info-green">
        <p><strong>GVAR</strong> = <strong>G</strong>lobal <strong>V</strong>ector <strong>A</strong>uto<strong>R</strong>egressive Model</p>
        <p>بالعربية: <strong>النموذج الشعاعي العالمي الذاتي الانحدار</strong></p>
        <p>هو نموذج اقتصادي قياسي يُمثّل <strong>مجموعة كبيرة من الدول</strong> (أو القطاعات) معًا ويحلّل كيف تتأثر كل واحدة بالأخرى بمرور الوقت.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # History
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">📅 التاريخ والنشأة</div>
    """, unsafe_allow_html=True)

    timeline = [
        ("1997", "💥", "الأزمة المالية الآسيوية", "أظهرت كيف تنتقل الأزمات بسرعة بين الدول — كان الباحثون بحاجة لنموذج يُقيس ذلك."),
        ("2004", "🚀", "ظهور GVAR", "اقترح Pesaran et al. النموذج لأول مرة لتحليل مخاطر الائتمان من منظور عالمي."),
        ("2007", "🔬", "التوسع النظري", "قدّم Dées et al. أساسًا نظريًا أعمق وتطبيقات على منطقة اليورو."),
        ("2013", "📚", "الكتاب الإرشادي", "صدر GVAR Handbook بـ 27 تطبيقًا عمليًا من باحثين حول العالم."),
        ("2014+", "🌐", "انتشار واسع", "أصبح GVAR أداةً معيارية في البنوك المركزية والمؤسسات الدولية."),
    ]
    for year, icon, title, desc in timeline:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-number" style='background: linear-gradient(135deg,#e65100,#ef6c00); min-width:60px; border-radius:10px; font-size:0.85em;'>{year}</div>
            <div class="step-content">
                <h4>{icon} {title}</h4>
                <p>{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Key idea
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">💡 الفكرة الجوهرية بمثال يومي</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-yellow">
        <p>🌍 <strong>مثال:</strong> تخيّل أن أسعار النفط ارتفعت فجأة. ماذا يحدث؟</p>
        <p>• الجزائر (مُصدِّر نفط) ← ارتفاع الإيرادات ← نمو اقتصادي</p>
        <p>• اليابان (مُستورِد نفط) ← ارتفاع التكاليف ← تراجع النمو</p>
        <p>• ألمانيا ← تأثير على صناعتها ← يؤثر على صادراتها للجزائر</p>
        <p>• ... والسلسلة تستمر!</p>
        <p><strong>GVAR يُمثّل هذه السلسلة كاملةً بشكل رياضي دقيق.</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Network visualization
    countries = ["USA", "EU", "China", "Algeria", "Japan", "Brazil", "India", "UK"]
    n = len(countries)
    angles = [2 * np.pi * i / n for i in range(n)]
    x_pos = [np.cos(a) * 3 for a in angles]
    y_pos = [np.sin(a) * 3 for a in angles]
    colors_c = ["#1565c0","#2e7d32","#e65100","#6a1b9a","#ad1457","#00695c","#f9a825","#0288d1"]

    edge_x, edge_y = [], []
    np.random.seed(42)
    for i in range(n):
        for j in range(i+1, n):
            if np.random.random() > 0.3:
                edge_x += [x_pos[i], x_pos[j], None]
                edge_y += [y_pos[i], y_pos[j], None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                             line=dict(color='#b0bec5', width=1.5), hoverinfo='none', opacity=0.6))
    fig.add_trace(go.Scatter(
        x=x_pos, y=y_pos, mode='markers+text',
        text=countries, textposition="top center",
        marker=dict(size=30, color=colors_c, line=dict(color='white', width=2),
                    symbol='circle'),
        textfont=dict(size=12, family='Cairo', color='#263238'),
        hoverinfo='text'
    ))
    fig.update_layout(
        title=dict(text="🌐 شبكة الترابط بين الاقتصادات في نموذج GVAR", font=dict(size=16, family='Cairo'), x=0.5),
        showlegend=False,
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # VAR vs GVAR
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">⚖️ المقارنة: VAR مقابل GVAR</div>
        <table class="compare-table">
            <tr><th>الجانب</th><th>نموذج VAR التقليدي</th><th>نموذج GVAR</th></tr>
            <tr><td>النطاق</td><td>دولة واحدة</td><td>عشرات الدول معًا</td></tr>
            <tr><td>عدد المعاملات</td><td>يتضاعف مع الحجم (لعنة الأبعاد)</td><td>محكوم ومُسيطَر عليه</td></tr>
            <tr><td>التفاعل الخارجي</td><td>مُهمَل أو محدود جداً</td><td>في صلب النموذج</td></tr>
            <tr><td>صلاحية للتنبؤ العالمي</td><td>ضعيفة</td><td>ممتازة</td></tr>
            <tr><td>التماسك كنظام مغلق</td><td>لا</td><td>نعم — ضرورة للسيناريوهات</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 3 — CURSE OF DIMENSIONALITY
# ═══════════════════════════════════════════════════════
elif menu == "⚠️  مشكلة الأبعاد الكبيرة":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">⚠️ لعنة الأبعاد (Curse of Dimensionality)</div>
        <div class="sec-subtitle">قبل أن نفهم الحل، يجب أن نفهم المشكلة أولاً</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-orange">
        <p><strong>المشكلة:</strong> إذا أردنا بناء نموذج VAR يشمل <strong>N</strong> دولة، كل دولة لها <strong>k</strong> متغير، فإن عدد المعاملات المجهولة يكبر بشكل رهيب.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>عدد المعاملات المجهولة في VAR تقليدي:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{عدد المعاملات} \approx (N \times k)^2 \times p")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#546e7a; font-size:0.95em;'>حيث p = عدد الفجوات الزمنية (lags)</p></div>", unsafe_allow_html=True)

    # Interactive demonstration
    st.markdown("<div class='sec-title' style='margin-top:20px;'>📊 جرّب بنفسك: شاهد كيف تتفجر المعاملات</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        n_countries = st.slider("عدد الدول (N)", 5, 50, 20, key="nc")
    with c2:
        k_vars = st.slider("عدد المتغيرات لكل دولة (k)", 2, 8, 4, key="kv")
    p_lags = st.slider("عدد الفجوات الزمنية (p)", 1, 4, 2, key="pl")

    total_vars = n_countries * k_vars
    params_var = (total_vars ** 2) * p_lags
    params_gvar = n_countries * (k_vars * (k_vars + k_vars) * p_lags + k_vars * 2)

    fig_dim = go.Figure()
    ns = list(range(5, 55, 5))
    params_var_line  = [(n_c * k_vars)**2 * p_lags for n_c in ns]
    params_gvar_line = [n_c * (k_vars*(k_vars+k_vars)*p_lags + k_vars*2) for n_c in ns]

    fig_dim.add_trace(go.Scatter(x=ns, y=params_var_line, mode='lines+markers', name='VAR تقليدي',
                                 line=dict(color='#e53935', width=3), marker=dict(size=8)))
    fig_dim.add_trace(go.Scatter(x=ns, y=params_gvar_line, mode='lines+markers', name='GVAR',
                                 line=dict(color='#1565c0', width=3), marker=dict(size=8)))
    fig_dim.add_vline(x=n_countries, line_dash="dash", line_color="#f9a825",
                      annotation_text=f"  {n_countries} دولة", annotation_font_color="#f9a825")
    fig_dim.update_layout(
        title=dict(text="مقارنة عدد المعاملات: VAR مقابل GVAR", font=dict(family='Cairo', size=15), x=0.5),
        xaxis_title="عدد الدول (N)", yaxis_title="عدد المعاملات",
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        font=dict(family='Cairo'),
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)', bordercolor='#e0e0e0', borderwidth=1),
        height=380
    )
    st.plotly_chart(fig_dim, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="info-box info-orange">
            <p>🔴 <strong>VAR تقليدي يحتاج:</strong></p>
            <p style='font-size:1.8em; font-weight:900; color:#c62828;'>{params_var:,}</p>
            <p>معاملاً مجهولاً — يستحيل تقديرها!</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="info-box info-blue">
            <p>🔵 <strong>GVAR يحتاج فقط:</strong></p>
            <p style='font-size:1.8em; font-weight:900; color:#1565c0;'>{params_gvar:,}</p>
            <p>معاملاً — قابل للتقدير بكفاءة!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # The three solutions
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">🛠️ الحلول الثلاثة لمشكلة الأبعاد</div>
    """, unsafe_allow_html=True)
    solutions = [
        ("نماذج العوامل (Factor Models)", "تُلخّص المتغيرات الكثيرة في عوامل مشتركة قليلة — مثل تكثيف المعلومات.", "#1565c0", "📊"),
        ("نماذج بايز الكبيرة (Bayesian VARs)", "تفرض قيودًا مسبقة على المعاملات لتقليص الفضاء المُقدَّر.", "#2e7d32", "📉"),
        ("نماذج GVAR ← الحل الأمثل", "تُقسّم النموذج الكبير إلى نماذج فرعية صغيرة مرتبطة عبر المتوسطات المرجحة.", "#e65100", "🌐"),
    ]
    for title, desc, clr, icon in solutions:
        st.markdown(f"""
        <div class="assume-card">
            <div class="assume-title" style='color:{clr};'>{icon} {title}</div>
            <div class="assume-body">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 4 — BUILDING THE MODEL
# ═══════════════════════════════════════════════════════
elif menu == "🔧  الحل: بناء النموذج":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🔧 كيف يُبنى نموذج GVAR؟ — الخطوتان الكبيرتان</div>
        <div class="sec-subtitle">يعتمد GVAR على نهج من خطوتين (Two-Step Approach) في غاية الذكاء</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#e8eaf6,#f3e5f5); border-radius:16px; padding:24px; text-align:center; margin:16px 0;'>
        <div style='font-size:1.5em; font-weight:700; color:#1a237e; margin-bottom:16px;'>مخطط سير النموذج</div>
        <div style='display:flex; justify-content:center; align-items:center; gap:16px; flex-wrap:wrap;'>
            <div style='background:#1565c0; color:white; border-radius:12px; padding:16px 24px; font-weight:700;'>النموذج الكبير المجهول</div>
            <div style='font-size:2em; color:#1565c0;'>→</div>
            <div style='background:#2e7d32; color:white; border-radius:12px; padding:16px 24px; font-weight:700;'>الخطوة 1: نماذج فردية لكل دولة</div>
            <div style='font-size:2em; color:#1565c0;'>→</div>
            <div style='background:#e65100; color:white; border-radius:12px; padding:16px 24px; font-weight:700;'>الخطوة 2: دمجها في نموذج واحد</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # STEP 1
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">🟢 الخطوة الأولى: نماذج الدول الفردية (VARX)</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-green">
        <p>لكل دولة <strong>i</strong>، نبني نموذجًا صغيرًا يشمل:</p>
        <p>• <strong>متغيراتها الداخلية (Domestic Variables)</strong> مثل: الناتج المحلي، التضخم، سعر الصرف...</p>
        <p>• <strong>متغيرات نجمية (Star Variables) x*ᵢₜ</strong>: وهي مُعدّلات مرجّحة لمتغيرات باقي دول العالم</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>النموذج الفردي لكل دولة i — معادلة VARX:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"x_{it} = \sum_{\ell=1}^{p_i} \Phi_{i\ell}\, x_{i,t-\ell} + \Lambda_{i0}\, x^*_{it} + \sum_{\ell=1}^{q_i} \Lambda_{i\ell}\, x^*_{i,t-\ell} + \varepsilon_{it}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; margin-top:12px; color:#546e7a; font-size:0.93em; line-height:2.2;'>
    ⬅️ <strong>xᵢₜ</strong>: شعاع المتغيرات الداخلية للدولة i في الزمن t (Domestic Variables Vector)<br>
    ⬅️ <strong>x*ᵢₜ</strong>: الشعاع النجمي — المتوسط المرجّح لمتغيرات الخارج (Star/Foreign Variables)<br>
    ⬅️ <strong>Φᵢℓ</strong>: مصفوفات معاملات المتغيرات الداخلية المتأخرة<br>
    ⬅️ <strong>Λᵢℓ</strong>: مصفوفات معاملات المتغيرات الأجنبية<br>
    ⬅️ <strong>εᵢₜ</strong>: حد الخطأ (Error Term)
    </div></div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-yellow">
        <p>🌟 <strong>المتغيرات النجمية x*ᵢₜ (Star Variables)</strong> — الفكرة الأذكى في GVAR!</p>
        <p>بدلاً من أن ندخل كل متغيرات العالم في النموذج، نُلخّصها في متوسط مرجّح واحد:</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"x^*_{it} = \tilde{W}_i' x_t = \sum_{j=1}^{N} w_{ij}\, x_{jt}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; margin-top:8px; color:#546e7a; font-size:0.93em;'>
    ⬅️ <strong>w_{ij}</strong>: الأوزان (عادةً من بيانات التجارة الثنائية — Trade Weights)<br>
    ⬅️ <strong>xₜ</strong>: شعاع كل متغيرات جميع الدول<br>
    ⬅️ <strong>W̃ᵢ</strong>: مصفوفة الأوزان الخاصة بالدولة i
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # STEP 2
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">🟠 الخطوة الثانية: تجميع النماذج في GVAR واحد</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-orange">
        <p>بعد تقدير كل نموذج فردي بشكل منفصل، ندمج جميع النماذج في <strong>نموذج VAR عالمي واحد ضخم</strong></p>
        <p>نستخدم مصفوفة الربط (Link Matrix) <strong>Wᵢ</strong> لتحقيق ذلك:</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>ربط المتغيرات الداخلية والنجمية بشعاع الحالة الكاملة:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"z_{it} = \begin{pmatrix} x_{it} \\ x^*_{it} \end{pmatrix} = W_i x_t")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>بعد التجميع لجميع الدول N، نحصل على GVAR الكامل:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"G_0 x_t = \sum_{\ell=1}^{p} G_\ell\, x_{t-\ell} + \varepsilon_t")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\Downarrow")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"x_t = \sum_{\ell=1}^{p} F_\ell\, x_{t-\ell} + G_0^{-1}\varepsilon_t \quad \text{(GVAR الكامل)}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:10px;'>
    ⬅️ <strong>G₀</strong>: مصفوفة المعاملات الآنية — يجب أن تكون قابلة للعكس (Invertible)<br>
    ⬅️ <strong>Fℓ = G₀⁻¹Gℓ</strong>: مصفوفات معاملات GVAR المُدمَج
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Visual flow
    fig_flow = go.Figure()
    countries_ex = ["الجزائر", "فرنسا", "أمريكا", "الصين", "ألمانيا"]
    colors_flow = ["#1565c0","#2e7d32","#e65100","#6a1b9a","#00695c"]
    for i, (country, clr) in enumerate(zip(countries_ex, colors_flow)):
        fig_flow.add_trace(go.Scatter(x=[0], y=[i], mode='markers+text',
                                      text=[f"نموذج {country}"], textposition="middle right",
                                      marker=dict(size=35, color=clr, symbol='square'),
                                      textfont=dict(size=12, family='Cairo', color=clr)))
        fig_flow.add_annotation(x=0.5, y=i, ax=0.1, ay=2, xref='x', yref='y',
                                axref='x', ayref='y',
                                showarrow=True, arrowhead=2, arrowcolor=clr, arrowwidth=2)
    fig_flow.add_trace(go.Scatter(x=[1], y=[2], mode='markers+text',
                                  text=["GVAR\nالكامل"], textposition="middle right",
                                  marker=dict(size=70, color='#f9a825', symbol='diamond'),
                                  textfont=dict(size=14, family='Cairo', color='#e65100')))
    fig_flow.update_layout(
        title=dict(text="من النماذج الفردية إلى GVAR الموحَّد", font=dict(family='Cairo', size=14), x=0.5),
        showlegend=False, plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.3, 2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=350, margin=dict(l=20, r=80, t=50, b=20)
    )
    st.plotly_chart(fig_flow, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE NEW-A — VARIABLE TYPES AND MEANINGS
# ═══════════════════════════════════════════════════════
elif menu == "🔬  أنواع المتغيرات ومعناها":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🔬 أنواع المتغيرات في نموذج GVAR ومعناها</div>
        <div class="sec-subtitle">قبل أن تبدأ البحث، يجب أن تعرف تماماً ما هي المتغيرات التي تستخدمها وما معناها ودورها</div>
    </div>
    """, unsafe_allow_html=True)

    # Classification overview
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">📦 التصنيف العام للمتغيرات</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-green">
        <p>تنقسم المتغيرات في GVAR إلى <strong>ثلاثة أصناف رئيسية</strong> — كل صنف له دور محدد في بنية النموذج:</p>
    </div>
    """, unsafe_allow_html=True)

    cat_cols = st.columns(3)
    cats = [
        ("🏠", "متغيرات داخلية", "Domestic Variables\nxᵢₜ", "#1565c0",
         "المتغيرات الاقتصادية الخاصة بكل دولة منفردة. يتم نمذجتها كمتغيرات داخلية (Endogenous) لأنها مُحدَّدة داخل النموذج."),
        ("🌍", "متغيرات أجنبية نجمية", "Star / Foreign Variables\nx*ᵢₜ", "#2e7d32",
         "مُعدّلات مرجّحة لمتغيرات باقي دول العالم. تُعامَل كمتغيرات خارجية ضعيفة (Weakly Exogenous) — تؤثر في الدولة لكنها لا تتأثر بها بشكل مباشر."),
        ("☀️", "متغيرات مشتركة عالمية", "Global Common Variables\nωₜ", "#e65100",
         "متغيرات تؤثر على جميع الدول في آنٍ واحد، مثل أسعار النفط العالمية أو أسعار الفائدة الأمريكية. قد تكون مرصودة أو غير مرصودة."),
    ]
    for col, (icon, name_ar, name_en, clr, desc) in zip(cat_cols, cats):
        with col:
            st.markdown(f"""
            <div style='background:{clr}; border-radius:14px; padding:22px; text-align:center; color:white; margin-bottom:12px;'>
                <div style='font-size:2em;'>{icon}</div>
                <div style='font-size:1.05em; font-weight:700; margin:8px 0;'>{name_ar}</div>
                <div style='font-size:0.78em; opacity:0.85; white-space:pre-line;'>{name_en}</div>
            </div>
            <div class='info-box' style='background:#f8f9ff; border-right: 4px solid {clr};'>
                <p style='color:#37474f;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Domestic variables detail
    st.markdown("""
    <div class="section-card section-card-indigo">
        <div class="sec-title">🏠 أولاً: المتغيرات الداخلية (Domestic Variables — xᵢₜ)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-purple">
        <p>هي المتغيرات الاقتصادية الكلية للدولة <strong>i</strong> في الزمن <strong>t</strong>. تُجمَع في شعاع: <strong>xᵢₜ = (kᵢ × 1)</strong></p>
        <p>عادةً ما يكون <strong>kᵢ صغيراً (3 إلى 6 متغيرات)</strong> لتجنّب لعنة الأبعاد داخل كل نموذج فردي.</p>
    </div>
    """, unsafe_allow_html=True)

    dom_vars = [
        ("📈 الناتج المحلي الإجمالي الحقيقي", "Real GDP (y)", "log(GDP الحقيقي)", "المتغير الأكثر استخداماً. يقيس حجم الاقتصاد. يُؤخذ اللوغاريتم عادةً لتحويله إلى معدل نمو بعد الفرق الأول. غالباً ما يكون I(1)."),
        ("💰 معدل التضخم", "Inflation (π)", "تغيّر مؤشر الأسعار", "يُقاس بتغيّر مؤشر أسعار المستهلك (CPI) أو مُفكّكة GDP. قد يكون I(0) أو I(1) حسب البلد والحقبة."),
        ("💵 سعر الصرف الحقيقي", "Real Exchange Rate (ep)", "log(سعر الصرف الاسمي × الأسعار)", "يؤثر في التجارة والتنافسية. غالباً I(1). مهم في ربط المتغيرات الداخلية بالخارجية."),
        ("🏦 أسعار الفائدة قصيرة الأجل", "Short Rate (rs)", "معدل الفائدة على الودائع 3 أشهر", "أداة السياسة النقدية. قد يكون I(1) أو I(0). يُدرج لتمثيل القناة النقدية."),
        ("📉 أسعار الفائدة طويلة الأجل", "Long Rate (rl)", "عائد السندات الحكومية 10 سنوات", "يعكس توقعات المستقبل وتكلفة التمويل طويل الأجل. عادةً I(1)."),
        ("📊 أسعار الأسهم الحقيقية", "Real Equity Prices (eq)", "log(مؤشر الأسهم / مستوى الأسعار)", "تعكس الثروة المالية وتوقعات المستثمرين. غالباً I(1). مهم في النماذج المالية."),
        ("🏠 أسعار العقارات الحقيقية", "Real House Prices", "log(مؤشر أسعار المساكن / CPI)", "يُضاف في التطبيقات المتخصصة بالدورة العقارية."),
        ("💳 الائتمان المصرفي الحقيقي", "Real Credit", "log(الائتمان للقطاع الخاص / CPI)", "يُدرج لدراسة دور الائتمان في دورة الأعمال."),
    ]
    for i in range(0, len(dom_vars), 2):
        c1, c2 = st.columns(2)
        for col, idx in zip([c1, c2], [i, i+1]):
            if idx < len(dom_vars):
                name, en, measure, desc = dom_vars[idx]
                with col:
                    st.markdown(f"""
                    <div class='assume-card'>
                        <div class='assume-title'>{name}</div>
                        <div style='color:#1565c0; font-size:0.88em; font-style:italic; margin-bottom:6px;'>{en} — القياس: {measure}</div>
                        <div class='assume-body'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Star variables detail
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">🌍 ثانياً: المتغيرات النجمية الأجنبية (Star Variables — x*ᵢₜ)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-green">
        <p><strong>المفهوم الجوهري:</strong> بدلاً من إدخال متغيرات كل دولة أجنبية على حدة (مما يُفجّر عدد المعاملات)، نُلخّصها في <strong>متوسط مرجّح واحد</strong> لكل متغير.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'><div class='math-label'>صيغة حساب المتغير النجمي:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"x^*_{it} = \sum_{j=1, j\neq i}^{N} w_{ij}\, x_{jt} \quad \text{حيث} \quad \sum_{j \neq i} w_{ij} = 1")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:10px; line-height:2.2;'>
    📌 <strong>wᵢⱼ</strong>: وزن الدولة j في حساب المتوسط الخارجي للدولة i<br>
    📌 الأوزان مشروطة بـ: wᵢᵢ = 0 (الدولة لا تدخل في حساب متوسطها الخاص)<br>
    📌 المجموع = 1: الأوزان مُعيَّرة (Normalized)
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-yellow">
        <p>⚖️ <strong>أنواع الأوزان المستخدمة في الممارسة:</strong></p>
        <p>• <strong>أوزان التجارة الثنائية</strong> (Trade Weights) — الأكثر شيوعاً: نسبة التجارة مع الدولة j إلى إجمالي تجارة الدولة i<br>
        • <strong>أوزان تدفقات رأس المال</strong> (Capital Flow Weights) — لتمثيل التكاملات المالية<br>
        • <strong>أوزان متساوية</strong> (Equal Weights) — وᵢⱼ = 1/(N-1) — تُستخدم عند عدم توفر بيانات التجارة<br>
        • <strong>أوزان متغيرة عبر الزمن</strong> (Time-Varying Weights) — لتمثيل التغيرات الهيكلية في العلاقات الاقتصادية</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-green">
        <p>✅ <strong>ما الذي يُقابل كل متغير داخلي بمتغير نجمي؟</strong></p>
        <p>• y*ᵢₜ = المتوسط المرجّح للناتج المحلي لكل الدول الأخرى (نمو العالم)<br>
        • π*ᵢₜ = التضخم العالمي المرجّح بالتجارة<br>
        • ep*ᵢₜ = سعر الصرف الحقيقي الخارجي المرجّح<br>
        • rs*ᵢₜ = أسعار الفائدة الدولية المرجّحة</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Global common variables
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">☀️ ثالثاً: المتغيرات المشتركة العالمية (Global Common Variables — ωₜ)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-orange">
        <p><strong>هي متغيرات تؤثر في جميع الدول في آنٍ واحد</strong> ولا يمكن تمثيلها بالمتوسطات المرجّحة لأنها خارج نموذج أي دولة بعينها.</p>
    </div>
    """, unsafe_allow_html=True)
    glob_vars = [
        ("🛢️ أسعار النفط العالمية", "Global Oil Prices (poil)", "متغير سائد (Dominant Variable)", "الأكثر استخداماً. يؤثر في جميع اقتصادات العالم — المُصدِّرة والمُستوردة. يُدخَل كمتغير خارجي في جميع النماذج الفردية."),
        ("🌾 أسعار السلع الأولية", "Global Commodity Prices", "مؤشر أسعار السلع الأولية", "يُضاف لدراسة أثر صدمات أسعار الغذاء والمعادن. مهم بشكل خاص للدول النامية."),
        ("💱 مؤشر الدولار الأمريكي", "US Dollar Index", "قيمة الدولار مقابل سلة عملات", "يُعكس الهيمنة المالية للولايات المتحدة ويستخدم في نماذج أسعار الصرف العالمية."),
        ("📡 عوامل مشتركة غير مرصودة", "Unobserved Common Factors (fₜ)", "تُقدَّر بالمتوسطات المرجّحة", "تتضمن صدمات التقنية العالمية، التحولات السياسية، وغيرها من العوامل غير المرئية التي تؤثر في الجميع."),
    ]
    for name, en, measure, desc in glob_vars:
        st.markdown(f"""
        <div class='assume-card'>
            <div class='assume-title'>{name}</div>
            <div style='color:#e65100; font-size:0.88em; font-style:italic; margin-bottom:6px;'>{en} — النوع: {measure}</div>
            <div class='assume-body'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Variable classification table
    st.markdown("""
    <div class="section-card section-card-teal">
        <div class="sec-title">📊 جدول ملخص: أنواع المتغيرات وخصائصها</div>
        <table class="compare-table">
            <tr>
                <th>نوع المتغير</th>
                <th>الرمز</th>
                <th>درجة التكامل الشائعة</th>
                <th>كيف يدخل في النموذج؟</th>
                <th>مثال</th>
            </tr>
            <tr>
                <td><strong>داخلي (Domestic)</strong></td>
                <td>xᵢₜ</td>
                <td>I(1) غالباً</td>
                <td>مُتأخّر داخلياً في معادلة الدولة i</td>
                <td>GDP الجزائر، تضخم فرنسا</td>
            </tr>
            <tr>
                <td><strong>نجمي أجنبي (Star)</strong></td>
                <td>x*ᵢₜ</td>
                <td>I(1) غالباً</td>
                <td>آني ومُتأخّر — خارجي ضعيف</td>
                <td>GDP* = متوسط GDP العالم</td>
            </tr>
            <tr>
                <td><strong>مشترك عالمي مرصود (Observed)</strong></td>
                <td>ωₜ</td>
                <td>I(1) أو I(0)</td>
                <td>آني ومُتأخّر في جميع النماذج</td>
                <td>سعر برنت، مؤشر VIX</td>
            </tr>
            <tr>
                <td><strong>مشترك غير مرصود (Unobserved)</strong></td>
                <td>fₜ</td>
                <td>I(1) أو I(0)</td>
                <td>يُقرَّب بالمتوسطات x*</td>
                <td>صدمة تقنية عالمية</td>
            </tr>
            <tr>
                <td><strong>حدودية حتمية (Deterministic)</strong></td>
                <td>dt</td>
                <td>ثابت، اتجاه</td>
                <td>ثابت وقد يُضاف اتجاه زمني</td>
                <td>الثابت، dummy الأزمات</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    # Integration orders
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">🔢 درجة تكامل المتغيرات — I(0) و I(1) وأهميتها</div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class='info-box info-blue'>
            <p>📘 <strong>I(0) — متغير مستقر (Stationary)</strong></p>
            <p>يعود إلى متوسطه بعد أي صدمة. يمكن نمذجته بـ VAR عادي بدون فروق أولى.</p>
            <p><strong>أمثلة في GVAR:</strong> نسبة الفائدة الحقيقية، نسب التجارة في بعض الدول</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='info-box info-orange'>
            <p>📙 <strong>I(1) — متغير غير مستقر بجذر وحدة</strong></p>
            <p>يحتاج إلى فرق أول ليصبح مستقراً. لكن قد يكون متكاملاً مشتركاً مع متغيرات أخرى.</p>
            <p><strong>أمثلة في GVAR:</strong> log(GDP)، log(الأسعار)، log(سعر الصرف)</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-teal">
        <p>🔑 <strong>لماذا يهم هذا التصنيف؟</strong></p>
        <p>• إذا كانت المتغيرات I(1) → يجب اختبار التكامل المشترك (Cointegration) قبل البناء<br>
        • اختلاط I(0) و I(1) → ممكن في GVAR ولكن يتطلب عناية في التقدير والتفسير<br>
        • نموذج GVAR في صيغة تصحيح الخطأ (ECM) يستوعب كلا النوعين معاً</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE NEW-B — RESEARCHER STEPS IN DETAIL
# ═══════════════════════════════════════════════════════
elif menu == "🗂️  خطوات الباحث التفصيلية":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🗂️ ماذا يفعل الباحث خطوة بخطوة؟</div>
        <div class="sec-subtitle">دليل عملي شامل من جمع البيانات حتى تفسير النتائج — ما يفعله الباحث فعلياً في كل مرحلة</div>
    </div>
    """, unsafe_allow_html=True)

    # Phase overview
    phases = [
        ("🔵", "المرحلة التحضيرية", "جمع البيانات وإعدادها وحساب الأوزان", "#1565c0"),
        ("🟢", "الخطوة الأولى", "اختبارات ما قبل التقدير (القبلية)", "#2e7d32"),
        ("🟠", "الخطوة الثانية", "تقدير نماذج الدول الفردية VARX", "#e65100"),
        ("🔴", "الخطوة الثالثة", "بناء GVAR الكامل وتحليل الصدمات", "#c62828"),
        ("🟣", "الخطوة الرابعة", "اختبارات ما بعد التقدير (البعدية)", "#6a1b9a"),
        ("⭐", "الخطوة الخامسة", "التفسير والتنبؤ والسيناريوهات", "#00695c"),
    ]
    cols_ph = st.columns(len(phases))
    for col, (icon, phase, desc, clr) in zip(cols_ph, phases):
        with col:
            st.markdown(f"""
            <div style='background:{clr}; border-radius:12px; padding:16px 10px; text-align:center; color:white; min-height:130px;'>
                <div style='font-size:1.8em;'>{icon}</div>
                <div style='font-size:0.9em; font-weight:700; margin:6px 0;'>{phase}</div>
                <div style='font-size:0.75em; opacity:0.88;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── PHASE 0: Data Preparation ──
    st.markdown("""
    <div class="section-card" style='border-top-color:#1565c0;'>
        <div class="sec-title">🔵 المرحلة التحضيرية: جمع البيانات وإعدادها</div>
    """, unsafe_allow_html=True)

    prep_steps = [
        ("1", "تحديد نطاق الدراسة",
         "حدّد: عدد الدول (N)، الفترة الزمنية (T)، المتغيرات الداخلية لكل دولة (kᵢ)، والمتغيرات المشتركة (ωₜ).",
         "مثال: 33 دولة، ربعية 1979Q2–2013Q4، المتغيرات: y, π, ep, rs, rl, eq وسعر النفط كمتغير مشترك."),
        ("2", "جمع البيانات",
         "استخرج البيانات من: البنك الدولي، صندوق النقد الدولي (IFS)، بلومبرج، بانك OECD، اليوروستات.",
         "تأكد من التجانس: نفس التواتر (ربعية/سنوية)، نفس تعريفات المتغيرات، معالجة القيم المفقودة."),
        ("3", "تحويل المتغيرات",
         "حوّل المتغيرات إلى الصيغة المناسبة: خذ اللوغاريتم الطبيعي للمستويات (log)، وفروق لوغاريتمية للنمو.",
         "مثال: yᵢₜ = 100 × log(GDPᵢₜ)، πᵢₜ = 400 × Δlog(CPIᵢₜ)، epᵢₜ = log(Eᵢₜ × P_USAₜ / Pᵢₜ)"),
        ("4", "حساب مصفوفة الأوزان التجارية",
         "للسنة المرجعية (عادةً متوسط 3 سنوات لتجنب السنوات الشاذة): wᵢⱼ = تجارة i مع j / إجمالي تجارة i مع العالم",
         "تأكد أن Σⱼ wᵢⱼ = 1 وwᵢᵢ = 0. يمكن استخدام أوزان متغيرة عبر الزمن للنماذج المتطورة."),
        ("5", "حساب المتغيرات النجمية",
         "لكل دولة i ولكل متغير v: v*ᵢₜ = Σⱼ wᵢⱼ × vⱼₜ — هذا يُلخّص كل الخارج في رقم واحد!",
         "يُنجز بسهولة: x*ᵢₜ = W̃ᵢ × xₜ حيث W̃ᵢ مصفوفة الأوزان المبرمجة مسبقاً."),
    ]
    for num, title, action, note in prep_steps:
        st.markdown(f"""
        <div style='display:flex; gap:16px; margin:12px 0; direction:rtl; align-items:flex-start;'>
            <div style='background:#1565c0; color:white; border-radius:50%; width:40px; height:40px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:1.1em; flex-shrink:0;'>{num}</div>
            <div style='flex:1;'>
                <div style='font-weight:700; color:#1a237e; font-size:1.05em; margin-bottom:6px;'>{title}</div>
                <div style='color:#37474f; line-height:1.8; margin-bottom:8px;'>{action}</div>
                <div style='background:#e3f2fd; border-right:4px solid #1565c0; padding:10px 14px; border-radius:8px; color:#1565c0; font-size:0.9em;'>💡 {note}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 1: Pre-estimation tests ──
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">🟢 الخطوة الأولى: الاختبارات القبلية (Pre-Estimation Tests)</div>
        <div class="sec-subtitle">لا تُقدِّر النموذج قبل أن تُجري هذه الاختبارات — فهي أساس صحة النموذج كله</div>
    """, unsafe_allow_html=True)

    pre_tests = [
        ("1أ", "اختبار جذر الوحدة لجميع المتغيرات", "ADF, PP, KPSS, Zivot-Andrews",
         "هل المتغيرات I(0) أم I(1) أم I(2)؟ GVAR مصمم أساساً للمتغيرات I(1). إذا كانت I(2) → تحويل إضافي. إذا I(0) → يمكن استخدام نموذج VAR عادي.",
         "#2e7d32"),
        ("1ب", "اختبار التكامل المشترك لكل دولة", "Johansen Trace & Max-Eigenvalue",
         "لكل نموذج دولة: كم عدد الأشعة التكامل المشترك (rᵢ)؟ هذا يُحدّد رتبة مصفوفة Πᵢ ويؤثر مباشرة على صيغة ECM وعدد العلاقات طويلة الأجل.",
         "#1a6b3c"),
        ("1ج", "اختبار الخارجية الضعيفة للمتغيرات النجمية", "F-test على معاملات التصحيح",
         "هل x*ᵢₜ خارجية ضعيفة فعلاً؟ أي: هل يمكن تجاهل أثر المتغيرات الداخلية على x*ᵢₜ في معادلة التصحيح؟ إذا رُفض → الدولة ليست صغيرة كما افترضنا.",
         "#2e7d32"),
        ("1د", "اختيار درجة الإبطاء الأمثل", "AIC, BIC, HQIC, LR Tests",
         "حدّد pᵢ (إبطاء المتغيرات الداخلية) وqᵢ (إبطاء المتغيرات النجمية) لكل نموذج دولة. عادةً pᵢ = qᵢ = 1 أو 2 للبيانات الربعية.",
         "#2e7d32"),
    ]
    for num, title, test_name, desc, clr in pre_tests:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style='background:{clr}; border-radius:12px; padding:18px; text-align:center; color:white; height:100%;'>
                <div style='font-size:1.6em; font-weight:900;'>{num}</div>
                <div style='font-size:0.95em; font-weight:700; margin-top:6px;'>{title}</div>
                <div style='margin-top:8px; background:rgba(255,255,255,0.2); border-radius:8px; padding:6px 10px; font-size:0.82em;'>{test_name}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='info-box info-green'>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 2: Estimation ──
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">🟠 الخطوة الثانية: تقدير نماذج الدول الفردية</div>
        <div class="sec-subtitle">هذا هو جوهر الخطوة الأولى في نهج GVAR ذي المرحلتين</div>
    """, unsafe_allow_html=True)

    est_steps = [
        ("2أ", "تقدير كل نموذج VARX فردياً بطريقة OLS أو MLE",
         "لكل دولة i على حدة (من 1 إلى N): قدّر معادلة VARX مع المتغيرات الداخلية والنجمية والمشتركة.",
         "كل نموذج دولة صغير الحجم (kᵢ + k* متغير)، لذا يمكن تقديره بسهولة حتى مع T صغير نسبياً.", "#e65100"),
        ("2ب", "تقدير صيغة تصحيح الخطأ (ECM) إذا كانت المتغيرات I(1)",
         "إذا وُجد تكامل مشترك (rᵢ > 0): قدّر نموذج VECMX باستخدام طريقة Johansen المُعدَّلة للمتغيرات الخارجية الضعيفة.",
         "يُمكّن من تقدير العلاقات قصيرة الأجل والطويلة الأجل في آنٍ واحد.", "#e65100"),
        ("2ج", "تحديد علاقات التكامل المشترك وتقييدها",
         "حدّد الأشعة التكامل المشترك βᵢ وفرض القيود الاقتصادية (مثل: نظرية تعادل القوة الشرائية، نظرية فيشر).",
         "اختبر القيود بإحصاء نسبة الاحتمال (LR). القيود الاقتصادية تُحسّن تفسير النتائج.", "#e65100"),
        ("2د", "تقدير نموذج المتغيرات المشتركة (ωₜ) بشكل منفصل",
         "إذا كانت هناك متغيرات مشتركة عالمية (كأسعار النفط): قدّر نموذج VAR مستقل لها، ثم أدمجه مع النماذج الفردية.",
         "نموذج المتغير المشترك يُحدد استمراريته وتفاعله مع الاقتصاد العالمي.", "#e65100"),
    ]
    for num, title, action, note, clr in est_steps:
        st.markdown(f"""
        <div style='background:#fff8f5; border-right:5px solid {clr}; border-radius:12px; padding:20px 24px; margin:10px 0;'>
            <div style='color:{clr}; font-size:1.1em; font-weight:700; margin-bottom:8px;'>{num} — {title}</div>
            <div style='color:#37474f; line-height:1.9; margin-bottom:8px;'>{action}</div>
            <div style='background:#fff3e0; border-radius:8px; padding:10px 14px; color:#bf360c; font-size:0.9em;'>📌 {note}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 3: Full GVAR and IRF ──
    st.markdown("""
    <div class="section-card" style='border-top-color:#c62828;'>
        <div class="sec-title">🔴 الخطوة الثالثة: بناء GVAR الكامل وتحليل الصدمات</div>
    """, unsafe_allow_html=True)
    step3_items = [
        ("3أ", "تجميع نماذج الدول في نموذج GVAR واحد", "اصنع مصفوفة G₀ وG₁...Gₚ من مصفوفات الدول الفردية ومصفوفات الأوزان. تحقق من أن G₀ ذات رتبة كاملة."),
        ("3ب", "حساب مصفوفات F_ℓ للنموذج الكلي", "Fℓ = G₀⁻¹ × Gℓ — هذه هي معاملات GVAR الكامل الذي يُحدد استجابة الجميع لأي صدمة."),
        ("3ج", "حساب دوال الاستجابة الآنية GIRF", "للصدمة j: GIRF(h) = Rₕ × G₀⁻¹ × eⱼ / √σⱼⱼ — احسبها لكل المتغيرات ولكل الآفاق الزمنية (h = 0,1,...,40)."),
        ("3د", "حساب تحليل تباين الخطأ GFEVD", "ما نسبة تباين المتغير i التي تُفسَّر بصدمة في المتغير j؟ — يوضّح أهمية كل مصدر صدمة."),
    ]
    for num, title, desc in step3_items:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-number' style='background:linear-gradient(135deg,#c62828,#e53935);'>{num}</div>
            <div class='step-content'><h4>{title}</h4><p>{desc}</p></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 4: Post-estimation diagnostics ──
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">🟣 الخطوة الرابعة: اختبارات ما بعد التقدير (Post-Estimation)</div>
    """, unsafe_allow_html=True)
    post_tests = [
        ("4أ", "اختبار استقرار النموذج الكلي", "فحص القيم الذاتية للمرافق: يجب أن تقع داخل أو على دائرة الوحدة. عدد القيم الذاتية على الدائرة = k - r (عدد الاتجاهات المشتركة)."),
        ("4ب", "اختبار التسلسل التلقائي للبواقي", "Portmanteau / Ljung-Box: هل بواقي كل نموذج دولة خالية من الارتباط الذاتي؟ الرفض يعني الحاجة لفجوات إضافية."),
        ("4ج", "اختبار الاستقرار الهيكلي", "CUSUM, MOSUM, اختبارات Nyblom, Andrews-Ploberger: هل المعاملات مستقرة عبر الزمن؟"),
        ("4د", "اختبار السببية والإسناد", "هل تحليل تباين الخطأ منطقي اقتصادياً؟ هل مسارات الاستجابة متوافقة مع النظرية الاقتصادية؟"),
        ("4ه", "اختبارات الحساسية (Robustness)", "غيّر: الأوزان، الفجوات، رتبة التكامل، حجم العينة، الدول المشمولة — وتحقق أن النتائج الجوهرية لا تتغير."),
    ]
    for num, title, desc in post_tests:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-number' style='background:linear-gradient(135deg,#6a1b9a,#8e24aa);'>{num}</div>
            <div class='step-content'><h4>{title}</h4><p>{desc}</p></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── STEP 5: Results and forecasting ──
    st.markdown("""
    <div class="section-card section-card-teal">
        <div class="sec-title">⭐ الخطوة الخامسة: تفسير النتائج والتنبؤ والسيناريوهات</div>
    """, unsafe_allow_html=True)
    final_steps = [
        ("5أ", "تفسير دوال الاستجابة الآنية (IRFs/GIRFs)",
         "ارسم GIRF للمتغيرات الرئيسية مع فترات الثقة (Bootstrap 95%). فسّر: الحجم، الاتجاه، سرعة العودة للتوازن."),
        ("5ب", "تفسير تحليل تباين الخطأ",
         "حدّد أهم مصادر عدم اليقين لكل متغير: كم نسبة التباين تعود لصدمات محلية؟ وكم لصدمات دولية؟"),
        ("5ج", "التنبؤ وتقييم دقة التنبؤ",
         "قارن تنبؤات GVAR مع: AR univariate، BVAR، Random Walk، وبيانات الاختبار خارج العينة."),
        ("5د", "تحليل السيناريوهات",
         "افرض صدمة افتراضية (مثل انخفاض أسعار النفط بنسبة 30%) وشاهد تأثيرها على جميع الدول في النموذج."),
        ("5ه", "تقدير المكوّنات الدائمة والمؤقتة",
         "استخدم تحليل Beveridge-Nelson لفصل الاتجاه الدائم (Permanent) عن الدورة المؤقتة (Transitory) لكل متغير."),
    ]
    for num, title, desc in final_steps:
        st.markdown(f"""
        <div class='step-card'>
            <div class='step-number' style='background:linear-gradient(135deg,#00695c,#00897b);'>{num}</div>
            <div class='step-content'><h4>{title}</h4><p>{desc}</p></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Full flowchart visualization
    st.markdown("""
    <div class="section-card">
        <div class="sec-title">📊 مخطط تدفق عملية البحث الكاملة</div>
    """, unsafe_allow_html=True)

    fig_flow2 = go.Figure()
    flow_nodes = [
        (0.5, 9.5, "📁 جمع البيانات\nوإعدادها", "#1565c0"),
        (0.5, 8.2, "⚖️ حساب\nالأوزان w_ij", "#1565c0"),
        (0.5, 6.9, "🔍 اختبارات\nجذر الوحدة", "#2e7d32"),
        (0.5, 5.6, "🔗 اختبار\nالتكامل المشترك", "#2e7d32"),
        (0.5, 4.3, "📊 تقدير VARX\nلكل دولة", "#e65100"),
        (0.5, 3.0, "🔧 بناء\nGVAR الكامل", "#c62828"),
        (0.5, 1.7, "💥 GIRF &\nGFEVD", "#6a1b9a"),
        (0.5, 0.4, "✅ اختبارات\nالتشخيص", "#00695c"),
    ]
    for x, y, label, clr in flow_nodes:
        fig_flow2.add_shape(type="rect", x0=x-0.35, y0=y-0.5, x1=x+0.35, y1=y+0.5,
                           fillcolor=clr, line=dict(color="white", width=2), opacity=0.9)
        fig_flow2.add_annotation(x=x, y=y, text=label.replace("\n", "<br>"),
                                font=dict(color="white", size=11, family="Cairo"),
                                showarrow=False, align="center")
        if y > 0.4:
            fig_flow2.add_annotation(x=x, y=y-0.5, ax=x, ay=y-0.9,
                                    arrowhead=2, arrowsize=1.5, arrowwidth=2,
                                    arrowcolor="#546e7a", showarrow=True)
    fig_flow2.update_layout(
        height=600, showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0,1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.2,10.2]),
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Cairo")
    )
    st.plotly_chart(fig_flow2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE NEW-C — PRE-ESTIMATION TESTS (DETAILED)
# ═══════════════════════════════════════════════════════
elif menu == "🧮  الاختبارات القبلية":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🧮 الاختبارات القبلية (Pre-Estimation Tests)</div>
        <div class="sec-subtitle">هذه الاختبارات تُحدد طبيعة بياناتك وتُلزمك باختيارات منهجية حاسمة قبل أي تقدير</div>
    </div>
    """, unsafe_allow_html=True)

    test_tabs = st.tabs([
        "🌱 اختبارات جذر الوحدة",
        "🔗 اختبارات التكامل المشترك",
        "🎯 اختبار الخارجية الضعيفة",
        "📏 اختيار درجة الإبطاء",
        "📐 اختبارات أخرى مسبقة",
    ])

    with test_tabs[0]:
        st.markdown("""
        <div class="section-card section-card-green">
            <div class="sec-title">🌱 اختبارات جذر الوحدة (Unit Root Tests)</div>
            <div class="sec-subtitle">السؤال: هل المتغير مستقر I(0) أم يحتوي جذر وحدة I(1)؟</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-blue">
            <p>⚠️ <strong>لماذا مهم جداً؟</strong> إذا قدّرت نموذجاً بمتغيرات I(1) دون معالجة → الانحدار الزائف (Spurious Regression) → معاملات غير موثوقة حتى مع R² مرتفع!</p>
        </div>
        """, unsafe_allow_html=True)

        ur_tests = [
            ("ADF", "Augmented Dickey-Fuller", "H₀: جذر وحدة (I(1)) | H₁: مستقر I(0)",
             "الأكثر شيوعاً. يُعالج الارتباط الذاتي بإضافة فجوات Δyₜ₋ₗ. يُطبَّق على: المتغير بدون ثابت، مع ثابت، مع ثابت واتجاه.",
             "إذا |إحصاء ADF| < القيمة الحرجة (5%) → فشل في رفض H₀ → المتغير I(1) → خذ الفرق الأول وأعِد الاختبار."),
            ("PP", "Phillips-Perron", "H₀: جذر وحدة | H₁: مستقر",
             "يُصحّح تلقائياً للارتباط الذاتي والتباين غير المتجانس دون إضافة فجوات. أكثر مرونة من ADF.",
             "يُستحسن تطبيقه بالتوازي مع ADF. إذا اختلفا → ثق بـ KPSS كاختبار مكمّل."),
            ("KPSS", "Kwiatkowski-Phillips-Schmidt-Shin", "H₀: مستقر I(0) | H₁: جذر وحدة",
             "عكس ADF وPP! الفرضية الصفرية هنا هي الاستقرار. يُستخدم للتحقق المزدوج: إذا رُفض ADF ولم يُرفض KPSS → تأكيد I(1).",
             "القاعدة الذهبية: إذا ADF يفشل في رفض I(1) و KPSS يرفض I(0) → المتغير I(1) بثقة عالية."),
            ("Zivot-Andrews", "Zivot-Andrews (1992)", "H₀: جذر وحدة مع كسر هيكلي",
             "يختبر جذر الوحدة مع السماح بكسر هيكلي في نقطة زمنية مجهولة. مهم للبيانات الطويلة التي تشمل أزمات.",
             "إذا رُفض H₀ → المتغير مستقر مع كسر هيكلي → حدّد تاريخ الكسر وضع متغير وهمي Dummy."),
        ]
        for name, full_name, hypothesis, desc, interpretation in ur_tests:
            with st.expander(f"📊 اختبار {name} — {full_name}"):
                st.markdown(f"""
                <div class='info-box info-blue'><p>📋 <strong>الفرضية:</strong> {hypothesis}</p></div>
                <div class='assume-card'><div class='assume-title'>كيف يعمل؟</div><div class='assume-body'>{desc}</div></div>
                <div class='info-box info-green'><p>✅ <strong>كيف تفسّر النتيجة؟</strong> {interpretation}</p></div>
                """, unsafe_allow_html=True)

        # Visualization of I(0) vs I(1)
        np.random.seed(123)
        T_ur = 100
        I0_series = np.cumsum(np.random.randn(T_ur) * 0.3) * 0 + np.random.randn(T_ur) * 1.5
        I1_series = np.cumsum(np.random.randn(T_ur) * 0.8)
        t_axis = list(range(T_ur))

        fig_ur = make_subplots(1, 2, subplot_titles=("✅ متغير مستقر I(0) — يعود لمتوسطه", "❌ متغير I(1) — يتجوّل عشوائياً"))
        fig_ur.add_trace(go.Scatter(x=t_axis, y=I0_series, mode='lines', line=dict(color='#1565c0', width=2), name='I(0)'), row=1, col=1)
        fig_ur.add_hline(y=np.mean(I0_series), line_dash='dash', line_color='#e53935', row=1, col=1)
        fig_ur.add_trace(go.Scatter(x=t_axis, y=I1_series, mode='lines', line=dict(color='#e53935', width=2), name='I(1)'), row=1, col=2)
        fig_ur.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', height=320, font=dict(family='Cairo'), showlegend=False)
        st.plotly_chart(fig_ur, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with test_tabs[1]:
        st.markdown("""
        <div class="section-card section-card-teal">
            <div class="sec-title">🔗 اختبارات التكامل المشترك (Cointegration Tests)</div>
            <div class="sec-subtitle">السؤال: هل المتغيرات I(1) تتحرك معاً على المدى البعيد بحيث توجد علاقة توازنية مستقرة؟</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-teal">
            <p>🌟 <strong>الأهمية لـ GVAR:</strong> اختبار التكامل المشترك يُحدد رتبة التكامل (rᵢ) لكل نموذج دولة، وهذا يُحدد كيفية كتابة معادلة ECM وعدد العلاقات طويلة الأجل الموجودة.</p>
        </div>
        """, unsafe_allow_html=True)

        coint_data = [
            ("اختبار أثر يوهانسن (Trace Test)", "H₀: عدد الأشعة التكامل ≤ r | H₁: عدد الأشعة التكامل > r",
             "يختبر تراكمياً. يبدأ بـ r=0 ثم r=1 وهكذا حتى يفشل في الرفض. عند الفشل → هذا هو عدد التكامل.",
             "أقوى إحصاءً وأكثر استخداماً. يُفضَّل في الممارسة. احتمال رفض زائد في العينات الصغيرة."),
            ("اختبار الحد الأقصى للقيمة الذاتية (Max-Eigenvalue)", "H₀: عدد الأشعة التكامل = r | H₁: عدد = r+1",
             "يختبر فرضية محددة مقابل بديل محدد. أقل حدة من الـ Trace ويُوفّر دليلاً تكميلياً.",
             "أقل استخداماً من Trace. قد يختلف عن Trace — في هذه الحالة استخدم Trace كمرجع."),
        ]
        for name, hypothesis, method, note in coint_data:
            st.markdown(f"""
            <div class='assume-card'>
                <div class='assume-title'>📊 {name}</div>
                <div style='color:#1565c0; font-size:0.9em; margin-bottom:8px;'><strong>الفرضية:</strong> {hypothesis}</div>
                <div class='assume-body'>{method}</div>
                <div style='background:#e0f2f1; border-right:4px solid #00695c; padding:10px 14px; border-radius:8px; margin-top:8px; color:#004d40;'>📌 {note}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-yellow">
            <p>⚠️ <strong>نقطة حاسمة في GVAR:</strong> التكامل المشترك يُختبر على شعاع zᵢₜ = (x'ᵢₜ, x*'ᵢₜ)' — أي المتغيرات الداخلية والنجمية معاً. هذا يسمح باكتشاف علاقات طويلة الأجل بين الاقتصادات الداخلية والخارجية!</p>
        </div>

        <div class="info-box info-blue">
            <p>📊 <strong>ماذا يعني كل قرار؟</strong></p>
            <p>• rᵢ = 0: لا تكامل مشترك → نموذج الفروق الأولى VAR(Δ)<br>
            • 0 < rᵢ < kᵢ: تكامل مشترك جزئي → نموذج VECMX (الأكثر شيوعاً في GVAR)<br>
            • rᵢ = kᵢ: جميع المتغيرات I(0) → نموذج مستويات VAR</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with test_tabs[2]:
        st.markdown("""
        <div class="section-card section-card-orange">
            <div class="sec-title">🎯 اختبار الخارجية الضعيفة (Weak Exogeneity Test)</div>
            <div class="sec-subtitle">اختبار أساسي خاص بـ GVAR: هل يمكن معاملة x*ᵢₜ كمتغيرات خارجية؟</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-orange">
            <p>🔑 <strong>لماذا هذا الاختبار مهم جداً؟</strong></p>
            <p>إذا كانت x*ᵢₜ خارجية ضعيفة، فإن تقدير نموذج الدولة i بشكل منفصل (Conditional on x*) يعطي تقديرات فعّالة وكفؤة. إذا لم تكن كذلك → نموذج الدولة يحتاج لمعالجة خاصة.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>شرط الخارجية الضعيفة رياضياً:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\text{x}^*_{it} \text{ خارجية ضعيفة إذا:} \quad \gamma_i = 0 \text{ في معادلة:} \quad \Delta x^*_{it} = \gamma_i' \beta_i' z_{i,t-1} + \ldots")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:10px;'>
        📌 أي: معاملات تصحيح الخطأ (γᵢ) في معادلة x* يجب أن تكون = 0<br>
        📌 بمعنى: x* لا تستجيب لأي انحراف عن التوازن طويل الأجل المُقدَّر
        </div></div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-green">
            <p>✅ <strong>الإجراء العملي:</strong> اختبر F أو Chi² على أن معاملات التصحيح (γᵢ) = 0 في النموذج الهامشي لـ x*ᵢₜ.</p>
            <p>📌 <strong>النتيجة الشائعة:</strong> عادةً لا يُرفض هذا الاختبار للدول الصغيرة نسبياً حجمها في الاقتصاد العالمي — وهو ما يُبرر استخدام GVAR.</p>
            <p>📌 <strong>استثناء:</strong> الولايات المتحدة والصين كدول سائدة (Dominant Units) — تُعامَل معاملة خاصة كمتغيرات مشتركة عالمية.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with test_tabs[3]:
        st.markdown("""
        <div class="section-card section-card-purple">
            <div class="sec-title">📏 اختيار درجة الإبطاء الأمثل (Lag Order Selection)</div>
        """, unsafe_allow_html=True)

        lag_criteria = [
            ("AIC", "Akaike Information Criterion", "AIC = -2L/T + 2k/T", "يُفضّل النماذج الأكبر — مناسب عندما T صغير والتنبؤ أولوية."),
            ("BIC", "Bayesian Information Criterion", "BIC = -2L/T + k×log(T)/T", "أكثر تشدداً — يُفضّل النماذج الأصغر — مناسب عندما T كبير."),
            ("HQIC", "Hannan-Quinn", "HQIC = -2L/T + 2k×log(log(T))/T", "وسط بين AIC وBIC — جيد للعينات المتوسطة."),
            ("LR", "Likelihood Ratio Test", "LR = 2(L₁ - L₀) ~ χ²(q)", "اختبار مباشر: هل إضافة فجوة إضافية تُحسّن النموذج إحصائياً؟"),
        ]
        for name, full, formula, note in lag_criteria:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
                <div style='background:#6a1b9a; border-radius:12px; padding:18px; text-align:center; color:white; height:100%;'>
                    <div style='font-size:1.5em; font-weight:900;'>{name}</div>
                    <div style='font-size:0.8em; opacity:0.85; margin-top:4px;'>{full}</div>
                    <div style='margin-top:10px; background:rgba(255,255,255,0.15); border-radius:8px; padding:6px; font-size:0.82em; font-family:monospace;'>{formula}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""<div class='info-box info-purple'><p>{note}</p></div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-yellow">
            <p>💡 <strong>القاعدة العملية في GVAR:</strong> في أغلب الأبحاث، تُستخدم p = q = 1 أو 2 للبيانات الربعية، وp = q = 1 للبيانات السنوية. اختر الحد الذي تتفق عليه معظم المعايير، مع الحرص على أن T/(kᵢ + k*)² يبقى معقولاً.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with test_tabs[4]:
        st.markdown("""
        <div class="section-card section-card-pink">
            <div class="sec-title">📐 اختبارات مسبقة إضافية</div>
        """, unsafe_allow_html=True)
        other_pre = [
            ("🌍 اختبار التبعية المقطعية (Cross-Section Dependence)",
             "CD Test (Pesaran 2004)", "هل بواقي النموذج ذات اعتمادية مقطعية قوية؟ إذا نعم → العوامل المشتركة مهمة ويجب التعامل معها بعناية."),
            ("📊 اختبار التجانس المقطعي (Cross-Section Homogeneity)",
             "Pesaran-Yamagata Δ Test", "هل المعاملات متجانسة عبر الدول؟ GVAR يفترض عدم التجانس (Parameter Heterogeneity) — وهذه ميزة وليست مشكلة."),
            ("🔄 اختبار التوزيع الطبيعي للبواقي",
             "Jarque-Bera, Doornik-Hansen", "هل بواقي النموذج موزعة توزيعاً طبيعياً؟ الانحراف يؤثر على صحة اختبارات t وF والتكامل المشترك في العينات الصغيرة."),
        ]
        for title, test_name, desc in other_pre:
            st.markdown(f"""
            <div class='assume-card'>
                <div class='assume-title'>{title}</div>
                <div style='color:#ad1457; font-size:0.88em; font-style:italic; margin-bottom:6px;'>الاختبار: {test_name}</div>
                <div class='assume-body'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE NEW-D — GVAR MODEL VARIANTS
# ═══════════════════════════════════════════════════════
elif menu == "🌲  نماذج GVAR المختلفة":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🌲 أنواع ونماذج GVAR المختلفة</div>
        <div class="sec-subtitle">تطوّر GVAR ليشمل امتدادات متعددة تتناسب مع أسئلة بحثية مختلفة</div>
    </div>
    """, unsafe_allow_html=True)

    model_tabs = st.tabs([
        "📘 النموذج الأساسي",
        "🌐 GVAR مع متغيرات سائدة",
        "📊 GVAR المختلطة المقاطع",
        "🔀 GVAR الانتقالي",
        "⏳ GVAR ذات الأوزان المتغيرة",
        "🤖 GVAR البيزي",
    ])

    with model_tabs[0]:
        st.markdown("""
        <div class="section-card section-card-indigo">
            <div class="sec-title">📘 النموذج الأساسي — GVAR Standard (Pesaran et al. 2004)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-blue">
            <p>🏛️ <strong>الوصف:</strong> النموذج الأصلي الذي اقترحه Pesaran, Schuermann and Weiner (PSW) عام 2004. يشمل N دولة، كل دولة لها نموذج VARX خاص مع متغيرات نجمية مُحسوبة بأوزان ثابتة.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='math-container'><div class='math-label'>النموذج الأساسي:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"x_{it} = \sum_{\ell=1}^{p_i} \Phi_{i\ell}\, x_{i,t-\ell} + \Lambda_{i0}\, x^*_{it} + \sum_{\ell=1}^{q_i} \Lambda_{i\ell}\, x^*_{i,t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-green">
            <p>✅ <strong>المتغيرات النموذجية (DdPS 2007 — النموذج المرجعي):</strong></p>
            <p>• Domestic: GDP الحقيقي (y), التضخم (π), سعر الصرف الحقيقي (ep), سعر الفائدة القصير (rs), سعر الفائدة الطويل (rl), أسعار الأسهم (eq)</p>
            <p>• Star: y*, π*, ep*, rs*, eq*</p>
            <p>• Global: أسعار النفط (poil) — كمتغير مشترك</p>
        </div>
        <div class="info-box info-yellow">
            <p>📌 <strong>التطبيق الأبرز:</strong> DdPS (2007) — 33 دولة، 1979Q1–2003Q4، الفجوات: p=1, q=1 لمعظم الدول</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with model_tabs[1]:
        st.markdown("""
        <div class="section-card section-card-orange">
            <div class="sec-title">🌐 GVAR مع الوحدة السائدة (Dominant Unit GVAR)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-orange">
            <p>🏛️ <strong>الوصف:</strong> امتداد يُعامل الاقتصاد الأمريكي (أو الصيني) كـ "وحدة سائدة" (Dominant Unit) — أي أن متغيراته تؤثر في جميع الدول مباشرة ولا تتأثر بالمتوسطات المرجّحة بنفس الطريقة.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='math-container'><div class='math-label'>نموذج الدولة i مع المتغيرات السائدة ωₜ (المتغيرات الأمريكية):</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"x_{it} = \sum_\ell \Phi_{i\ell} x_{i,t-\ell} + \Lambda_{i0} x^*_{it} + \sum_\ell \Lambda_{i\ell} x^*_{i,t-\ell} + D_{i0}\omega_t + \sum_\ell D_{i\ell}\omega_{t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-green">
            <p>✅ <strong>متى تستخدم هذا النموذج؟</strong></p>
            <p>• عندما تهتم بدراسة تأثير صدمة أمريكية تحديداً على دول العالم<br>
            • عندما تريد فصل الأثر الأمريكي المباشر عن أثر التكتلات التجارية<br>
            • الدراسة: Chudik & Smith (2013) — "The GVAR Approach and the Dominance of the US Economy"</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with model_tabs[2]:
        st.markdown("""
        <div class="section-card section-card-teal">
            <div class="sec-title">📊 GVAR المختلطة المقاطع (Mixed Cross-Section GVAR)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-teal">
            <p>🏛️ <strong>الوصف:</strong> يجمع بين وحدات مقطعية مختلفة النوع في نفس النموذج — مثل دمج بيانات الدول مع بيانات البنوك أو الشركات.</p>
            <p>📌 <strong>مثال:</strong> Gross & Kok (2013) — 23 دولة + 41 بنكاً دولياً في نفس النموذج لدراسة العدوى المالية بين السيادات والبنوك.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-yellow">
            <p>⚙️ <strong>الفائدة البحثية:</strong></p>
            <p>• يُتيح ربط السلوك الاقتصادي الكلي (Macro) بالسلوك على مستوى الشركة أو البنك (Micro)<br>
            • يُمكّن من دراسة كيف تنتقل الأزمات من الاقتصاد الكلي إلى النظام المالي والعكس<br>
            • أكثر تطلباً للبيانات لكنه أغنى معلوماتياً</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with model_tabs[3]:
        st.markdown("""
        <div class="section-card section-card-pink">
            <div class="sec-title">🔀 GVAR الانتقالي (Regime-Switching GVAR)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-pink">
            <p>🏛️ <strong>الوصف:</strong> يُدمج منهجية GVAR مع نماذج التحوّل بين الأنظمة (Markov Switching) للتقاط عدم الخطية والتغيرات الهيكلية.</p>
            <p>📌 <strong>مثال:</strong> Binder & Gross (2013) — نموذج RS-GVAR يفوق دقته في التنبؤ على GVAR الخطي في التنبؤ بـ GDP والتضخم وأسعار الأسهم.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-yellow">
            <p>⚙️ <strong>متى يُفضَّل؟</strong></p>
            <p>• عندما تشمل الفترة الزمنية أزمات حادة (2008-09 مثلاً) تُغيّر ديناميكيات النظام<br>
            • عندما تشير اختبارات الاستقرار إلى كسور هيكلية متعددة<br>
            • عندما يُشير النظري الاقتصادي لسلوك مختلف في فترات الانتعاش والركود</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with model_tabs[4]:
        st.markdown("""
        <div class="section-card section-card-green">
            <div class="sec-title">⏳ GVAR بأوزان متغيرة عبر الزمن (Time-Varying Weights GVAR)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-green">
            <p>🏛️ <strong>الوصف:</strong> بدلاً من استخدام أوزان تجارية ثابتة، يُستخدم مصفوفة أوزان تتغير عبر الزمن لتعكس التحولات في أنماط التجارة العالمية.</p>
            <p>📌 <strong>مثال أبرز:</strong> Cesa-Bianchi et al. (2012) — استخدام أوزان متغيرة عبر الزمن لإظهار كيف أدى صعود الصين لتضاعف تأثير الصدمات الصينية على أمريكا اللاتينية ثلاثة أضعاف منذ منتصف التسعينيات.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-blue">
            <p>⚙️ <strong>الفائدة:</strong> يتقاطع مع دراسة التحولات الهيكلية في الاقتصاد العالمي. خاصة مهم لدراسة فترات ما قبل وبعد: انضمام دول لـ WTO، تأسيس منطقة اليورو، الأزمات المالية الكبرى.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with model_tabs[5]:
        st.markdown("""
        <div class="section-card section-card-purple">
            <div class="sec-title">🤖 GVAR البيزي (Bayesian GVAR — BGVAR)</div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-purple">
            <p>🏛️ <strong>الوصف:</strong> يُقدَّر نموذج الدولة الفردي بطريقة بيزية بدلاً من OLS/MLE. يُضيف قيوداً مسبقة (Priors) على المعاملات لتقليص التباين وتحسين التنبؤ.</p>
        </div>
        """, unsafe_allow_html=True)
        priors_list = [
            ("Minnesota Prior", "يُقلّص المعاملات نحو نموذج السير العشوائي — يُقلل التباين بشكل ملحوظ."),
            ("Stochastic Search Variable Selection (SSVS)", "يُحدد تلقائياً المتغيرات الأكثر أهمية — النتائج أكثر دقة خارج العينة."),
            ("Normal-Conjugate Prior", "يُعطي تحليلاً بيزياً كاملاً مع توزيع مشترك للمعاملات والتباين."),
            ("Ridge Shrinkage (Frequentist)", "مشابه للبيزي لكن بدون إطار احتمالي — يُحسن الدقة التنبؤية بشكل مقارب."),
        ]
        for name, desc in priors_list:
            st.markdown(f"""
            <div class='assume-card'>
                <div class='assume-title'>📊 {name}</div>
                <div class='assume-body'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box info-green">
            <p>✅ <strong>النتيجة:</strong> Feldkircher et al. (2014) وجدوا أن التقدير البيزي يُحسّن دقة التنبؤ لجميع أنواع القيود المسبقة مقارنة بـ OLS، وأن SSVS هو الأفضل تنبؤياً خارج العينة.</p>
        </div>
        """, unsafe_allow_html=True)

        # Comparison table
        st.markdown("""
        <table class="compare-table">
            <tr><th>نوع النموذج</th><th>الفائدة الرئيسية</th><th>متى تستخدمه؟</th><th>الورقة المرجعية</th></tr>
            <tr><td>GVAR Standard</td><td>النموذج الأساسي والأسهل تطبيقاً</td><td>دراسة الانتقال الدولي للصدمات</td><td>Pesaran et al. (2004)</td></tr>
            <tr><td>Dominant Unit</td><td>تمييز تأثير الاقتصاد المهيمن</td><td>عند وجود قوة اقتصادية سائدة واضحة</td><td>Chudik & Smith (2013)</td></tr>
            <tr><td>Mixed Cross-Section</td><td>ربط الكلي بالجزئي</td><td>دراسة المخاطر المالية متعددة الأبعاد</td><td>Gross & Kok (2013)</td></tr>
            <tr><td>Regime-Switching</td><td>التقاط عدم الخطية</td><td>عند وجود أزمات وكسور هيكلية</td><td>Binder & Gross (2013)</td></tr>
            <tr><td>Time-Varying Weights</td><td>التغيرات الهيكلية في التجارة</td><td>دراسة صعود الاقتصادات الناشئة</td><td>Cesa-Bianchi et al. (2012)</td></tr>
            <tr><td>Bayesian GVAR</td><td>تحسين دقة التنبؤ</td><td>عند T صغير أو N كبير جداً</td><td>Feldkircher et al. (2014)</td></tr>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 5 — MATHEMATICS IN DETAIL
# ═══════════════════════════════════════════════════════
elif menu == "📐  الرياضيات خطوة بخطوة":
    show_hero()

    tabs = st.tabs(["1️⃣ النموذج الكبير الأصلي", "2️⃣ معادلة VARX لكل دولة", "3️⃣ صيغة تصحيح الخطأ ECM", "4️⃣ دمج النماذج (GVAR)", "5️⃣ النموذج مع المتغيرات المشتركة"])

    with tabs[0]:
        st.markdown("""
        <div class="section-card">
            <div class="sec-title">1️⃣ نموذج VAR المُعزَّز بعوامل — البداية النظرية</div>
            <div class="sec-subtitle">نبدأ بـ DGP (Data Generating Process): النموذج الحقيقي الكامن الذي يُولّد البيانات</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>الجهاز المُولِّد للبيانات (DGP) — نموذج VAR(p) المُعزَّز:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\Phi(L, p)\, x_t = \Gamma_f(L, s_f)\, f_t + \Gamma_\omega(L, s_\omega)\, \omega_t + u_t")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:12px; line-height:2.3;'>
        📌 <strong>xₜ</strong>: شعاع (k × 1) يحوي جميع متغيرات جميع الدول في الزمن t<br>
        📌 <strong>k = Σkᵢ</strong>: مجموع عدد متغيرات كل الدول<br>
        📌 <strong>Φ(L,p)</strong>: متعدد حدود المصفوفة في عامل الإبطاء L، من الدرجة p<br>
        📌 <strong>fₜ</strong>: شعاع (mf × 1) عوامل مشتركة <strong>غير مرصودة (Unobserved Common Factors)</strong><br>
        📌 <strong>ωₜ</strong>: شعاع (mω × 1) عوامل مشتركة <strong>مرصودة (Observed Common Effects)</strong> — كأسعار النفط<br>
        📌 <strong>uₜ</strong>: شعاع الأخطاء المختزلة (Reduced Form Errors)
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-orange">
            <p>⚠️ <strong>المشكلة:</strong> هذا النموذج لا يمكن تقديره مباشرةً لأن عدد معاملاته يتناسب مع k² وهو ضخم جداً عندما N كبير — هنا تظهر قيمة GVAR!</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("""
        <div class="section-card section-card-green">
            <div class="sec-title">2️⃣ معادلة النموذج الفردي لكل دولة (VARX)</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>نموذج VARX للدولة i:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"x_{it} = \sum_{\ell=1}^{p_i} \Phi_{i\ell}\, x_{i,t-\ell} + \Lambda_{i0}\, x^*_{it} + \sum_{\ell=1}^{q_i} \Lambda_{i\ell}\, x^*_{i,t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>صيغة المصفوفة المُدمَجة — تعريف zᵢₜ:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"z_{it} = \begin{pmatrix} x_{it} \\ x^*_{it} \end{pmatrix}_{(k_i + k^*) \times 1}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"A_{i0}\, z_{it} = \sum_{\ell=1}^{p} A_{i\ell}\, z_{i,t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:10px; line-height:2.2;'>
        📌 <strong>Aᵢ₀ = [Ikᵢ , -Λᵢ₀]</strong>: مصفوفة المعاملات الآنية للدولة i<br>
        📌 <strong>Aᵢℓ = [Φᵢℓ , Λᵢℓ]</strong>: مصفوفة معاملات الفجوة ℓ<br>
        📌 <strong>p = max(pᵢ, qᵢ)</strong>: الحد الأقصى للفجوات
        </div></div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-green">
            <p>✅ <strong>الحجم صغير ومُسيطَر عليه:</strong> كلٌّ من kᵢ و k* صغيرَان عادةً (3 إلى 6 متغيرات)، مما يجعل التقدير ممكناً وكفئاً.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("""
        <div class="section-card section-card-teal">
            <div class="sec-title">3️⃣ صيغة تصحيح الخطأ (Error Correction — ECM)</div>
            <div class="sec-subtitle">هذه الصيغة تُمكّن من تمثيل التكامل المشترك (Cointegration) داخل النموذج</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>صيغة تصحيح الخطأ للدولة i:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\Delta x_{it} = \Lambda_{i0}\, \Delta x^*_{it} - \Pi_i\, z_{i,t-1} + \sum_{\ell=1}^{p-1} H_{i\ell}\, \Delta z_{i,t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:12px; line-height:2.3;'>
        📌 <strong>Δ</strong>: مُشغّل الفروق الأولى (First Difference Operator) أي Δxₜ = xₜ - xₜ₋₁<br>
        📌 <strong>Πᵢ = Aᵢ₀ - Σ Aᵢℓ</strong>: مصفوفة التصحيح — رتبتها rᵢ تُحدّد عدد علاقات التكامل المشترك<br>
        📌 <strong>rᵢ = rank(Πᵢ)</strong>: عدد الأشعة التكامل المشترك (Cointegrating Vectors)<br>
        📌 <strong>Hᵢℓ</strong>: مصفوفات الديناميكيات قصيرة الأجل
        </div></div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>تحليل مصفوفة التصحيح (Πᵢ):</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\Pi_i = \alpha_i \beta_i' \quad \text{حيث:} \begin{cases} \alpha_i: \text{ مصفوفة سرعة التعديل (Loading Matrix)} \\ \beta_i: \text{ مصفوفة الأشعة التكامل المشترك (Cointegrating Vectors)} \end{cases}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-teal">
            <p>🔗 <strong>ماذا يعني التكامل المشترك (Cointegration)؟</strong></p>
            <p>عندما تكون متغيرَان أو أكثر غير مستقرَّيْن بشكل منفرد (I(1))، لكنهما يتحرّكان معًا على المدى البعيد بحيث توجد تركيبة خطية مستقرة بينهما — هذه العلاقة طويلة الأجل هي التكامل المشترك.</p>
            <p><strong>مثال:</strong> الأسعار المحلية وسعر الصرف قد يتذبذبان ولكن نسبتهما تبقى ثابتة على المدى البعيد.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("""
        <div class="section-card section-card-orange">
            <div class="sec-title">4️⃣ تجميع النماذج في GVAR الكامل</div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>مصفوفة الربط (Link Matrix) لكل دولة i:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"W_i = \begin{pmatrix} E_i' \\ \tilde{W}_i' \end{pmatrix}_{(k_i + k^*) \times k}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"z_{it} = W_i x_t")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>بعد الاستبدال وتجميع جميع الدول N:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"G_0 = \begin{pmatrix} A_{10} W_1 \\ A_{20} W_2 \\ \vdots \\ A_{N0} W_N \end{pmatrix}, \quad G_\ell = \begin{pmatrix} A_{1\ell} W_1 \\ A_{2\ell} W_2 \\ \vdots \\ A_{N\ell} W_N \end{pmatrix}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>النموذج المُدمَج — شرط الرتبة الكاملة لـ G₀:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\underbrace{G_0}_{k\times k} x_t = \sum_{\ell=1}^p G_\ell\, x_{t-\ell} + \varepsilon_t")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\xRightarrow{\text{إذا } \text{rank}(G_0) = k} \quad x_t = \sum_{\ell=1}^p F_\ell\, x_{t-\ell} + G_0^{-1}\varepsilon_t")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"F_\ell = G_0^{-1} G_\ell, \quad \ell = 1, 2, \ldots, p")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-orange">
            <p>⚠️ <strong>شرط حاسم:</strong> مصفوفة G₀ يجب أن تكون ذات رتبة كاملة (Full Rank) حتى يكون النموذج محدَّداً ويمكن حلّه. إذا كانت ناقصة الرتبة، فإن النظام غير مكتمل ويحتاج إلى معادلات إضافية.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("""
        <div class="section-card section-card-purple">
            <div class="sec-title">5️⃣ النموذج مع المتغيرات المشتركة (Common Variables)</div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box info-purple">
            <p>بعض المتغيرات تُؤثّر على <strong>جميع الدول</strong> في وقتٍ واحد، كأسعار النفط العالمية أو الأزمات المالية الكبرى. هذه نُسمّيها <strong>متغيرات مهيمنة أو مشتركة</strong> (Dominant / Common Variables) ونُرمز إليها بـ <strong>ωₜ</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>النموذج الفردي مع المتغيرات المشتركة:</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"x_{it} = \sum_{\ell=1}^{p_i} \Phi_{i\ell}\, x_{i,t-\ell} + \Lambda_{i0}\, x^*_{it} + \sum_{\ell=1}^{q_i} \Lambda_{i\ell}\, x^*_{i,t-\ell} + \sum_{\ell=0}^{s_i} D_{i\ell}\, \omega_{t-\ell} + \varepsilon_{it}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>نموذج المتغيرات المشتركة (الهامشي):</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"\omega_t = \sum_{\ell=1}^{p_\omega} \Psi_\ell\, \omega_{t-\ell} + \sum_{\ell=1}^{q_\omega} \Theta_\ell\, x^*_{\omega,t-\ell} + \eta_t")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='math-container'><div class='math-label'>GVAR الكامل مع المتغيرات المشتركة (yₜ = [ωₜ', xₜ']'):</div>", unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"y_t = \begin{pmatrix} \omega_t \\ x_t \end{pmatrix}, \quad G_{y,0} y_t = \sum_{\ell=1}^p G_{y,\ell}\, y_{t-\ell} + \varepsilon_{yt}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
        st.latex(r"G_{y,0} = \begin{pmatrix} I_{m_\omega} & 0 \\ D_0 & G_0 \end{pmatrix} \quad \Rightarrow \quad \det(G_{y,0}) \neq 0 \iff \det(G_0) \neq 0")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 6 — ASSUMPTIONS & CONDITIONS
# ═══════════════════════════════════════════════════════
elif menu == "📋  الافتراضات والشروط":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">📋 الافتراضات والشروط الأساسية للنموذج</div>
        <div class="sec-subtitle">هذه الشروط ضرورية لصحة النموذج ونتائجه. سنشرح كل شرط بلغة بسيطة ثم بصيغته الرياضية</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Assumption 1
    st.markdown("""<div class="section-card section-card-green">
    <div class="sec-title">1️⃣ شرط الضعف الخارجي (Weak Exogeneity)</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-green">
        <p>📖 <strong>بالكلمات البسيطة:</strong> المتغيرات النجمية (x*ᵢₜ) لا يُعود عليها بأثر من المتغيرات الداخلية للدولة i عند تقدير النموذج الفردي. بمعنى أن الدولة i "صغيرة" بالنسبة للعالم فلا تؤثر فيه.</p>
        <p>📖 <strong>بالمعنى الإحصائي:</strong> معاملات التصحيح في المعادلة الهامشية لـ x* غير معنوية.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{Weak Exogeneity: } \quad \alpha^*_i = 0")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{أي: } x^*_{it} \text{ لا يتأثر بانحرافات التوازن طويل الأجل للدولة } i")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-yellow">
        <p>✅ <strong>ملاحظة:</strong> هذا الشرط <strong>قابل للاختبار</strong> تجريبياً ونادراً ما يُرفض عندما تكون الدولة صغيرة نسبياً والأوزان حبيبية (Granular).</p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Assumption 2
    st.markdown("""<div class="section-card section-card-orange">
    <div class="sec-title">2️⃣ شرط الحبيبية (Granularity Conditions)</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-orange">
        <p>📖 <strong>بالكلمات البسيطة:</strong> الأوزان المستخدمة في بناء المتغيرات النجمية يجب أن تكون "صغيرة ومُوزَّعة" — لا يُهيمن عليها وزن واحد ضخم. كمثال: لا تجعل وزن الاقتصاد الأمريكي 90% من الإجمالي.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\|\tilde{W}_i\|_\infty \leq \frac{K}{\sqrt{N}}, \quad \forall i")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\|\tilde{W}_{ij}\| \leq \frac{K}{\sqrt{N}}, \quad \forall i, j")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:8px;'>
    ⬅️ هذا يضمن أن المتغيرات النجمية تُقرّب العوامل المشتركة عندما N → ∞<br>
    ⬅️ K ثابت لا يعتمد على N أو i أو j
    </div></div>
    """, unsafe_allow_html=True)

    # Vizualise granularity
    np.random.seed(10)
    n_c = 20
    w_granular = np.random.dirichlet(np.ones(n_c))
    w_concentrated = np.zeros(n_c); w_concentrated[0] = 0.7; w_concentrated[1:] = 0.3/(n_c-1)
    fig_gran = make_subplots(1, 2, subplot_titles=("✅ أوزان حبيبية (جيدة)", "❌ أوزان متمركزة (سيئة)"))
    fig_gran.add_trace(go.Bar(x=list(range(n_c)), y=w_granular, marker_color='#1565c0', name='حبيبية'), row=1, col=1)
    fig_gran.add_trace(go.Bar(x=list(range(n_c)), y=w_concentrated, marker_color='#e53935', name='متمركزة'), row=1, col=2)
    fig_gran.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', showlegend=False,
                           title=dict(text="مثال على توزيع الأوزان", font=dict(family='Cairo', size=14), x=0.5),
                           height=280, margin=dict(t=70, b=20))
    st.plotly_chart(fig_gran, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Assumption 3
    st.markdown("""<div class="section-card section-card-teal">
    <div class="sec-title">3️⃣ شرط انعدام الارتباط المقطعي الضعيف (Weak Cross-Sectional Dependence)</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-teal">
        <p>📖 <strong>بالكلمات البسيطة:</strong> أخطاء النموذج يمكن أن تترابط بشكل محدود بين الدول، لكن لا يجب أن يكون هذا الترابط قوياً (من نوع العوامل المشتركة القوية) بعد تضمين المتغيرات النجمية في النموذج.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\|E(u_t u_t')\|_{\text{spectral}} = \|\Sigma_u\| < K < \infty")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{أي أن القيمة الذاتية العُظمى لـ } \Sigma_u \text{ تبقى محدودة عندما } N \to \infty")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Assumption 4 — Spectral radius
    st.markdown("""<div class="section-card section-card-purple">
    <div class="sec-title">4️⃣ شرط الاستقرار (Stability Condition)</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-purple">
        <p>📖 <strong>بالكلمات البسيطة:</strong> النموذج يجب أن يكون مستقراً — أي أن الصدمات تتلاشى مع الزمن ولا تتراكم إلى ما لا نهاية. هذا يضمن وجود حالة توازن.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\rho(\Phi_0) < 1 - \delta, \quad \text{لعدد صغير موجب } \delta > 0 \text{ لا يعتمد على } N")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\rho(\Phi_0) = |\lambda_{\max}(\Phi_0)| \quad \text{(نصف القطر الطيفي — Spectral Radius)}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:8px;'>
    ⬅️ هذا أقوى من شرط الاستقرار العادي لأنه يضمن محدودية التباين عندما N → ∞
    </div></div>
    """, unsafe_allow_html=True)

    # Visualization of eigenvalues
    np.random.seed(42)
    n_eig = 30
    eigs_stable = np.random.uniform(0, 0.85, n_eig) * np.exp(1j * np.random.uniform(0, 2*np.pi, n_eig))
    eigs_unstable = np.random.uniform(0, 1.1, n_eig//2) * np.exp(1j * np.random.uniform(0, 2*np.pi, n_eig//2))

    theta = np.linspace(0, 2*np.pi, 100)
    fig_eig = make_subplots(1, 2, subplot_titles=("✅ GVAR مستقر: قيم ذاتية داخل الدائرة", "❌ GVAR غير مستقر"))
    for fig_data, row_col, eigs, clr in [(fig_eig, (1,1), eigs_stable, '#1565c0'), (fig_eig, (1,2), eigs_unstable, '#e53935')]:
        fig_eig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode='lines',
                                     line=dict(color='#f9a825', width=2, dash='dash'), name='دائرة الوحدة'), row=row_col[0], col=row_col[1])
        fig_eig.add_trace(go.Scatter(x=eigs.real, y=eigs.imag, mode='markers',
                                     marker=dict(color=clr, size=10, symbol='circle-open', line=dict(width=2, color=clr)),
                                     name='القيم الذاتية'), row=row_col[0], col=row_col[1])
    fig_eig.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', showlegend=False, height=320,
                          title=dict(text="القيم الذاتية لمصفوفة GVAR — شرط الاستقرار",
                                     font=dict(family='Cairo', size=14), x=0.5), margin=dict(t=70))
    for row, col in [(1,1),(1,2)]:
        fig_eig.update_xaxes(scaleanchor=f"y{'' if row==1 and col==1 else str(row+col-1)}", row=row, col=col)
    st.plotly_chart(fig_eig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Assumption 5
    st.markdown("""<div class="section-card section-card-pink">
    <div class="sec-title">5️⃣ شرط رتبة G₀ الكاملة (Full Rank Condition)</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-pink">
        <p>📖 <strong>بالكلمات البسيطة:</strong> مصفوفة المعاملات الآنية G₀ يجب أن تكون قابلة للعكس (Invertible) حتى يكون النموذج محدَّداً بشكل وحيد. إذا كانت ناقصة الرتبة، النموذج لا يُعطي حلاً وحيداً.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{rank}(G_0) = k \quad \Longleftrightarrow \quad \det(G_0) \neq 0")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{إذا } \text{rank}(G_0) = k - m \text{ (نقصان) } \Rightarrow \text{نحتاج إلى إضافة } m \text{ معادلات إضافية}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 7 — IMPULSE RESPONSE ANALYSIS
# ═══════════════════════════════════════════════════════
elif menu == "💥  تحليل الصدمات (IRF)":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">💥 تحليل دوال الاستجابة للصدمات (Impulse Response Functions - IRF)</div>
        <div class="sec-subtitle">الأداة الرئيسية لتفسير GVAR: كيف تنتشر الصدمة في الاقتصاد العالمي؟</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-blue">
        <p>🎯 <strong>السؤال الجوهري:</strong> إذا حدثت صدمة فجائية في الاقتصاد الأمريكي (مثلاً رفع الفائدة)، كيف يتأثر الناتج المحلي في الجزائر؟ وبعد كم ربع سنوي تصل الذروة؟ ومتى يعود الاقتصاد لمساره الطبيعي؟</p>
        <p>🛠️ <strong>الإجابة:</strong> دوال الاستجابة للصدمات (IRF) توضح هذا كله رياضياً وبيانياً.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # GIRF Section
    st.markdown("""
    <div class="section-card section-card-teal">
        <div class="sec-title">🌟 دوال الاستجابة التعميمية (Generalized IRF - GIRF)</div>
        <div class="sec-subtitle">هذا النوع هو الأكثر استخدامًا في GVAR لأنه لا يتطلب تحديد ترتيب الصدمات</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>شعاع GIRF للصدمة في المتغير j عند الأفق h:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"g_{\varepsilon_j}(h) = E\!\left[x_{t+h}\,\big|\,\varepsilon_{jt} = \sqrt{\sigma_{jj}},\, \mathcal{I}_{t-1}\right] - E\!\left[x_{t+h}\,\big|\,\mathcal{I}_{t-1}\right]")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"= \frac{R_h\, G_0^{-1}\, e_j}{\sqrt{e_j'\Sigma\, e_j}}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:10px; line-height:2.3;'>
    📌 <strong>Rh</strong>: مصفوفة معاملات الاستجابة عند الأفق h، تُحسب تكراراً:<br>
    &nbsp;&nbsp;&nbsp;&nbsp; R₀ = Iₖ , وRₕ = Σ Fℓ Rₕ₋ℓ<br>
    📌 <strong>eⱼ</strong>: شعاع الاختيار (Selection Vector) يُحدّد المتغير j المُصدوم<br>
    📌 <strong>√σⱼⱼ</strong>: حجم الصدمة = انحراف معياري واحد لـ εⱼ<br>
    📌 <strong>Σ</strong>: مصفوفة تباين-تغاير الأخطاء
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Structural IRF
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">🔩 دوال الاستجابة الهيكلية (Structural IRF)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-purple">
        <p>📖 تتطلب تحديد مصفوفة التحويل <strong>P</strong> (Identification Matrix) بحيث PP' = Σ. وهذا يتطلب فرض قيود نظرية كافية.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'><div class='math-label'>دالة الاستجابة الهيكلية للصدمة j:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"g_{v_j}(h) = \frac{R_h\, G_0^{-1}\, P\, e_j}{\sqrt{e_j'\, e_j}}, \quad \text{حيث } v_t = P^{-1}\varepsilon_t")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"E(v_t v_t') = I_k \quad \Rightarrow \quad \Sigma = PP'")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:8px;'>
    ⬅️ تُحدَّد P بـ k(k-1)/2 قيداً إضافياً — هذا العدد ضخم في نماذج GVAR ذات الأبعاد الكبيرة
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive IRF simulation
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">📊 محاكاة تفاعلية لـ IRF</div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        shock_size = st.slider("حجم الصدمة (معياري)", 0.5, 3.0, 1.0, 0.1)
    with c2:
        persistence = st.slider("معامل الاستمرارية (ρ)", 0.1, 0.99, 0.7, 0.01)
    with c3:
        spillover = st.slider("معامل الانتقال (β)", 0.0, 0.5, 0.2, 0.05)

    horizons = np.arange(0, 21)
    irf_direct    = shock_size * persistence**horizons
    irf_neighbor  = shock_size * spillover * persistence**(horizons) * (1 - np.exp(-0.5*horizons))
    irf_distant   = shock_size * spillover * 0.5 * persistence**(horizons) * (1 - np.exp(-0.8*horizons))
    irf_global    = (irf_direct + irf_neighbor + irf_distant) / 3

    fig_irf = go.Figure()
    traces_irf = [
        ("الدولة المُصدوم اقتصادها", irf_direct, '#e53935', 'solid'),
        ("دولة مجاورة (ترابط قوي)", irf_neighbor, '#1565c0', 'solid'),
        ("دولة بعيدة (ترابط ضعيف)", irf_distant, '#2e7d32', 'dash'),
        ("المتوسط العالمي", irf_global, '#f9a825', 'dot'),
    ]
    for name, y, clr, dash in traces_irf:
        fig_irf.add_trace(go.Scatter(x=horizons, y=y, name=name, mode='lines+markers',
                                     line=dict(color=clr, width=2.5, dash=dash),
                                     marker=dict(size=6, color=clr)))
    fig_irf.add_hline(y=0, line_dash="dash", line_color="#90a4ae", line_width=1)
    fig_irf.update_layout(
        title=dict(text="📈 دوال الاستجابة للصدمات — Impulse Response Functions",
                   font=dict(family='Cairo', size=15), x=0.5),
        xaxis_title="الأفق الزمني (أرباع السنة)",
        yaxis_title="الاستجابة التراكمية",
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        font=dict(family='Cairo'),
        legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='#e0e0e0', borderwidth=1),
        height=420
    )
    st.plotly_chart(fig_irf, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # FEVD
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">📊 تحليل تباين خطأ التنبؤ (FEVD)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-orange">
        <p>📖 <strong>السؤال:</strong> ما نسبة تباين متغير معين يُفسّرها كلٌّ من الصدمات المختلفة؟ هذا ما يكشفه تحليل FEVD (Forecast Error Variance Decomposition).</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'><div class='math-label'>نسبة إسهام الصدمة j في تباين خطأ التنبؤ للمتغير i عند الأفق h:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{GFEVD}(x_{it},\, \varepsilon_{jt},\, h) = \frac{\sigma_{jj}^{-1}\,\sum_{\ell=0}^{h}\!\left(e_i' F^h G_0^{-1} e_j\right)^2}{\sum_{\ell=0}^{h} e_i' F^\ell G_0^{-1} \Sigma G_0^{-1'} F^{\ell'} e_i}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Pie chart of FEVD
    np.random.seed(7)
    sources = ["صدمة أمريكية", "صدمة أوروبية", "صدمة صينية", "صدمة نفطية", "صدمة محلية", "أخرى"]
    sizes = [30, 20, 18, 15, 10, 7]
    clrs_fevd = ['#1565c0','#2e7d32','#e53935','#f9a825','#6a1b9a','#00695c']
    fig_fevd = go.Figure(go.Pie(labels=sources, values=sizes, hole=0.45,
                                 marker=dict(colors=clrs_fevd, line=dict(color='white', width=2)),
                                 textfont=dict(family='Cairo', size=12)))
    fig_fevd.update_layout(
        title=dict(text="مثال: مصادر تباين الناتج المحلي الجزائري",
                   font=dict(family='Cairo', size=14), x=0.5),
        paper_bgcolor='#f8f9ff', height=380,
        legend=dict(font=dict(family='Cairo'))
    )
    st.plotly_chart(fig_fevd, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 8 — FORECASTING
# ═══════════════════════════════════════════════════════
elif menu == "🔮  التنبؤ بالنموذج":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🔮 التنبؤ بنموذج GVAR</div>
        <div class="sec-subtitle">GVAR ليس فقط أداة تحليل — بل أيضًا آلة تنبؤ قوية للمتغيرات الاقتصادية الكلية</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>التنبؤ القياسي h خطوات للأمام:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"E\!\left[x_{t_0+h}\,\big|\,\mathcal{I}_{t_0}\right] = \sum_{\ell=1}^{p} F_\ell\, E\!\left[x_{t_0+h-\ell}\,\big|\,\mathcal{I}_{t_0}\right]")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{مع الشرط الابتدائي: } E\!\left[x_{t_0+h-\ell}\,\big|\,\mathcal{I}_{t_0}\right] = x_{t_0+h-\ell} \text{ لـ } h-\ell \leq 0")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Forecast types
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="section-card section-card-green">
            <div class="sec-title">📡 التنبؤ بمعلومة متاحة (Conditional Forecast)</div>
            <div class="info-box info-green">
                <p>نُشرط التنبؤ على معلومة مستقبلية معلومة جزئياً — مثلاً نعرف قيمة الناتج الأمريكي ولكن لا نعرف الأوروبي.</p>
                <p>مثال: "إذا ارتفع سعر النفط إلى 100$، ما هو متوقع للتضخم؟"</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="section-card section-card-orange">
            <div class="sec-title">📊 التنبؤ بمعلومة غير مكتملة (Nowcasting)</div>
            <div class="info-box info-orange">
                <p>نستخدم البيانات المتاحة (مثل مؤشرات مديري المشتريات PMI) لتقدير قيمة الربع الحالي قبل صدور البيانات الرسمية.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Forecast combination
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">🧩 تحسين التنبؤ: الجمع بين النماذج والنوافذ</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-purple">
        <p>🔑 <strong>اكتشاف Pesaran et al. (2009a):</strong> البسيط يتفوق على المعقد! الجمع بين:</p>
        <p>• <strong>AveM</strong>: متوسط عبر مواصفات مختلفة للنموذج</p>
        <p>• <strong>AveW</strong>: متوسط عبر نوافذ تقدير مختلفة</p>
        <p>• <strong>AveAve</strong>: متوسط الاثنين معًا ← الأفضل!</p>
    </div>
    """, unsafe_allow_html=True)

    # Simulation
    np.random.seed(42)
    t_train = np.arange(0, 40)
    t_fore  = np.arange(39, 52)
    true_path = 100 + 0.5*t_train + 3*np.sin(t_train/5) + np.random.randn(40)*2
    actual_fore = 100 + 0.5*t_fore + 3*np.sin(t_fore/5) + np.random.randn(len(t_fore))*2

    last_val = true_path[-1]
    gvar_fore  = last_val + np.cumsum(0.45 + np.random.randn(len(t_fore))*0.3)
    avg_fore   = last_val + np.cumsum(0.5 + np.random.randn(len(t_fore))*0.2)
    ar_fore    = last_val + np.cumsum(0.3 + np.random.randn(len(t_fore))*0.5)
    ci_upper   = avg_fore + np.arange(len(t_fore))*0.5
    ci_lower   = avg_fore - np.arange(len(t_fore))*0.5

    fig_fore = go.Figure()
    fig_fore.add_trace(go.Scatter(x=t_train, y=true_path, name='البيانات الفعلية',
                                  line=dict(color='#263238', width=2.5), mode='lines'))
    fig_fore.add_trace(go.Scatter(x=t_fore, y=actual_fore, name='المستقبل الفعلي',
                                  line=dict(color='#263238', width=2.5, dash='dash'), mode='lines'))
    fig_fore.add_trace(go.Scatter(x=list(t_fore)+list(t_fore[::-1]),
                                  y=list(ci_upper)+list(ci_lower[::-1]),
                                  fill='toself', fillcolor='rgba(21,101,192,0.12)',
                                  line=dict(color='rgba(21,101,192,0)'), name='فترة ثقة 95%'))
    fig_fore.add_trace(go.Scatter(x=t_fore, y=avg_fore, name='GVAR — AveAve (الأفضل)',
                                  line=dict(color='#1565c0', width=3), mode='lines+markers', marker=dict(size=6)))
    fig_fore.add_trace(go.Scatter(x=t_fore, y=gvar_fore, name='GVAR قياسي',
                                  line=dict(color='#2e7d32', width=2, dash='dot'), mode='lines'))
    fig_fore.add_trace(go.Scatter(x=t_fore, y=ar_fore, name='AR نموذج المرجع',
                                  line=dict(color='#e53935', width=2, dash='dash'), mode='lines'))
    fig_fore.add_vline(x=39, line_dash="dash", line_color="#f9a825",
                       annotation_text="  بداية التنبؤ", annotation_font_color="#f9a825", line_width=2)
    fig_fore.update_layout(
        title=dict(text="🔮 مقارنة التنبؤات: GVAR مقابل النماذج البديلة",
                   font=dict(family='Cairo', size=15), x=0.5),
        xaxis_title="الزمن (أرباع السنة)",
        yaxis_title="قيمة المتغير",
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff',
        font=dict(family='Cairo'),
        legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='#e0e0e0'),
        height=430
    )
    st.plotly_chart(fig_fore, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Structural breaks
    st.markdown("""
    <div class="section-card section-card-indigo">
        <div class="sec-title">⚡ تحديات التنبؤ العالمي</div>
        <table class="compare-table">
            <tr><th>التحدي</th><th>السبب</th><th>الحل المقترح في GVAR</th></tr>
            <tr><td>التغيرات الهيكلية (Structural Breaks)</td><td>حروب، أزمات، تغيرات سياسية</td><td>متوسط نوافذ تقدير متغيرة AveW</td></tr>
            <tr><td>عدم اليقين النموذجي (Model Uncertainty)</td><td>لا نعرف المواصفة الصحيحة</td><td>متوسط نماذج متعددة AveM</td></tr>
            <tr><td>بيانات غير مكتملة (Unbalanced Data)</td><td>تصدر البيانات في تواريخ مختلفة</td><td>التنبؤ المشروط بالمعلومة المتاحة</td></tr>
            <tr><td>مصفوفة التباين الضخمة</td><td>k×k كبيرة جداً</td><td>مُقدّرات Shrinkage كـ Ridge/Lasso</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 9 — LONG-RUN ANALYSIS
# ═══════════════════════════════════════════════════════
elif menu == "📊  العلاقات طويلة الأجل":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">📊 التكامل المشترك والعلاقات طويلة الأجل</div>
        <div class="sec-subtitle">GVAR يُمكّن من دراسة علاقات الاتزان طويلة الأجل بين الاقتصادات العالمية</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Cointegration
    st.markdown("""
    <div class="section-card section-card-teal">
        <div class="sec-title">🔗 مفهوم التكامل المشترك (Cointegration)</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-teal">
        <p>🏄 <strong>مثال يومي:</strong> تخيّل سكيّراً يمشي مع كلبه. السكير يسير بشكل عشوائي والكلب كذلك، لكنهما مربوطَان بحبل — فمهما تشعّبا فإن المسافة بينهما محدودة. هذا هو التكامل المشترك: متغيّران I(1) لكن فرقهما I(0).</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='math-container'><div class='math-label'>شرط التكامل المشترك بين متغيرات الدولة i:</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"r_i = \text{rank}(\Pi_i) \leq k_i")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\Pi_i = \alpha_i \beta_i', \quad z_{it} \sim I(1) \text{ لكن } \beta_i' z_{it} \sim I(0)")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\text{العدد الكلي لعلاقات التكامل في GVAR: } r \leq \sum_{i=1}^{N} r_i")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Simulate cointegration
    np.random.seed(123)
    T = 100
    shocks = np.cumsum(np.random.randn(T))
    x1 = shocks + np.random.randn(T) * 0.3
    x2 = 1.5 * shocks + 0.8 + np.random.randn(T) * 0.3
    coint_relation = x1 - (x2 - 0.8) / 1.5

    fig_coint = make_subplots(1, 2,
        subplot_titles=("المتغيران المتكاملان: x₁ و x₂", "علاقة التكامل المشترك β'z ≈ I(0)"))
    fig_coint.add_trace(go.Scatter(y=x1, name='x₁', line=dict(color='#1565c0', width=2)), row=1, col=1)
    fig_coint.add_trace(go.Scatter(y=x2, name='x₂', line=dict(color='#e53935', width=2)), row=1, col=1)
    fig_coint.add_trace(go.Scatter(y=coint_relation, name='β\'z', line=dict(color='#2e7d32', width=2.5),
                                   fill='tozeroy', fillcolor='rgba(46,125,50,0.1)'), row=1, col=2)
    fig_coint.add_hline(y=0, line_dash="dash", line_color='#f9a825', row=1, col=2)
    fig_coint.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', height=350,
                            font=dict(family='Cairo'),
                            title=dict(text="توضيح التكامل المشترك", font=dict(family='Cairo', size=14), x=0.5))
    st.plotly_chart(fig_coint, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Tests
    st.markdown("""
    <div class="section-card section-card-purple">
        <div class="sec-title">🧪 اختبارات رتبة التكامل المشترك</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <table class="compare-table">
        <tr><th>الاختبار</th><th>المسمى الإنجليزي</th><th>الفرضية الصفرية</th><th>الأداء</th></tr>
        <tr><td>اختبار الأثر</td><td>Johansen Trace Test</td><td>rᵢ = r₀ ضد rᵢ > r₀</td><td>✅ الأفضل أداءً في العينات الصغيرة</td></tr>
        <tr><td>اختبار القيمة الذاتية العُظمى</td><td>Max Eigenvalue Test</td><td>rᵢ = r₀ ضد rᵢ = r₀+1</td><td>⚠️ أقل قوةً مع الأخطاء غير الطبيعية</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Persistence Profiles
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">📐 ملفات الاستمرارية (Persistence Profiles - PP)</div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box info-green">
        <p>📖 ملفات الاستمرارية توضح <strong>سرعة التقارب</strong> نحو علاقات التوازن طويلة الأجل بعد صدمة عالمية. كلما انحدر المنحنى بشكل أسرع نحو الصفر، كلما كان التعديل أسرع.</p>
    </div>
    """, unsafe_allow_html=True)

    h = np.arange(0, 25)
    pp_fast   = np.exp(-0.5*h)
    pp_medium = np.exp(-0.2*h)
    pp_slow   = np.exp(-0.08*h)
    fig_pp = go.Figure()
    fig_pp.add_trace(go.Scatter(x=h, y=pp_fast,   name='تعديل سريع (نصف عمر ~2 أرباع)', line=dict(color='#2e7d32', width=2.5)))
    fig_pp.add_trace(go.Scatter(x=h, y=pp_medium, name='تعديل متوسط (نصف عمر ~5 أرباع)', line=dict(color='#1565c0', width=2.5)))
    fig_pp.add_trace(go.Scatter(x=h, y=pp_slow,   name='تعديل بطيء (نصف عمر ~12 ربع)', line=dict(color='#e53935', width=2.5)))
    fig_pp.add_hline(y=0, line_dash='dash', line_color='#90a4ae')
    fig_pp.update_layout(
        title=dict(text="ملفات الاستمرارية: سرعة التعديل نحو التوازن", font=dict(family='Cairo', size=14), x=0.5),
        xaxis_title="الأفق (أرباع)", yaxis_title="الانحراف عن التوازن",
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', font=dict(family='Cairo'), height=360
    )
    st.plotly_chart(fig_pp, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Permanent/Transitory
    st.markdown("""
    <div class="section-card section-card-orange">
        <div class="sec-title">🔄 تحليل المكوّنَين: الدائم والزائل</div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='math-container'><div class='math-label'>تعريف المكوّن الدائم (Permanent Component):</div>", unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"x^P_t = \lim_{h\to\infty} E_t(x_{t+h})")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="direction:ltr; text-align:center;">', unsafe_allow_html=True)
    st.latex(r"\tilde{x}_t = x_t - x^P_t \quad \text{(المكوّن الزائل — Transitory Component)}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:right; color:#546e7a; font-size:0.93em; margin-top:8px;'>
    ⬅️ يُحسَب هذا من GVAR باستخدام تحليل Beveridge-Nelson<br>
    ⬅️ x_t^P يمتلك خاصية المارتينجال: Eₜ(x_{t+1}^P) = x_t^P<br>
    ⬅️ هذا أفضل من مرشّح Hodrick-Prescott (HP) لأنه يراعي التأثيرات العالمية
    </div></div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 10 — APPLICATIONS
# ═══════════════════════════════════════════════════════
elif menu == "🌍  التطبيقات العملية":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🌍 التطبيقات العملية لنموذج GVAR</div>
        <div class="sec-subtitle">منذ 2004 تجاوزت التطبيقات 100+ ورقة بحثية في مختلف مجالات الاقتصاد الكلي والمالي</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Applications categories
    apps = [
        ("🏦", "تحليل مخاطر الائتمان", "Credit Risk Analysis", "الاستخدام الأصلي لـ GVAR: تقييم الخسائر المحتملة في محافظ القروض البنكية في ظل صدمات عالمية متعددة.", "#1565c0", "section-card"),
        ("💸", "التضخم العالمي", "Global Inflation", "دراسة كيف تنتشر صدمات أسعار النفط والغذاء في معدلات التضخم عبر دول العالم المتقدم والنامي.", "#2e7d32", "section-card section-card-green"),
        ("📉", "الاختلالات التجارية", "Global Imbalances", "تحليل عجز وفائض الميزان التجاري وكيف تؤثر صدمات الطلب والأسعار النسبية على تدفقات التجارة.", "#e65100", "section-card section-card-orange"),
        ("🏘️", "أسواق الإسكان", "Housing Markets", "دراسة الانتقال العابر للحدود لصدمات أسواق الإسكان بين الدول الأوروبية ومناطق الولايات المتحدة.", "#00695c", "section-card section-card-teal"),
        ("🇨🇳", "صعود الاقتصاد الصيني", "China's Rise", "قياس الأثر المتزايد للصدمات الصينية على الاقتصادات اللاتينية والإفريقية والآسيوية.", "#6a1b9a", "section-card section-card-purple"),
        ("💰", "السياسة المالية", "Fiscal Policy", "تحليل المضاعفات المالية عبر الحدود وكيف تختلف بحسب درجة الانفتاح ومستوى الديون.", "#ad1457", "section-card section-card-pink"),
        ("🛢️", "أسواق السلع", "Commodity Markets", "تحليل تأثير عرض وطلب النفط على الأسعار العالمية وأسعار الصرف الحقيقية لمختلف الدول.", "#0288d1", "section-card section-card-indigo"),
        ("⚠️", "المخاطر النظامية", "Systemic Risk", "قياس العدوى المالية بين البنوك والحكومات وتحديد آليات الانتقال خلال الأزمات الكبرى.", "#e65100", "section-card section-card-orange"),
    ]

    for i in range(0, len(apps), 2):
        c1, c2 = st.columns(2)
        for col, (icon, title_ar, title_en, desc, clr, cls) in zip([c1,c2], apps[i:i+2]):
            with col:
                st.markdown(f"""
                <div class="{cls}">
                    <div style='display:flex; align-items:center; gap:12px; margin-bottom:14px;'>
                        <div style='font-size:2.2em;'>{icon}</div>
                        <div>
                            <div class='sec-title' style='margin:0; font-size:1.2em;'>{title_ar}</div>
                            <div style='color:#90a4ae; font-size:0.88em; font-style:italic;'>{title_en}</div>
                        </div>
                    </div>
                    <p style='color:#546e7a; line-height:1.9; margin:0; font-size:0.96em;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    # Key findings visualization
    st.markdown("""
    <div class="section-card section-card-green">
        <div class="sec-title">🔍 نتائج رئيسية من التطبيقات</div>
    """, unsafe_allow_html=True)

    findings = {
        "الدول": ["USA", "EU", "China", "Japan", "Brazil", "Algeria", "India", "UK"],
        "تأثير صدمة نفطية +10%": [0.3, -0.4, -0.5, -0.8, 0.6, 1.2, -0.6, -0.2],
        "تأثير صدمة أمريكية +1%": [1.0, 0.5, 0.3, 0.4, 0.45, 0.25, 0.2, 0.55],
    }
    df_findings = pd.DataFrame(findings)

    fig_bar = make_subplots(1, 2, subplot_titles=("تأثير صدمة نفطية (+10%) على الناتج %",
                                                   "تأثير صدمة أمريكية (+1%) على الناتج %"))
    colors_bar = ['#2e7d32' if x > 0 else '#e53935' for x in findings["تأثير صدمة نفطية +10%"]]
    fig_bar.add_trace(go.Bar(x=findings["الدول"], y=findings["تأثير صدمة نفطية +10%"],
                             marker_color=colors_bar, name="نفطية"), row=1, col=1)
    fig_bar.add_trace(go.Bar(x=findings["الدول"], y=findings["تأثير صدمة أمريكية +1%"],
                             marker_color='#1565c0', name="أمريكية"), row=1, col=2)
    fig_bar.add_hline(y=0, line_dash='dash', line_color='#90a4ae', row=1, col=1)
    fig_bar.add_hline(y=0, line_dash='dash', line_color='#90a4ae', row=1, col=2)
    fig_bar.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', height=380,
                          font=dict(family='Cairo'), showlegend=False,
                          title=dict(text="أمثلة على نتائج GVAR من الأدبيات", font=dict(family='Cairo', size=14), x=0.5))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 11 — SPECIFICATION TESTS
# ═══════════════════════════════════════════════════════
elif menu == "🧪  اختبارات التشخيص":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">🧪 اختبارات التشخيص والمصداقية (Specification Tests)</div>
        <div class="sec-subtitle">قبل الثقة بنتائج GVAR، يجب إجراء مجموعة من الاختبارات للتحقق من صحة الافتراضات</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    tests = [
        ("1", "اختبار الضعف الخارجي", "Weak Exogeneity Test",
         "نختبر هل المتغيرات النجمية (x*) ضعيفة الخارجية فعلاً، أي هل معاملات التصحيح في معادلاتها الهامشية معدومة.",
         "نستخدم اختبار F أو Wald على معاملات التصحيح. عدم الرفض → الافتراض صالح.", "#1565c0", "info-blue"),
        ("2", "اختبار الاستقرار الهيكلي", "Structural Stability Tests",
         "نختبر هل معاملات النموذج ثابتة عبر الزمن أم أن هناك تغيرات هيكلية (كالأزمات أو تغير السياسات).",
         "اختبارات CUSUM، Nyblom، Quandt-Andrews، Hansen. الرفض يشير إلى تغيّر هيكلي.", "#2e7d32", "info-green"),
        ("3", "اختبار رتبة التكامل", "Cointegration Rank Tests",
         "تحديد عدد علاقات التكامل المشترك rᵢ في كل نموذج دولة بدقة، لأن الخطأ في ذلك يُفسد الاستقرار.",
         "اختبار Johansen Trace و Max-Eigenvalue بقيم حرجة محاكاة Bootstrap.", "#e65100", "info-orange"),
        ("4", "اختبار الارتباط الذاتي في البواقي", "Serial Correlation Tests",
         "التحقق من أن بواقي النموذج لا تعاني من ارتباط ذاتي قد يُقلّل من كفاءة التقدير.",
         "اختبار Portmanteau وLjung-Box. الرفض يعني زيادة عدد الفجوات في النموذج.", "#6a1b9a", "info-purple"),
        ("5", "اختبار التجانس (تجانس التباين)", "Heteroskedasticity Tests",
         "التحقق من ثبات تباين الأخطاء عبر الزمن. التباين المتغير يؤثر على دقة فترات الثقة للـ IRF.",
         "اختبارات ARCH وWhite. يمكن معالجته بنسخة GVAR ذات تباين متغير.", "#00695c", "info-teal"),
        ("6", "اختبار التكيّف (Robustness Checks)", "Robustness Checks",
         "اختبار حساسية النتائج لتغيير الافتراضات: الأوزان، الفجوات، رتبة التكامل، حجم العينة.",
         "إذا بقيت النتائج الجوهرية ثابتة رغم التغييرات ← دليل على متانة النموذج.", "#ad1457", "info-pink"),
    ]

    for num, name_ar, name_en, desc, result, clr, box_cls in tests:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style='background:{clr}; border-radius:14px; padding:20px; text-align:center; color:white; height:100%;'>
                <div style='font-size:2em; font-weight:900;'>{num}</div>
                <div style='font-size:1.0em; font-weight:700; margin-top:8px;'>{name_ar}</div>
                <div style='font-size:0.83em; opacity:0.85; font-style:italic; margin-top:4px;'>{name_en}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='section-card' style='margin:0; border-top-color:{clr};'>
                <p style='color:#37474f; line-height:1.9; margin-bottom:10px;'>{desc}</p>
                <div class='info-box {box_cls}'>
                    <p><strong>📊 الإجراء:</strong> {result}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # CUSUM illustration
    st.markdown("""
    <div class="section-card section-card-teal">
        <div class="sec-title">📈 مثال توضيحي: اختبار CUSUM للاستقرار</div>
    """, unsafe_allow_html=True)

    np.random.seed(33)
    T_cusum = 80
    cusum_stable = np.cumsum(np.random.randn(T_cusum) * 0.4)
    cusum_break  = np.concatenate([np.cumsum(np.random.randn(40)*0.4),
                                   np.cumsum(np.random.randn(40)*0.4 + 0.6) + cusum_stable[39]])
    upper_band = np.linspace(1.36*np.sqrt(T_cusum)*0.1, 1.36*np.sqrt(T_cusum)*0.5, T_cusum)
    lower_band = -upper_band

    fig_cusum = make_subplots(1, 2, subplot_titles=("✅ معاملات مستقرة", "❌ تغيّر هيكلي عند الربع 40"))
    for col_idx, (cusum_data, title) in enumerate([(cusum_stable, "مستقر"), (cusum_break, "كسر")], 1):
        t = list(range(T_cusum))
        clr_line = '#1565c0' if col_idx==1 else '#e53935'
        fig_cusum.add_trace(go.Scatter(x=t, y=upper_band, mode='lines', line=dict(color='#f9a825', dash='dash', width=1.5), name='حد أعلى', showlegend=(col_idx==1)), row=1, col=col_idx)
        fig_cusum.add_trace(go.Scatter(x=t, y=lower_band, mode='lines', line=dict(color='#f9a825', dash='dash', width=1.5), name='حد أدنى', showlegend=(col_idx==1), fill='tonexty', fillcolor='rgba(249,168,37,0.08)'), row=1, col=col_idx)
        fig_cusum.add_trace(go.Scatter(x=t, y=cusum_data, mode='lines', name=f'CUSUM ({title})', line=dict(color=clr_line, width=2.5)), row=1, col=col_idx)
    fig_cusum.update_layout(plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', height=340,
                            font=dict(family='Cairo'),
                            title=dict(text="اختبار CUSUM: CUSUM داخل الحزمة = استقرار",
                                       font=dict(family='Cairo', size=13), x=0.5))
    st.plotly_chart(fig_cusum, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE 12 — INTERACTIVE SIMULATION
# ═══════════════════════════════════════════════════════
elif menu == "📈  محاكاة تفاعلية":
    show_hero()

    st.markdown("""
    <div class="section-card">
        <div class="sec-title">📈 محاكاة GVAR تفاعلية — جرّب بنفسك!</div>
        <div class="sec-subtitle">غيّر المعاملات وشاهد كيف يتغير سلوك نموذج GVAR في الوقت الفعلي</div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box info-blue">
        <p>🧮 <strong>تبسيط النموذج:</strong> سنُحاكي نموذج GVAR مُبسّطاً من 4 دول مع متغير واحد لكل دولة — الناتج المحلي الإجمالي (GDP). هذا يُوضّح المبادئ الأساسية بوضوح.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="section-card section-card-green">
    <div class="sec-title">⚙️ إعدادات النموذج</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        rho = st.slider("معامل الاستمرارية الذاتية (ρ)", 0.1, 0.99, 0.6, 0.01, key="rho")
        phi = st.slider("معامل التأثير الخارجي (φ)", 0.0, 0.5, 0.25, 0.01, key="phi")
    with c2:
        shock_country = st.selectbox("الدولة المُصدومة", ["أمريكا", "أوروبا", "الصين", "الجزائر"])
        shock_mag = st.slider("حجم الصدمة (% من الناتج)", -5.0, 5.0, 1.0, 0.1, key="smag")
    with c3:
        T_sim = st.slider("أفق المحاكاة (أرباع سنة)", 8, 40, 20, key="tsim")
        noise_level = st.slider("مستوى التشويش (σ)", 0.0, 1.0, 0.3, 0.05, key="nz")

    countries_sim = ["أمريكا", "أوروبا", "الصين", "الجزائر"]
    trade_weights = {
        "أمريكا":  [0, 0.35, 0.30, 0.05],
        "أوروبا":  [0.35, 0, 0.25, 0.20],
        "الصين":   [0.30, 0.25, 0, 0.15],
        "الجزائر": [0.05, 0.40, 0.25, 0],
    }
    colors_sim = {"أمريكا": "#1565c0", "أوروبا": "#2e7d32", "الصين": "#e53935", "الجزائر": "#6a1b9a"}

    np.random.seed(42)
    T_total = T_sim + 1
    gdp = {c: np.zeros(T_total) for c in countries_sim}
    shock_idx = 0
    shock_size = shock_mag

    for t in range(1, T_total):
        for c in countries_sim:
            w = trade_weights[c]
            x_star = sum(w[j]*gdp[cn][t-1] for j,cn in enumerate(countries_sim))
            own_effect = rho * gdp[c][t-1]
            foreign_effect = phi * x_star
            noise = noise_level * np.random.randn()
            gdp[c][t] = own_effect + foreign_effect + noise
            if t == 1 and c == shock_country:
                gdp[c][t] += shock_size

    fig_sim = go.Figure()
    for c in countries_sim:
        fig_sim.add_trace(go.Scatter(
            y=gdp[c], x=list(range(T_total)), name=c, mode='lines+markers',
            line=dict(color=colors_sim[c], width=2.5),
            marker=dict(size=5, color=colors_sim[c])
        ))
    fig_sim.add_vline(x=1, line_dash='dash', line_color='#f9a825', line_width=2,
                      annotation_text=f"  صدمة {shock_country}", annotation_font_color='#f9a825')
    fig_sim.add_hline(y=0, line_dash='dash', line_color='#90a4ae', line_width=1)
    fig_sim.update_layout(
        title=dict(text=f"🌐 انتشار الصدمة من {shock_country} — محاكاة GVAR",
                   font=dict(family='Cairo', size=15), x=0.5),
        xaxis_title="الزمن (أرباع السنة)", yaxis_title="الانحراف عن الاتزان (%)",
        plot_bgcolor='#f8f9ff', paper_bgcolor='#f8f9ff', font=dict(family='Cairo'),
        legend=dict(bgcolor='rgba(255,255,255,0.9)', bordercolor='#e0e0e0'), height=420
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    # Summary stats
    st.markdown("<div class='sec-title' style='margin-top:16px;'>📊 ملخص تأثير الصدمة</div>", unsafe_allow_html=True)
    col_stats = st.columns(len(countries_sim))
    for col, c in zip(col_stats, countries_sim):
        peak = max(abs(gdp[c]), key=abs)
        peak_t = list(gdp[c]).index(peak) if max(gdp[c]) >= abs(min(gdp[c])) else list(gdp[c]).index(min(gdp[c]))
        clr_bg = colors_sim[c]
        with col:
            st.markdown(f"""
            <div style='background:{clr_bg}; border-radius:14px; padding:20px; text-align:center; color:white;'>
                <div style='font-size:1.1em; font-weight:700; margin-bottom:8px;'>{c}</div>
                <div style='font-size:1.6em; font-weight:900;'>{peak:.2f}%</div>
                <div style='font-size:0.85em; opacity:0.85;'>ذروة الأثر</div>
                <div style='font-size:0.9em; margin-top:6px; opacity:0.9;'>الربع {peak_t}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Weights visualization
    st.markdown("""<div class="section-card section-card-orange">
    <div class="sec-title">⚖️ الأوزان التجارية المستخدمة في المحاكاة</div>""", unsafe_allow_html=True)
    weight_matrix = pd.DataFrame(trade_weights, index=countries_sim)
    fig_heat = go.Figure(go.Heatmap(
        z=weight_matrix.values,
        x=countries_sim, y=countries_sim,
        colorscale='Blues', text=weight_matrix.values,
        texttemplate="%{text:.2f}",
        textfont=dict(size=14, family='Cairo'),
        hoverongaps=False,
        colorbar=dict(title="الوزن", tickfont=dict(family='Cairo'))
    ))
    fig_heat.update_layout(
        title=dict(text="مصفوفة الأوزان التجارية الثنائية",
                   font=dict(family='Cairo', size=14), x=0.5),
        paper_bgcolor='#f8f9ff', height=320,
        xaxis=dict(tickfont=dict(family='Cairo', size=12)),
        yaxis=dict(tickfont=dict(family='Cairo', size=12)),
        margin=dict(t=60)
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════
st.markdown("""
<div class="footer-bar">
    <div style='font-size:1.3em; font-weight:700; margin-bottom:8px;'>
        👨‍🏫 Dr. Merwan Roudane &nbsp;|&nbsp; د. مروان رودان
    </div>
    <div style='opacity:0.85; font-size:0.95em; margin-bottom:6px;'>
        اقتصاد قياسي &nbsp;•&nbsp; نماذج الاقتصاد الكلي العالمي &nbsp;•&nbsp; Econometrics & Global Macro Modeling
    </div>
    <div style='opacity:0.65; font-size:0.85em;'>
        استناداً إلى: Chudik & Pesaran (2014) — "Theory and Practice of GVAR Modeling"
    </div>
    <div style='opacity:0.55; font-size:0.8em; margin-top:8px;'>
        CESifo Working Paper No. 4807 &nbsp;|&nbsp; Federal Reserve Bank of Dallas & USC
    </div>
</div>
""", unsafe_allow_html=True)
