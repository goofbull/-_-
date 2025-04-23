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

columns = ['index', 'text', 'clean_text', 'judge', 'case_number', 'publication_date', 'articles', 'number_of_words_in_text', 'claimant', 'defendant', 'research_data', 'location', 'decision']

def create_table(filename: str):
    filepath, df = create_empty_excel(columns=columns,
                                  filename=filename)
    return df, filepath

def make_excel_file(number_of_files: int, excel_directory: str):
    for i in range(1, number_of_files + 1):
        current_row = i
        df.loc[current_row] = [None] * len(columns)
        active_file_number = str(i)
        x = dict[active_file_number]
        u = 0
        for u, y in enumerate(x):
            if u < len(columns):
                df.at[current_row, columns[u]] = y
    df.to_excel(excel_directory, index=False)

directory = "./pdf_cases/"
filename='data_for_training.xlsx'


df, filepath = create_table(filename)

number_of_files = 100

dict = get_dict_with_data(directory, number_of_files)


active_file_number = ''
excel_directory = 'excel_files/data_for_training.xlsx'


make_excel_file(number_of_files, excel_directory)



directory = "./pdf_cases_for_testing/"
filename='data_for_testing.xlsx'


df, filepath = create_table(filename)


number_of_files = 100

dict = get_dict_with_data(directory, number_of_files)


active_file_number = ''
excel_directory = 'excel_files/data_for_testing.xlsx'

make_excel_file(number_of_files, excel_directory)