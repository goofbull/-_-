import pandas as pd
from collections import Counter
import csv
import plotly.express as px
import os


def read_cell(x, y, filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

def make_words_frequency_csv(filename: str):
    all_words_list = []

    text = read_cell(3, 1, filename)
    split_into_words_text = text.split()
    for word in split_into_words_text:
        all_words_list.append(word)
        #print("СТРОКА ", i, " ОБРАБОТАНА")

    counter = Counter(all_words_list)

    unique_words = list(set(all_words_list))

    with open('./csv/words_frequency.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ["word", "frequency"]

        writer.writerow(field)
        
        for word in unique_words:
            frequency = counter[word]
            row = [word, frequency]
            writer.writerow(row)
    #return all_words_list

def show_density(filename: str):

    if not os.path.exists("images"):
        os.mkdir("images")

    new_filename = './csv/' + filename + '.csv'
    make_words_frequency_csv(new_filename)
    dataset = pd.read_csv('./csv/words_frequency.csv')

    fig = px.bar(dataset, x="word", y="frequency", title="Histogram of Unique Words Frequency", color = 'frequency')
    fig.show()
    fig.write_image("images/fig1.pdf")