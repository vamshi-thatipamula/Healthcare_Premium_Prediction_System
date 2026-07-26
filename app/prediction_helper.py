# Import Required Libraries

from pathlib import Path

import joblib
import pandas as pd


# Define Artifact Directory

BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS = BASE_DIR / "artifacts"


# Load Trained Models

model_young = joblib.load(ARTIFACTS / "model_young.joblib")
model_rest = joblib.load(ARTIFACTS / "model_rest.joblib")


# Load Preprocessing Scalers

scaler_young = joblib.load(ARTIFACTS / "scaler_young.joblib")
scaler_rest = joblib.load(ARTIFACTS / "scaler_rest.joblib")


# Calculate Normalized Medical Risk Score

def calculate_normalized_risk(medical_history):


    # Define risk score for each medical condition
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    # Split the medical history into individual diseases
    diseases = medical_history.lower().split(" & ")

    # Calculate the total risk score by summing the risk scores
    total_risk_score = sum(
        risk_scores.get(disease, 0)
        for disease in diseases
    )

    # Define the minimum and maximum possible risk scores
    max_score = 14
    min_score = 0

    # Normalize the risk score between 0 and 1
    normalized_risk_score = (
        total_risk_score - min_score
    ) / (max_score - min_score)

    # Return the normalized medical risk score
    return normalized_risk_score

# Preprocess User Input

def preprocess_input(input_dict):

    # Define all input features expected by the trained models
    expected_columns = [
        "age",
        "number_of_dependants",
        "income_lakhs",
        "insurance_plan",
        "genetical_risk",
        "normalized_risk_score",
        "gender_Male",
        "region_Northwest",
        "region_Southeast",
        "region_Southwest",
        "marital_status_Unmarried",
        "bmi_category_Obesity",
        "bmi_category_Overweight",
        "bmi_category_Underweight",
        "smoking_status_Occasional",
        "smoking_status_Regular",
        "employment_status_Salaried",
        "employment_status_Self-Employed"
    ]

    # Encode insurance plans into numerical values
    insurance_plan_encoding = {
        "Bronze": 1,
        "Silver": 2,
        "Gold": 3
    }

    # Create an empty dataframe with all required model features
    df = pd.DataFrame(
        0,
        columns=expected_columns,
        index=[0]
    )

    # Map user inputs to the model's expected feature format
    for key, value in input_dict.items():

        # Encode gender
        if key == "Gender":
            df["gender_Male"] = 1 if value == "Male" else 0

        # Encode region
        elif key == "Region":
            if value == "Northwest":
                df["region_Northwest"] = 1
            elif value == "Southeast":
                df["region_Southeast"] = 1
            elif value == "Southwest":
                df["region_Southwest"] = 1

        # Encode marital status
        elif key == "Marital Status":
            df["marital_status_Unmarried"] = 1 if value == "Unmarried" else 0

        # Encode BMI category
        elif key == "BMI Category":
            if value == "Obesity":
                df["bmi_category_Obesity"] = 1
            elif value == "Overweight":
                df["bmi_category_Overweight"] = 1
            elif value == "Underweight":
                df["bmi_category_Underweight"] = 1

        # Encode smoking status
        elif key == "Smoking Status":
            if value == "Occasional":
                df["smoking_status_Occasional"] = 1
            elif value == "Regular":
                df["smoking_status_Regular"] = 1

        # Encode employment status
        elif key == "Employment Status":
            if value == "Salaried":
                df["employment_status_Salaried"] = 1
            elif value == "Self-Employed":
                df["employment_status_Self-Employed"] = 1

        # Encode insurance plan
        elif key == "Insurance Plan":
            df["insurance_plan"] = insurance_plan_encoding[value]

        # Assign numerical features
        elif key == "Age":
            df["age"] = value

        elif key == "Number of Dependants":
            df["number_of_dependants"] = value

        elif key == "Income in Lakhs":
            df["income_lakhs"] = value

        elif key == "Genetical Risk":
            df["genetical_risk"] = value

    # Generate the normalized medical risk score
    df["normalized_risk_score"] = calculate_normalized_risk(
        input_dict["Medical History"]
    )

    # Scale numerical features using the appropriate scaler
    df = handle_scaling(
        input_dict["Age"],
        df
    )

    # Return the processed dataframe
    return df


# Scale Numerical Features

def handle_scaling(age, df):

    # Select the scaler according to the customer's age
    scaler_object = scaler_young if age <= 25 else scaler_rest

    # Retrieve the scaler and columns that require scaling
    scaler = scaler_object["scaler"]
    cols_to_scale = scaler_object["cols_to_scale"]

    # Add a temporary column required by the saved scaler
    df["income_level"] = 0

    # Apply feature scaling
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Remove the temporary column
    df.drop(columns=["income_level"], inplace=True)

    # Return the scaled dataframe
    return df

# Generate Insurance Premium Prediction

def predict(input_dict):

    # Preprocess the customer input data
    input_df = preprocess_input(input_dict)

    # Select the appropriate prediction model based on age
    # Predict the annual health insurance premium
    if input_dict["Age"] <= 25:
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)

    # Return the predicted premium as an integer
    return round(float(prediction[0]))