from functions.process_inputs import InputProcessor
from utils.setup import APISetup
from streamlit_pages.mainpage import MainPage

import streamlit as st


if __name__ == "__main__":

    # fundamental setups
    apiSetup = APISetup()
    setups = apiSetup.get_setups()

    mainpage = MainPage()

    material_inputs = None
    if mainpage.generate_materials() is not None:
        material_inputs = mainpage.generate_materials()

        inputProcessor = InputProcessor(material_inputs, setups)
        inputProcessor.process_input()

        print("processing inputs...")