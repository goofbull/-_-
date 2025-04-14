
# df = pd.read_csv('./csv/words_frequency.csv', header=None)
# print(df.shape)
# print(df.head())
#df.info()


import csv
from prettytable import PrettyTable
import webbrowser
filename = "./csv/arbitr_dataset.csv"
# Read CSV data.
with open(filename, 'r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file)
    columns = next(reader)
    rows = [row for row in reader]

# Create HTML table from it.
tbl = PrettyTable(columns)
for row in rows:  # Add data to table.
    tbl.add_row(row)

with open('table.html', 'w', encoding='utf-8') as html_file:
    html_file.write(tbl.get_html_string())

webbrowser.open('table.html', new=1) 