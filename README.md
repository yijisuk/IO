# IO

## 🔍 Description
IO utilizes advanced AI to transform education, enhancing engagement and interaction. Education goes beyond the simple quest for knowledge. We prioritize presenting accessible information and offering innovative learning experiences for educators and students.

This repository hosts a technical demo of a program engineered for streamlining the creation of lecture materials. Leveraging the power of advanced language models, including OpenAI's GPT-4, the program automates the development of various educational contents. 

Users provide the essential structure and reference materials in the form of URLs or .pdf/.docx/.txt files. From these, the system auto-generates:

- Lecture notes, either as detailed paragraphs or concise bullet points
- Comprehensive summaries for quick reviews
- Question sets, including multiple-choice questions or written queries

## 🤔 What Can Be Done?
With this program, users can use a variety of file formats (URL, pdf, docx, txt) as reference materials to generate:

- Lecture notes based on reference materials
- Create comprehensive summaries for quick review
- Formulate question sets for testing knowledge retention

## 🦾 Running the Code
To run the code, follow these steps:

**First, clone the repository**

```git clone https://github.com/yijisuk/IO.git```

**Install the dependencies**

```pip install -r requirements.txt```

**Add configurations:**

1. Create a ```core``` folder
2. Create and save your [OpenAI](https://openai.com/product) API Key in ```openai-api-key.txt``` - OpenAI's GPT models will be the main language models used in this program.
3. Create and save [Pinecone](https://www.pinecone.io/) API Key in ```pinecone-api-key.txt``` - Pinecone is a vector database which will store the vectorized lecture reference materials, formatted for easy reference by language models.
4. Save the passphrase of the email address in ```email-password.txt``` - this will be used for sending out generated lecture materials.

**Run the main Python file**

```python main.py```
