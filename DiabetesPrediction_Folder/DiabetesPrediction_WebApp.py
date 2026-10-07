# -*- coding: utf-8 -*-
"""
Created on Sat Oct  4 13:43:15 2025

@author: Lyle John
"""
# -*- coding: utf-8 -*-
"""
Diabetes Prediction Web App (Updated for Scaled Model)
"""
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

import numpy as np
import pickle
import streamlit as st

# Load the saved model and scaler
loaded_model = pickle.load(open('C:/Projects/Deploying Machine Learning Model/DiabetesPrediction_Folder/diabetes_model.sav', 'rb'))
scaler = pickle.load(open('C:/Projects/Deploying Machine Learning Model/DiabetesPrediction_Folder/scaler.sav', 'rb'))

# Prediction function
def diabetes_prediction(input_data):
    # Convert to numpy array and reshape
    input_data_as_numpy_array = np.asarray(input_data, dtype=float).reshape(1, -1)

    # Scale input
    scaled_input = scaler.transform(input_data_as_numpy_array)

    # Predict
    prediction = loaded_model.predict(scaled_input)
    probability = loaded_model.predict_proba(scaled_input)[0][prediction[0]] * 100

    # Return result
    if prediction[0] == 0:
        return f'The person is NOT diabetic (Confidence: {probability:.2f}%)'
    else:
        return f'The person IS diabetic (Confidence: {probability:.2f}%)'


# Streamlit UI
def main():
    st.title('🩺 Diabetes Prediction Web Application')

    st.write('Enter the required health parameters below:')

    Pregnancies = st.text_input('Number of Pregnancies')
    Glucose = st.text_input('Glucose Level')
    BloodPressure = st.text_input('Blood Pressure Value')
    SkinThickness = st.text_input('Skin Thickness Value')
    Insulin = st.text_input('Insulin Level')
    BMI = st.text_input('BMI Value')
    DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
    Age = st.text_input('Age of the Person')

    diagnosis = ''

    if st.button('Run Diabetes Test'):
        try:
            input_data = [float(Pregnancies), float(Glucose), float(BloodPressure),
                          float(SkinThickness), float(Insulin), float(BMI),
                          float(DiabetesPedigreeFunction), float(Age)]
            diagnosis = diabetes_prediction(input_data)
        except ValueError:
            diagnosis = '⚠️ Please enter valid numeric values for all fields.'

    st.success(diagnosis)


if __name__ == '__main__':
    main()

    