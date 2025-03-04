import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_registration_email(user_email, user_name, event_name,date):
        # Email credentials
        sender_email = r"projectexpo745@gmail.com"
        sender_password = r"btornwkiapiystcd"
    
        # Set up the SMTP server (using Gmail's SMTP server)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    
        # Create the email content
        subject = "Event Registration Confirmation"
        body = f"""
        Hi {user_name},
 
        Thank you for registering for {event_name}! held on {date}!

        We're excited to have you join us. If you have any questions, feel free to reach out.

        Best regards,
        The Event Team
        """

        # Set up the MIME structure
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = user_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable TLS for security
            server.login(sender_email, sender_password)
        
            # Send the email
            server.sendmail(sender_email, user_email, message.as_string())
            print("Email sent successfully!")
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            server.quit()
        st.markdown("<h3 style='font-size: 20px;'>Event sent successfully to Your Mail id!</h3>", unsafe_allow_html=True)
        if st.button("Go back to login page"):
            st.session_state['current_page']='page1'
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
    def show_event_details():
        index=0
        for i in st.session_state['predictions']:
            a=st.session_state['event_dataset'][st.session_state['event_dataset']['Event Name']==i]
            for col in a.columns.tolist():
                if a[col].dtype == 'object':  # Only process string columns
                    # Split the string by "Name"
                    split_vals = a[col].str.split('Name')
                    # Safely handle the splitting and remove '16'
                    if isinstance(split_vals.iloc[0], list):
                        val = split_vals.iloc[0][0].replace('16', '').strip()  # Remove '16' and strip spaces
                    else:
                        val = split_vals.iloc[0]
                else:
                    val = a[col].iloc[0] 
                st.write(f"{col} : {val}")
            if st.button("Register",key=f"button{index}"):
                user_email =st.session_state['user_mail']
                user_name =st.session_state['name']
                event_name = a['Event Name']
                date=a['Month']
                send_registration_email(user_email, user_name, event_name,date)
            index+=1
                #st.markdown("<h3 style='font-size: 20px;'>Event sent successfully to Your Mail id!</h3>", unsafe_allow_html=True)
            st.write("--------------------------------------------------------------------")
    

    # Display recommendations
    st.title(f"WE RECOMMEND")
    st.write(", ".join(st.session_state['predictions']))
    st.markdown("<h3 style='font-size: 30px;'>Event Details</h3>", unsafe_allow_html=True)
    st.write("--------------------------------------------------------------------")
    show_event_details()
    if st.button("Previous Page"):
        st.session_state['current_page']='final_model'
        st.rerun()