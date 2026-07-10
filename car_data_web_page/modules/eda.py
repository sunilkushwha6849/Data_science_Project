import streamlit as st
import pandas as pd
def show():

    st.title("Exploratory Data Analysis (EDA)")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["df"]
    st.subheader("Statistical Summary")
    st.dataframe(df.describe())
    st.subheader("Column Analysis")
    selected_column = st.selectbox(
    "Select a Column",
    df.columns
)
    st.write("Data Type:", df[selected_column].dtype)
    st.write("Missing Values:", df[selected_column].isnull().sum())
    st.write("Unique Values:", df[selected_column].nunique())
    st.subheader("Value Counts")
    st.dataframe(df[selected_column].value_counts())
    if df[selected_column].dtype != "object":
        st.subheader("Numerical Summary")
        st.write("Minimum:", df[selected_column].min())
        st.write("Maximum:", df[selected_column].max())
        st.write("Mean:", round(df[selected_column].mean(), 2))
        st.write("Median:", df[selected_column].median())
        st.write("Standard Deviation:", round(df[selected_column].std(), 2))
    else:
        st.subheader("Categorical Summary")

        st.write("Most Frequent Value:",
            df[selected_column].mode()[0])

        st.write("Frequency:",
            df[selected_column].value_counts().iloc[0])
    st.subheader("Correlation Matrix")
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    correlation = numeric_df.corr()
    st.dataframe(correlation)
    st.subheader("GroupBy Analysis")
    group_column = st.selectbox(
    "Select Group Column",
    df.columns
)
    value_column = st.selectbox(
    "Select Value Column",
    df.select_dtypes(include=["int64", "float64"]).columns
)
    aggregation = st.selectbox(
    "Select Aggregation",
    ["Mean", "Sum", "Max", "Min", "Count"]
)
    if aggregation == "Mean":
        grouped_data = df.groupby(group_column)[value_column].mean()

    elif aggregation == "Sum":
        grouped_data = df.groupby(group_column)[value_column].sum()

    elif aggregation == "Max":
        grouped_data = df.groupby(group_column)[value_column].max()

    elif aggregation == "Min":
        grouped_data = df.groupby(group_column)[value_column].min()

    else:
        grouped_data = df.groupby(group_column)[value_column].count()
    st.dataframe(grouped_data.reset_index())
    st.subheader("Pivot Table")
    pivot_index = st.selectbox(
    "Select Row",
    df.columns,
    key="pivot_index"
)
    pivot_column = st.selectbox(
    "Select Column",
    df.columns,
    key="pivot_column"
)
    pivot_value = st.selectbox(
    "Select Value",
    df.select_dtypes(include=["int64", "float64"]).columns,
    key="pivot_value"
)
    pivot_agg = st.selectbox(
    "Aggregation Function",
    ["mean", "sum", "max", "min", "count"],
    key="pivot_agg"
)
    pivot_table = df.pivot_table(
    values=pivot_value,
    index=pivot_index,
    columns=pivot_column,
    aggfunc=pivot_agg
)
    st.dataframe(pivot_table)
    st.subheader("Crosstab Analysis")
    cross_row = st.selectbox(
    "Select First Column",
    df.select_dtypes(include=["object"]).columns,
    key="cross_row"
)
    cross_column = st.selectbox(
    "Select Second Column",
    df.select_dtypes(include=["object"]).columns,
    key="cross_column"
)
    cross_table = pd.crosstab(
    df[cross_row],
    df[cross_column]
)
    st.dataframe(cross_table)