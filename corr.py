import pandas as pd
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('./csv/prepared_data.csv')
df_encoded = df.copy()

# Кодируем категориальные столбцы
for column in df_encoded.columns:
    if df_encoded[column].dtype == 'object':
        df_encoded[column] = LabelEncoder().fit_transform(df_encoded[column].astype(str))

corr_matrix = df_encoded.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Корреляционная матрица")
plt.show()