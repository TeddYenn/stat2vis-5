import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, norm

# --- Set up the Streamlit page layout and metadata ---
st.set_page_config(
    page_title="Two-sample CI & HT", 
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'About': "This work authored by Teddy (Yen-Hsiang Huang) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# --- App header and introduction ---
st.title("Ch. 6: Two-sample Test  |  雙樣本檢定")
st.caption("**Developed by Teddy (Yen-Hsiang Huang)**")

# --- Introduction ---
st.write("This chapter explains how to conduct statistical inference for comparing two population means. Depending on the independence of the samples and assumptions about variances, the appropriate form of the t-test is selected. The results of confidence interval estimation and hypothesis testing are illustrated.")
st.write("本章節說明如何針對兩組母體平均數進行統計推論，並依據樣本的獨立性與變異數假設，選用合適的 t 檢定，展示信賴區間與假設檢定結果。")

# --- Test type selection ---
st.write("### 1️⃣ Select Test Type | 檢定類型")

col1, col2, col3 = st.columns(3)
with col1:
    test_type = st.radio(
    "Choose distribution type:",
    ["Pooled t-test (equal variance)", "Welch's t-test (unequal variance)"]
    )

with col2:
    if test_type == "Pooled t-test (equal variance)":
        st.latex(r"""
        \text{CI} = (\overline{x}_1 - \overline{x}_2) \pm t_{n_1 + n_2 - 2,\,\alpha/2} \cdot \sqrt{ s_p^2 \left( \frac{1}{n_1} + \frac{1}{n_2} \right) }
        """)
        st.latex(r"""
        s_p^2 = \frac{ (n_1 - 1)s_1^2 + (n_2 - 1)s_2^2 }{ n_1 + n_2 - 2 }
        """)

    elif test_type == "Welch's t-test (unequal variance)":
        st.latex(r"""
        \text{CI} = (\overline{x}_1 - \overline{x}_2) \pm t_{df,\,\alpha/2} \cdot \sqrt{ \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} }
        """)
        st.latex(r"""
        df = \frac{ \left( \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} \right)^2 }{ \frac{ (s_1^2/n_1)^2 }{ n_1 - 1 } + \frac{ (s_2^2/n_2)^2 }{ n_2 - 1 } }
        """)


    elif test_type == "Paired t-test":
        st.latex(r"""
        CI = \bar{D} \pm t^* \cdot \frac{s_D}{\sqrt{n}}
        """)

with col3:
    if test_type == "Pooled t-test (equal variance)":
        st.latex(r"""
        T = \frac{\overline{x}_1 - \overline{x}_2}{\sqrt{ s_p^2 \left( \frac{1}{n_1} + \frac{1}{n_2} \right) }}
        """)

    elif test_type == "Welch's t-test (unequal variance)":
        st.latex(r"""
        T = \frac{\overline{x}_1 - \overline{x}_2}{\sqrt{ \frac{s_1^2}{n_1} + \frac{s_2^2}{n_2} }}
        """)

    elif test_type == "Paired t-test":
        st.latex(r"""
        t = \frac{\bar{D}}{s_D / \sqrt{n}}
        """)

# --- Parameter input ---
st.write("### 2️⃣ Parameter Settings | 參數設定")

col1, col2 = st.columns(2)
with col1:
    mu1 = st.number_input("Group 1 Mean (x̄₁)", value=100.0, step=0.1, format="%0.1f")
    sd1 = st.number_input("Group 1 Std. Dev. (s₁)", value=15.0, step=0.1, format="%0.1f")
    n1 = st.slider("Group 1 Sample Size (n₁)", 5, 300, 30)
    alpha = st.select_slider("Significance Level (α)", options=[0.10, 0.05, 0.01], value=0.05)

with col2:
    mu2 = st.number_input("Group 2 Mean (x̄₂)", value=110.0, step=0.1, format="%0.1f")
    sd2 = st.number_input("Group 2 Std. Dev. (s₂)", value=15.0, step=0.1, format="%0.1f")
    n2 = st.slider("Group 2 Sample Size (n₂)", 5, 300, 30)

# --- Mean difference and standard error ---
mean_diff = mu1 - mu2

if test_type == "Pooled t-test (equal variance)":
    # Pooled standard deviation
    sp_squared = ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)
    se_diff = np.sqrt(sp_squared * (1/n1 + 1/n2))
    df = n1 + n2 - 2
elif test_type == "Welch's t-test (unequal variance)":
    se_diff = np.sqrt((sd1**2 / n1) + (sd2**2 / n2))
    df_num = (sd1**2 / n1 + sd2**2 / n2)**2
    df_den = ((sd1**2 / n1)**2 / (n1 - 1)) + ((sd2**2 / n2)**2 / (n2 - 1))
    df = df_num / df_den
elif test_type == "Paired t-test":
    # Assume each group has the same sample size and std dev of differences is known
    sd_diff = st.number_input("Std Dev of Differences (σ_d)", value=10.0)
    se_diff = sd_diff / np.sqrt(n1)
    df = n1 - 1

