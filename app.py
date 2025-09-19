import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Pediatric Dose Calculator",
    page_icon="💊",
    layout="centered"
)

# --- Custom Styling (Bright, Cheerful + Bigger Fonts) ---
st.markdown("""
    <style>
        /* Import custom fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Quicksand:wght@700&display=swap');

        /* Main background with gradient */
        .stApp {
            background: linear-gradient(135deg, #f9a8d4, #facc15, #4ade80, #38bdf8);
            font-family: 'Inter', sans-serif;
        }

        /* Main container for widgets */
        .main .block-container {
            background-color: #ffffff;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        /* Title styling */
        h1 {
            font-family: 'Quicksand', sans-serif;
            text-align: center;
            color: #1e293b;
            font-size: 2.8rem !important;
        }
        h2 {
            font-family: 'Quicksand', sans-serif;
            text-align: center;
            font-weight: 700;
            color: #334155;
            font-size: 2rem !important;
        }

        /* ----------------- GLOBAL FONT OVERRIDE ----------------- */
        html, body, [class*="css"] {
            font-size: 18px !important;
        }

        .stMarkdown p, .stMarkdown, .stMarkdown span, .stMarkdown li {
            font-size: 18px !important;
            line-height: 1.6 !important;
        }

        .stTabs [role="tab"] {
            font-size: 20px !important;
            font-weight: 700 !important;
        }

        div[data-testid="stWidgetLabel"] p {
            font-size: 20px !important;
            font-weight: 700 !important;
            color: #2563eb !important; /* Bright Blue */
        }

        div[data-testid="stRadio"] label,
        div[data-testid="stSelectbox"] div,
        div[data-testid="stNumberInput"] input {
            font-size: 18px !important;
        }
        /* -------------------------------------------------------- */

        /* Radio options (styling + cheerful highlight) */
        div[data-testid="stRadio"] label {
             font-weight: 600;
             border-radius: 0.5rem;
             padding: 0.5rem 0.75rem;
             margin-right: 0.5rem;
             border: 2px solid transparent;
             transition: all 0.2s;
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            border-color: #f97316 !important;
            background-color: #fff7ed !important;
            color: #000 !important;
        }

        /* Tabs cheerful highlight */
        .stTabs [role="tablist"] > div[aria-selected="true"] {
            background-color: #facc15 !important; /* Bright Yellow */
            color: #000 !important;
        }

        /* Bright Calculate button */
        .stButton>button {
            border: none;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            background-color: #f97316; /* Bright Orange */
            color: white;
            font-weight: bold;
            transition: background-color 0.2s;
            font-size: 1.3rem !important;
        }
        .stButton>button:hover {
            background-color: #ea580c; /* Darker Orange */
        }
    </style>
    """, unsafe_allow_html=True)


# --- App Header ---
st.title("Pediatric Dose Calculator")
st.markdown("<h2 style='font-family: Quicksand, sans-serif;'>Ibuprofen and Acetaminophen</h2>", unsafe_allow_html=True)


# --- Input Fields ---
col1, col2 = st.columns([3, 1])
with col1:
    weight = st.number_input("Child's Weight", min_value=0.1, step=0.1, format="%.1f")
with col2:
    weight_unit = st.radio("Unit", ["kg", "lb"], label_visibility="collapsed")


# --- Medication Selection Tabs ---
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Ibuprofen"

tabs = st.tabs(["Ibuprofen", "Acetaminophen"])

with tabs[0]: # Ibuprofen
    st.session_state.active_tab = "Ibuprofen"
    age_range = st.radio(
        "Child's Age",
        ["> 6 months", "≤ 6 months"],
        horizontal=True,
        key='ibu_age'
    )
    ibu_formulation_option = st.selectbox(
        "Ibuprofen Formulation",
        ["Children's Liquid (100 mg / 5 mL)", "Infant Drops (200 mg / 5 mL)"],
        key='ibu_form'
    )

with tabs[1]: # Acetaminophen
    st.session_state.active_tab = "Acetaminophen"
    ace_formulation_option = st.selectbox(
        "Acetaminophen Formulation",
        ["Children's Liquid (160 mg / 5 mL)", "Infant Drops (80 mg / 1 mL)"],
        key='ace_form'
    )


# --- Calculation Logic & Display ---
if st.button("Calculate Dose", use_container_width=True):
    active_tab_on_click = st.session_state.get('active_tab', 'Ibuprofen')
    
    if not weight or weight <= 0:
        st.error("Please enter a valid weight.")
    else:
        weight_in_kg = weight if weight_unit == 'kg' else weight / 2.20462
        
        total_mg, total_ml, timing, dose_rate, med_name, concentration_text = 0, 0, "", 0, "", ""
        
        if active_tab_on_click == 'Ibuprofen':
            med_name = "Ibuprofen"
            dose_rate = 10 if st.session_state.ibu_age == '> 6 months' else 5
            timing = 'every 6 hours' if st.session_state.ibu_age == '> 6 months' else 'every 8 hours'
            
            concentration_text = "100 mg / 5 mL" if "100 mg / 5 mL" in st.session_state.ibu_form else "200 mg / 5 mL"
            concentration = (100 / 5) if "100 mg / 5 mL" in st.session_state.ibu_form else (200 / 5)
            
            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration
        else: # Acetaminophen
            med_name = "Acetaminophen"
            dose_rate = 15
            timing = 'every 4 hours'
            
            concentration_text = "160 mg / 5 mL" if "160 mg / 5 mL" in st.session_state.ace_form else "80 mg / 1 mL"
            concentration = (160 / 5) if "160 mg / 5 mL" in st.session_state.ace_form else (80 / 1)

            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration

        # --- Display Result (Brightened Box) ---
        st.success("Calculation Complete!")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: #fff7ed; border-radius: 0.75rem; border: 3px solid #facc15;">
            <p style="font-size: 1.6rem; font-weight: bold; color: #f97316;">{total_mg:.0f} mg</p>
            <p style="font-size: 2.4rem; font-weight: bold; color: #2563eb;">{total_ml:.1f} mL</p>
            <p style="font-weight: 600; color: #4b5563; font-size: 1.2rem;">{timing}</p>
            <p style="font-size: 1rem; color: #6b7280; margin-top: 0.5rem;">
                ({med_name} @ {dose_rate} mg/kg for {concentration_text})
            </p>
        </div>
        """, unsafe_allow_html=True)


# --- Disclaimer ---
st.markdown("""
<div style="text-align: center; margin-top: 2rem; font-size: 1rem; color: #4b5563;">
    <strong>Disclaimer:</strong> This tool is for informational purposes only. 
    Always consult with a qualified healthcare provider for medical advice and before administering any medication.
</div>
""", unsafe_allow_html=True)
