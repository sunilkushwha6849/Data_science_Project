import streamlit as st

def show():

    st.title("Data Check")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset in the Home page first.")
        return

    df = st.session_state["df"]

    rows, columns = df.shape

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Rows", rows)

    with col2:
        st.metric("Total Columns", columns)

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows == 0:
        st.success("No Duplicate Rows Found")
    else:
        st.warning(f"Duplicate Rows Found: {duplicate_rows}")

    missing_values = df.isnull().sum()
    missing_columns = missing_values[missing_values > 0]

    if missing_columns.empty:
        st.success("No Missing Values Found")
    else:
        st.subheader("Missing Values by Column")
        st.dataframe(missing_columns)

    st.subheader("Data Types")
    st.dataframe(df.dtypes)

    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_columns = df.select_dtypes(include=["object"]).columns

    st.subheader("Column Categories")

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Numerical Columns", len(numerical_columns))

    with col4:
        st.metric("Categorical Columns", len(categorical_columns))