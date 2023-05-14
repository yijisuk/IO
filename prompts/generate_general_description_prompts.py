from enum import Enum


class GenerateGeneralDescriptionPrompts(Enum):

    CHAIN1_PROMPT = """
        As a helpful knowledge provider,
        Refer to the given document: {document},
        generate a detailed description for the keyword: {keyword},
        and add the details to the description: {description} if needed.
        If context overlaps with the description, skip.
    """
