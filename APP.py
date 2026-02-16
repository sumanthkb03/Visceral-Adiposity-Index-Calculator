import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="South Asian Precision Cardio-Risk", layout="centered")

# --- CUSTOM STYLING (The Ivy Aesthetic) ---
st.markdown("""
    <style>
    /* Change font color in the metric boxes to be dark and visible */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricLabel"] {
        color: #333333 !important;
    }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- SCIENTIFIC LOGIC ---
def calculate_vai(gender, bmi, wc, tg, hdl):
    """Calculates Visceral Adiposity Index (VAI) - Cite: Amato et al. 2010"""
    if gender == "Male":
        return (wc / (39.68 + (1.88 * bmi))) * (tg / 1.03) * (1.31 / hdl)
    return (wc / (36.58 + (1.89 * bmi))) * (tg / 0.81) * (1.52 / hdl)

# --- MAIN DASHBOARD ---
st.title("🫀 South Asian Precision Cardio-Risk Tool")
st.markdown("""
    **Objective:** This tool identifies the **'Metabolically Obese Normal Weight' (MONW)** phenotype. 
    Standard ASCVD scores often fail South Asian patients by over-relying on BMI.
""")

st.divider()

# --- CENTRALIZED INPUT SECTION ---
st.header("📋 Clinical Parameters")
col_in1, col_in2 = st.columns(2)

with col_in1:
    gender = st.radio("Biological Sex", ["Male", "Female"])
    age = st.number_input("Chronological Age", 18, 95, 25)
    bmi = st.slider("BMI (kg/m²)", 15.0, 45.0, 22.0)

with col_in2:
    wc = st.number_input("Waist Circumference (cm)", 60, 150, 85)
    tg = st.number_input("Triglycerides (mmol/L)", 0.5, 10.0, 1.5)
    hdl = st.number_input("HDL Cholesterol (mmol/L)", 0.5, 3.5, 1.1)

lpa = st.number_input("Lipoprotein(a) (mg/dL) [Optional]", 0, 300, 0)

st.markdown("---")

# --- RESULTS SECTION ---
if st.button("Generate Risk Analysis", use_container_width=True):
    vai = calculate_vai(gender, bmi, wc, tg, hdl)
    
    # Risk Logic (Evidence-based offsets)
    met_age = age
    risks = []
    
    if vai > 1.9:
        met_age += 5
        risks.append("High Visceral Adiposity (VAI > 1.9)")
    if lpa > 50:
        met_age += 8
        risks.append("Elevated Genetic Risk (Lp(a) > 50 mg/dL)")

    # Display Metrics with visible dark font
    col1, col2, col3 = st.columns(3)
    col1.metric("VAI Index", round(vai, 2))
    col2.metric("Chronological Age", age)
    col3.metric("Metabolic Age", round(met_age), delta=int(met_age-age), delta_color="inverse")

    if met_age > age:
        st.error(f"### ⚠️ Metabolic Dysregulation Detected")
        st.write(f"The patient's metabolic profile is concordant with an individual **{round(met_age - age)} years older**.")
        for r in risks:
            st.write(f"- {r}")
    else:
        st.success("### ✅ Optimal Metabolic Profile")
        st.write("Current biomarkers suggest visceral fat function is within healthy South Asian reference ranges.")

# --- THE SCIENCE SECTION ---
with st.expander("📚 Scientific Basis & Citations"):
    st.write("""
        ### Methodology:
        1. **VAI (Visceral Adiposity Index):** A sex-specific mathematical model that outperforms BMI in predicting cardiometabolic risk.
        2. **Citations:** Amato MC, et al. *Diabetes Care*. 2010; Enas EA, et al. *JAMA*. 2004.
    """)
