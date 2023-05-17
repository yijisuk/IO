from datetime import datetime, timedelta, timezone
import streamlit as st

class APISetup:

    def __init__(self):

        # Streamlit deployment version
        # self.openai_api_key = st.secrets["openai_api_key"]
        # self.pinecone_api_key = st.secrets["pinecone_api_key"]

        with open("./core/openai-api-key.txt") as f:
            self.openai_api_key = f.read()

        with open("./core/pinecone-api-key.txt") as f:
            self.pinecone_api_key = f.read()

        self.pinecone_env = "us-east-1-aws"
    
    def get_setups(self):

        return {
            "openai_api_key": self.openai_api_key,
            "pinecone_api_key": self.pinecone_api_key,
            "pinecone_env": self.pinecone_env
        }

class PineConeIndexSetup:

    def __init__(self, topic, timezone):

        self.topic = topic.replace(" ", "").lower()
        self.timezone = timezone
    
    def get_index(self):

        if len(self.topic) > 10:
            self.topic = self.topic[:10]
        
        timestamp = datetime.now(tz=self.timezone).timestamp()
        timestamp = str(timestamp).replace(".", "-")

        return f"{self.topic}-{timestamp}"
