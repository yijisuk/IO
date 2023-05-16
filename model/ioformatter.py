import openai
import pinecone
import tiktoken

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import SequentialChain
from langchain.memory import SimpleMemory

from keybert import KeyBERT
import ast
from tqdm import tqdm

from prompts.reformat_keywords_prompts import ReformatKeywordsPrompts
from prompts.purpose import Purpose, PurposePrompts
from prompts.generate_general_description_prompts import GenerateGeneralDescriptionPrompts


class IOFormatter:

    def __init__(self, input_file, output_file,
                 openai_api_key, pinecone_api_key, pinecone_env, pinecone_index):

        # Input and output files
        self.input_file = input_file
        self.output_file = output_file

        # OpenAI LLMs
        self.openai_api_key = openai_api_key
        self.gpt4_llm = ChatOpenAI(
            temperature=0, model_name="gpt-4", openai_api_key=openai_api_key)
        self.gpt35_llm = ChatOpenAI(
            temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

        # Tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.tokenizer = tiktoken.encoding_for_model("gpt-4")

        # Pinecone
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_env = pinecone_env
        self.pinecone_index = pinecone_index

        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        openai.api_key = openai_api_key
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key, model="text-embedding-ada-002")

        self.retriever = None
        if pinecone_index not in pinecone.list_indexes():
            pinecone.create_index(
                pinecone_index, dimension=1536, metric="cosine")

        else:
            self.retriever = Pinecone.from_existing_index(
                pinecone_index, self.embeddings)

    """
    Extract keywords from the input file
    """

    def extract_keywords(self, keyword_count):

        keybert_model = KeyBERT()
        keywords = keybert_model.extract_keywords(
            self.input_file,
            top_n = keyword_count,
            keyphrase_ngram_range = (1, 2),
            stop_words = 'english'
        )

        keywords = [keyword[0] for keyword in keywords]

        return keywords

    """
    Reformat the document keywords,
    given the overall summary of the document.
    """

    def reformat_keywords(self, keywords, keyword_count):

        # CHAIN 1: Summarize document
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=0)

        texts = text_splitter.split_text(self.input_file)
        docs = [Document(page_content=t) for t in texts]

        summarizer_chain = load_summarize_chain(
            llm=self.gpt35_llm,
            chain_type="map_reduce",
            output_key="summary")

        # CHAIN 2: Reformat keywords
        PROMPT = PromptTemplate(
            input_variables=["keywords", "summary", "keyword_count"],
            template=ReformatKeywordsPrompts.CHAIN2_PROMPT.value
        )

        # reformatter_chain = LLMChain(llm=self.gpt4_llm, prompt=PROMPT)
        reformatter_chain = LLMChain(llm=self.gpt35_llm, prompt=PROMPT)

        # MAIN CHAIN
        main_chain = SequentialChain(
            memory=SimpleMemory(memories={"keywords": keywords, "keyword_count": keyword_count}),
            chains=[summarizer_chain, reformatter_chain],
            input_variables=["input_documents"],
            # verbose=True
        )

        response = main_chain.run({"input_documents": docs})
        keywords = ast.literal_eval(response)

        return keywords

    """
    Finalize setting up the vectorstore retriever.
    """

    def vectorstore(self):

        if self.retriever is None and self.pinecone_index is not None:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000, chunk_overlap=0)
            texts = text_splitter.split_text(self.input_file)

            self.retriever = Pinecone.from_texts(
                texts=texts, 
                embedding=self.embeddings, 
                index_name=self.pinecone_index)

    """
    Refer to the given document,
    and generate a general description for each keyword.
    """

    def generate_general_description(self, keywords):

        keyword_description_dict = {}

        for keyword in keywords:

            description = ""

            docs = self.retriever.similarity_search(keyword)
            docs_set = set([doc.page_content for doc in docs])

            # CHAIN1: Generating a detailed description for the keyword
            CHAIN1_PROMPT = PromptTemplate(
                input_variables=["keyword", "document", "description"],
                template=GenerateGeneralDescriptionPrompts.CHAIN1_PROMPT.value
            )

            # description_chain = LLMChain(
            #     llm=self.gpt4_llm, prompt=CHAIN1_PROMPT)
            description_chain = LLMChain(
                llm=self.gpt35_llm, prompt=CHAIN1_PROMPT)

            for doc in docs_set:
                description = description_chain.run(
                    {
                        "keyword": keyword,
                        "document": doc,
                        "description": description
                    }
                )

            keyword_description_dict[keyword] = description

        for key in keyword_description_dict.keys():

            description = keyword_description_dict[key]
            description = description.replace("\n\n", "")

            keyword_description_dict[key] = description

        return keyword_description_dict

    """
    Given the general description of each keyword,
    return the desired format of notes/questions.
    """

    def formatting(self, purpose, keyword_description_dict: dict):

        PROMPT = ""
        if purpose == Purpose.NOTE_LINEAR.value:
            PROMPT = PurposePrompts.NOTE_LINEAR.value

        elif purpose == Purpose.NOTE_BULLET.value:
            PROMPT = PurposePrompts.NOTE_BULLET.value

        elif purpose == Purpose.NOTE_BOTH.value:
            PROMPT = PurposePrompts.NOTE_BOTH.value

        elif purpose == Purpose.QUESTIONSET_MCQ.value:
            PROMPT = PurposePrompts.QUESTIONSET_MCQ.value

        elif purpose == Purpose.QUESTIONSET_WRITTEN.value:
            PROMPT = PurposePrompts.QUESTIONSET_WRITTEN.value

        elif purpose == Purpose.QUESTIONSET_BOTH.value:
            PROMPT = PurposePrompts.QUESTIONSET_BOTH.value

        formatted_contents = {}

        print("Generating...")
        for key in tqdm(keyword_description_dict.keys()):
            description = keyword_description_dict[key]

            # CHAIN1: Process query depending on the purpose
            if PROMPT == "":
                print(f"Prompt empty for purpose: {purpose}")
                
            CHAIN1_PROMPT = PromptTemplate(
                input_variables=["description", "key"],
                template=PROMPT,
            )

            # formatting_chain = LLMChain(
            #     llm=self.gpt4_llm, prompt=CHAIN1_PROMPT)
            formatting_chain = LLMChain(
                llm=self.gpt35_llm, prompt=CHAIN1_PROMPT)

            response = formatting_chain.run(
                {"description": description, "key": key})

            # TODO: Further processings of response

            formatted_contents[key] = response

        return formatted_contents

    """
    Given the general description of each keyword,
    return a summary.
    """

    def summary(self, keyword_description_dict: dict):

        formatted_contents = {}

        print("Generating...")
        for key in tqdm(keyword_description_dict.keys()):
            description = keyword_description_dict[key]

            # summary_chain = load_summarize_chain(
            #     self.gpt4_llm, chain_type="map_reduce")
            summary_chain = load_summarize_chain(
                self.gpt35_llm, chain_type="map_reduce")

            response = summary_chain.run([Document(page_content=description)])

            formatted_contents[key] = response

        return formatted_contents

    """
    Finalize the output format and export the file.
    """

    def format_output(self, formatted_contents):

        output_str = ""
        indent = '    '

        for key in formatted_contents.keys():
            output_str += f"{key}\n"
            indented_content = '\n'.join(
                indent + line for line in formatted_contents[key].split('\n'))
            output_str += f"{indented_content}\n\n"

        with open(self.output_file, "w") as f:
            f.write(output_str)

        print(f"Output file saved to {self.output_file}")
