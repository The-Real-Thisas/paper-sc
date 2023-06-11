import pdfplumber
import re

def extract_left_margin_words(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        left_margin_words = []
        
        for page_number, page in enumerate(pdf.pages, 1):
            page_words = page.extract_words()
            
            min_x = min(word['x0'] for word in page_words)
            
            threshold = 1.0
            
            for line_number, word in enumerate(page_words, 1):
                if word['x0'] <= min_x + threshold:
                    left_margin_words.append({
                        'word': word['text'],
                        'line_number': line_number,
                        'page_number': page_number
                    })
                    
        return left_margin_words
    
def extract_sub_questions(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        sub_questions = []
        
        for page_number, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            page_words = page.extract_words()
            
            for word in page_words:
                text = word['text']
                # Use regex to check for sub-question pattern (brackets with a single alphabet)
                if re.match(r'\([a-zA-Z]\)', text):
                    sub_questions.append({
                        'sub_question': text,
                        'line_number': word['top'],
                        'page_number': page_number
                    })
        
        return sub_questions

# Usage example
pdf_path = 'demo.pdf'
left_margin_words = extract_left_margin_words(pdf_path)
sub_questions = extract_sub_questions(pdf_path)

# Print the extracted numeric words with line number and page number
for word_info in left_margin_words:
    word = word_info['word']
    if word.isdigit():
        line_number = word_info['line_number']
        page_number = word_info['page_number']
        print(f"Word: {word}, Line: {line_number}, Page: {page_number}")

# Print the extracted sub-questions with line number and page number
for sub_question_info in sub_questions:
    sub_question = sub_question_info['sub_question']
    line_number = sub_question_info['line_number']
    page_number = sub_question_info['page_number']
    print(f"Sub-question: {sub_question}, Line: {line_number}, Page: {page_number}")