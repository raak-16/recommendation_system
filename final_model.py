import streamlit as st
import pickle as pic
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import mysql.connector


# Prediction function
def predict(models, X_test,label_encoders):
    predictions = []
    for model in models:
        pred = model.predict(X_test)
        s = label_encoders['Event Name'].inverse_transform(pred)[0]
        if s not in predictions:
             predictions.append(s)
    return predictions

# Function to store user input in the database
def store_user_input(name, dept, college, city, event_type):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='localhost',           # e.g., 'localhost'
        user='root',                # your MySQL username
        password='nara@123',     # your MySQL password
        database='expo'       # your database name
    )
    
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Users (name, dept, college, city, event_type) 
    VALUES (%s, %s, %s, %s, %s)
    ''', (name, dept, college, city, event_type))
    
    conn.commit()
    conn.close()
    cursor.close()


# Streamlit app
def recommend():
    event_data = st.session_state['event_dataset']
    student_data = st.session_state['students_dataset']
    new_events=pd.read_csv("newlyadded_events.csv")

    # Merge both datasets on 'Event Name' for complete feature information
    data = pd.merge(student_data, event_data, on='Event Name')
    # Combine 'College' and 'City' into a new feature
    data['College_City'] =data['College'] + '_' + data['City']
    # Encoding categorical columns
    label_encoders = {}
    for column in ['Dept', 'College', 'City', 'Domain', 'Event Name', 'College_City', 'Event Type','Month']:
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column])
    label_encoders2={}
    for column in ['Domain','Event Type','Month']:
        label_encoders2[column]=LabelEncoder()
        new_events[column]=label_encoders2[column].fit_transform(new_events[column])

    #---------------------------------------updated till encoding----------------------------------

# Create a mapping of valid city options based on the college selected
    college_city_mapping =data[['College', 'City']].drop_duplicates().set_index('College')['City'].to_dict()
    st.title("Event Recommendation System")

    # Input fields in Streamlit with unique keys for selectboxes

    dept = st.selectbox("Enter Dept:", label_encoders['Dept'].classes_, key="dept_select")
    
    college = st.selectbox("Enter College:", label_encoders['College'].classes_, key="college_select")

    # Automatically select city based on the selected college
    if college in college_city_mapping:
        city = college_city_mapping[college]
        st.session_state['selected_city'] = city  # Store selected city in session state
    else:
        city = st.selectbox("Enter City:", label_encoders['City'].classes_, key="city_select")
        st.session_state['selected_city'] = city  # Allow manual city selection if college not mapped

    # Show selected city for confirmation
    st.write(f"Selected City: {st.session_state['selected_city']}")

    domain_inst = st.selectbox("Enter Your Domain interest:", label_encoders['Domain'].classes_, key="domain_select")
    event_type = st.selectbox("Enter Your Event Type preference:", label_encoders['Event Type'].classes_, key="event_type_select")
    if st.button("Previous Page"):
        st.session_state['current_page']='search_bar'
        st.rerun()
    if st.button('Recommend'):
        st.session_state['predictions']=[]
        x_test=[]
        '''x_test.append(label_encoders['Dept'].transform([dept])[0])
        x_test.append(label_encoders['College'].transform([college])[0])
        x_test.append(label_encoders['City'].transform([st.session_state.selected_city])[0])
        x_test.append(label_encoders['Domain'].transform([domain_inst])[0])
        x_test.append(label_encoders['Event Type'].transform([event_type])[0])
        college_city_label = college + '_' + st.session_state['selected_city']
        x_test.append(label_encoders['College_City'].transform([college_city_label])[0])
        X_test = pd.DataFrame([x_test], columns=['Dept','College','City','Domain','Event Type','College_City'])
        models = train(data[['Dept','College','City','Domain','Event Type','College_City']],data['Event Name'])
        predictions = predict(models, X_test,label_encoders)
        st.session_state['predictions'].extend([predictions[0]])'''        

        x_col = []
        x_test = []

        if dept in label_encoders['Dept'].inverse_transform(data['Dept']):
            x_col.append('Dept')
            x_test.append(label_encoders['Dept'].transform([dept])[0])
        
        if college in label_encoders['College'].inverse_transform(data['College']):
            x_col.append('College')
            x_test.append(label_encoders['College'].transform([college])[0])

        if st.session_state.selected_city in label_encoders['City'].inverse_transform(data['City']):
            x_col.append('City')
            x_test.append(label_encoders['City'].transform([st.session_state.selected_city])[0])
                
        if domain_inst in label_encoders['Domain'].inverse_transform(data['Domain']):
            x_col.append('Domain')
            x_test.append(label_encoders['Domain'].transform([domain_inst])[0])

        if event_type in label_encoders['Event Type'].inverse_transform(data['Event Type']):
            x_col.append('Event Type')
            x_test.append(label_encoders['Event Type'].transform([event_type])[0])
            
        if 'College' in x_col and 'City' in x_col:
            college_city_label = college + '_' + st.session_state['selected_city']
            if college_city_label in label_encoders['College_City'].inverse_transform(data['College_City']):
                x_col.append('College_City')
                x_test.append(label_encoders['College_City'].transform([college_city_label])[0])
            else:
                st.write("KINDLY ENTER THE VALID LOCATION OF YOUR COLLEGE!!")
                return  # Exit if the label is not valid
        
        if not x_col:
            st.write(f"SORRY {st.session_state['name']}, PROVIDED DATA IS UNIQUE, UNABLE TO RECOMMEND!")
        else:
            X_test = pd.DataFrame([x_test], columns=x_col)

                # Train and predict
            with open('expo_model.pkl', 'rb') as f:
                model = pic.load(f)
            models=model[st.session_state['dataset']]
            #models = train(data[x_col], data['Event Name'])
            predictions = predict(models, X_test,label_encoders)

                    # Store user input into the database
                    #store_user_input(name, dept, college, st.session_state['selected_city'], event_type)
            st.session_state['predictions'].extend(predictions)
            st.session_state['current_page']='page2'
            st.rerun()
            
            

def show():
    st.markdown(
    """
    <style>
    /* Style the title */
    .stTitle {
        color: #1abc9c;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    /* Style the text input */
    .stTextInput > div {
        border: 2px solid #1abc9c;
        border-radius: 5px;
        padding: 5px;
    }

    /* Style the button */
    .stButton>button {
        background-color: #1abc9c;
        color: white;
        padding: 8px 20px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #16a085;
        color: white;
    }

    /* Style the warning text */
    .stMarkdown {
        color: #e74c3c;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True)

    recommend()