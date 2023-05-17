import streamlit as st
from io import StringIO
import validators
import mimetypes

from utils.resource_formatter import ResourceFormatter

class SubtopicManager:

    def __init__(self, count):
        self.count = count
        self.subtopics = []

    def reload(self):
        self.subtopics = [Subtopic(i) for i in range(1, self.count + 1)]
    
    def confirm_status(self):
        return all([subtopic.confirm_status() for subtopic in self.subtopics])
    
    def get_subtopics(self):
        return self.subtopics
    
    def get_subtopic_contents(self):
        return [subtopic.get_contents() for subtopic in self.subtopics]

class Subtopic:

    def __init__(self, count):

        self.count = count
        st.divider()
        st.subheader(f"Subtopic {count}", anchor=False)

        self.subtopic = st.text_input(
            f"subtopic-{count}", "", 
            placeholder="Enter a subtopic", 
            label_visibility="collapsed")

        self.ref1 = st.text_input(
            f"st-{count}-ref-url", "", 
            placeholder="Reference URL", 
            label_visibility="collapsed")

        uploaded_file = st.file_uploader(
            f"st-{count}-ref-file", 
            type=["pdf", "docx", "txt"], 
            accept_multiple_files=False, 
            label_visibility="collapsed")
        
        self.file_data = ""
        if validators.url(self.ref1):
            resourceFormatter = ResourceFormatter(self.ref1)
            url_html = resourceFormatter.get_plain_text_from_url()
            self.file_data += resourceFormatter.convert_plain_text_to_paragraph(url_html)

        if uploaded_file is not None:
            
            file_extension = uploaded_file.name.split('.')[-1]
            mime_type = mimetypes.guess_type(uploaded_file.name)[0]

            resourceFormatter = ResourceFormatter(uploaded_file)

            if file_extension.lower() == 'pdf' and mime_type == 'application/pdf':
                self.file_data += resourceFormatter.get_pdf_text()

            elif file_extension.lower() == 'docx' and mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                self.file_data += resourceFormatter.get_plain_text_from_docx()

            elif file_extension.lower() == 'txt' and mime_type == 'text/plain':
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                self.file_data += stringio.read()

    def confirm_status(self):

        return self.subtopic != "" and (validators.url(self.ref1) or self.file_data != "")
    
    def get_contents(self):

        return {
            "subtopic": self.subtopic, 
            "ref": self.ref1, 
            "file_data": self.file_data,
        }