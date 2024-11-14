import sys


# Reads in a text file and returns a list of the tokens in that file.
# A token is a sequence of alphanumeric characters, independent of capitalization.
# 
# Runtime Complexity
# O(n) where n is the number of characters in the file;
# each character must be read once.
def tokenize(text_file_path: str) -> list[str]:
    token_list = []
    try:
        with open(text_file_path, "r", encoding = "utf-8") as text_file:
            token = ""
            while True:
                char = text_file.read(1)
                if not char:
                    token_list.append(token)
                    break
                elif ("0" <= char <= "9") or ("A" <= char <= "Z") or ("a" <= char <= "z"):
                    token += char
                else:
                    token_list.append(token)
                    token = ""
    except FileNotFoundError:
        print(f"File \"{text_file_path}\" not found.")
        sys.exit()
    except PermissionError:
        print(f"Cannot access \"{text_file_path}\".")
        sys.exit()

    return list(filter(lambda token : token != "", token_list))


# Counts the number of occurrences of each token in the token list.
# 
# Runtime Complexity
# O(n) where n is the number of tokens in the list;
# each token must be normalized once.
# 
# Counting is also O(n) where n is the number of normalized tokens;
# each token must be counted once.
def compute_word_frequencies(token_list: list[str]) -> dict[str, int]:
    token_dict = {}
    normalized_list = [token.lower() for token in token_list]
    for token in normalized_list:
        if token in token_dict:
            token_dict[token] += 1
        else:
            token_dict[token] = 1
    return token_dict


# Prints out the word frequency count onto the screen.
# The print out should be ordered by decreasing frequency (so, the highest frequency words first).
# 
# Runtime Complexity
# O(n) where n is the number of tokens in the dictionary;
# each token must be printed once with its frequency.
def print_frequencies(frequencies: dict[str, int]) -> None:
    inverted_frequencies = [(frequencies[token], token) for token in frequencies]
    sorted_tokens = sorted(inverted_frequencies, reverse = True)
    for token in sorted_tokens:
        print(f"{token[1]} - {token[0]}")


if __name__ == "__main__":
    try:
        print_frequencies(compute_word_frequencies(tokenize(sys.argv[1])))
    except IndexError:
        print("File name not provided.")

