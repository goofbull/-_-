from PyPDF2 import PdfReader
from docx import Document
import os

# Файлов 100
number_of_docs = 100
directory = "./pdf_cases/"
output_directory = "./docx_cases/"

for i in range (1, number_of_docs + 1):

    active_file_number = str(i)
    # Создание нового документа Word
    document = Document()

    filename = "case_" + active_file_number + ".pdf"
    file_path = os.path.join(directory, filename)

    output_filename = "case_" + active_file_number + ".docx"
    output_path = os.path.join(output_directory, output_filename)


    with open(file_path, "rb") as file:
        
        # Создание объекта PdfReader
        pdf_reader = PdfReader(file)

        # Открытие документа Word для записи
        with open(output_path, "wb") as output_file:

            # Перебор каждой страницы PDF-файла
            for page_num in range(len(pdf_reader.pages)):
                
                # Получение текущей страницы
                page = pdf_reader.pages[page_num]

                # Извлечение текста со страницы
                text = page.extract_text()
                
                # Добавление абзаца в Word, содержащего текст
                document.add_paragraph(text)

    # Сохранение документа Word
    document.save(output_path)
    print("Файл " + filename + " был отформатирован")
