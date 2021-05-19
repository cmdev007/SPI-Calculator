import streamlit as st
import time
from load_css import local_css
import os, sqlite3
import pandas as pd

st.set_page_config(
    page_title="SPI:Calc",
    page_icon="😸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

local_css("style.css")

############### SQLITTE ###############

def create_table():
    conn = sqlite3.connect('spidata.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS spilog(unix REAL, uname TEXT, spi TEXT, sem TEXT)")
    c.close()
    conn.close()


def data_entry(unix, uname, spi, sem):
    uname = uname.replace("'", "''")
    conn = sqlite3.connect('spidata.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO spilog VALUES('{unix}', '{uname}', '{spi}', '{sem}')")
    conn.commit()
    c.close()
    conn.close()

def read_data(sem):
    conn = sqlite3.connect('spidata.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM spilog WHERE sem = '{sem}'")
    data = c.fetchall()
    return data

############## SQLITE ################

if "spidata.db" not in os.listdir():
    create_table()

placeTitle = st.empty()
placeTitle.markdown(f"<div style='font-size: 50px;;color:grey;font-family:orbitron;'><center><b>SPI Calculator</b></center></div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 12px;'><center>By <a href='https://github.com/cmdev007/'><span class='highlight blue'><span class='bold'>cMDev007</span></span></a></center></div>", unsafe_allow_html=True)
st.markdown("---")
SEM = st.sidebar.radio("",("Semester-2","Semester-1"))
if SEM == "Semester-2":
    app_state = st.experimental_get_query_params()
    if app_state == {}:
        with st.beta_expander("SPI Calculator",expanded=True):
            with st.form(key='columns_in_form'):

                nInput = st.text_input("Your name please (keep empty if want to hide identity)")

                elec = st.selectbox("Technical Elective", ("","Information Retrieval","No SQL Databases","Advanced Image Processing","Multimedia Security and Forensics"))

                submitted = st.form_submit_button('Submit')
                if submitted:
                    if nInput.strip()=="":
                        nInput = "anonymous"
                    else:
                        nInput = nInput.lower().strip()
                    st.experimental_set_query_params(**{"nInput": nInput, "elec": elec})
    app_state = st.experimental_get_query_params()
    if app_state != {}:
        placeTitle.markdown(f"<div style='font-size:30px;color:grey;font-family:orbitron;'>\
            <center><b>SPI Calculator</b></center></div>",
                            unsafe_allow_html=True)
        app_state = st.experimental_get_query_params()
        allSub = ["Big Data Processing", "Machine Learning", "Numerical Methods for Data Science", "Optimization",
                  "SAS based Mini Project - 1"]
        allSub.extend(app_state["elec"])
        nInput = app_state["nInput"][0]
        st.write(f"Hello, {nInput.title()}! Please enter your grades.")
        subIndex = {}
        subCred = {"Big Data Processing":3, "Machine Learning":4, "Numerical Methods for Data Science":4,
                    "Optimization":3, "SAS based Mini Project - 1":2, "Information Retrieval":4,
                    "No SQL Databases":4, "Advanced Image Processing":4, "Multimedia Security and Forensics":3}
        gradeNum = {"":0,"AA":10,"AB":9,"BB":8,"BC":7,"CC":6,"CD":5,"DD":4}
        for i in allSub:
            subIndex[i] = ""
        with st.form(key='gradedata'):
            for i in allSub:
                subIndex[i] = gradeNum[st.select_slider(i, ("AA","AB","BB","BC","CC","CD","DD"))]

            submitted = st.form_submit_button('Submit')
        if submitted:
            Numerator = 0
            Denominator = 0
            MFleg = False
            for i in allSub:
                if subIndex[i] == 0:
                    MFleg = True
                    break
                Numerator += subIndex[i]*subCred[i]
                Denominator += 10*subCred[i]
            if not MFleg:
                SPI = str(round((Numerator*10/Denominator),2))
                st.markdown(f"<div style='font-size: 16px;'><center>Your SPI: <span class='highlight green'><span class='bold'>{SPI}</span></span></center></div>", unsafe_allow_html=True)
                data_entry(int(time.time()), nInput, SPI, SEM)
            else:
                st.markdown(f"<div style='font-size: 16px;'><center>Please select grades of <span class='highlight green'><span class='bold'>All Subjects!</span></span></center></div>", unsafe_allow_html=True)
            st.markdown("---")
    # Leaderboard
    with st.beta_expander("Leader Board", expanded=False):
        # st.markdown(
        #     f"<div style='font-size: 20px;'><center><span class='highlight green'><span class='bold'>Coming Soon!</span></span></center></div>",
        #     unsafe_allow_html=True)
        allSPI = []
        for i in read_data(SEM):
            allSPI.append(float(i[2]))
        allSPI.sort(reverse=True)
        allName = [f"Classmate {i+1}" for i in range(len(allSPI))]
        st.write(pd.DataFrame({
        'Anonymous Name': allName,
        'SPI': allSPI,
        }))
if SEM == "Semester-1":
    st.markdown(
        f"<div style='font-size: 20px;'><center><span class='highlight green'><span class='bold'>Coming Soon!</span></span></center></div>",
        unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)