import csv
import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import category_encoders as ce
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
import srsly.ujson


nlp = spacy.load("ru_core_news_sm")

df = pd.read_csv('./csv/arbitr_dataset.csv')

#print(df.isnull().sum())

def read_cell(x, y):
    with open('./csv/arbitr_dataset.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1


low_reg_text = []
for i in range(1, 2 + 1):
        text = read_cell(3, i)
        low_reg_text = nlp(text.lower())
        print("СТРОКА ", i, " ОБРАБОТАНА")


documents = low_reg_text

# clean_text, judge, articles, location
X = df.drop(['Unnamed: 0', 'index', 'text', 'case_number', 'number_of_words_in_text', 'publication_date', 'claimant', 'defendant', 'decision'], axis=1)
y = df['prediction']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=44)

print(X_train.shape, X_test.shape)
print(X_train.dtypes)

encoder = ce.OrdinalEncoder(cols=['clean_text', 'judge', 'doarticlesors', 'location'])


X_train = encoder.fit_transform(X_train)

X_test = encoder.transform(X_test)





model = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(y_pred)