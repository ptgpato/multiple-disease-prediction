# -*- coding: utf-8 -*-
"""
Diabetes Prediction System (Updated for Scaled Model)
"""

import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

import numpy as np
import pickle

# Load the saved model and scaler
loaded_model = pickle.load(open('C:/Projects/Deploying Machine Learning Model/DiabetesPrediction_Folder/diabetes_model.sav', 'rb'))
scaler = pickle.load(open('C:/Projects/Deploying Machine Learning Model/DiabetesPrediction_Folder/scaler.sav', 'rb'))

# Example input data: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
input_data = (1,85,66,29,0,26.6,0.351,31)

# Convert input data to numpy array and reshape for a single sample
input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)

# Scale the input before prediction
input_data_scaled = scaler.transform(input_data_as_numpy_array)

# Make prediction
prediction = loaded_model.predict(input_data_scaled)
probability = loaded_model.predict_proba(input_data_scaled)[0][prediction[0]] * 100

# Output the result
if prediction[0] == 0:
    print('The person is NOT diabetic')
else:
    print('The person IS diabetic')

print(f'Confidence: {probability:.2f}%')
