from prompts.purpose import Purpose

class GetInputs():

    # Get user input for desired material type
    def get_purpose(self):

        PURPOSE = -1
        while PURPOSE < 0:
            try:
                PURPOSE = int(input(
                    """
Enter the material to generate:
    1. Notes in full sentence
    2. Notes in bullet points
    3. Notes in both full sentence and bullet points
    4. MCQ questions
    5. Written questions
    6. Both MCQ and written questions

Choice: """
                ))

                if PURPOSE > 6:
                    print("Invalid choice. Please enter a number between 1 and 6.")

            except ValueError:
                print("Invalid input. Please enter a number.")

        purpose_list = [elem.value for elem in Purpose]

        return purpose_list[PURPOSE - 1]
    
    # Get user input for desired extracted keyword count
    def get_keyword_count(self):

        KEYWORD_COUNT = -1
        while KEYWORD_COUNT < 0:
            try:
                KEYWORD_COUNT = int(input("""
How many key concepts should be in subject?
Enter a number between 1 and 10:

Choice: """
                ))

                if KEYWORD_COUNT > 10:
                    print("Invalid choice. Please enter a number between 1 and 10.")

            except ValueError:
                print("Invalid input. Please enter a number.")
        
        return KEYWORD_COUNT
