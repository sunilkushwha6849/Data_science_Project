import streamlit as st
from modules import home
from modules import data_check
from modules import data_cleaning
from modules import eda
from modules import visualizations
st.set_page_config(
    page_title="Car EDA Dashboard",
    layout="wide"
)

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Data Check", "Data Cleaning", "EDA", "Visualization"]
)

if page == "Home":
    home.show()
if page == "Data Check":
    data_check.show()
if page == "Data Cleaning":
    data_cleaning.show()
if page == "EDA":
    eda.show()
if page == "Visualization":
    visualizations.show()
