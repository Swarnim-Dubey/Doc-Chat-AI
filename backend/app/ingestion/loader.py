import pdfplumber

with pdfplumber.open("dsa-viva.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"\n---Page{i}---")
        print(page.extract_text())