# --- t test ---
test_stat = mean_diff / se_diff
p_value = 2 * (1 - t.cdf(abs(test_stat), df))
reject_null = p_value < alpha

# --- Critical values ---
t_crit = t.ppf(1 - alpha / 2, df)
crit_left = 0 - t_crit * se_diff
crit_right = 0 + t_crit * se_diff

# --- Plot distributions ---
st.write("### 3️⃣ Sampling Distribution | 取樣分布")
st.markdown(f"""
- **Null Hypothesis (H₀)**: μ₁ = μ₂  
  **虛無假設**：兩群母體平均數相等，無差異

- **Alternative Hypothesis (H₁)**: μ₁ ≠ μ₂
  **對立假設**：兩群母體平均數不相等
""")

# Create x and y values
x = np.linspace(mean_diff - 8 * se_diff, mean_diff + 8 * se_diff, 500)
y_h0 = norm.pdf(x, loc=0, scale=se_diff)
y_h1 = norm.pdf(x, loc=mean_diff, scale=se_diff)

# Calculate Type II Error (β)
beta = norm.cdf(crit_right, loc=mean_diff, scale=se_diff) - norm.cdf(crit_left, loc=mean_diff, scale=se_diff)
power = 1 - beta

# Create figure
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.plot(x, y_h0, label="H₀ Distribution (mean diff = 0)", color="blue")
ax.plot(x, y_h1, label=f"H₁ Distribution (mean diff = {mean_diff:.2f})", color="orange")

# Critical regions
ax.axvline(crit_left, linestyle='-', color="black", label=f"Critical t = ±{t_crit:.2f}")
ax.axvline(crit_right, linestyle='-', color="black")

# Fill α regions under H0
x_alpha_left = x[x <= crit_left]
x_alpha_right = x[x >= crit_right]
ax.fill_between(x_alpha_left, norm.pdf(x_alpha_left, 0, se_diff), color='red', alpha=0.3, label=f"Type I Error (α = {alpha:.2f})")
ax.fill_between(x_alpha_right, norm.pdf(x_alpha_right, 0, se_diff), color='red', alpha=0.3)

# β region
x_beta = x[(x > crit_left) & (x < crit_right)]
ax.fill_between(x_beta, norm.pdf(x_beta, mean_diff, se_diff), color='skyblue', alpha=0.4, label=f"Type II Error (β ≈ {beta:.2f})")

# CI boundaries
ci_lower = mean_diff - t_crit * se_diff
ci_upper = mean_diff + t_crit * se_diff
ax.axvline(ci_lower, color='green', linestyle=':', label=f"CI Lower ≈ {ci_lower:.2f}")
ax.axvline(ci_upper, color='green', linestyle=':', label=f"CI Upper ≈ {ci_upper:.2f}")

# Sample observed t (converted back to value)
sample_t = (mean_diff - 0) / se_diff  # observed t from sample
sample_x = sample_t * se_diff         # transform back to raw score (same as mean_diff)
ax.axvline(sample_x, color='red', linestyle='--', label=f"Sample Mean Diff = {sample_x:.2f}")

ax.legend(fontsize="small")
st.pyplot(fig)

# --- Output summary ---
st.write("")
st.write("### 3️⃣ Conclusion Summary | 結論摘要")

confidence = 1 - alpha

st.markdown("#### 🔸 Confidence Interval")
st.markdown(f"""
- **Confidence Level**: {int(confidence*100)}%  
- **Interval Estimate**: [{ci_lower:.2f}, {ci_upper:.2f}]  
- **Interpretation**: The population mean is estimated to fall within this interval with {int(confidence*100)}% confidence.  
- **解釋**：在 {int(confidence*100)}% 的信心水準下，推論母體平均數可能落在此區間內。
""")

st.markdown("#### 🔸 Hypothesis Testing")
st.markdown(f"""
- **Null Hypothesis (H₀)**: u₁ = u₂ = {mu2} 
- **Alternative Hypothesis (H₁)**: u₁ ≠ u₂
- **Degree of Freedom**: df = {df}  
- **Test Statistic**: {test_stat:.2f}  
- **p-value**: {p_value:.4f}  
- **Interpretation**: A p-value less than α = {alpha} indicates significant evidence against H₀.  
- **解釋**：p 值若小於顯著水準 α = {alpha}，表示拒絕 H₀，達統計上的顯著差異。
""")

st.markdown("#### 🔸 Conclusion")
if reject_null:
    st.success(f"""
🔴 Reject the null hypothesis H₀.  
There is **statistically significant evidence** to support the alternative hypothesis H₁.

---

🔴 拒絕虛無假設 H₀，有統計上的顯著證據支持對立假設 H₁。  
因為 μ₀ 不在信賴區間內，且 p 值 < α，  
我們有足夠的統計證據支持 H₁。
""")
else:
    st.info(f"""
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