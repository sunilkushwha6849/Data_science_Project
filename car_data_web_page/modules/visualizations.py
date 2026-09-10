import streamlit as st
import plotly.express as px


def show():
    st.title("Data Visualization")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state["df"]

    st.sidebar.header("Filters")

    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

    filter_column = st.sidebar.selectbox(
        "Select Filter Column",
        ["None"] + cat_cols
    )

    if filter_column != "None":
        filter_value = st.sidebar.multiselect(
            "Select Value",
            df[filter_column].dropna().unique()
        )

        if filter_value:
            df = df[df[filter_column].isin(filter_value)]

    st.subheader("Filtered Dataset")
    st.write("Rows :", len(df))
    st.dataframe(df.head())

    st.subheader("Create Charts")

    chart_type = st.selectbox(
        "Select Chart",
        [
            "Bar Chart",
            "Line Chart",
            "Histogram",
            "Scatter Plot",
            "Box Plot",
            "Pie Chart"
        ]
    )

    x_column = st.selectbox(
        "Select X-axis",
        df.columns
    )

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    if not numeric_cols:
        st.warning("No numeric columns available for Y-axis.")
        return

    y_column = st.selectbox(
        "Select Y-axis",
        numeric_cols
    )

    if chart_type == "Bar Chart":

        st.subheader("Bar Chart Settings")

        bar_color = st.color_picker(
            "Bar Color",
            "#1f77b4",
            key="bar_color"
        )

        orientation = st.selectbox(
            "Orientation",
            ["Vertical", "Horizontal"],
            key="orientation"
        )

        show_value = st.checkbox(
            "Show Values",
            True,
            key="show_value"
        )

        chart_data = (
            df.groupby(x_column)[y_column]
            .mean()
            .reset_index()
        )

        if orientation == "Vertical":
            fig = px.bar(
                chart_data,
                x=x_column,
                y=y_column,
                color_discrete_sequence=[bar_color],
                title=f"{y_column} vs {x_column}"
            )
        else:
            fig = px.bar(
                chart_data,
                x=y_column,
                y=x_column,
                orientation="h",
                color_discrete_sequence=[bar_color],
                title=f"{y_column} vs {x_column}"
            )

        if show_value:
            fig.update_traces(texttemplate="%{y:.2f}")

        st.plotly_chart(
            fig,
            width="stretch",
            key="bar_chart"
        )

    elif chart_type == "Line Chart":

        st.subheader("Line Chart Settings")

        line_color = st.color_picker(
            "Line Color",
            "#ff0000",
            key="line_color"
        )

        marker_symbol = st.selectbox(
            "Marker Style",
            [
                "circle",
                "square",
                "diamond",
                "cross",
                "x",
                "triangle-up",
                "triangle-down",
                "star"
            ],
            key="marker_style"
        )

        marker_size = st.slider(
            "Marker Size",
            4,
            20,
            8,
            key="marker_size"
        )

        line_width = st.slider(
            "Line Width",
            1,
            10,
            2,
            key="line_width"
        )

        line_style = st.selectbox(
            "Line Style",
            [
                "solid",
                "dash",
                "dot",
                "dashdot",
                "longdash"
            ],
            key="line_style"
        )

        show_marker = st.checkbox(
            "Show Marker",
            True,
            key="show_marker"
        )

        show_grid = st.checkbox(
            "Show Grid",
            True,
            key="line_grid"
        )

        chart_title = st.text_input(
            "Chart Title",
            "Line Chart",
            key="line_title"
        )

        chart_data = (
            df.groupby(x_column)[y_column]
            .mean()
            .reset_index()
        )

        fig = px.line(
            chart_data,
            x=x_column,
            y=y_column,
            title=chart_title
        )

        mode = "lines+markers" if show_marker else "lines"

        fig.update_traces(
            mode=mode,
            line=dict(
                color=line_color,
                width=line_width,
                dash=line_style
            ),
            marker=dict(
                symbol=marker_symbol,
                size=marker_size,
                color=line_color
            )
        )

        fig.update_xaxes(showgrid=show_grid)
        fig.update_yaxes(showgrid=show_grid)

        st.plotly_chart(
            fig,
            width="stretch",
            key="line_chart"
        )

    elif chart_type == "Histogram":

        fig = px.histogram(
            df,
            x=y_column,
            title="Histogram"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="histogram"
        )

    elif chart_type == "Scatter Plot":

        fig = px.scatter(
            df.head(1000),
            x=x_column,
            y=y_column,
            title="Scatter Plot"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="scatter_plot"
        )

    elif chart_type == "Box Plot":

        fig = px.box(
            df,
            x=x_column,
            y=y_column,
            title="Box Plot"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="box_plot"
        )

    elif chart_type == "Pie Chart":

        pie_data = (
            df[x_column]
            .value_counts()
            .reset_index()
        )

        pie_data.columns = [x_column, "Count"]

        fig = px.pie(
            pie_data,
            names=x_column,
            values="Count",
            title="Pie Chart"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="pie_chart"
        )
