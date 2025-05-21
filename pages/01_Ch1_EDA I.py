import streamlit as st
import pandas as pd
import plotly.express as px  # For interactive charts
import plotly.figure_factory as ff  # For distplots, table charts
import plotly.graph_objects as go  # For more flexible chart components

# --- Set up the Streamlit page layout and metadata ---
st.set_page_config(
    page_title="Exploratory Data Analysis (EDA) I", 
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'About': "This work authored by Teddy (Yen-Hsiang Huang) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# --- App header and introduction ---
st.title("Ch. 1: Exploratory Data Analysis I  |  探索式資料分析 I")
st.caption("**Developed by Teddy (Yen-Hsiang Huang)**")

# Introduction (bilingual)
st.write("Exploratory Data Analysis (EDA) is a data analysis method that combines data visualization and statistical techniques. It aims to explore data from different perspectives, uncover potential problem clues, and identify possible solutions. In this chapter, we will briefly overview the basic structure and distribution of the data.")
st.write("探索式資料分析是一種資料分析方法，結合了資料視覺化與統計技術，旨在從不同角度探索數據，發掘潛在的問題線索，並尋找可能的解決方案。這一章節，我們將概略了解資料的基本結構與分布。")

# --- Section 1: Data Input ---
st.write("")
st.write("")
st.write("### 1️⃣ Data Input  |  資料輸入")
st.write("##### 🔸 You can use the demo data or upload your own Excel file for this section.")
st.write("")
st.write("**📌 Data Selection:**")

# --- Initialize session state for checkboxes ---
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
    # 2️⃣ Descriptive Statistics
    # ==========================================
    st.write("### 2️⃣ Descriptive Statistics  |  敘述統計量")
    st.write("🔸 **Type**: Categorical (Cat.), Numerical (Num.); **Level**: The number of unique values in categorical data; **Top**: The most frequently occurring value in categorical data; **Freq**: The count of how many times the 'Top' value appears.")

    # Create summary table with describe()
    summary_df = df.describe(include='all').transpose()

    # Rename columns for clarity
    rename_dict = {
        'count': 'Count', 'mean': 'Mean', 'std': 'Std', 'min': 'Min',
        '25%': 'Q1', '50%': 'Q2; Median', '75%': 'Q3', 'max': 'Max',
        'unique': 'Level', 'top': 'Mode', 'freq': 'Freq'
    }
    summary_df.rename(columns={col: rename_dict[col] for col in summary_df.columns if col in rename_dict}, inplace=True)

    # Add a 'Type' column to indicate if variable is categorical or numerical
    summary_df['Type'] = summary_df.index.map(lambda x: 'Cat.' if x in categorical_cols else 'Num.')

    # --- Add statistics for numerical variables ---
    if numerical_cols:
        # Compute additional stats for numerical variables
        mode_values = df[numerical_cols].mode().iloc[0]
        variance_values = df[numerical_cols].var(ddof=1)
        std_values = df[numerical_cols].std(ddof=1)
        cv_values = (std_values / df[numerical_cols].mean()).replace([float('inf'), -float('inf')], None)

        # Insert new stats into summary table
        for col in numerical_cols:
            if col in summary_df.index:
                summary_df.loc[col, 'Mode'] = mode_values[col]
                summary_df["Mode"] = summary_df["Mode"].astype(str)
                summary_df.loc[col, 'Variance'] = variance_values[col]
                summary_df.loc[col, 'SD'] = std_values[col]
                summary_df.loc[col, 'CV'] = cv_values[col]

    # --- Clean and display summary table ---
    # Reorder and filter the summary columns
    desired_cols = ['Type', 'Count', 'Level', 'Mode', 'Freq', 'Mean', 'Variance', 'SD', 'CV', 'Min', 'Q1', 'Q2; Median', 'Q3', 'Max']
    summary_df = summary_df[[col for col in desired_cols if col in summary_df.columns]]

    # Round numeric values
    numeric_cols = summary_df.select_dtypes(include=['number']).columns.tolist()
    summary_df[numeric_cols] = summary_df[numeric_cols].round(2)

    # Show summary statistics table
    st.write(summary_df)
    st.markdown("---")

    # ==========================================
    # 3️⃣ Categorical Data Visualization
    # ==========================================
    st.write("### 3️⃣ Categorical Data Visualization  |  類別型資料視覺化")
    st.write("##### 🔸 Data with categorical variables (e.g., groups, labels).")

    if len(categorical_cols) > 0:
        # Let user choose a categorical variable
        selected_cat_col = st.selectbox("Select a categorical variable:", categorical_cols, key="category_selection")

        # Let user choose sort method
        sort_order = st.radio("Sorting method:", ('Freqency', 'Name'), key="category_sort_order")

        # Count frequency of each category
        value_counts = df[selected_cat_col].value_counts().reset_index()
        value_counts.columns = ['Category', 'Count']

        # Apply sorting
        if sort_order == 'Name':
            value_counts = value_counts.sort_values(by='Category')
        else:
            value_counts = value_counts.sort_values(by='Count', ascending=False)

        # --- Bar chart ---
        fig_bar = px.bar(
            value_counts,
            x='Category',
            y='Count',
            color='Category',
            labels={'Category': selected_cat_col, 'Count': 'Count'},
            title=f'Bar Chart',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig_bar.update_layout(
            title_font_size=20,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            xaxis_tickfont_size=14,
            yaxis_tickfont_size=14,
            bargap=0.3,
            legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.7)
        )

        # --- Pie chart ---
        fig_pie = px.pie(
            value_counts,
            names='Category',
            values='Count',
            title=f'Pie Chart',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.3
        )

        fig_pie.update_layout(
            title_font_size=20,
            legend=dict(title=None, orientation="h", yanchor="bottom", y=-0.7)
        )

        # Show bar and pie charts side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar)
        with col2:
            st.plotly_chart(fig_pie)

        st.markdown("---")

    # ==========================================
    # 4️⃣ Numerical Data Visualization
    # ==========================================
    st.write("### 4️⃣ Numerical Data Visualization  |  連續型資料視覺化")
    st.write("##### 🔸 Data with continuous variables (e.g., height, weight).")

    if len(numerical_cols) > 0:
        # User selects one numerical variable
        selected_num_col = st.selectbox("Select a numerical variable:", numerical_cols, key="num_selection")
        data = df[selected_num_col].dropna().tolist()

        # Calculate default bin size for histogram
        data_range = max(data) - min(data) if len(data) > 1 else 1
        min_bin = max(1, round(data_range / 50))
        max_bin = max(10, round(data_range / 5))
        default_bin = round(data_range / 20)

        # Let user adjust bin size
        bin_size = st.slider("Adjust histogram bin size:", min_value=min_bin, max_value=max_bin, value=default_bin, step=min_bin)

        # --- Box plot ---
        box_trace = go.Box(
            y=data,
            name="Box Plot",
            boxpoints="all",
            jitter=0.25,
            line=dict(width=3),
            pointpos=0,
            marker=dict(color=px.colors.qualitative.Set2[0], opacity=0.4, size=8)
        )

        fig_combined = go.Figure([box_trace])
        fig_combined.update_layout(
            title=f'Box Plot',
            title_font_size=20,
            yaxis_title=selected_num_col,
            yaxis_title_font_size=16,
            xaxis_tickfont_size=14,
            yaxis_tickfont_size=14
        )

        # --- Histogram + density plot ---
        fig_dist = ff.create_distplot(
            [data], [selected_num_col],
            show_hist=True,
            show_curve=True,
            colors=px.colors.qualitative.Set2,
            bin_size=bin_size
        )

        fig_dist.update_layout(
            title=f'Histogram & Density Plot',
            title_font_size=20,
            xaxis_title=selected_num_col,
            xaxis_title_font_size=16,
            yaxis_title="Density",
            yaxis_title_font_size=16,
            xaxis_tickfont_size=14,
            yaxis_tickfont_size=14,
            bargap=0.01,
            showlegend=False
        )

        # Display both plots side by side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_combined)
        with col2:
            st.plotly_chart(fig_dist)


# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")