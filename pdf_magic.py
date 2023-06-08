import subprocess
import pdfplumber

class PdfPage:
    def __init__(self, pdf_path, page_number):
        self.pdf_path = pdf_path
        self.page_number = page_number

    def extract_text(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[self.page_number - 1]
            return page.extract_text()

    def extract_rectangles(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            page = pdf.pages[self.page_number - 1]
            return page.rects

    def extract_svg(self, output_path):
        subprocess.run(['pdf2svg', self.pdf_path, output_path, str(self.page_number)])

# Example usage
pdf_path = "demo.pdf"
page_number = 3

pdf_page = PdfPage(pdf_path, page_number)

text_content = pdf_page.extract_text()
print("Text Content:")
print(text_content)

rectangles = pdf_page.extract_rectangles()
print("Rectangles:")
for rect in rectangles:
    print(rect)

output_svg_path = "output.svg"
pdf_page.extract_svg(output_svg_path)
print(f"SVG saved to {output_svg_path}")
