import re
import PyPDF2
import requests
import os
import urllib.parse
from tqdm import tqdm
import json 
import concurrent.futures

class Question:
    def __init__(self, question, line_number, page_number, url):
        self.question = question
        self.line_number = line_number
        self.page_number = page_number
        self.url = url
        self.file_name = self.url.split('/')[-1]

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
    # Made question into Question object
    for i, (question, (line_number, page_number)) in enumerate(questions_with_lines_and_pages):
        master_questions_list.append(Question(question, line_number, page_number, pdf_url))
    # Delete PDF
    os.remove(urllib.parse.unquote(pdf_url.split('/')[-1]))
    return questions_with_lines_and_pages


master_pdf_list = [] 
master_questions_list = [] 

with open('master_pdf_list.txt', 'r') as f:
    for line in f:
        master_pdf_list.append(line.strip())
    
# extract_questions_from_pdf(master_pdf_list[2])

# print(master_pdf_list[2])
# print(master_questions_list)

# for pdf in tqdm(master_pdf_list, desc="Extracting questions from PDFs"):
#     extract_questions_from_pdf(pdf)

# Create a ThreadPoolExecutor with a maximum of 10 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Create a list to store the submitted tasks
    futures = []

    # Iterate over the PDFs in master_pdf_list
    for pdf in master_pdf_list:
        # Submit the extract_questions_from_pdf task to the executor
        future = executor.submit(extract_questions_from_pdf, pdf)
        futures.append(future)

    # Use tqdm to track the progress of the tasks
    for future in tqdm(concurrent.futures.as_completed(futures), desc="Extracting questions from PDFs", total=len(master_pdf_list), unit="PDF"):
        # Wait for the task to complete and handle any exceptions
        try:
            result = future.result()
        except Exception as e:
            # Handle exception from the task
            print(f"Exception: {e}")

# Dump to json
with open('master_questions_list.json', 'w') as f:
    json.dump([question.__dict__ for question in master_questions_list], f, indent=4)
