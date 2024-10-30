import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the datasets
try:
    event_data = pd.read_csv('event_name (1).csv')
    student_data = pd.read_csv('students_data3 (2) (1).csv')
except FileNotFoundError as e:
    st.error(f"File not found: {e}")
    st.stop()

# Merge the datasets
data = pd.merge(student_data, event_data, on='Event Name')
data['College_City'] = data['College'] + '_' + data['City']

# Encode categorical columns
label_encoders = {}
original_values = {}
for column in ['Dept', 'College', 'City', 'Domain', 'Event Name', 'College_City', 'Event Type']:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])
    original_values[column] = label_encoders[column].inverse_transform(data[column].unique())

# Separate features and target variable
X = data[['Dept', 'College', 'City', 'Event Type', 'College_City']]
y = data['Event Name']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Function to train models
def train(x_train, y_train):
    models = [RandomForestClassifier(n_estimators=120, random_state=i) for i in range(3)]
    models += [KNeighborsClassifier(n_neighbors=5) for i in range(2)]
    for model in models:
        model.fit(x_train, y_train)
    return models

# Function to show multiple predictions for a single test case
def show_multiple_predictions(models, input_data):
    predictions = []
    for model in models:
        pred = model.predict(input_data)
        s = label_encoders['Event Name'].inverse_transform(pred)[0]
        if s not in predictions:
            predictions.append(s)
    return predictions

# Train the models
models = train(X_train, y_train)

# Streamlit app
st.title("Event Prediction App")

# User input fields with original category names
dept = st.selectbox("Select Department", options=original_values['Dept'])
college = st.selectbox("Select College", options=original_values['College'])
city = st.selectbox("Select City", options=original_values['City'])
event_type = st.selectbox("Select Event Type", options=original_values['Event Type'])

# Encode selected values for prediction
def safe_transform(encoder, value, column_name):
    try:
        return encoder.transform([value])[0]
    except ValueError:
        st.warning(f"Unseen label '{value}' in {column_name}. Using default value.")
        return 0  # Assign a default value if unseen (adjust as needed)

# Combine inputs into a DataFrame with encoded values
input_data = pd.DataFrame({
    'Dept': [safe_transform(label_encoders['Dept'], dept, 'Dept')],
    'College': [safe_transform(label_encoders['College'], college, 'College')],
    'City': [safe_transform(label_encoders['City'], city, 'City')],
    'Event Type': [safe_transform(label_encoders['Event Type'], event_type, 'Event Type')],
    'College_City': [safe_transform(label_encoders['College_City'], f"{college}_{city}", 'College_City')]
})

# Prediction button
if st.button("Predict"):
    predictions = show_multiple_predictions(models, input_data)
    st.write("Predicted Event Names:")
    for prediction in predictions:
        st.write(prediction)

# Calculate and display accuracy
accuracy = (sum(model.score(X_test, y_test) for model in models) / len(models)) * 100
st.write(f"Model Accuracy: {accuracy:.2f}%")
