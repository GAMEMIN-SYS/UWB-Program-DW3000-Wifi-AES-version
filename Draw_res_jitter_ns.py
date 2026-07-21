import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 非加密數據（💡 修正點 1：補上字典各欄位結尾漏掉的逗號）
data = {
    'Tags':          [1, 2, 3, 4, 5],
    'Residual':      [0.0164, 0.0171, 0.0197, 0.0196, 0.0194],
    'Raw_Data_Jump': [0.8804, 0.9511, 0.8791, 0.8701, 0.9107],
    'TOF_Delay':     [0.00128 , 0.00201 , 0.00121,0.00111,0.00167]
}

df = pd.DataFrame(data) 

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# 左圖: Raw_Data_Jump
sns.lineplot(ax=axes[0], data=df, x='Tags', y='Raw_Data_Jump', marker='s', label='Distance STD', color='g', errorbar=None)
axes[0].set_title('Distance', fontsize=14)
axes[0].set_xlabel('Number of Distance')
axes[0].set_ylabel('Distance(m)')
# 💡 修正點 2：將刻度從 [1, 2, 3, 4] 改成 [1, 2, 3, 4, 5]，防止 Tag 5 的數據在圖上邊緣被切掉
axes[0].set_xticks([1, 2, 3, 4, 5])
axes[0].legend()

# 右圖: TOF_Delay
sns.lineplot(ax=axes[1], data=df, x='Tags', y='TOF_Delay', marker='o', label='inter-arrival Time STD', color='orange', errorbar=None)
axes[1].set_title('inter-arrival Time', fontsize=14)
axes[1].set_xlabel("Number of inter-arrival Time")
axes[1].set_ylabel('inter-arrival Time(s)')
# 💡 修正點 3：右圖的 X 軸刻度也同步改為 [1, 2, 3, 4, 5]
axes[1].set_xticks([1, 2, 3, 4, 5])
axes[1].legend()

plt.tight_layout()
plt.show()