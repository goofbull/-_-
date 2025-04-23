import pandas as pd
import csv
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

stop_words_set = {"я", "ты", "он", "она", "оно", "мы", "вы", "они", "не", "нет", "того" "это", "тот", "та", "те", "который", "чей", "кто", "что", 
                      "да", "а", "но", "и", "или", "да", "также", "же", "ли", "бы", "для", "от", "из", "с", "на", 
                      "в", "по", "к", "у", "о", "об", "при", "для", "за", "перед", "после", "до", "через", "между", "над", 
                      "под", "вокруг", "из-за", "около", "через", "вон", "про", "между", "если", "когда", "пока", "хотя", 
                      "как", "так", "потому что", "чтобы", "ибо", "то есть", "где", "когда", "куда", "откуда", "уж", "вот", "вот такой", 
                      "именно", "вот это", "тот", "всё", "вся", "все", "некоторый", "несколько", "один", "два", "три", "первый", "второй", 
                      "последний", "каждый", "любой", "любой", "даже", "довольно", "вовсе", "только", "никогда", "всегда", "потом", "когда-то", 
                      "везде", "впрочем", "мало", "много", "больше", "меньше", "слишком", "скорее", "уж", "как бы", "например", "например", 
                      "возможно", "следует", "конечно", "вроде", "чем", "что-то", "тот", "этот", "такой", "никакой", "другой", "так как", 
                      "а вот", "пусть", "либо", "просто", "типо", "короче", "хотя бы", "и так далее", "далее", "есть", "потому", "то", "поскольку", "б"}

filename = './csv/arbitr_dataset_for_training.csv'
def read_cell(x, y, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

with open('./csv/prepared_data.csv', 'w', newline='', encoding='utf-8') as file:

    writer = csv.writer(file)
    field = ["data", "decision"]

    writer.writerow(field)
    for i in range(1, 100 + 1):
        text = read_cell(11, i, filename)
        dec = read_cell(13, i, filename)
        if text == '' or dec == '' or text == None or dec == None:
            pass
        else:
            writer.writerow([text, dec])

    print('\ncsv Data copied to target csv files')

filename = './csv/arbitr_dataset_for_testing.csv'
with open('./csv/prepared_data_for_testing.csv', 'w', newline='', encoding='utf-8') as file:

    writer = csv.writer(file)
    field = ["data", "decision"]

    writer.writerow(field)
    for i in range(1, 100 + 1):
        text = read_cell(11, i, filename)
        dec = read_cell(13, i, filename)
        if text == '' or dec == '' or text == None or dec == None:
            pass
        else:
            writer.writerow([text, dec])

    print('\ncsv Data copied to target csv files')



