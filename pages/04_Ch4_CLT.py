import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, t
import time

# --- Set up the Streamlit page layout and metadata ---
st.set_page_config(
    page_title="Central Limit Theorem", 
    page_icon="📊",
    layout="wide", 
    initial_sidebar_state="auto",
    menu_items={
        'About': "This work authored by Teddy (Yen-Hsiang Huang) from the NCHU, Taiwan.",
        'Get Help': 'https://github.com/TeddYenn/stat2vis',
        'Report a bug': "https://github.com/TeddYenn/stat2vis/issues"
    })

# --- App header and introduction ---
st.title("Ch. 4: Central Limit Theorem (CLT)  |  中央極限定理")
st.caption("**Developed by Teddy (Yen-Hsiang Huang)**")

# Introduction (bilingual)
st.write("The Central Limit Theorem states that **regardless of the original population distribution, the sampling distribution of the sample mean will approximate a normal distribution as long as sufficiently large random samples are repeatedly drawn.** In practice, this approximation is generally considered reliable when the sample size is 30 or more. This property allows us to assume a normal sampling distribution of the sample mean—even when the population distribution is unknown—and apply normal-based statistical inference accordingly. Therefore, the Central Limit Theorem provides the theoretical foundation for many inference methods focused on the mean, such as t-tests and confidence interval estimation.")
st.write("**CLT：「不論母體分布為何，只要從中重複抽取足夠多的隨機樣本(樣本大小)，其樣本平均數的取樣分布將會趨近於常態分布。」** 實務上，當樣本大小達到30以上時，近似通常已相當可靠。此性質使我們即使在不知道母體實際分布形狀的情況下，仍能假設樣本平均數的取樣分布近似常態，進而針對平均數使用常態分布模型來進行統計推論。因此，中央極限定理是許多以平均值為推論對象的方法（如t-test與信賴區間）的基礎理論。")

# --- Section 1: User inputs ---
distribution_options = {
    "Normal Dist. (μ=0, σ=1)": "Normal Dist.",
    "Exponential Dist. (λ=1)": "Exponential Dist.",
    "Uniform Dist. (-2, 2)": "Uniform Dist."
}

st.write("")
st.write("")
st.write("### 1️⃣ Parameters  |  參數設定")
col1, col2 = st.columns(2)
with col1:
    dist_label = st.selectbox("Select a distribution (母體分布)", list(distribution_options.keys()))
    dist_type = distribution_options[dist_label]
    sample_size = st.slider("Sample size (n) (樣本大小)", 2, 200, 30, 1)
    num_samples = st.slider("Number of samples (抽樣次數)", 10, 1000, 500, 10)

st.markdown("---")

# --- Generate Population Function ---
def generate_population(dist_type, size=100000):
    np.random.seed(42)
    if dist_type == "Normal Dist.":
        return np.random.normal(loc=0, scale=1, size=size)
    elif dist_type == "Exponential Dist.":
        return np.random.exponential(scale=1, size=size)
    elif dist_type == "Uniform Dist.":
        return np.random.uniform(low=-2, high=2, size=size)
    
# --- Generate Population ---
population = generate_population(dist_type)

st.write("### 2️⃣ Distributions  |  分布")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Population Distribution | 母體分布")
with col2:
    st.subheader("Distribution of Sample Means | 樣本平均值分布")
    run_animation = st.button("▶️ Animate Sampling")
    show_final = st.button("⏩ Show Final Distribution")

col1, col2 = st.columns(2)

# --- Plot 1: Population Distribution ---
with col1:
    fig_pop, ax_pop = plt.subplots()
    sns.histplot(population, bins=50, kde=True, ax=ax_pop)
    ax_pop.set_title("Population Distribution")
    ax_pop.set_xlabel("Mean")
    ax_pop.set_ylabel("Count")
    st.pyplot(fig_pop)

    if dist_type == "Normal Dist.":
        pop_mean = 0
        pop_std = 1
    elif dist_type == "Exponential Dist.":
        pop_mean = 1
        pop_std = 1
    elif dist_type == "Uniform Dist.":
        pop_mean = 0
        pop_std = np.sqrt((2 - (-2))**2 / 12)

    st.markdown(f"""
    **Summary of Population Dist.**  
    - Mean (μ): `{pop_mean:.4f}`  
    - Standard Deviation (σ): `{pop_std:.4f}`  
    """)

# --- Plot 2: Sampling Distribution ---

with col2:

    sample_means = []
    placeholder = st.empty()

    mu = np.mean(population)
    sigma = np.std(population)
    theoretical_std = sigma / np.sqrt(sample_size)

    if run_animation:
        for i in range(num_samples):
            sample = np.random.choice(population, size=sample_size, replace=False)
            sample_means.append(np.mean(sample))

            x = np.linspace(min(sample_means), max(sample_means), 200)
            y = norm.pdf(x, loc=mu, scale=theoretical_std)

            with placeholder.container():
                fig2, ax2 = plt.subplots()
                sns.histplot(sample_means, bins=30, kde=False, color='orange', stat='density', ax=ax2)
                ax2.plot(x, y, color='blue', linestyle='--', label=f"Theoretical Normal (μ={mu:.2f}, σ/√n={theoretical_std:.2f})")
                ax2.legend()
                ax2.set_title(f"Sampling Distribution (1~{i+1} samples)")
                ax2.set_xlabel("Sample Mean")
                ax2.set_ylabel("Density")
                st.pyplot(fig2)

            time.sleep(0.01)

    elif show_final:
        for i in range(num_samples):
            sample = np.random.choice(population, size=sample_size, replace=False)
            sample_means.append(np.mean(sample))

        x = np.linspace(min(sample_means), max(sample_means), 200)
        y = norm.pdf(x, loc=mu, scale=theoretical_std)

        with placeholder.container():
            fig2, ax2 = plt.subplots()
            sns.histplot(sample_means, bins=30, kde=False, color='orange', stat='density', ax=ax2)
            ax2.plot(x, y, color='blue', linestyle='--', label=f"Theoretical Normal Dist.")
            ax2.legend()
            ax2.set_title(f"Sampling Distribution ({num_samples} samples)")
            ax2.set_xlabel("Sample Mean")
            ax2.set_ylabel("Density")
            st.pyplot(fig2)

    mean_of_sample_means = np.mean(sample_means)
    std_of_sample_means = np.std(sample_means)

    st.markdown(f"""
    **Summary of Sample Means Dist.**  
    - Mean: `{mean_of_sample_means:.4f}`  
    - Standard deviation: `{std_of_sample_means:.4f}`  
    ---
    **Summary of Theoretical Normal Dist.**
    - Mean(μ): `{pop_mean:.4f}`  
    - Standard deviation (σ/√n): `{theoretical_std:.4f}`  
    """)

# Footer
st.markdown("---")
st.write("stat2vis: Collection of Applications for Visualizing Statistics")
st.write("GitHub: https://github.com/TeddYenn/stat2vis")