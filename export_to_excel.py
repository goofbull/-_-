import os
import pandas as pd
import xlsxwriter
from test6 import get_dict_with_data

def create_empty_excel(columns: list, filename: str, sheet_name: str = 'arbitr_files_dataset'):
    df = pd.DataFrame(columns=columns)

    if not os.path.exists('excel_files'):
        os.makedirs('excel_files')

    filepath = os.path.join('excel_files', filename)
    excel_writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    df.to_excel(excel_writer, index=False, sheet_name=sheet_name, freeze_panes=(1, 0))
    excel_writer._save()

    return filepath, df

columns = ['index', 'text', 'clean_text', 'judge', 'case_number', 'publication_date', 'articles', 'number_or_words_in_text', 'claimant', 'defendant', 'location', 'decision']

def create_tabel():
    filepath, df = create_empty_excel(columns=columns,
                                  filename='data.xlsx')
    return df, filepath


df, filepath = create_tabel()

dict = get_dict_with_data()
number_of_files = 100
active_file_number = ''



for i in range(1, number_of_files + 1):
    current_row = i
    df.loc[current_row] = [None] * len(columns)
    active_file_number = str(i)
    x = dict[active_file_number]
    u = 0
    for u, y in enumerate(x):
        if u < len(columns):
            df.at[current_row, columns[u]] = y

df.to_excel('excel_files/data.xlsx', index=False)


