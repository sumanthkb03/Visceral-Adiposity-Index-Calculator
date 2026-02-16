import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Global Precision Cardio-Metabolic Tool", layout="centered")

# --- UI FIX: WHITE TEXT & DARK THEME ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #cccccc !important;
        font-weight: 600 !important;
    }
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { text-align: center; color: #ffffff; }
    .stMarkdown { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- SCIENTIFIC LOGIC ---
def calculate_vai(gender, bmi, wc, tg, hdl):
    if gender == "Male":
        return (wc / (39.68 + (1.88 * bmi))) * (tg / 1.03) * (1.31 / hdl)
    return (wc / (36.58 + (1.89 * bmi))) * (tg / 0.81) * (1.52 / hdl)

# --- HEADER ---
st.title("🫀 Global Precision Cardio-Metabolic Tool")
st.markdown("### Assessing Adipose Tissue Dysfunction and 'Hidden' Metabolic Risk")
st.divider()

# --- INPUTS ---
col_a, col_b = st.columns(2)
with col_a:
    gender = st.radio("Biological Sex", ["Male", "Female"])
    age = st.number_input("Chronological Age", 18, 95, 25)
    bmi = st.slider("BMI (kg/m²)", 15.0, 45.0, 22.0)

with col_b:
    wc = st.number_input("Waist Circumference (cm)", 60, 150, 85)
    tg = st.number_input("Triglycerides (mmol/L)", 0.5, 10.0, 1.5)
    hdl = st.number_input("HDL Cholesterol (mmol/L)", 0.5, 3.5, 1.1)

lpa = st.number_input("Lipoprotein(a) (mg/dL) [Optional]", 0, 300, 0)

# --- CALCULATIONS ---
if st.button("Generate Risk Analysis", use_container_width=True):
    vai = calculate_vai(gender, bmi, wc, tg, hdl)
    met_age = age
    # Global thresholds for VAI and Lp(a)
    if vai > 1.9: met_age += 5
    if lpa > 50: met_age += 8

    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("VAI Index", round(vai, 2))
    m_col2.metric("Chronological Age", age)
    m_col3.metric("Metabolic Age", round(met_age), delta=int(met_age-age), delta_color="inverse")

    st.divider()

# --- DETAILED SCIENTIFIC DESCRIPTION (CITED) ---
st.header("📖 Clinical Rationale")

st.markdown("""
**What is the Visceral Adiposity Index (VAI)?**
* The VAI is a sex-specific mathematical model that serves as a reliable indicator of visceral fat function and cellular adipose tissue dysregulation. 
* It integrates anthropometric data (BMI and Waist Circumference) with functional metabolic markers (Triglycerides and HDL) to provide a holistic risk profile. 
* Traditional metrics like BMI fail to differentiate between subcutaneous fat and dangerous ectopic visceral fat.
* Consequently, the VAI identifies "Metabolically Obese, Normal Weight" (MONW) individuals who possess high cardiovascular risk despite a standard body weight.

**Global Clinical Utility**
* Across diverse global populations, obesity and metabolic syndrome are rising sharply due to nutritional and lifestyle shifts. 
* High visceral adiposity is a primary driver of systemic inflammation and insulin resistance regardless of geographic location. 
* Early intervention through lifestyle modification or metformin has been proven to significantly reduce diabetes incidence.
* Cardiovascular disease prediction requires integrating multiple risk factor categories rather than relying on isolated variables.
* Lipoprotein(a) is a genetically determined, independent causal factor for atherosclerosis and is a critical "risk-enhancing" marker for patients worldwide.
* Managing blood cholesterol through targeted, precision assessment is now the global gold standard for preventing premature mortality.
* Global health equity requires using advanced metrics to uncover hidden risks in populations that do not fit traditional "obese" phenotypes.
""")

# --- CITATION LIST ---
with st.expander("📚 Complete Peer-Reviewed References"):
    st.write("""
    1. Amato MC, et al. *Diabetes Care*. 2010.
    2. Enas EA, et al. *J CardioMetab Syndr*. 2007.
    3. Misra A, et al. *J Clin Endocrinol Metab*. 2009.
    4. Toth PP, et al. *Eur J Prev Cardiol*. 2019.
    5. Amato MC & Giordano C. *Expert Rev Endocrinol Metab*. 2014.
    6. Unni S, et al. *Glob Health Action*. 2014.
    7. Yajnik CS, et al. *Int J Obes*. 2003.
    8. Knowler WC, et al. *N Engl J Med*. 2002.
    9. Wilson PW, et al. *Circulation*. 1998.
    10. Grundy SM, et al. *J Am Coll Cardiol*. 2019.
    """)
