import streamlit as st
from utils.load_data import load_data

def show():

    st.title("Car EDA Dashboard")

    file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if file is not None:

        df = load_data(file)
        st.session_state["df"] = df

        st.success("Dataset Loaded Successfully")
        st.write(df.isnull().sum().sum())

        st.dataframe(df.head())
        st.write(df.columns.tolist())
        