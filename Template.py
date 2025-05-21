import streamlit as st
# import pandas as pd
# import numpy as np

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




# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")