import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="South Asian Precision Cardio-Risk", layout="centered")

# --- UI FIX: HIGH CONTRAST & CENTERING ---
st.markdown("""
    <style>
    /* 1. Force metric numbers to be DEEP BLACK for visibility */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    /* 2. Make labels dark grey */
    [data-testid="stMetricLabel"] {
        color: #222222 !important;
        font-weight: 600 !important;
    }
    /* 3. Center the title and intro */
    .stApp {
        background-color: #0e1117;
    }
    h1, h3 {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SCIENTIFIC LOGIC ---
def calculate_vai(gender, bmi, wc, tg, hdl):
    if gender == "Male":
        return (wc / (39.68 + (1.88 * bmi))) * (tg / 1.03) * (1.31 / hdl)
    return (wc / (36.58 + (1.89 * bmi))) * (tg / 0.81) * (1.52 / hdl)

# --- MAIN INTERFACE ---
st.title("🫀 South Asian Precision Cardio-Risk Tool")
st.markdown("### Precision Metabolic Assessment for MONW Phenotypes")
st.divider()

# --- CENTRALIZED INPUTS ---
# Using columns to organize the middle section
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

st.divider()

# --- ACTION & RESULTS ---
if st.button("Generate Risk Analysis", use_container_width=True):
    vai = calculate_vai(gender, bmi, wc, tg, hdl)
    
    # Calculation Logic
    met_age = age
    risks = []
    if vai > 1.9:
        met_age += 5
        risks.append("High Visceral Adiposity (VAI > 1.9)")
    if lpa > 50:
        met_age += 8
        risks.append("Elevated Genetic Risk (Lp(a) > 50 mg/dL)")

    # The 3 White Boxes with Visible Numbers
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("VAI Index", round(vai, 2))
    m_col2.metric("Chronological Age", age)
    m_col3.metric("Metabolic Age", round(met_age), delta=int(met_age-age), delta_color="inverse")

    st.markdown("---")

    if met_age > age:
        st.error(f"### ⚠️ Metabolic Dysregulation Detected")
        st.write(f"The patient's metabolic profile is concordant with an individual **{round(met_age - age)} years older**.")
        for r in risks:
            st.write(f"- {r}")
    else:
        st.success("### ✅ Optimal Metabolic Profile")
        st.write("Current biomarkers suggest visceral fat function is within healthy South Asian reference ranges.")

# --- SCIENCE SECTION ---
with st.expander("📚 Scientific Basis & Citations"):
    st.write("Amato MC, et al. *Diabetes Care*. 2010; Enas EA, et al. *JAMA*. 2004.")
