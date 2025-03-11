import fitz
from natasha import (
        Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)
from nltk import tokenize
directory = "./pdf_cases/"
segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

def lemmatize_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    return " ".join(token.lemma for token in doc.tokens)

number_of_docs = 100
dl = ["край", "края", "область", "области", "район", "района", "России", "РФ", "Российской Федерации"]
for i in range (1, number_of_docs + 1):
    active_file_number = str(i)

    filename = "case_" + active_file_number + ".pdf"
    doc = fitz.open(directory+filename)
    text = "\n".join([page.get_text() for page in doc])
    text = text.replace('Дело', '')
    clean_text = ' '.join(text.split())
    t2 = tokenize.sent_tokenize(clean_text)
    
    for text in t2:
        if 'Р Е Ш Е Н И Е' in text:
            
            t1, t2 = text.split('Р Е Ш Е Н И Е')  # Разделяем текст
            doc = Doc(t2)  # Создаем объект Doc с t2
            doc.segment(segmenter)
            doc.tag_ner(ner_tagger)
            loc = [span.text for span in doc.spans if span.type == "LOC"]
            filtered_loc = [phrase for phrase in loc if not any(word in phrase for word in dl)]
                
            if filtered_loc != []:
                #print(filtered_loc[0])
                pass
            else:
                print("ФАЙЛ", active_file_number)
