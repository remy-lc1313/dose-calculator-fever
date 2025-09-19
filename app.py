import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Pediatric Dose Calculator",
    page_icon="💊",
    layout="centered"
)

# --- Custom Styling (More Robust for Streamlit Cloud) ---
st.markdown("""
    <style>
        /* Import custom fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Quicksand:wght@700&display=swap');

        /* Main background color */
        .stApp {
            background-color: #14b8a6; /* Saturated Teal */
        }
        
        /* Main container for widgets */
        .main .block-container {
            background-color: #ffffff;
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Title styling */
        h1 {
            font-family: 'Quicksand', sans-serif;
            text-align: center;
            color: #0f766e; /* Darker Teal */
        }
        h2 {
            font-family: 'Quicksand', sans-serif;
            text-align: center;
            font-weight: 700;
            color: #475569; /* Slate Gray */
        }

        /* Style for the radio button options to give a colorful feel on selection */
        .stRadio [role="radiogroup"] > label {
            background-color: #f1f5f9; /* Light gray background for options */
            border-radius: 0.5rem;
            padding: 0.5rem 0.75rem;
            margin-right: 0.5rem;
            border: 2px solid transparent;
            transition: all 0.2s;
        }
        /* Style for the SELECTED radio button */
         .stRadio [role="radiogroup"] > label:has(input:checked) {
            border-color: #f97316; /* Bright Orange Border */
            background-color: #fff7ed; /* Light Orange Background */
         }

        /* Style for the main Calculate button */
        .stButton>button {
            border: none;
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            background-color: #0d9488;
            color: white;
            font-weight: bold;
            transition: background-color 0.2s;
        }
        .stButton>button:hover {
            background-color: #0f766e;
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
med_tab1, med_tab2 = st.tabs(["Ibuprofen", "Acetaminophen"])
is_ibuprofen = True # Default to true, will be changed in acetaminophen tab

with med_tab1:
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
    # This tab is selected, so we calculate for Ibuprofen
    if 'active_tab' not in st.session_state or st.session_state.active_tab == 'Acetaminophen':
        is_ibuprofen = True
        st.session_state.active_tab = 'Ibuprofen'


with med_tab2:
    ace_formulation_option = st.selectbox(
        "Acetaminophen Formulation",
        ["Children's Liquid (160 mg / 5 mL)", "Infant Drops (80 mg / 1 mL)"],
        key='ace_form'
    )
    # This tab is selected, so we calculate for Acetaminophen
    if 'active_tab' not in st.session_state or st.session_state.active_tab == 'Ibuprofen':
        is_ibuprofen = False
        st.session_state.active_tab = 'Acetaminophen'

# --- Calculation Logic & Display ---
if st.button("Calculate Dose", use_container_width=True):
    # Determine which medication is active based on the last known state of the tabs
    active_med = st.session_state.get('active_tab', 'Ibuprofen')
    
    if not weight or weight <= 0:
        st.error("Please enter a valid weight.")
    else:
        weight_in_kg = weight if weight_unit == 'kg' else weight / 2.20462
        
        total_mg, total_ml, timing, dose_rate, med_name, concentration_text = 0, 0, "", 0, "", ""
        
        if active_med == 'Ibuprofen':
            med_name = "Ibuprofen"
            dose_rate = 10 if age_range == '> 6 months' else 5
            timing = 'every 6 hours' if age_range == '> 6 months' else 'every 8 hours'
            
            concentration_text = "100 mg / 5 mL" if "100 mg / 5 mL" in ibu_formulation_option else "200 mg / 5 mL"
            concentration = (100 / 5) if "100 mg / 5 mL" in ibu_formulation_option else (200 / 5)
            
            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration
        else: # Acetaminophen
            med_name = "Acetaminophen"
            dose_rate = 15
            timing = 'every 4 hours'
            
            concentration_text = "160 mg / 5 mL" if "160 mg / 5 mL" in ace_formulation_option else "80 mg / 1 mL"
            concentration = (160 / 5) if "160 mg / 5 mL" in ace_formulation_option else (80 / 1)

            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration

        # --- Display Result ---
        st.success("Calculation Complete!")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem; border: 2px solid #e5e7eb;">
            <p style="font-size: 1.2rem; font-weight: bold; color: #f97316;">{total_mg:.0f} mg</p>
            <p style="font-size: 2rem; font-weight: bold; color: #0ea5e9;">{total_ml:.1f} mL</p>
            <p style="font-weight: 600; color: #4b5563;">{timing}</p>
            <p style="font-size: 0.8rem; color: #6b7280; margin-top: 0.5rem;">
                ({med_name} @ {dose_rate} mg/kg for {concentration_text})
            </p>
        </div>
        """, unsafe_allow_html=True)


# --- Disclaimer ---
st.markdown("""
<div style="text-align: center; margin-top: 2rem; font-size: 0.75rem; color: #4b5563;">
    <strong>Disclaimer:</strong> This tool is for informational purposes only. 
    Always consult with a qualified healthcare provider for medical advice and before administering any medication.
</div>
""", unsafe_allow_html=True)


