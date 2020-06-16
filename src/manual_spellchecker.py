class spell_checker:
    def __init__(self, dataframe, column_names, tokenizer=None, num_n_words_dis=5, save_path=None):
        # Import appropriate version of tqdm based on editor
        try:
            shell = get_ipython().__class__.__name__
            if shell == 'ZMQInteractiveShell':
                from tqdm.notebook import tqdm
            else:
                from tqdm import tqdm
        except NameError:
            from tqdm import tqdm
        import enchant
        import numpy as np
        
        # The pyenchant model for checking if spelling is correct
        self.enc_dict = enchant.Dict("en_US")
        self.tqdm = tqdm
        self.dataframe = dataframe
        self.column_names = column_names
        self.tokenizer = tokenizer
        self.num_n_words_dis = num_n_words_dis
        self.save_path = save_path
        self.error_list = list()
        self.np = np
    
    # Tokenizer
    def split_tokenizer(self, text, tokenizer):
        if tokenizer:
            return tokenizer(text)
        else:
            return text.split()
    
    # Returns a list of all misspelled words
    def get_all_errors(self):
        if len(self.error_list) == 0:
            print("Either there are no errors in your dataset or you forgot to run the 'spell_check' function")
        return self.error_list
    
    # If only a single column is required to be analyzed for spelling errors
    def find_errors(self, enc_dict, tqdm, dataframe, tokenizer, column_names):
        for index in tqdm(range(len(dataframe.index))):
            # Get the text
            row = dataframe.loc[index, column_names]
            # Split the text into tokens
            tokens = self.np.array(self.split_tokenizer(row, tokenizer))
            errors = [False if (self.enc_dict.check(word) or word in string.punctuation) else True for word in tokens]
            # Add the misspelled words to the error list
            self.error_list.extend(tokens[errors])
    
    # Correct errors with user input
    def correct_errors(self, enc_dict, dataframe, tokenizer, column_names, num_n_words_dis):
        break_flag = False
        for index in range(len(dataframe.index)):
            # Get the text
            row = dataframe.loc[index, column_names]
            # Split the text into tokens
            tokens = self.split_tokenizer(row, tokenizer)
            # Same error could exist in the same text, so use set()
            error_list = list(set([word for word in tokens if not (enc_dict.check(word) or word in string.punctuation)]))
            # Individually correct the errors
            for misspelled_word in error_list:
                string_to_print = ""
                mid_index = tokens.index(misspelled_word)
                start_index = mid_index-num_n_words_dis if mid_index-num_n_words_dis > 0 else 0
                final_index = mid_index+1+num_n_words_dis if mid_index+1+num_n_words_dis < len(tokens) else len(tokens)
                if start_index > 0:
                    string_to_print+= ".... "
                string_to_print+= " ".join(tokens[start_index: mid_index]) + " " + "\033[41;30m" + misspelled_word + "\033[m" + " " + " ".join(tokens[mid_index+1: final_index])
                if final_index < len(tokens):
                    string_to_print+= " ...."
                suggestions = enc_dict.suggest(misspelled_word)
                print("\n\nMisspelled Word: " + string_to_print)
                print("Suggestions: ", suggestions)
                correct_word = input("Correct Version: ")
                if correct_word == "-999":
                    break_flag = True
                    break
                elif correct_word.isdigit() and int(correct_word) < len(suggestions): # User wants to use suggestion
                    dataframe.loc[index, column_names] = dataframe.loc[index, column_names].replace(misspelled_word, suggestions[int(correct_word)-1])
                elif len(correct_word) == 0: # User wants to Skip
                    continue
                elif correct_word == "''" or correct_word == '""': # User wants to remove the word
                    dataframe.loc[index, column_names] = dataframe.loc[index, column_names].replace(misspelled_word, "")
                else:
                    dataframe.loc[index, column_names] = dataframe.loc[index, column_names].replace(misspelled_word, correct_word)
            if break_flag:
                break
        return [dataframe, break_flag]
    
    # Driver for finding all misspelled words
    def spell_check(self):    
        print("\nAnalyzing suspected errors")
        # If only single column passed, column_names will be a string
        if type(self.column_names) == str:
            self.find_errors(self.enc_dict, self.tqdm, self.dataframe, self.tokenizer, self.column_names)
        else:
            for column in self.column_names:
                self.find_errors(self.enc_dict, self.tqdm, self.dataframe, self.tokenizer, column)
        print("\nTotal suspected errors = ", len(self.error_list))
        
    # Driver for correcting all misspelled words
    def correct_words(self):    
        # If only single column passed, column_names will be a string
        if type(self.column_names) == str:
            new_dataframe, _ = self.correct_errors(self.enc_dict, self.dataframe, self.tokenizer, self.column_names, self.num_n_words_dis)
        else:
            new_dataframe = self.dataframe.copy()
            for column in self.column_names:
                tmp, break_flag = self.correct_errors(self.enc_dict, self.dataframe, self.tokenizer, column, self.num_n_words_dis)
                new_dataframe[column] = tmp[column]
                if break_flag:
                    break
        
        # If path to save file is provided, save it
        if self.save_path:
            new_dataframe.to_csv(self.save_path, index=False)
        return new_dataframe
