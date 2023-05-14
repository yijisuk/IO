from enum import Enum


class ReformatKeywordsPrompts(Enum):

    CHAIN2_PROMPT = """
        Given a list of keywords: {keywords},
        filter out the similar or overlapping keywords,
        reformat the keywords to match the context of the text: {summary}
        Feel free to add any additional keywords that you think are relevant.
        But only {keyword_count} MAIN KEYWORDS should be returned. So CHOOSE WISELY.
        Do note that the extracted keywords will be later used for key concept note and summary purposes.
        Therefore, only include the necessary keywords.
        Each keyword should be a SINGLE WORD or a VALID PHRASE.
        DO NOT include keywords containing adjectives or any form of decorative words.
        TAKE OUT adjectives.
        Each keyword should be a valid word or a phrase, that fits context.
        If the keyword contains more than a single word, say:
        '''
        wordA wordB
        '''
        other keywords sharing similar combinations, say:
        '''
        wordB word A
        '''
        should be filtered out.
        Return the keywords in a list. Each keyword should be capitalized.
        Example:
        '''
        ['keyword1', 'keyword2', 'keyword3' ... and so on]
        '''
    """
