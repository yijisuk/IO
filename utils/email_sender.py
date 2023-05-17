from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import ssl
import smtplib
import streamlit as st

class EmailSender:

    def __init__(self):

        self.sender = "ioed2023@gmail.com"

        # Streamlit deployment version
        self.password = st.secrets["email_password"]

        # with open("./core/email-password.txt", "r") as f:
        #     self.password = f.read()
    
    def send_email(self, receiver, pdf_dirs):

        subject = "Here are your materials by IO"
        body_content = "Hi! Thank you for using IO. Here are your materials."
        body = MIMEText(body_content, "plain")

        em = MIMEMultipart()
        em["From"] = self.sender
        em["To"] = receiver
        em["Subject"] = subject
        em.attach(body)
        
        # MIMEApplication attach multiple pdfs
        for pdf_dir in pdf_dirs:
            with open(pdf_dir, "rb") as f:
                pdf = MIMEApplication(f.read(), _subtype="pdf")
                pdf_filename = pdf_dir.split("/")[-1]

                pdf.add_header("Content-Disposition", "attachment", filename=pdf_filename)
                em.attach(pdf)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.sender, self.password)
            smtp.send_message(em, from_addr = self.sender, to_addrs = receiver)