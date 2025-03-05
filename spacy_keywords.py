import spacy

nlp = spacy.load("ru_core_news_lg")

myfile = open("text.txt", "rt")
text = myfile.read()
myfile.close()

nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10, "min_ngram": 3, "max_ngram": 3, "strict": True, "top_n_sent": 3})

doc = nlp(text)

print("Top Document Keywords:", doc._.keywords)
for sent in doc.sents:
    print(f"Sentence: {sent.text}")
    print("Top Sentence Keywords:", sent._.sent_keywords)