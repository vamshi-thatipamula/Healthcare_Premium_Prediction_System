# Import Required Libraries

import streamlit as st
from prediction_helper import predict

# Configure Streamlit Page

st.set_page_config(
    page_title="Healthcare Premium Prediction System",
    page_icon="🏥",
    layout="wide")

# Display Application Title

st.title("🏥 Healthcare Premium Prediction System")

st.write(
    "Provide the customer details below to estimate the annual health insurance premium.")

# Define Dropdown Options

categorical_options = {
    "Gender": ["Male", "Female"],

    "Marital Status": [
        "Unmarried",
        "Married"
    ],

    "BMI Category": [
        "Normal",
        "Obesity",
        "Overweight",
        "Underweight"
    ],

    "Smoking Status": [
        "No Smoking",
        "Regular",
        "Occasional"
    ],

    "Employment Status": [
        "Salaried",
        "Self-Employed",
        "Freelancer"
    ],

    "Region": [
        "Northwest",
        "Northeast",
        "Southwest",
        "Southeast"
    ],

    "Medical History": [
        "No Disease",
        "Diabetes",
        "High blood pressure",
        "Diabetes & High blood pressure",
        "Thyroid",
        "Heart disease",
        "High blood pressure & Heart disease",
        "Diabetes & Thyroid",
        "Diabetes & Heart disease"
    ],

    "Insurance Plan": [
        "Bronze",
        "Silver",
        "Gold"
    ]
}

# Collect Customer Information

st.subheader("👤 Customer Information")

row1 = st.columns(3)

with row1[0]:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        step=1
    )

with row1[1]:
    gender = st.selectbox(
        "Gender",
        categorical_options["Gender"]
    )

with row1[2]:
    marital_status = st.selectbox(
        "Marital Status",
        categorical_options["Marital Status"]
    )

# Collect Health Information

st.subheader("❤️ Health Information")

row2 = st.columns(3)

with row2[0]:
    bmi_category = st.selectbox(
        "BMI Category",
        categorical_options["BMI Category"]
    )

with row2[1]:
    smoking_status = st.selectbox(
        "Smoking Status",
        categorical_options["Smoking Status"]
    )

with row2[2]:
    medical_history = st.selectbox(
        "Medical History",
        categorical_options["Medical History"]
    )

# Collect Insurance Information

st.subheader("📄 Insurance Information")

row3 = st.columns(3)

with row3[0]:
    insurance_plan = st.selectbox(
        "Insurance Plan",
        categorical_options["Insurance Plan"]
    )

with row3[1]:
    employment_status = st.selectbox(
        "Employment Status",
        categorical_options["Employment Status"]
    )

with row3[2]:
    region = st.selectbox(
        "Region",
        categorical_options["Region"]
    )

# Collect Additional Information

st.subheader("📊 Additional Information")

row4 = st.columns(3)

with row4[0]:
    number_of_dependants = st.number_input(
        "Number of Dependants",
        min_value=0,
        max_value=20,
        step=1
    )

with row4[1]:
    income_lakhs = st.number_input(
        "Annual Income (INR Lakhs)",
        min_value=0.0,
        max_value=200.0,
        step=0.5,
        format="%.1f",
        help="Enter the annual income in INR lakhs. 1 Lakh = INR 100,000."
    )

with row4[2]:
    genetical_risk = st.number_input(
        "Genetical Risk",
        min_value=0,
        max_value=5,
        step=1,
        value=0,
        disabled=age > 25,
        help=(
            "Represents the customer's inherited health risk based on family medical history. "
            "Applicable only for customers aged 18–25. "
            "0 = No genetic risk, 5 = Very high genetic risk."
        )
    )

    if age > 25:
        st.caption("Genetical Risk is applicable only for customers aged 18–25.")

# Store User Inputs

input_dict = {
    "Age": age,
    "Number of Dependants": number_of_dependants,
    "Income in Lakhs": income_lakhs,
    "Genetical Risk": genetical_risk,
    "Insurance Plan": insurance_plan,
    "Employment Status": employment_status,
    "Gender": gender,
    "Marital Status": marital_status,
    "BMI Category": bmi_category,
    "Smoking Status": smoking_status,
    "Region": region,
    "Medical History": medical_history
}

# Generate Insurance Premium Prediction

if st.button("Predict Premium", use_container_width=True):

    prediction = predict(input_dict)

    st.success(
        f"### Estimated Annual Health Insurance Premium: INR {prediction:,.0f}"
    )

