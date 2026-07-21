import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# ================= 1. 輸入你的實驗數據 =================

n_samples = 150000

categories = [
    'AES + 4B Counter IV',
    'AES + 4B Random IV'
]

# Mean (m)
means = [
    0.9874,
    0.9108
]

# Standard Deviation (m)
stds = [
    0.0324,
    8.7308
]

# ================= 2. 計算 95% Confidence Interval =================

def calculate_ci(means, stds, n):
    ci_err = []

    for m, s in zip(means, stds):

        se = s / np.sqrt(n)

        t_crit = stats.t.ppf(0.975, df=n-1)

        margin = t_crit * se

        ci_err.append(margin)

    return ci_err

ci_err = calculate_ci(means, stds, n_samples)

# ================= 3. Welch t-test =================

t_stat, p_value = stats.ttest_ind_from_stats(
    mean1=means[0],
    std1=stds[0],
    nobs1=n_samples,

    mean2=means[1],
    std2=stds[1],
    nobs2=n_samples,

    equal_var=False       # Welch's t-test
)

print("="*40)
print("Welch's t-test")
print("="*40)

print(f"T statistic : {t_stat:.6f}")
print(f"P-value     : {p_value:.8e}")

if p_value < 0.001:
    print("Result : p < 0.001 (Highly Significant)")
elif p_value < 0.01:
    print("Result : p < 0.01")
elif p_value < 0.05:
    print("Result : p < 0.05")
else:
    print("Result : Not Significant")

# ================= 4. Confidence Interval =================

print("\n95% Confidence Interval")

for i in range(len(categories)):

    lower = means[i] - ci_err[i]
    upper = means[i] + ci_err[i]

    print(f"{categories[i]}")
    print(f"Mean = {means[i]:.4f}")
    print(f"SE   = {stds[i]/np.sqrt(n_samples):.6f}")
    print(f"95% CI = ({lower:.4f}, {upper:.4f})")
    print()

# ================= 5. Plot =================

x = np.arange(len(categories))

fig, ax = plt.subplots(figsize=(8,6))

bars = ax.bar(
    x,
    means,
    yerr=ci_err,
    capsize=6,
    color=["#4A81DA","#36C756"]
)

ax.bar_label(
    bars,
    fmt="%.4f",
    padding=8,
    fontsize=11
)

ax.set_ylabel("Distance Mean (m)")
ax.set_xticks(x)
ax.set_xticklabels(categories)

ax.set_title("Distance Comparison with 95% CI")

ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()