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
    """, unsafe_allow_html=True)
    st.session_state
    data=st.session_state['event_dataset']
    eve=st.selectbox("Select a Event",data['Event Name'],key='reg_eve')
    cole=st.selectbox("Select The College name",data['college_location'].unique(),key='reg_col')
    sort_D=data[data['college_location']==cole]
    st.dataframe(sort_D)
    if st.button("Confirm"):
        if eve not in sort_D['Event Name'].values:
             st.write(f"There is no such event in the college {cole}")
        else:
            st.session_state['event_name']=eve
            st.session_state['current_page']='direct_reg'
            mon=sort_D[sort_D['Event Name'] == eve]['Month'].iloc[0]
            st.session_state['Month']=mon
            st.rerun()
    if st.button("Previous"):
        st.session_state['current_page']='search_bar'
        st.rerun()