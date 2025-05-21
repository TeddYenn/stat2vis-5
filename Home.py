import streamlit as st

st.set_page_config(
    page_title="stat2vis", 
    page_icon= "📊",
    layout="wide", 
    initial_sidebar_state = "auto",
    menu_items={
        'About': "This work created by Teddy (Yen-Hsiang Huang; 黃彥翔) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# App Info.
st.title("stat2vis; Visualizing Statistics!")
st.caption("**統計分析視覺化; Developed by Teddy (Yen-Hsiang Huang; 黃彥翔)**")

# Functionalities
st.write("")
st.subheader("Functions")
st.write("Here are apps crafted to turn statistical data into visual magic:")
st.markdown("""1. **Exploratory Data Analysis (EDA)  |  探索式資料分析**""")
st.markdown("""2. **Probability Distributions  |  機率分布**""")
st.markdown("""3. **Central Limit Theorem (CLT)  |  中央極限定理**""")
st.markdown("""4. **Confidence Intervals  |  信賴區間**""")
st.markdown("""5. **Hypothesis Testing  |  假設檢定**""")
st.write("")

# Log Updates
st.subheader("Updates")

# st.write("2025/03/17: Start creating app.")
# st.write("2025/03/18: Finish EDA I.")
# st.write("2025/03/25: Finish EDA II.")
# st.write("2025/04/13: Finish Dist.")

# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")