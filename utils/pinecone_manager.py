import pinecone


class PineconeManager:

    def __init__(self):
        with open("./core/pinecone-api-key.txt") as f:
            self.pinecone_api_key = f.read()

        pinecone.init(api_key=self.pinecone_api_key,
                      environment="us-east-1-aws")

    def empty_pinecone(self):
        print("Removing all pinecone indexes...")

        pinecone_indexes = pinecone.list_indexes()

        if len(pinecone_indexes) > 0:
            print(f"Total {len(pinecone_indexes)} indexes found")

            for index in pinecone_indexes:
                pinecone.delete_index(index)

        print("Done!")
