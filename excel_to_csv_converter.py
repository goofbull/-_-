import pandas as pd

data_xls = pd.read_excel('./excel_files/data.xlsx', 'Sheet1', index_col=None)
data_xls.to_csv('./csv/arbitr_dataset_for_training.csv', encoding='utf-8')

data_xls = pd.read_excel('./excel_files/data_for_testing.xlsx', 'Sheet1', index_col=None)
data_xls.to_csv('./csv/arbitr_dataset_for_testing.csv', encoding='utf-8')