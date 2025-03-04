import streamlit as st

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

    st.title("WELCOME")
    name=st.text_input("Enter Your Name:")
    st.session_state['name']=name
    mail=st.text_input("Enter Your mail id:")
    if st.button("Goto next page"):
        if "@" not in mail:
            st.write("Enter valid email id")
        else:
            st.session_state['user_mail']=mail
            st.session_state['current_page']='search_bar'
            st.rerun()