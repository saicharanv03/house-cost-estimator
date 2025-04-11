import streamlit as st
import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Set up Streamlit UI
st.set_page_config(page_title="House Cost Estimator", layout="centered")
st.title("INR House Cost Estimator")
st.markdown("Estimate the construction cost of a house based on input features.")

# User input
square_footage = st.number_input("Square Footage", min_value=300, max_value=10000, value=1200)
num_floors = st.selectbox("Number of Floors", [1, 2, 3])
has_basement = st.selectbox("Has Basement", ["Yes", "No"]) == "Yes"
has_garage = st.selectbox("Has Garage", ["Yes", "No"]) == "Yes"
quality = st.selectbox("Construction Quality", ["Low", "Medium", "High"])
location_tier = st.selectbox("Location Tier", ["Tier 1", "Tier 2", "Tier 3"])

# Estimate
if st.button("Estimate Cost"):
    # Create raw input DataFrame
    input_df = pd.DataFrame([{
        "square_footage": square_footage,
        "num_floors": num_floors,
        "has_basement": int(has_basement),
        "has_garage": int(has_garage),
        "quality": quality,
        "location_tier": location_tier
    }])

    # One-hot encode categorical columns to match training
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    cat_cols = ["quality", "location_tier"]
    enc_df = pd.DataFrame(
        encoder.fit([["Low", "Tier 1"], ["Medium", "Tier 2"], ["High", "Tier 3"]]).transform(input_df[cat_cols]),
        columns=encoder.get_feature_names_out(cat_cols)
    )

    # Combine with numeric features
    num_df = input_df.drop(columns=cat_cols).reset_index(drop=True)
    final_input = pd.concat([num_df, enc_df], axis=1)

    # Predict
    prediction = model.predict(final_input)[0]
    st.success(f"Estimated Cost: ₹{int(prediction):,}")
