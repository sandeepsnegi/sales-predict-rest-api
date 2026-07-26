import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Prediction Platform")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product features

Product_Weight = st.number_input("Product Weight", min_value=0.0, max_value=30.0, step=0.01, value=1.0)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["No Sugar", "Low Sugar", "Regular"])
Product_Allocated_Area =st.number_input("Product Allocated Area", min_value=0.0, max_value=0.1, step=0.01, value=0.01)
Product_MRP = st.number_input("Product MRP", min_value=0.0, max_value=300.0, step=0.01, value=1.0)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Departmental Store", "Supermarket Type1", "Supermarket Type2", "Food Mart"])
Product_Id_char = st.text_input("Product Id (DR|FC|NC)", value="DR")
Store_Age_Years = st.number_input("Store Age ", min_value=0, max_value=50, step=1, value=1)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Id_char': Product_Id_char,
    'Store_Age_Years': Store_Age_Years,
    'Product_Type_Category': Product_Type_Category
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0],timeout=10)  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted sales (in units)']
        st.success(f"Predicted Sales (in units): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")
        st.error(response.status_code)

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
            st.error(response.status_code)
