import pandas as pd
import matplotlib.pyplot as plt
from extract_data import number_of_docs
from collections import Counter
import csv
import plotly.express as px


def read_cell(x, y):
    with open('./csv/arbitr_dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

def make_words_frequency_csv():
    all_words_list = []
    for i in range(1, 2 + 1):
        text = read_cell(3, i)
        split_into_words_text = text.split()
        for word in split_into_words_text:
            all_words_list.append(word)
        print("СТРОКА ", i, " ОБРАБОТАНА")

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
    return all_words_list


#make_words_frequency_csv()
dataset = pd.read_csv('./csv/words_frequency.csv')

fig = px.bar(dataset, x="word", y="frequency", title="Histogram of Unique Words Frequency", color = 'frequency')
fig.show()


