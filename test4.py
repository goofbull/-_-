from rake_nltk import Rake
import nltk
#import spacy
from summa import keywords # TextRank
from Testo import text_case2
import yake
#nlp = spacy.load("ru_core_news_lg")

nltk.download('punkt_tab')
rake = Rake(language='russian')

def FindKeyWords(text: str):
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()

    print("Ключевые фразы, найденные rake: ", keywords)

    #doc = nlp(text)

    #key_phrases = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]

    #print("Ключевые слова, найденные spacy: ",key_phrases)


print(FindKeyWords(text_case2))
text_clean = ""
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

# уберем стоп-слова
for i in text_case2.split():
    if i not in stop_words_set:
        text_clean += i + " "
print("Ключевые фразы, найденные TextRank: ", keywords.keywords (text_clean, language = "russian").split("\n"))

extractor = yake.KeywordExtractor (

    lan = "ru",     # язык
    n = 3,          # максимальное количество слов в фразе
    dedupLim = 0.3, # порог похожести слов
    top = 100        # количество ключевых слов
)
print("Ключевые фразы, найденные yake: ", extractor.extract_keywords(text_case2))
extractor = yake.KeywordExtractor (

    lan = "ru",     # язык
    n = 4,          # максимальное количество слов в фразе
    dedupLim = 0.3, # порог похожести слов
    top = 100        # количество ключевых слов
)
print("Ключевые фразы, найденные yake: ", extractor.extract_keywords(text_case2))

