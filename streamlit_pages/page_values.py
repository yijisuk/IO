from enum import Enum

class MainPageValues(Enum):

    MATERIALS_Q = "What materials?"
    MATERIALS_OPTIONS = ["Notes", "Summary", "Question Set"]

    KEYWORD_COUNT_Q = "How many key concepts?"

    DEPTH_Q = "Depth"
    DEPTH_OPTIONS = ["High-school", "University Y1-2", "University Y3-4"]

    SUBTOPIC_Q = "How many subtopics?"

    NOTES_CONFIG_Q = "Notes Configuration"
    NOTES_CONFIG_OPTIONS = ["Complete sentences", "Bullet points", "Both"]

    QUESTIONS_CONFIG_Q = "Question Set Configuration"
    QUESTIONS_CONFIG_OPTIONS = ["MCQs", "Written questions", "Both"]