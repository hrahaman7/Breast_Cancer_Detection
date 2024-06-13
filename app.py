# app.py

# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib

# Load the saved model
model = joblib.load('best_model.pkl')

# Set Streamlit page config
st.set_page_config(
    page_title="Breast Cancer Prediction",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define custom CSS for a black and yellow theme
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #f0ad4e;
            color: black;
        }
        .stTextInput>div>div>input {
            background-color: #2f2f2f;
            color: white;
        }
        .stDataFrame>div>div>div>div>div>table {
            color: white;
        }
        .css-1f8qtks {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title and description
st.title('🔬 Breast Cancer Prediction from CSV File')
st.markdown("""
Welcome to the Breast Cancer Prediction App! Upload a CSV file with the required features and get predictions instantly.
""")

# File uploader for CSV files
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    input_data = pd.read_csv(uploaded_file)

    # Display the uploaded data
    st.subheader("📄 Uploaded Data:")
    st.dataframe(input_data)

    # Check for required columns
    required_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
                         'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean',
                         'fractal_dimension_mean', 'radius_se', 'texture_se', 'perimeter_se', 'area_se',
                         'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se',
                         'symmetry_se', 'fractal_dimension_se', 'radius_worst', 'texture_worst',
                         'perimeter_worst', 'area_worst', 'smoothness_worst', 'compactness_worst',
                         'concavity_worst', 'concave points_worst', 'symmetry_worst',
                         'fractal_dimension_worst']

    missing_cols = [col for col in required_features if col not in input_data.columns]
    if missing_cols:
        st.error(f"🚨 Missing required columns: {', '.join(missing_cols)}")
    else:
        # Make predictions
        predictions = model.predict(input_data[required_features])
        
        # Map predictions to diagnosis labels
        input_data['Diagnosis'] = ['🔴 Malignant' if pred == 1 else '🟢 Benign' for pred in predictions]

        # Display the predictions
        st.subheader("🔍 Predictions:")
        st.dataframe(input_data)

        # Show summary statistics
        st.subheader("📊 Summary Statistics:")
        st.write(input_data['Diagnosis'].value_counts())

        # Download predictions
        csv = input_data.to_csv(index=False)
        st.download_button(
            label="💾 Download predictions as CSV",
            data=csv,
            file_name='predictions.csv',
            mime='text/csv',
        )
else:
    st.info("📂 Please upload a CSV file to get predictions.")
