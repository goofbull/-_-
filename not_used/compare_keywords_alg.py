from rake_nltk import Rake
import nltk
from summa import keywords # TextRank
import yake
import os
from docx import Document

directory = "./compare_results_keywords/"

filename_rank = "rake_keywords_result.docx"
filename_text_rank = "text_rank_keywords_result.docx"
filename_yake_01 = "yake_01_keywords_result.docx"
filename_yake_02 = "yake_02_keywords_result.docx"
filename_yake_03 = "yake_03_keywords_result.docx"
filename_yake_04 = "yake_04_keywords_result.docx"

def PrintToDocx(filename: str, keywords: str):
    file_path = os.path.join(directory, filename)

    document = Document()

    list_result = list(keywords)
    with open(file_path, 'wb') as file:
        for word in list_result:
            document.add_paragraph(word)

    document.save(file_path)



nltk.download('punkt_tab')
rake = Rake(language='russian')


myfile = open("text.txt", "rt")
text = myfile.read()
myfile.close()

rake.extract_keywords_from_text(text)
keywords_rake = rake.get_ranked_phrases()
print("\nКлючевые фразы, найденные rake: ", keywords_rake)
PrintToDocx(filename_rank, keywords_rake)


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

for i in text.split():
    if i not in stop_words_set:
        text_clean += i + " "
text_rank_keywords = keywords.keywords(text_clean, language = "russian").split("\n")
print("\nКлючевые фразы, найденные TextRank: ", text_rank_keywords)
PrintToDocx(filename_text_rank, text_rank_keywords)

# Максимальное количество слов в фразе (n) затем меняется на 4

extractor = yake.KeywordExtractor (
    lan = "ru",
    n = 2,
    dedupLim = 0.1,
    top = 100
)
result_list = extractor.extract_keywords(text_clean)
end_result = [x[0] for x in result_list]
print("\nКлючевые фразы, найденные yake, порог похожести слов = 0,1: ", end_result)
PrintToDocx(filename_yake_01, end_result)

extractor = yake.KeywordExtractor (
    lan = "ru",
    n = 2,
    dedupLim = 0.2,
    top = 100
)
result_list = extractor.extract_keywords(text_clean)
end_result = [x[0] for x in result_list]
print("\nКлючевые фразы, найденные yake, порог похожести слов = 0,2: ", end_result)
PrintToDocx(filename_yake_02, end_result)

extractor = yake.KeywordExtractor (
    lan = "ru",     # язык
    n = 2,          # максимальное количество слов в фразе
    dedupLim = 0.3, # порог похожести слов
    top = 100       # количество ключевых слов
)
result_list = extractor.extract_keywords(text_clean)
end_result = [x[0] for x in result_list]
print("\nКлючевые фразы, найденные yake, порог похожести слов = 0,3: ", end_result)
PrintToDocx(filename_yake_03, end_result)

extractor = yake.KeywordExtractor (
    lan = "ru",
    n = 2,
    dedupLim = 0.4,
    top = 100
)
result_list = extractor.extract_keywords(text_clean)
end_result = [x[0] for x in result_list]
print("\nКлючевые фразы, найденные yake, порог похожести слов = 0,4: ", end_result)
PrintToDocx(filename_yake_04, end_result)