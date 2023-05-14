from utils.get_inputs import GetInputs
from model.iopipeline import IOPipeline

if __name__ == "__main__":

    INPUT_DIR = "./data/guidetoinvestors.txt"
    OUTPUT_DIR = "./outputs/guidetoinvestors.txt"

    with open("./core/openai-api-key.txt") as f:
        OPENAI_API_KEY = f.read()

    with open("./core/pinecone-api-key.txt") as f:
        PINECONE_API_KEY = f.read()

    PINECONE_ENV = "asia-southeast1-gcp-free"
    PINECONE_INDEX = "guidetoinvestors"

    inputs_processor = GetInputs()

    PURPOSE = inputs_processor.get_purpose()
    KEYWORD_COUNT = inputs_processor.get_keyword_count()

    iopipeline = IOPipeline(
        INPUT_DIR, OUTPUT_DIR, PURPOSE, KEYWORD_COUNT, \
        OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX)

    iopipeline.run()