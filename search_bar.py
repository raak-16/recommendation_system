import streamlit as st
import pandas as pd

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
    event_ssn=pd.read_csv("event_ssn.csv")
    event_kpr=pd.read_csv("event_kpr.csv")
    event_itech=pd.read_csv("event_data2.csv")
    event_nit=pd.read_csv("event_nit.csv")
    new_event=pd.read_csv("newlyadded_events.csv")

    students_ssn=pd.read_csv("feedback_ssn.csv")
    students_kpr=pd.read_csv("feedback_kpr.csv")
    students_itech=pd.read_csv("feedback_itech.csv")
    students_nit=pd.read_csv("feedback_nit.csv")

    event_ssn['college_location']=['SSN College of Engineering' for i in range(len(event_ssn))]
    event_kpr['college_location']=['KPR Institute of Engineering and Technology' for i in range(len(event_kpr))]
    event_itech['college_location']=['PSG Institute of Technology and Applied Research' for i in range(len(event_itech))]
    event_nit['college_location']=['NIT Trichy' for i in range(len(event_nit))]

    con=pd.concat([event_ssn,event_kpr,event_itech,event_nit],ignore_index=True).reset_index()
    search_data=con
    st.markdown("<h3 style='font-size: 20px;'>Events Available:</h3>", unsafe_allow_html=True)
    col1,col2=st.columns([3,1])
    with col1:
        sea_input=st.text_input("Search bar","Enter a month")
        search_input=sea_input.capitalize()
    with col2:
        col2.markdown("<br>"*1, unsafe_allow_html=True)
        if st.button("search"):
            events=pd.concat([event_itech,event_kpr,event_ssn,event_nit,new_event],axis=0,ignore_index=True) 
            global filter_data
            filter_data = events[events['Month'] == search_input].reset_index(drop=True)
            st.session_state['month_searched'] = search_input
            if not filter_data.empty:
                search_data=filter_data
            else:
                pass
    st.dataframe(search_data[['Event Name','Domain','Month','Event Type','college_location']])
    if st.button("Register Event",key='final2'):
            if 'month_searched' not in st.session_state:
                st.write("Search event month wise to Register")
            else:
                st.session_state['reg_dataset2']=filter_data
                st.session_state['current_page']='reg_form'
                st.rerun()

    st.write("-----------------------------------------------------------------------------------")
    st.write("Select a City")
    with st.expander("Filter by Region"):
        search_input2=st.selectbox("Select your preferable Region",["Chennai","Coimbatore","Trichy"])

        if search_input2=='Chennai':
            st.session_state['event_dataset']=event_ssn
            st.session_state['dataset']='Chennai'
            st.session_state['students_dataset']=students_ssn
            st.dataframe(event_ssn)

        elif search_input2=='Coimbatore':
            stu=pd.concat([students_itech,students_kpr],axis=0,ignore_index=True)
            coim=pd.concat([event_itech,event_kpr],axis=0,ignore_index=True)
            st.session_state['dataset']='Coimbatore'
            st.session_state['event_dataset']=coim
            st.session_state['students_dataset']=stu
            st.dataframe(coim)

        elif search_input2=='Trichy':
            st.session_state['event_dataset']=event_nit
            st.session_state['dataset']='Trichy'
            st.session_state['students_dataset']=students_nit
            st.dataframe(event_nit)
        if st.button("Register Event",key='final1'):
            if 'event_dataset' not in st.session_state:
                st.write("Select the Region")
            else:
                st.session_state['current_page']='reg_form'
                eve=st.session_state['event_dataset']
                st.session_state['reg_dataset2']=eve
                st.rerun()
    #st.write("-----------------------------------------------------------------------------------")
    if st.button("Go Back to login page"):
        st.session_state['current_page']='page1'
        st.rerun()
    if st.button("Goto next page"):
        st.session_state['current_page']='final_model'
        st.rerun()