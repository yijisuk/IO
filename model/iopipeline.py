from model.ioformatter import IOFormatter


class IOPipeline:

    def __init__(self, input_file, output_file, purpose, keyword_count,
                 openai_api_key, pinecone_api_key, pinecone_env, pinecone_index):

        self.ioformatter = IOFormatter(
            input_file, output_file, openai_api_key, pinecone_api_key, pinecone_env, pinecone_index)
        self.purpose = purpose
        self.keyword_count = keyword_count

    def run(self):

        init_keywords = self.ioformatter.extract_keywords(self.keyword_count)
        keywords = self.ioformatter.reformat_keywords(init_keywords, self.keyword_count)

        self.ioformatter.vectorstore()
        keyword_description_dict = self.ioformatter.generate_general_description(keywords)

        if self.purpose == "summary":
            formatted_contents = self.ioformatter.summary(keyword_description_dict)

        else:
            formatted_contents = self.ioformatter.formatting(self.purpose, keyword_description_dict)

        self.ioformatter.format_output(formatted_contents)
