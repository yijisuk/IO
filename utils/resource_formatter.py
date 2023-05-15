from bs4 import BeautifulSoup
import requests
import re
from PyPDF2 import PdfReader

class ResourceFormatter:

    def __init__(self, resource):
        self.resource = resource

    # Retrieves the plain text content of the specified URL.
    def get_plain_text_from_url(self):
        
        response = requests.get(self.resource)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            return text
        else:
            raise Exception('Error retrieving text from URL: {}'.format(url))

    # Converts the plain text to a good-looking paragraph.
    def convert_plain_text_to_paragraph(self, txt):

        # Remove all HTML markup.
        text = re.sub('<[^>]+>', '', txt)

        # Replace all newline characters with spaces.
        text = text.replace('\n', ' ')

        # Remove all leading and trailing spaces.
        text = text.strip()

        # Split the text into paragraphs.
        paragraphs = text.split('\n\n')

        # For each paragraph, add a blank line before and after it.
        for i in range(len(paragraphs)):
            paragraphs[i] = '\n\n{}\n\n'.format(paragraphs[i])

        para = ''.join(paragraphs)

        # Replace all consecutive whitespace characters with a single space.
        para = re.sub('\s{2,}', ' ', para)

        # Remove all leading and trailing spaces.
        para = para.strip()

        # Return the paragraphs as a single string.
        return para
    
    # Read the PDF file and return the text content.
    def get_plain_text_from_pdf(self):

        reader = PdfReader(self.resource)

        text = []

        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text.append(page.extract_text())
            text.append("\n\n")
        
        return ''.join(text)
