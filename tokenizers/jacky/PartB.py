# Assignment 1, Part B: Intersection of two files
# By Jacky Cheng

import PartA as A
import sys

# assignment function(s):

def find_common_tokens(file_1_path: str, file_2_path: str) -> list:
    """
    Runtime complexity: O(n + m)
    Runs in linear time relative to the size of the text file input. tokenize() is O(n) since the file is read 
    character-by-character, and each character is read once and processed one at a time. This function is 
    O(n + m) due to the conversion of file_2_token_list into a set, allowing for comparing tokens in O(1).

    Takes file 1 and file 2 as arguments, tokenizes them, and returns number of tokens they have in common.

    :param file_1_path: Path to the text file to be read.
    :param file_2_path: Path to the text file to be read.
    :return: List of common tokens in file_1_path and file_2_path
    """

    try:
        file_1_token_list = A.tokenize(file_1_path)
        file_2_token_list = A.tokenize(file_2_path)

        file_2_token_set = set(file_2_token_list) # convert file 2 list to set

        common_tokens = []

        # iterate through tokens in file 1
        for token_1 in file_1_token_list:
            # if token is also in file 2 and not in common_tokens, append token to common_tokens
            if token_1 in file_2_token_set and token_1 not in common_tokens:
                common_tokens.append(token_1)

    except FileNotFoundError as e:
        print(f"Error: {e}") # if file cannot be found, print error
    except IOError as e:
        print(f"Error: {e}") # if file cannot be read, print error

    return common_tokens

# run program:

if __name__ == "__main__":
    # take in file 1 and file 2 from command line as arguments
    text_file_1 = sys.argv[1]
    text_file_2 = sys.argv[2]

    # find common tokens between file 1 and file 2, print common_tokens, and print length of common_tokens
    common_tokens = find_common_tokens(text_file_1, text_file_2)
    print(common_tokens)
    print(len(common_tokens))