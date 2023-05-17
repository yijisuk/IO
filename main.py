from functions.process_inputs import InputProcessor
from utils.setup import APISetup
from streamlit_pages.mainpage import MainPage
from utils.pinecone_manager import PineconeManager

import os
import shutil
import pinecone


if __name__ == "__main__":

    # fundamental setups
    apiSetup = APISetup()
    setups = apiSetup.get_setups()

    mainpage = MainPage()

    material_inputs = None
    if mainpage.generate_materials() is not None:
        material_inputs = mainpage.generate_materials()

        inputProcessor = InputProcessor(material_inputs, setups)

        print("processing inputs...")
        inputProcessor.process_input()

        # Empty the outputs folder
        # print("Emptying outputs folder...")
        # shutil.rmtree("./outputs")
        # os.makedirs("./outputs")

        # Remove all pinecone indexes
        # print("Removing all pinecone indexes...")
        # for index in pinecone.list_indexes():
        #     pinecone.delete_index(index)

# Empty pinecone project
# if __name__ == "__main__":

#     pineconeManager = PineconeManager()
#     pineconeManager.empty_pinecone()
