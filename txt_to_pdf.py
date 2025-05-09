from fpdf import FPDF

def txt_to_pdf_fpdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    
    # Подключаем шрифт с поддержкой кириллицы
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    with open(txt_path, 'r', encoding='utf-8') as f:
        for line in f:
            pdf.cell(200, 10, txt=line.strip(), ln=True)

    pdf.output(pdf_path)