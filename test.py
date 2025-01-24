from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from docx import Document
from docx.shared import Inches

# Создание нового документа Word
document = Document()

# Открытие PDF-файла
with open("Дело_1.pdf", "rb") as file:
    
    # Создание объекта PdfReader
    pdf_reader = PdfReader(file)

    # Открытие документа Word для записи
    with open("output.docx", "wb") as output_file:

        # Перебор каждой страницы PDF-файла
        for page_num in range(len(pdf_reader.pages)):
            
            # Получение текущей страницы
            page = pdf_reader.pages[page_num]

            # Извлечение текста со страницы
            text = page.extract_text()
            
            # Добавление абзаца в Word, содержащего текст
            document.add_paragraph(text)

# Сохранение документа Word
document.save("output.docx")
