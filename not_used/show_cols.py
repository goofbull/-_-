import pandas as pd

# Загрузка CSV-файла
df = pd.read_csv('justice.csv')

# Вывод названий колонок
print(df.columns.tolist())
