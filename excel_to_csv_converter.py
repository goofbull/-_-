import pandas as pd

# data_xls = pd.read_excel('./excel_files/data_for_training.xlsx', 'Sheet1', index_col=None)
# data_xls.to_csv('./csv/arbitr_dataset_for_training.csv', encoding='utf-8')

# data_xls = pd.read_excel('./excel_files/data_for_testing.xlsx', 'Sheet1', index_col=None)
# data_xls.to_csv('./csv/arbitr_dataset_for_testing.csv', encoding='utf-8')

def convert(filename:str):
    filename_new = './excel_files/' + filename + '.xlsx'
    data_xls = pd.read_excel(filename_new, 'Sheet1', index_col=None)
    csv_name = './csv/' + filename + '.csv'
    data_xls.to_csv(csv_name, encoding='utf-8')