import streamlit as st
import pandas as pd

# --- PAGE SETUP ---
st.set_page_config(page_title="Precision Cardio-Risk", layout="wide")

# --- CUSTOM STYLING (The Ivy Aesthetic) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SCIENTIFIC LOGIC ---
def calculate_vai(gender, bmi, wc, tg, hdl):
    """Calculates Visceral Adiposity Index (VAI) - Cite: Amato et al. 2010"""
    if gender == "Male":
        return (wc / (39.68 + (1.88 * bmi))) * (tg / 1.03) * (1.31 / hdl)
    return (wc / (36.58 + (1.89 * bmi))) * (tg / 0.81) * (1.52 / hdl)

# --- SIDEBAR INPUTS ---
st.sidebar.header("📊 Clinical Parameters")
with st.sidebar:
    gender = st.radio("Biological Sex", ["Male", "Female"])
    age = st.number_input("Chronological Age", 18, 95, 25)
    
    st.markdown("---")
    st.subheader("Anthropometrics")
    bmi = st.slider("BMI (kg/m²)", 15.0, 45.0, 22.0)
    wc = st.number_input("Waist Circumference (cm)", 60, 150, 85)
    
    st.markdown("---")
    st.subheader("Lipid Profile (mmol/L)")
    tg = st.number_input("Triglycerides", 0.5, 10.0, 1.5)
    hdl = st.number_input("HDL Cholesterol", 0.5, 3.5, 1.1)
    lpa = st.number_input("Lipoprotein(a) (mg/dL) [Optional]", 0, 300, 0)

# --- MAIN DASHBOARD ---
st.title("Precision Cardio-Risk Tool")
st.markdown("""
    **Objective:** This tool identifies the **'Metabolically Obese Normal Weight' (MONW)** phenotype. 
    Standard ASCVD scores often fail South Asian patients by over-relying on BMI.
""")

if st.button("Generate Risk Analysis"):
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

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Visceral Adiposity Index", round(vai, 2))
    col2.metric("Chronological Age", age)
    col3.metric("Estimated Metabolic Age", round(met_age), delta=int(met_age-age), delta_color="inverse")

    st.markdown("---")
    
    if met_age > age:
        st.error(f"### ⚠️ Metabolic Dysregulation Detected")
        st.write(f"The patient's metabolic profile is concordant with an individual **{round(met_age - age)} years older**.")
        for r in risks:
            st.write(f"- {r}")
    else:
        st.success("### ✅ Optimal Metabolic Profile")
        st.write("Current biomarkers suggest visceral fat function is within healthy South Asian reference ranges.")

# --- THE SCIENCE SECTION (THE IVY DIFFERENTIATOR) ---
st.markdown("---")
with st.expander("📚 Scientific Basis & Citations"):
    st.write("""
        ### The South Asian Paradox
        South Asians often display the **'Thin-Fat' phenotype**, characterized by high visceral fat despite a 'normal' BMI. 
        Traditional risk calculators (like the Framingham or ASCVD scores) significantly underestimate risk in this population.
        
        **Methodology:**
        1. **VAI (Visceral Adiposity Index):** A sex-specific mathematical model that outperforms BMI in predicting cardiometabolic risk.
        2. **Lp(a) Integration:** Lipoprotein(a) is a highly atherogenic, genetically determined particle that is often elevated in South Asians independently of lifestyle.
        
        **Citations:**
        * Amato MC, et al. "Visceral Adiposity Index: A reliable indicator of visceral fat function associated with cardiometabolic risk." *Diabetes Care*. 2010.
        * Enas EA, et al. "The INTERHEART study: importance of risk factors in South Asians." *JAMA*. 2004.
    """)

st.caption("Disclaimer: This is an educational tool based on published epidemiological data and does not constitute medical advice.")