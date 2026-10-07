import pickle
import os
import streamlit as st
from streamlit_option_menu import option_menu

def load_model(filename):
    base_path = os.path.join(os.path.dirname(__file__), 'saved models')
    full_path = os.path.join(base_path, filename)
    try:
        with open(full_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"⚠️ Model file not found: {filename}")
        st.stop()

diabetes_model = load_model('diabetes_model.sav')
diabetes_scaler = load_model('diabetes_scaler.sav')
heart_model = load_model('heartdisease_model.sav')
heart_scaler = load_model('heartdisease_scaler.sav')
parkinsons_model = load_model('parkinsons_model.sav')
parkinsons_scaler = load_model('parkinsons_scaler.sav')

with st.sidebar:
    selected = option_menu(
        '🩺 Multiple Disease Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

if selected == 'Diabetes Prediction':
    st.title('🩸 Diabetes Prediction using Machine Learning')

    col1, col2, col3 = st.columns(3)
    with col1: Pregnancies = st.text_input('Number of Pregnancies')
    with col2: Glucose = st.text_input('Glucose Level')
    with col3: BloodPressure = st.text_input('Blood Pressure Value')
    with col1: SkinThickness = st.text_input('Skin Thickness Value')
    with col2: Insulin = st.text_input('Insulin Level')
    with col3: BMI = st.text_input('BMI Value')
    with col1: DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
    with col2: Age = st.text_input('Age of the Person')

    diab_diagnosis = ''
    if st.button('Get Diabetes Test Result'):
        try:
            inputs = [float(Pregnancies), float(Glucose), float(BloodPressure),
                      float(SkinThickness), float(Insulin), float(BMI),
                      float(DiabetesPedigreeFunction), float(Age)]

            scaled_inputs = diabetes_scaler.transform([inputs])
            prediction = diabetes_model.predict(scaled_inputs)

            diab_diagnosis = '✅ The person is NOT Diabetic' if prediction[0] == 0 else '⚠️ The person IS Diabetic'

        except ValueError:
            st.error("⚠️ Please enter valid numeric values.")
    st.success(diab_diagnosis)

if selected == 'Heart Disease Prediction':
    st.title('❤️ Heart Disease Prediction using Machine Learning')

    col1, col2, col3 = st.columns(3)
    with col1: age = st.text_input('Age')
    with col2: sex = st.text_input('Sex (1 = male; 0 = female)')
    with col3: cp = st.text_input('Chest Pain Type (0–3)')
    with col1: trestbps = st.text_input('Resting Blood Pressure')
    with col2: chol = st.text_input('Serum Cholesterol (mg/dl)')
    with col3: fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)')
    with col1: restecg = st.text_input('Resting ECG Results (0–2)')
    with col2: thalach = st.text_input('Max Heart Rate Achieved')
    with col3: exang = st.text_input('Exercise Induced Angina (1 = yes; 0 = no)')
    with col1: oldpeak = st.text_input('ST Depression induced by Exercise')
    with col2: slope = st.text_input('Slope of the Peak Exercise ST Segment (0–2)')
    with col3: ca = st.text_input('Major Vessels colored by Fluoroscopy (0–3)')
    with col1: thal = st.text_input('Thal (0 = normal; 1 = fixed defect; 2 = reversible defect)')

    heart_diagnosis = ''
    if st.button('Get Heart Disease Test Result'):
        try:
            inputs = [float(age), float(sex), float(cp), float(trestbps), float(chol),
                      float(fbs), float(restecg), float(thalach), float(exang),
                      float(oldpeak), float(slope), float(ca), float(thal)]

            scaled_inputs = heart_scaler.transform([inputs])
            prediction = heart_model.predict(scaled_inputs)

            heart_diagnosis = "✅ The Person's Heart is Healthy" if prediction[0] == 0 else "⚠️ The Person has Heart Disease"

        except ValueError:
            st.error("⚠️ Please enter valid numeric values.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    st.success(heart_diagnosis)

if selected == 'Parkinsons Prediction':
    st.title('🧠 Parkinson’s Disease Prediction using Machine Learning')

    inputs = {}
    cols = st.columns(5)
    fields = [
        'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)', 'MDVP:Jitter(Abs)',
        'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP', 'MDVP:Shimmer', 'MDVP:Shimmer(dB)',
        'Shimmer:APQ3', 'Shimmer:APQ5', 'MDVP:APQ', 'Shimmer:DDA', 'NHR',
        'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE'
    ]

    for i, field in enumerate(fields):
        col = cols[i % 5]
        inputs[field] = col.text_input(field)

    parkinsons_diagnosis = ''
    if st.button('Get Parkinsons Test Result'):
        try:
            values = [float(inputs[f]) for f in fields]
            scaled_inputs = parkinsons_scaler.transform([values])
            prediction = parkinsons_model.predict(scaled_inputs)

            parkinsons_diagnosis = '✅ The Person does NOT have Parkinson’s Disease' if prediction[0] == 0 else '⚠️ The Person has Parkinson’s Disease'

        except ValueError:
            st.error("⚠️ Please enter valid numeric values.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
    st.success(parkinsons_diagnosis)
