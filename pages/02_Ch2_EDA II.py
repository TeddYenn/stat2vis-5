import streamlit as st
import pandas as pd
import plotly.express as px 

# Streamlit page configuration
st.set_page_config(
    page_title="Exploratory Data Analysis (EDA) II", 
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'About': "This work authored by Teddy (Yen-Hsiang Huang) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# App header and intro
st.title("Ch. 2: Exploratory Data Analysis II  |  探索式資料分析 II")
st.caption("**Developed by Teddy (Yen-Hsiang Huang)**")

st.write("Through basic exploratory data analysis, we have gained an understanding of the fundamental structure of the data. In this chapter, we will also use data visualization to assist in exploring the relationships between various variables.")
st.write("透過上一章節基本的探索式資料分析，我們已了解資料的基本結構。這一章節，將再次透過資料視覺化的方式，輔助我們探索各個變數的關聯性。")

# Section: Data Input
st.write("")
st.write("")
st.write("### 1️⃣ Data Input  |  資料輸入")
st.write("##### 🔸 You can use the demo data or upload your own Excel file for this section.")
st.write("")
st.write("**📌 Data Selection:**")

# --- Initialize state for checkboxes ---
if "use_demo_data" not in st.session_state:
    st.session_state.use_demo_data = False
if "upload_data" not in st.session_state:
    st.session_state.upload_data = False

# --- Callback: Only one checkbox can be selected at a time ---
def toggle_use_demo():
    if st.session_state.use_demo_data:
        st.session_state.upload_data = False

def toggle_upload_data():
    if st.session_state.upload_data:
        st.session_state.use_demo_data = False

# --- Data selection checkboxes (mutually exclusive) ---
st.checkbox(
    "Use demo data",
    key="use_demo_data",
    on_change=toggle_use_demo
)

st.checkbox(
    "Upload your own data",
    key="upload_data",
    on_change=toggle_upload_data
)

# --- Load data from selected source ---
df = None
uploaded_file = None

# Upload your own data
if st.session_state.upload_data:
    uploaded_file = st.file_uploader("📂 Upload your data file (上傳您的數據)", type=["xlsx", "csv"])

# Load demo or uploaded data
if st.session_state.use_demo_data:
    df = pd.read_csv('demo_data.csv')
elif uploaded_file is not None:
    if uploaded_file.type == 'text/csv':
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

# --- Display editable data table ---
if df is not None:
    st.markdown("---")
    st.write("##### 🔸 Your data should be displayed here.")
    st.write("##### 🔽 Editable Table!")
    edited_df = st.data_editor(df)  # Allow user to interactively edit table
    st.markdown("---")

if df is not None:
    # --- Variable type detection ---
    cols = df.columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_cols = df.select_dtypes(exclude=['object', 'category']).columns.tolist()

    # ==========================================
    # 2️⃣ Categorical Dataset Visualization
    # ==========================================
    st.write("### 2️⃣ Categorical Dataset Visualization  |  類別型資料集視覺化")
    st.write("##### 🔸 Dataset with more than one categorical variables.")

    # Allow user to select multiple categorical variables
    selected_cat_col = st.multiselect("Select categorical variables:", categorical_cols, key="cat_selector")

    if len(selected_cat_col) == 2:
        # Create a 2-way contingency table
        row_var, col_var = selected_cat_col
        cross_tab = pd.crosstab(df[row_var], df[col_var])
        st.write("")
        st.write("##### 🔽 Contingency table")
        st.dataframe(cross_tab)

        # Create heatmap
        fig1 = px.imshow(
            cross_tab.values,
            x=cross_tab.columns,
            y=cross_tab.index,
            text_auto=True,
            color_continuous_scale="Emrld",
            labels=dict(x=col_var, y=row_var, color="Count"),
            aspect="auto",
        )

        # Create sunburst chart based on hierarchy of categorical variables
        fig2 = px.sunburst(df, path=selected_cat_col)

        # Show both charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1, use_container_width=False)
        with col2:
            st.plotly_chart(fig2, use_container_width=False)

    elif len(selected_cat_col) == 3:
        # For 3 categorical variables: one as group (faceting)
        row_var, col_var, group_var = selected_cat_col
        st.write("")
        st.write("##### 🔽 Contingency table, " f"grouped by: {group_var}")

        for level in df[group_var].dropna().unique():
            sub_df = df[df[group_var] == level]
            cross_tab = pd.crosstab(sub_df[row_var], sub_df[col_var])

            st.write(f"Group: {group_var} = {level}")
            st.dataframe(cross_tab)

            fig1 = px.imshow(
                cross_tab.values,
                x=cross_tab.columns,
                y=cross_tab.index,
                text_auto=True,
                color_continuous_scale="Emrld",
                labels=dict(x=col_var, y=row_var, color="Count"),
                aspect="auto",
                width=500,
                height=500
            )
            st.plotly_chart(fig1, use_container_width=False)

        # Sunburst for 3-layer categorical structure
        fig2 = px.sunburst(df, path=selected_cat_col)
        st.plotly_chart(fig2, use_container_width=False)

    else:
        st.info("Please select 2 or 3 variables.")

    st.markdown("---")

    # ==========================================
    # 3️⃣ Numerical Dataset Visualization
    # ==========================================
    st.write("### 3️⃣ Numerical Dataset Visualization  |  連續型資料視覺化")
    st.write("##### 🔸 Dataset with more than one numerical variables.")

    # User selects numerical variables
    selected_num_col = st.multiselect("Select numerical variables:", numerical_cols, key="num_selector")

    if len(selected_num_col) < 2:
        st.info("Please select at least 2 variables.")
    else:
        # Scatter matrix (pairplot) using Plotly
        st.write("")
        st.write("##### 🔽 Pairplot")
        fig3 = px.scatter_matrix(
            df,
            dimensions=selected_num_col,
            title="",
            height=600,
            width=600
        )
        fig3.update_traces(diagonal_visible=False)
        st.plotly_chart(fig3, use_container_width=False)

        # Correlation heatmap
        st.write("##### 🔽 Correlation heatmap")
        corr = df[selected_num_col].corr()
        fig4 = px.imshow(
            corr,
            text_auto=".3f",
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1,
            labels=dict(color="Correlation"),
            aspect="auto",
            width=600,
            height=500
        )
        fig4.update_traces(textfont=dict(size=16))
        st.plotly_chart(fig4, use_container_width=False)

    st.markdown("---")

    # ==========================================
    # 4️⃣ Mixed-Type Dataset Visualization
    # ==========================================
    st.write("### 4️⃣ Mixed-Type Dataset Visualization  |  混合型資料集視覺化")
    st.write("##### 🔸 Dataset with both numeric and categorical variables.")

    # User selects type of visualization
    chart_type = st.radio(
        "Select chart type to display:",
        ["Box plot", "Violin plot", "Scatter plot (2D)", "Scatter plot (3D)"],
        index=0
    )

    # --- Box plot ---
    if chart_type == "Box plot":
        cat_var1 = st.selectbox("Choose a categorical variable for X-axis", categorical_cols)
        num_var1 = st.selectbox("Choose a numerical variable for Y-axis", numerical_cols)
        cat_var2 = st.selectbox("Choose a categorical variable for color", ["None"] + categorical_cols, index=1)
        color_arg = cat_var2 if cat_var2 != "None" else None

        fig5 = px.box(
            df,
            x=cat_var1,
            y=num_var1,
            color=color_arg,
            width=700,
            height=500
        )
        st.plotly_chart(fig5, use_container_width=False)

    # --- Violin plot ---
    elif chart_type == "Violin plot":
        cat_var1 = st.selectbox("Choose a categorical variable for X-axis", categorical_cols)
        num_var1 = st.selectbox("Choose a numerical variable for Y-axis", numerical_cols)
        cat_var2 = st.selectbox("Choose a categorical variable for color", ["None"] + categorical_cols, index=1)
        color_arg = cat_var2 if cat_var2 != "None" else None

        fig5 = px.violin(
            df,
            x=cat_var1,
            y=num_var1,
            color=color_arg,
            box=True,
            points="all",
            width=700,
            height=500
        )
        st.plotly_chart(fig5, use_container_width=False)

    # --- 2D Scatter plot (strip plot) ---
    elif chart_type == "Scatter plot (2D)":
        num_var1 = st.selectbox("Choose a numerical variable for X-axis", numerical_cols, index=0)
        num_var2 = st.selectbox("Choose a numerical variable for Y-axis", numerical_cols, index=1)
        cat_var1 = st.selectbox("Choose a categorical variable for color", ["None"] + categorical_cols, index=1)
        color_arg = cat_var1 if cat_var1 != "None" else None

        fig5 = px.strip(
            df,
            x=num_var1,
            y=num_var2,
            color=color_arg,
            stripmode='overlay',
            width=700,
            height=500
        )
        st.plotly_chart(fig5, use_container_width=False)

    # --- 3D Scatter plot ---
    elif chart_type == "Scatter plot (3D)":
        num_var1 = st.selectbox("Choose numerical variable for X-axis", numerical_cols, key="x_axis", index=0)
        num_var2 = st.selectbox("Choose numerical variable for Y-axis", numerical_cols, key="y_axis", index=1)
        num_var3 = st.selectbox("Choose numerical variable for Z-axis", numerical_cols, key="z_axis", index=2)

        cat_var1 = st.selectbox("Choose a categorical variable for color", ["None"] + categorical_cols, key="color_axis", index=1)
        color_arg = cat_var1 if cat_var1 != "None" else None

        fig5 = px.scatter_3d(
            df,
            x=num_var1,
            y=num_var2,
            z=num_var3,
            color=color_arg,
            width=700,
            height=500
        )
        st.plotly_chart(fig5, use_container_width=False)

# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")