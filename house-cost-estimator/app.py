import streamlit as st
import pickle
import pandas as pd

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="House Cost Estimator", layout="centered")
st.title("INR House Cost Estimator")
st.markdown("Estimate the construction cost of a house based on input features.")

square_footage = st.number_input("Square Footage", min_value=300, max_value=10000, value=1200)
num_floors = st.selectbox("Number of Floors", [1, 2, 3])
has_basement = st.selectbox("Has Basement", ["Yes", "No"]) == "Yes"
has_garage = st.selectbox("Has Garage", ["Yes", "No"]) == "Yes"
quality = st.selectbox("Construction Quality", ["Low", "Medium", "High"])
location_tier = st.selectbox("Location Tier", ["Tier 1", "Tier 2", "Tier 3"])

if st.button("Estimate Cost"):
    input_df = pd.DataFrame([{
        "square_footage": square_footage,
        "num_floors": num_floors,
        "has_basement": int(has_basement),
        "has_garage": int(has_garage),
        "quality": quality,
        "location_tier": location_tier
    }])
    prediction = model.predict(input_df)[0]
    st.success(f"Estimated Cost: ₹{int(prediction):,}")
