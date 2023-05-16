from streamlit_pages.subtopic import SubtopicManager
from streamlit_pages.page_values import MainPageValues

import streamlit as st
import validate_email

class MainPage:

    def __init__(self):

        st.title("Introducing IO", anchor=False)
        st.header("Topic", anchor=False)
        self.topic = st.text_input("", "", placeholder="Enter the topic of your lecture material", label_visibility="collapsed")
        self.generate_confirmed = False

        self.configs = None
        self.notes_config = None
        self.qs_config = None

        # materials_col, key_concepts_col, depth_col, subtopic_count_col = st.columns(4)
        materials_col, key_concepts_col, subtopic_count_col = st.columns(3)

        with materials_col:
            self.materials = st.multiselect(
                MainPageValues.MATERIALS_Q.value,
                MainPageValues.MATERIALS_OPTIONS.value
            )
        
        with key_concepts_col:
            self.keyword_count = st.number_input(
                MainPageValues.KEYWORD_COUNT_Q.value,
                min_value=1, max_value=5, value=1, step=1)

        # with depth_col:
        #     self.depth = st.selectbox(
        #         MainPageValues.DEPTH_Q.value,
        #         MainPageValues.DEPTH_OPTIONS.value
        #     )

        with subtopic_count_col:
            subtopic_count = st.number_input(
                MainPageValues.SUBTOPIC_Q.value,
                min_value=1, max_value=5, value=1, step=1)

        if "Notes" in self.materials and "Question Set" in self.materials:

            with st.container():
                notes_config_col, qs_config_col = st.columns(2)

                with notes_config_col:
                    self.notes_config = st.selectbox(
                        MainPageValues.NOTES_CONFIG_Q.value,
                        MainPageValues.NOTES_CONFIG_OPTIONS.value
                    )
                
                with qs_config_col:
                    self.qs_config = st.selectbox(
                        MainPageValues.QUESTIONS_CONFIG_Q.value,
                        MainPageValues.QUESTIONS_CONFIG_OPTIONS.value
                    )
        
        elif "Notes" in self.materials:
                
            with st.container():
                notes_config_col, _ = st.columns(2)

                with notes_config_col:
                    self.notes_config = st.selectbox(
                        MainPageValues.NOTES_CONFIG_Q.value,
                        MainPageValues.NOTES_CONFIG_OPTIONS.value
                    )
        
        elif "Question Set" in self.materials:

            with st.container():
                qs_config_col, _ = st.columns(2)

                with qs_config_col:
                    self.qs_config = st.selectbox(
                        MainPageValues.QUESTIONS_CONFIG_Q.value,
                        MainPageValues.QUESTIONS_CONFIG_OPTIONS.value
                    )
        
        self.subtopicManager = SubtopicManager(subtopic_count)
        with st.container():
            self.subtopicManager.reload()

        st.divider()

        self.email = st.text_input(f"email", "", placeholder="your@email.com", label_visibility="collapsed")

        _, midcol, _ = st.columns(3)

        with midcol:
            generate = st.button("Generate!", type="primary", use_container_width=True)

        if generate and self.confirm_status():
            self.generate_confirmed = True

            st.write("Your materials are being generated, and will be delivered to your email shortly...")
            st.write("Please check your inbox!")
            st.write("You may close the window now.")
        
        elif generate and not self.confirm_status():
            st.write("Either your email is invalid, or you have not filled in all the fields as required.")
            st.write("Please fill in all the fields before generating your materials.")
    
    def confirm_status(self):

        # return self.topic != "" \
        #     and len(self.materials) > 0 \
        #     and self.depth != "" \
        #     and self.subtopicManager.confirm_status() \
        #     and validate_email.validate_email(self.email)
    
        return self.topic != "" \
            and len(self.materials) > 0 \
            and self.subtopicManager.confirm_status() \
            and validate_email.validate_email(self.email)
    
    def get_details(self):

        if self.notes_config is not None and self.qs_config is not None:
            self.configs = {
                "notes_config": self.notes_config,
                "qs_config": self.qs_config
            }
        
        elif self.notes_config is not None:
            self.configs = {
                "notes_config": self.notes_config
            }
        
        elif self.qs_config is not None:
            self.configs = {
                "qs_config": self.qs_config
            }
        
        if self.configs is not None:
            return_details = {
                "topic": self.topic,
                "materials": self.materials,
                "keyword_count": self.keyword_count,
                "configs": self.configs,
                # "depth": self.depth,
                "subtopic_contents": self.subtopicManager.get_subtopic_contents(),
                "email": self.email,
            }
        
        else:
            return_details = {
                "topic": self.topic,
                "materials": self.materials,
                "keyword_count": self.keyword_count,
                # "depth": self.depth,
                "subtopic_contents": self.subtopicManager.get_subtopic_contents(),
                "email": self.email,
            }

        return return_details
    
    def generate_materials(self):

        if self.generate_confirmed:
            return self.get_details()
        else:
            return None

# mainpage = MainPage()