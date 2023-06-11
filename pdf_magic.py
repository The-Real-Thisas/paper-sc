import pdfplumber

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

# Usage example
pdf_path = 'demo.pdf'
left_margin_words = extract_left_margin_words(pdf_path)

# Print the extracted numeric words with line number and page number
for word_info in left_margin_words:
    word = word_info['word']
    if word.isdigit():
        line_number = word_info['line_number']
        page_number = word_info['page_number']
        print(f"Word: {word}, Line: {line_number}, Page: {page_number}")
