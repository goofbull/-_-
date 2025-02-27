
from razdel import tokenize, sentenize
import nltk
from nltk.corpus import stopwords 
from pymorphy3 import MorphAnalyzer
from navec import Navec 
import slovnet
import spacy



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

sent = "Сложно представить задачу более востребованную и частотную, чем задачу текстового поиска. Упростить ее помогают совершенно разные инструменты и методы, однако универсального решения нет. Как один из оптимальных вариантов в статье представлен парсер библиотеки Natasha для поиска почти любой структурированной информации в тексте."
doc = segment_text(sent)

syntax_markup = syntax(["tokens"][0])
for token_info in syntax_markup.tokens:
    print(token_info)

sent_word_id ={}
for token in syntax_markup.tokens:
    sent_word_id[token.id] = token.text


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

text = "Сложно представить задачу более востребованную и частотную, чем задачу текстового поиска. Упростить ее помогают совершенно разные инструменты и методы, однако универсального решения нет. Как один из оптимальных вариантов в статье представлен парсер библиотеки Natasha для поиска почти любой структурированной информации в тексте."
doc = segment_text(text)
doc = extract_candidates(doc)
doc = syntax_collocations(doc)
print(doc["collocations"])