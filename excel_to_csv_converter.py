import pandas as pd

data_xls = pd.read_excel('./excel_files/data.xlsx', 'Sheet1', index_col=None)
data_xls.to_csv('./csv/arbitr_dataset.csv', encoding='utf-8')