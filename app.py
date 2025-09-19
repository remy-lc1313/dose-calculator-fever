import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Pediatric Dose Calculator",
    page_icon="💊",
    layout="centered"
)

# --- Custom Styling ---
# Streamlit doesn't allow direct CSS like the HTML file, but we can use Markdown and some custom theming.
st.markdown("""
    <style>
        .stApp {
            background-color: #2dd4bf; /* Teal background */
        }
        .st-emotion-cache-1y4p8pa { /* Main container styling */
            border-radius: 1rem;
        }
        h1, h2 {
            font-family: 'Quicksand', sans-serif;
            text-align: center;
        }
        /* Style buttons to be colorful */
        .stButton>button {
            border-radius: 0.5rem;
            color: white;
            font-weight: bold;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Quicksand:wght@700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


# --- App Header ---
st.title("Pediatric Dose Calculator")
st.markdown("<h2 style='text-align: center; color: #374151;'>Ibuprofen and Acetaminophen</h2>", unsafe_allow_html=True)


# --- Input Fields ---
col1, col2 = st.columns([3, 1])

with col1:
    weight = st.number_input("Child's Weight", min_value=0.1, step=0.1, format="%.1f")

with col2:
    weight_unit = st.radio("Unit", ["kg", "lb"], label_visibility="collapsed")


# --- Medication Selection Tabs ---
med_tab1, med_tab2 = st.tabs(["Ibuprofen", "Acetaminophen"])

# --- Ibuprofen Tab ---
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
    is_ibuprofen = True

# --- Acetaminophen Tab ---
with med_tab2:
    ace_formulation_option = st.selectbox(
        "Acetaminophen Formulation",
        ["Children's Liquid (160 mg / 5 mL)", "Infant Drops (80 mg / 1 mL)"],
        key='ace_form'
    )
    is_ibuprofen = False


# --- Calculation Logic & Display ---
if st.button("Calculate Dose", use_container_width=True):
    if not weight or weight <= 0:
        st.error("Please enter a valid weight.")
    else:
        weight_in_kg = weight if weight_unit == 'kg' else weight / 2.20462
        
        total_mg = 0
        total_ml = 0
        timing = ""
        dose_rate = 0
        med_name = ""
        concentration_text = ""
        
        if is_ibuprofen:
            med_name = "Ibuprofen"
            if age_range == '> 6 months':
                dose_rate = 10
                timing = 'every 6 hours'
            else: # age is under 6 months
                dose_rate = 5
                timing = 'every 8 hours'
            
            concentration = (100 / 5) if "100 mg / 5 mL" in ibu_formulation_option else (200 / 5)
            concentration_text = "100 mg / 5 mL" if "100 mg / 5 mL" in ibu_formulation_option else "200 mg / 5 mL"
            
            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration

        else: # Acetaminophen
            med_name = "Acetaminophen"
            dose_rate = 15
            timing = 'every 4 hours'
            
            concentration = (160 / 5) if "160 mg / 5 mL" in ace_formulation_option else (80 / 1)
            concentration_text = "160 mg / 5 mL" if "160 mg / 5 mL" in ace_formulation_option else "80 mg / 1 mL"

            total_mg = weight_in_kg * dose_rate
            total_ml = total_mg / concentration

        # --- Display Result ---
        st.success("Calculation Complete!")
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background-color: #f3f4f6; border-radius: 0.5rem;">
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
