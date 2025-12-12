import pandas as pd
import matplotlib.pyplot as plt

key_length = list(range(1, 61))
acc_list_1_str = [
'0%', '0%', '0%', '75.0%', '0%', '88.33%', '0%', '85.0%', '86.66%', '91.0%', '0%', '81.66%', '0%', '89.28%', '89.33%', '90.0%', '0%', '91.11%', '0%', '91.5%', '86.19%', '91.81%', '0%', '89.58%', '86.0%', '88.84%', '89.62%', '89.64%', '0%', '94.66%', '0%', '92.81%', '90.60%', '92.94%', '88.85%', '94.16%', '0%', '92.63%', '92.05%', '91.5%', '2.439%', '91.66%', '0%', '93.63%', '91.33%', '90.0%', '0%', '91.04%', '88.57%', '92.80%', '91.37%', '94.61%', '0%', '91.48%', '89.45%', '92.5%', '92.63%', '93.10%', '3.389%', '91.16%']

acc_list_2_str = [
'0%', '0%', '0%', '5.0%', '0%', '5.0%', '0%', '65.0%', '0%', '34.0%', '0%', '76.66%', '0%', '63.57%', '0%', '71.87%', '0%', '77.22%', '0%', '74.0%', '59.52%', '76.36%', '0%', '82.08%', '9.6%', '68.84%', '81.85%', '76.07%', '0%', '82.66%', '0%', '82.81%', '81.81%', '75.29%', '87.71%', '84.44%', '0%', '71.84%', '78.71%', '83.0%', '2.439%', '81.66%', '0%', '83.40%', '81.77%', '73.04%', '0%', '85.0%', '12.04%', '85.8%', '83.13%', '86.34%', '0%', '80.92%', '86.72%', '83.21%', '84.56%', '75.34%', '3.389%', '82.83%']

acc_list_1_str = [100-float(a[:-1]) for a in acc_list_1_str]
acc_list_2_str = [100-float(a[:-1]) for a in acc_list_2_str]

df = pd.DataFrame({
    'Key_Length': key_length,
    'Kasiski': acc_list_1_str,
    'IoC': acc_list_2_str
})


plt.figure(figsize=(12, 6))

plt.plot(df['Key_Length'], df['Kasiski'], label='Kasiski (Avg acc: 30.64%)', marker='o', linestyle='-', markersize=4)
plt.plot(df['Key_Length'], df['IoC'], label='IoC (Avg acc: 43.32%)', marker='o', linestyle='-', markersize=4)

plt.title('Accuracy vs. Key-Length (kl)', fontsize=16)
plt.xlabel('Key-Length (kl)', fontsize=14)
plt.ylabel('Accuracy (%)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(range(0, 61, 5))
plt.ylim(0, 120)
plt.tight_layout()

# print('accuracy_vs_key_length.png')
# plt.savefig('accuracy_vs_key_length.png')

plt.show()