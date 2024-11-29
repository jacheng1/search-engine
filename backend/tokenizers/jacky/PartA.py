# Assignment 1, Part A: Word Frequencies
# By Jacky Cheng

import sys
from typing import List, Dict, Tuple

# helper function(s):

def selection_sort(list: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Runtime complexity: O(n^2)
    Runs in exponential time relative to the size of the list input, due to its nested for-loop.

    Use selection sort algorithm to sort parameter list of tuples by int in descending order

    :param list: Unsorted list of tuples.
    :return: Sorted list of tuples.
    """

    size = len(list) # retrieve length of list

    # iterate through list
    for index in range(size):
        max_index = index

        # iterate through unsorted partition of list
        for j in range(index + 1, size):
            # if element at j has greater int than element at max_index, select maximum element j
            if list[j][1] > list[max_index][1]:
                max_index = j

        list[index], list[max_index] = list[max_index], list[index] # swap element at max_index with element at first index

    return list

# assignment function(s):

def tokenize(text_file_path: str) -> List[str]:
    """
    Runtime complexity: O(n)
    Runs in linear time relative to the size of the text file input. The file is read character-by-character, 
    and each character is read once and processed one at a time.
    
    Reads in a text file and returns a list of the tokens in that file.
    For the purpose of this assignment, a token is a sequence of alphanumeric characters, independent of capitalization.

    :param text_file_path: Path to the text file to be read.
    :return: List of the tokens in that file.
    """

    current_token = []
    token_list = []

    try:
        # open text_file_path as read, assign as file
        with open(text_file_path, 'r', encoding='utf-8') as file:
            # read file character-by-character
            while True:
                char = file.read(1) # read one character

                # if EOF, end tokenization of file
                if not char:
                    break

                # if current char is alphanumeric and ASCII, add it to current_token as lowercase
                if char.isalnum() and char.isascii():
                    current_token.append(char.lower())
                else:
                    # else, if not alphanumeric, add current_token to token_list
                    if current_token:
                        token_list.append(''.join(current_token))

                        current_token = [] # reset current_token

            # if token in file exists after EOF, add it to token_list
            if current_token:
                token_list.append(''.join(current_token))
            
    except FileNotFoundError:
        print(f"Error: file path '{text_file_path}' not found.") # if file cannot be found, print error
    except IOError:
        print(f"Error: cannot read file '{text_file_path}'.") # if file cannot be read, print error

    return token_list

def compute_word_frequencies(token_list: List[str]) -> Dict[str, int]:
    """
    Runtime complexity: O(n)
    Runs in linear time relative to the size of the list input, because the for-loop runs n times,
    where n is the size of token_list.
    
    Counts the number of occurrences of each token in the given token list.

    :param token_list: List of tokens.
    :return: Dict, mapping each token to the number of occurrences.
    """

    token_frequencies = {}

    # for each token element in token_list
    for token in token_list:
        # if token element is in token_frequencies, increment by 1
        if token in token_frequencies:
            token_frequencies[token] += 1
        else:
            # else, set to 1
            token_frequencies[token] = 1

    return token_frequencies

def print_frequencies(token_frequencies: Dict[str, int]) -> None:
    """
    Runtime complexity: O(n^2)
    Runs in exponential time relative to the size of the dict input. The function for-loop is O(n) because
    it runs n times, where n is the size of sorted_frequency_list. The function selection_sort is O(n^2) because
    of its nested for-loop. O(n^2) dominates O(n), so this function is O(n^2).

    Prints out the word frequency count as output, ordered by decreasing frequency.

    :param token_frequencies: Dict, mapping each token to the number of occurrences.
    """

    frequency_list = [(token, count) for token, count in token_frequencies.items()] # derive list of tuples from dictionary

    sorted_frequency_list = selection_sort(frequency_list) # sort list of tuples with selection_sort helper function

    # iterate through sorted list of tuples, print each word frequency count
    for token, count in sorted_frequency_list:
        print(f"{token} - {count}")

# run program:

if __name__ == "__main__":
    # take in file from command line as an argument
    text_file_1 = sys.argv[1]

    # test tokenize()
    tokens = tokenize(text_file_1) # tokenize file specified on command line arguments

    # test compute_word_frequencies()
    token_frequencies = compute_word_frequencies(tokens)

    # test print_frequencies()
    print_frequencies(token_frequencies)