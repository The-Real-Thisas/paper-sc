import re
import PyPDF2
import requests
import os
import urllib.parse

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text, reader

def extract_questions(text, reader):
    pattern = r"(\(\w+\) .*?)(?=\n|$)"
    questions = re.findall(pattern, text, re.DOTALL)
    lines = text.split("\n")
    question_lines = [(line_number+1, page_number+1) for line_number, line in enumerate(lines) if any(question in line for question in questions) for page_number in range(len(reader.pages)) if line in reader.pages[page_number].extract_text()]
    return list(zip(questions, question_lines))


# Example usage
# pdf_file_path = 'demo.pdf'
# pdf_file_path = 'ms_demo.pdf'
# extracted_text, reader = extract_text_from_pdf(pdf_file_path)
# questions_with_lines_and_pages = extract_questions(extracted_text, reader)

# for i, (question, (line_number, page_number)) in enumerate(questions_with_lines_and_pages):
#     print(f"Index {i+1}, Page {page_number}, Line {line_number}: {question}")


def extract_questions_from_pdf(pdf_url):
    """
    - Downloads URL to a PDF file
    - Extracts questions from the PDF file
    - Appends the questions to a list
    - Deletes the PDF file
    """
    # Download PDF
    response = requests.get(pdf_url)
    with open(f"{urllib.parse.unquote(pdf_url.split('/')[-1])}", 'wb') as f:
        f.write(response.content)
    # Extract questions
    extracted_text, reader = extract_text_from_pdf(urllib.parse.unquote(pdf_url.split('/')[-1]))
    questions_with_lines_and_pages = extract_questions(extracted_text, reader)
    # Append questions to list
    master_questions_list.append(questions_with_lines_and_pages)
    # Delete PDF
    os.remove(urllib.parse.unquote(pdf_url.split('/')[-1]))
    return questions_with_lines_and_pages


master_pdf_list = [] 
master_questions_list = [] 

with open('master_pdf_list.txt', 'r') as f:
    for line in f:
        master_pdf_list.append(line.strip())
    
extract_questions_from_pdf(master_pdf_list[2])

print(master_pdf_list[2])
print(master_questions_list)