from enum import Enum


class Purpose(Enum):

    NOTE_LINEAR = "note-linear"
    NOTE_BULLET = "note-bullet"
    NOTE_BOTH = "note-both"
    QUESTIONSET_MCQ = "questionset-mcq"
    QUESTIONSET_WRITTEN = "questionset-written"
    QUESTIONSET_BOTH = "questionset-both"


class PurposePrompts(Enum):

    NOTE_LINEAR = """
        Referring to the following description: {description},
        write a lecturer's note that explains the concept of: {key}.
        No need for a heading nor title.
        Explanations should be formatted in complete sentences.
    """

    NOTE_BULLET = """
        Referring to the following description: {description},
        write a lecturer's note that explains the concept of: {key}.
        No need for a heading nor title.
        Explanations should be formatted in bullet points.
    """
    NOTE_BOTH = """
        Referring to the following description: {description},
        write a lecturer's note that explains the concept of: {key}.
        No need for a heading nor title.
        Notes should involve both complete sentences and bullet points.
        You determine the suitable format for each content.
    """

    QUESTIONSET_MCQ = """
        Referring to the following description: {description},
        write a set of mcq questions dealing with the concept of: {key}.
        No need for a heading nor title.
        Questions should be formatted in complete sentences.
        There should be five available choices for each question.
        You determine the suitable combination of basic and in-depth questions.
    """

    QUESTIONSET_WRITTEN = """
        Referring to the following description: {description},
        write a set of written and open-ended questions dealing with the concept of: {key}.
        No need for a heading nor title.
        Questions should be formatted in complete sentences.
        You determine the suitable combination of basic and in-depth questions.
    """
    QUESTIONSET_BOTH = """
        Referring to the following description: {description},
        write a set of (1) mcq questions and (2) written and open-ended questions
        dealing with the concept of: {key}.
        No need for a heading nor title.
        Questions should be formatted in complete sentences.
        If it's a mcq, there should be five available choices for each question.
        You determine the combination of mcq and written questions.
        You determine the suitable combination of basic and in-depth questions.
    """
