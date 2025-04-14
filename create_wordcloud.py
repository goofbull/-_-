import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import csv


def read_cell(x, y):
    with open('./csv/arbitr_dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

all_words_dict = ''
for i in range(1, 2 + 1):
    text = read_cell(3, i)
    string = str(text)
    string.replace(',', '')
    all_words_dict = all_words_dict + string
    
print(all_words_dict)

cloud = WordCloud(max_font_size=80,colormap="hsv").generate(all_words_dict)
plt.figure(figsize=(16,12))
plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.show()