import pandas as pd
import matplotlib.pyplot as plt
from test6 import number_of_docs
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
    #print(all_words_list)

    unique_words = list(set(all_words_list))

    with open('./csv/words_frequency.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        field = ["word", "frequency"]

        writer.writerow(field)
        
        for word in unique_words:
            frequency = counter[word]
            row = [word, frequency]
            writer.writerow(row)

#make_words_frequency_csv()
data = pd.read_csv('./csv/words_frequency.csv')

fig = px.bar(data, x="word", y="frequency", title="Histogram of Unique Words Frequency", color = 'frequency')
fig.show()

# # Plot a histogram of the 'Age' column
# data['clean_text'].plot.hist()
# plt.xlabel('Age')
# plt.title('Age Distribution')
# plt.show()