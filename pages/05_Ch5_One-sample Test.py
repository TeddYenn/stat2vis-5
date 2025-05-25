import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t

# --- Set up the Streamlit page layout and metadata ---
st.set_page_config(
    page_title="One-sample CI & HT", 
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'About': "This work authored by Teddy (Yen-Hsiang Huang) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# --- App header and introduction ---
st.title("Ch. 5: One-sample Test  |  單一樣本檢定")
st.caption("**Developed by Teddy (Yen-Hsiang Huang)**")


# --- Introduction ---
st.write("This chapter illustrates the connection between confidence intervals and hypothesis testing using either the Z or t distribution, depending on whether the population standard deviation is known.")
st.write("本章節展示在母體標準差已知或未知下，如何透過 Z 或 t 分布進行信賴區間推論與假設檢定，並視覺化其關聯性。")

# --- Parameters input ---
st.write("### 1️⃣ Parameter Settings | 參數設定")

col1, col2, col3 = st.columns(3)
with col1:
    dist_type = st.radio(
    "Choose distribution type:",
    ["σ known: Z distribution", "σ unknown: t distribution"])
    if dist_type == "σ known: Z distribution":
        st.latex(r"""
        CI = \bar{x} \pm Z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}
        """)
        st.latex(r"""
        Z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}
        """)
        use_z = True
    else:
        st.latex(r"""
        CI = \bar{x} \pm t_{\alpha/2, \ df} \cdot \frac{s}{\sqrt{n}}
        """)
        st.latex(r"""
        T = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}
        """)
        use_z = False

with col2:
    sample_mean = st.number_input("Sample Mean (x̄)", value=105.0, step=0.1, format="%0.1f")
    if use_z == True:
        sigma = st.number_input("Population Std. Dev. (σ)", value=15.0, step=0.1, format="%0.1f")
    else:
        sigma = st.number_input("Sample Std. Dev. (s)", value=15.0, step=0.1, format="%0.1f")
    sample_size = st.slider("Sample Size (n)", 5, 300, 30)

with col3:
    mu_0 = st.number_input("Null Hypothesis Mean (μ₀)", value=100.0, step=0.1, format="%0.1f")
    alpha = st.select_slider("Significance Level (α)", options=[0.10, 0.05, 0.01], value=0.05)

# --- Calculations ---
se = sigma / np.sqrt(sample_size)
df = sample_size - 1
confidence = 1 - alpha
tail_type = "Two-tailed"

if use_z == True:
    critical = norm.ppf(1 - alpha/2)
    test_stat = (sample_mean - mu_0) / se
    p_value = 2 * (1 - norm.cdf(abs(test_stat)))
else:
    critical = t.ppf(1 - alpha/2, df=df)
    test_stat = (sample_mean - mu_0) / se
    p_value = 2 * (1 - t.cdf(abs(test_stat), df=df))

ci_low = sample_mean - critical * se
ci_high = sample_mean + critical * se
reject_null = (mu_0 < ci_low) or (mu_0 > ci_high)

# --- CI plot ---
st.write("### 2️⃣ Sampling Distribution | 取樣分布")
st.markdown(f"""
- **Null Hypothesis (H₀)**: μ = μ₀ = {mu_0}  
  **虛無假設**：母體平均數等於 {mu_0}

- **Alternative Hypothesis (H₁)**: μ ≠ {mu_0}  
  **對立假設**：母體平均數不等於 {mu_0}（雙尾檢定）
""")

fig, ax = plt.subplots(figsize=(10, 2.5))
x = np.linspace(sample_mean - 4 * se, sample_mean + 4 * se, 500)
y = norm.pdf(x, loc=sample_mean, scale=se)

ax.plot(x, y, label='Sampling distribution of x̄')
ax.axvline(ci_low, color='green', linestyle=':', label='Lower CI bound')
ax.axvline(ci_high, color='green', linestyle=':', label='Upper CI bound')
ax.axvline(sample_mean, color='black', linestyle='-', label='Sample Mean')
ax.axvline(mu_0, color='red', linestyle='--', label='Null Mean (μ₀)')

ax.fill_between(x, 0, y, where=(x < ci_low) | (x > ci_high), color='orange', alpha=0.3, label='Rejection Region')
ax.legend()
st.pyplot(fig)

# --- Output Summary ---
st.write("")
st.write("### 3️⃣ Conclusion Summary | 結論摘要")

st.markdown("#### 🔸 Confidence Interval")
st.markdown(f"""
- **Confidence Level**: {int(confidence*100)}%  
- **Interval Estimate**: [{ci_low:.2f}, {ci_high:.2f}]  
- **Interpretation**: The population mean is estimated to fall within this interval with {int(confidence*100)}% confidence.  
- **解釋**：在 {int(confidence*100)}% 的信心水準下，推論母體平均數可能落在此區間內。
""")

st.markdown("#### 🔸 Hypothesis Testing")
st.markdown(f"""
- **Null Hypothesis (H₀)**: μ = {mu_0}  
- **Sample Mean**: x̄ = {sample_mean:.2f}  
- **Degree of freedom**: df = {sample_size} - 1 = {df}
- **Test Statistic**: {test_stat:.2f}  
- **p-value**: {p_value:.4f}  
- **Interpretation**: A p-value less than α = {alpha} indicates significant evidence against H₀.  
- **解釋**：p 值若小於顯著水準 α = {alpha}，表示拒絕 H₀，達統計上的顯著差異。
""")

st.markdown("#### 🔸 Conclusion")
if reject_null:
    st.success("""
🔴 Reject the null hypothesis H₀.  
There is **statistically significant evidence** to support the alternative hypothesis H₁.

---

🔴 拒絕虛無假設 H₀，有統計上的顯著證據支持對立假設 H₁。  
因為 μ₀ 不在信賴區間內，且 p 值 < α，  
我們有足夠的統計證據支持 H₁。
""")
else:
    st.info("""
🟢 Fail to reject the null hypothesis H₀.  
There is **not enough statistical evidence** to support the alternative hypothesis H₁.
            
---
            
🟢 無法拒絕虛無假設 H₀，沒有足夠的統計證據支持對立假設 H₁。  
因為 μ₀ 落在信賴區間內，且 p 值 > α，  
目前沒有足夠的統計證據支持 H₁。
""")







# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")