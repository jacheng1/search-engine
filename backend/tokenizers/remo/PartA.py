# Part A: Tokenizer
import sys

def tokenize(text_file_path: str) -> list:
    """
    Runtime Complexity: O(n)

    Outer loop (reading each line): Line by line is O(n) with n being the 
    total number of characters in the file

    Inner loop (processing each character in a line): O(n) - length of line

    Reads in a text file and returns a list of the tokens in that file.
    For the purposes of this project, a token is a sequence of alphanumeric characters, independent
    of capitalization.

    :param textFilePath: Path to the text file to be read
    :return: List of the tokens in that file.
    """
    tokens = []
    try:
        with open(text_file_path, "r") as file:
            for currLine in file:
                currentToken = ''

                for letter in currLine:
                    if letter.isalnum():
                        currentToken += letter
                    else:
                        if currentToken:
                            tokens.append(currentToken.lower())
                            currentToken = ''
                
                if currentToken:
                    tokens.append(currentToken.lower())

    except FileNotFoundError:
        print(f"Error: the file {text_file_path} was not found.")
        sys.exit(1)

    return list(tokens)


def compute_word_frequencies(tokens: list) -> dict:
    """
    Runtime Complexity: O(n) 

    Linear iteration of token in tokens

    Counts the number of occurrences of each token in the token list
    Must write this from scratch.

    :param tokens: List of tokens
    :return: dict, mapping each token to the number of occurrences
    """
    word_count = {}
    for token in tokens:
        if token in word_count:
            word_count[token] += 1
        else:
            word_count[token] = 1 

    return word_count    


def print_frequencies(frequencies: dict) -> None:
    """
    Runtime Complexity: O(nlogn)

    Sorting the items takes O(n log n) and iteration is O(n) -> O(nlogn)

    Outputs each token with their respective frequency in the output 
    <token> = <freq>
    """
    for token, freq in sorted(frequencies.items(),key=lambda item: item[1], reverse=True):
        print(token, " = ",  freq)


if __name__ == '__main__':
    a = tokenize(sys.argv[1])
    b = compute_word_frequencies(a)
    print_frequencies(b)