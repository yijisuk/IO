from model.iopipeline import IOPipeline
from streamlit_pages.page_values import MainPageValues
from prompts.purpose import Purpose
from utils.setup import PineConeIndexSetup

from datetime import timedelta, timezone
from fpdf import FPDF

class InputProcessor:

    def __init__(self, material_inputs, setups):
        self.material_inputs = material_inputs
        self.setups = setups

        self.topic = self.material_inputs["topic"]
        self.materials = self.material_inputs["materials"]
        self.keyword_count = self.material_inputs["keyword_count"]

        self.configs = None
        if "configs" in self.material_inputs.keys():
            self.configs = self.material_inputs["configs"]

        self.tz_sg = timezone(timedelta(hours=8))

        self.pineconeIndexSetup = PineConeIndexSetup(self.topic, self.tz_sg)
        self.pinecone_index = self.pineconeIndexSetup.get_index()

    def process_input(self):

        for material in self.materials:

            document_dirs = {}
            subtopic_contents = self.material_inputs["subtopic_contents"]

            if material == "Notes" and self.configs is not None:
                config = self.configs["notes_config"]
            
            elif material == "Questions" and self.configs is not None:
                config = self.configs["qs_config"]

            for subtopic_content in subtopic_contents:

                subtopic = subtopic_content["subtopic"]
                reference = subtopic_content["ref"]
                file_data = subtopic_content["file_data"]

                input_data = ""
                if reference == "":
                    input_data = file_data

                elif file_data is None:
                    input_data = reference

                else:
                    input_data = reference + "\n" + file_data

                output_dir = "./outputs/" + \
                    f"{self.topic}{subtopic}-{material}" + ".txt"

                if config is not None:
                    # If creating notes,
                    if material == "Notes" and config == MainPageValues.NOTES_CONFIG_OPTIONS.value[0]:
                        purpose = Purpose.NOTE_LINEAR.value
                    
                    elif material == "Notes" and config == MainPageValues.NOTES_CONFIG_OPTIONS.value[1]:
                        purpose = Purpose.NOTE_BULLET.value
                    
                    elif material == "Notes" and config == MainPageValues.NOTES_CONFIG_OPTIONS.value[2]:
                        purpose = Purpose.NOTE_BOTH.value
                    
                    # If creating questions,
                    elif material == "Question Set" and config == MainPageValues.QUESTIONS_CONFIG_OPTIONS.value[0]:
                        purpose = Purpose.QUESTIONSET_MCQ.value
                    
                    elif material == "Question Set" and config == MainPageValues.QUESTIONS_CONFIG_OPTIONS.value[1]:
                        purpose = Purpose.QUESTIONSET_WRITTEN.value
                    
                    elif material == "Question Set" and config == MainPageValues.QUESTIONS_CONFIG_OPTIONS.value[2]:
                        purpose = Purpose.QUESTIONSET_BOTH.value
                
                else:
                    # If creating a summary,
                    purpose = material

                # Now given the subtopic and data, generate the lecture material in a desired format (material).                
                iopipeline = IOPipeline(
                    input_data, output_dir, purpose, self.keyword_count,
                    self.setups["openai_api_key"], self.setups["pinecone_api_key"], 
                    self.setups["pinecone_env"], self.pinecone_index)

                iopipeline.run()
                document_dirs[subtopic] = output_dir

            pdfGenerator = PDFGenerator(self.topic, material, document_dirs)
            pdfGenerator.generate_pdf()
            

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
        pdf_output_dir = "./outputs/" + f"{self.topic}-{self.material}" + ".pdf"
        pdf.output(pdf_output_dir)
