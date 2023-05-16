import os
from fpdf import FPDF

class PDFGenerator:

    def __init__(self, topic, material, document_dirs):

        self.topic = topic
        self.material = material
        self.document_dirs = document_dirs
    
    def generate_pdf(self):

        # Create a new PDF document
        pdf = FPDF()
        pdf.add_page()

        # Add title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, self.topic, align='C')
        pdf.ln()

        # Loop through the list of strings and add them to the PDF document
        for subtopic in self.document_dirs.keys():
            with open(self.document_dirs[subtopic], 'r', encoding='utf-8') as f:

                # Add heading for subtopic
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 10, subtopic, align='L')
                pdf.ln()

                # Add contents for subtopic
                document = f.read()
                pdf.set_font('Arial', size=12)
                pdf.multi_cell(0, 10, document)
                pdf.ln()

        # Save the PDF document
        root_dir = os.path.join("outputs", self.topic.replace(' ', ''), "pdfs")
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        pdf_output = f"{self.topic}-{self.material}.pdf"
        pdf_output_dir = os.path.join(root_dir, pdf_output)
        pdf.output(pdf_output_dir)

        return pdf_output_dir