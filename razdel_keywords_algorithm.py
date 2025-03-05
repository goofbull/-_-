
from razdel import tokenize, sentenize
import nltk
from nltk.corpus import stopwords 
from pymorphy3 import MorphAnalyzer
from navec import Navec 
import slovnet
import os
import pickle
from docx import Document
nltk.download("stopwords")

def segment_text(doc: str|dict) -> dict:
    if isinstance(doc, str): 
        doc = {"text": doc}
    doc ["tokens"] = []
    for sent in sentenize(doc ["text"]):
        doc ["tokens"].append( [_.text for _ in tokenize (sent.text)])
    return doc

analyzer = MorphAnalyzer()
stop_words = stopwords.words ("russian")
pos = { 'NOUN', 'ADJF', 'ADJS', 'VERB', 'INFN', 'PRTF', 'PRTS'}

def extract_candidates (doc: dict, stop_words: list = stop_words, pos: set = pos) -> dict:
    res = set()
    for sent in doc ["tokens"]:
        for token in sent:
            if token in stop_words or token in res:
                continue
            parsed = analyzer.parse(token) [0]

            if parsed.tag.POS not in pos:
                continue

            res.add(token)
    doc["candidates"] = res
    return doc


navec = Navec.load("navec_news_v1_1B_250K_300d_100q.tar")
syntax = slovnet.Syntax.load("slovnet_syntax_news_v1.tar")
syntax.navec(navec)


def syntax_collocations(doc: dict, syntax: slovnet.api.Syntax = syntax) -> dict:
    syntax_colloc = []
    for sent in doc ["tokens"]:

        syntax_markup = syntax(sent)

        sent_word_id = {}
        for token in syntax_markup.tokens: 
            sent_word_id[token.id] = token.text
        for token in syntax_markup.tokens:
            if token.head_id !='0' and token.text in doc["candidates"]:
                syntax_colloc.append(sent_word_id[token.head_id] + ' ' + token.text)
    doc["collocations"] = set(syntax_colloc)
    return doc

myfile = open("text.txt", "rt")
text = myfile.read()
myfile.close()

doc = segment_text(text)
doc = extract_candidates(doc)
doc = syntax_collocations(doc)

result = doc["collocations"]
print(result)

directory = "./compare_results_keywords/"
filename = "razdel_keywords_result.docx"
file_path = os.path.join(directory, filename)

document = Document()

list_result = list(result)
with open(file_path, 'wb') as file:
    for word in list_result:
        document.add_paragraph(word)

document.save(file_path)