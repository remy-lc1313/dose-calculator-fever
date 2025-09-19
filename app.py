import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Pediatric Dose Calculator",
    page_icon="💊",
    layout="centered"
)

# --- App Header ---
st.title("Pediatric Dose Calculator")
st.write("For Ibuprofen and Acetaminophen")

# --- Input Fields ---
st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    weight = st.number_input("Child's Weight", min_value=0.1, step=0.1, format="%.1f")
with col2:
    # Adding a little space for alignment
    st.write("")
    st.write("")
    weight_unit = st.radio("Unit", ["kg", "lb"], horizontal=True, label_visibility="collapsed")

medication = st.radio("Select Medication", ["Ibuprofen", "Acetaminophen"], horizontal=True)

# --- Conditional Inputs based on Medication Selection ---
if medication == "Ibuprofen":
    st.subheader("Ibuprofen Details")
    age_range = st.radio(
        "Child's Age",
        ["> 6 months", "≤ 6 months"],
        horizontal=True
    )
    formulation_option = st.selectbox(
        "Formulation",
        ["Children's Liquid (100 mg / 5 mL)", "Infant Drops (200 mg / 5 mL)"],
        key='ibu_form'
    )
else: # Acetaminophen
    st.subheader("Acetaminophen Details")
    formulation_option = st.selectbox(
        "Formulation",
        ["Children's Liquid (160 mg / 5 mL)", "Infant Drops (80 mg / 1 mL)"],
        key='ace_form'
    )

st.divider()

# --- Calculation Logic & Display ---
if st.button("Calculate Dose", use_container_width=True):
    if not weight or weight <= 0:
        st.error("Please enter a valid weight.")
    else:
        # Convert weight to kg if necessary
        weight_in_kg = weight if weight_unit == 'kg' else weight / 2.20462

        # Initialize variables
        total_mg, total_ml, timing, dose_rate, concentration_text = 0, 0, "", 0, ""

        if medication == 'Ibuprofen':
            dose_rate = 10 if age_range == '> 6 months' else 5
            timing = 'every 6 hours as needed' if age_range == '> 6 months' else 'every 8 hours as needed'
            
            if "100 mg / 5 mL" in formulation_option:
                concentration_text = "100 mg / 5 mL"
                concentration = 100 / 5
            else:
                concentration_text = "200 mg / 5 mL"
                concentration = 200 / 5
        
        else: # Acetaminophen
            dose_rate = 15
            timing = 'every 4 hours as needed'

            if "160 mg / 5 mL" in formulation_option:
                concentration_text = "160 mg / 5 mL"
                concentration = 160 / 5
            else:
                concentration_text = "80 mg / 1 mL"
                concentration = 80 / 1

        # Perform calculations
        total_mg = weight_in_kg * dose_rate
        total_ml = total_mg / concentration

        # --- Display Result using clean Streamlit components ---
        st.subheader("Recommended Dose:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Dose (in mg)", value=f"{total_mg:.0f} mg")
        with col2:
            st.metric(label="Dose (in mL)", value=f"{total_ml:.1f} mL")

        st.info(f"Give {timing}.")
        st.caption(f"Calculation based on: {dose_rate} mg/kg for a child of {weight_in_kg:.1f} kg using {concentration_text} concentration.")


# --- Disclaimer ---
st.divider()
st.warning(
    """
    **Disclaimer:** This tool is for informational purposes only. 
    Always consult with a qualified healthcare provider for medical advice and before administering any medication.
    """, 
    icon="⚠️"
)

