from model.iopipeline import IOPipeline
from streamlit_pages.page_values import MainPageValues
from prompts.purpose import Purpose
from utils.setup import PineConeIndexSetup
from utils.pdf_generator import PDFGenerator
from utils.email_sender import EmailSender

import os
from datetime import timedelta, timezone

class InputProcessor:

    def __init__(self, material_inputs, setups):
        self.material_inputs = material_inputs
        self.setups = setups

        self.topic = self.material_inputs["topic"]
        self.materials = self.material_inputs["materials"]
        self.keyword_count = self.material_inputs["keyword_count"]
        self.receiver = self.material_inputs["email"]

        self.configs = None
        if "configs" in self.material_inputs.keys():
            self.configs = self.material_inputs["configs"]

        self.tz_sg = timezone(timedelta(hours=8))

        self.pineconeIndexSetup = PineConeIndexSetup(self.topic, self.tz_sg)
        self.pinecone_index = self.pineconeIndexSetup.get_index()

    def process_input(self):

        pdf_dirs = []

        for material in self.materials:

            config = None
            document_dirs = {}
            subtopic_contents = self.material_inputs["subtopic_contents"]

            if material == "Notes" and self.configs is not None:
                config = self.configs["notes_config"]
            
            elif material == "Question Set" and self.configs is not None:
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

                root_dir = os.path.join("outputs", self.topic.replace(' ', ''), subtopic.replace(' ', ''))
                
                if not os.path.exists(root_dir):
                    os.makedirs(root_dir)

                output_dir = os.path.join(root_dir, material + ".txt")

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
                    purpose = material.lower()
                
                print(f"Generating {purpose} for {subtopic}...")

                # Now given the subtopic and data, generate the lecture material in a desired format (material).                
                iopipeline = IOPipeline(
                    input_data, output_dir, purpose, self.keyword_count,
                    self.setups["openai_api_key"], self.setups["pinecone_api_key"], 
                    self.setups["pinecone_env"], self.pinecone_index)

                iopipeline.run()
                document_dirs[subtopic] = output_dir

            pdfGenerator = PDFGenerator(self.topic, material, document_dirs)
            pdf_output_dir = pdfGenerator.generate_pdf()
            pdf_dirs.append(pdf_output_dir)

        emailSender = EmailSender()
        emailSender.send_email(self.receiver, pdf_dirs)

        print(f"Sent an email to: {self.receiver}")