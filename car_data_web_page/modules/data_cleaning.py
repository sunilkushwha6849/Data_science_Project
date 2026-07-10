import streamlit as st
import pandas as pd

def show():

    st.title("Data Cleaning")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["df"]
    clean_df=df.copy()
    st.subheader("Fill Missing Values")
    method = st.selectbox(
    "Select Filling Method",
    ["Mean", "Median", "Mode"]
)
    if st.button("Fill Missing Values"):
        if method == "Mean":
            numeric_columns = clean_df.select_dtypes(include=["int64","float64"]).columns
            clean_df[numeric_columns] = clean_df[numeric_columns].fillna(
            clean_df[numeric_columns].mean()
            )
            st.success("Missing Values Filled Using Mean")
            st.dataframe(clean_df.head())
    duplicate_rows = clean_df.duplicated().sum()
    st.subheader("Duplicate Rows Cleaning")
    st.write("Total Duplicate Rows:", duplicate_rows)
    if st.button("Remove Duplicate Rows"):
        before_rows = clean_df.shape[0]
        clean_df = clean_df.drop_duplicates()
        after_rows = clean_df.shape[0]
        removed_rows = before_rows - after_rows
        st.success("Duplicate Rows Removed Successfully")
        st.metric("Rows Removed", removed_rows)
        st.dataframe(clean_df.head())
        st.session_state["df"] = clean_df
    missing_values = clean_df.isnull().sum().sum()
    st.subheader("Change Data Type")
    column = st.selectbox(
    "Select Column",
    df.columns
    )
    new_dtype = st.selectbox(
    "Select New Data Type",
    [
        "int",
        "float",
        "str",
        "datetime"
    ]
    )
    if st.button("Change Data Type"):
        try:

            if new_dtype == "int":
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).astype("Int64")
        
            elif new_dtype == "float":
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )
        
            elif new_dtype == "str":
                df[column] = df[column].astype(str)
        
            elif new_dtype == "datetime":
                df[column] = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )
        
            st.session_state["df"] = df
        
            st.success("Data Type Changed Successfully")
        
        except Exception as e:
            st.error(e)
    st.subheader("Rename Column")
    old_name = st.selectbox(
    "Select Column",
    df.columns,
    key="rename_column"
    )
    new_name = st.text_input(
    "Enter New Column Name"
    )
    if st.button("Rename Column"):
        try:

            if new_name.strip() != "":
    
                df.rename(
                    columns={old_name: new_name},
                    inplace=True
                )
    
                st.session_state["df"] = df
    
                st.success("Column Renamed Successfully")
    
            else:
                st.warning("Please Enter Column Name")

        except Exception as e:
            st.error(e)
    st.subheader("Drop Column")
    drop_column = st.selectbox(
    "Select Column to Drop",
    df.columns,
    key="drop_column"
    )
    if st.button("Drop Column"):
        try:

            df = df.drop(columns=[drop_column])

            st.session_state["df"] = df

            st.success(f"{drop_column} dropped successfully.")

        except Exception as e:
            st.error(e)
    st.subheader("Missing Values Cleaning")
    st.write("Total Missing Values:", missing_values)
    if st.button("Remove Missing Values"):
        before_rows = clean_df.shape[0]
        clean_df = clean_df.dropna()
        after_rows = clean_df.shape[0]
        removed_rows = before_rows - after_rows
        st.success("Missing Values Removed Successfully")
        st.write("Rows Removed:", removed_rows)
        st.dataframe(clean_df.head())
        st.session_state["df"] = clean_df
    st.subheader("Download Cleaned Dataset")
    csv = clean_df.to_csv(index=False).encode("utf-8")
    st.download_button(
    label="Download Cleaned CSV",
    data=csv,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)