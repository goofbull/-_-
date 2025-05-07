# from ruslingua import RusLingua
# from untitled import lemmatized_and_no_stop_words
# from untitled import extract_text_from_docx
# import logging
# import time



# # Настройка логирования
# logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

# ruslingua = RusLingua()
# key_words = []

# # Путь к Word файлу
# file_path = "output_terminology.docx"


# 
# # Извлекаем текст
# terminology_list = extract_text_from_docx(file_path)
# logging.debug(f"Терминология: {terminology_list}")



# for word in lemmatized_and_no_stop_words:
#     start_time = time.time()
#     logging.debug(f"Обрабатываем слово: {word}")

#     # Однокоренные слова
#     cognates = ruslingua.get_cognate_words(''+str(word)+'')
#     time.sleep(2)
#     logging.debug(f"Однокоренные слова для {word}: {cognates}")

#     if cognates == []:
#         logging.info("Нет однокоренных слов, проверяем по списку терминов...")
#         for y in terminology_list:
#             if word == y:
#                 logging.info(f"Найдено совпадение: {word}")
#                 key_words.append(word)
#     else:
#         for i in cognates:
#             for y in terminology_list:
#                 if i == y:
#                     logging.info(f"Найдено совпадение: {i}")
#                     key_words.append(i)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Время выполнения операции: {execution_time:.4f} секунд")
# print(lemmatized_and_no_stop_words)
# for i in lemmatized_and_no_stop_words:
#     if i == "банктрот":
#         print("yes")
