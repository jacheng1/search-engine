import PartA as A
import sys


# Return the number of common tokens from both files.
# 
# Runtime Complexity
# Worst case O(n * m) where n and m are the number of normalized tokens in each file, respectively;
# each token from both sets must be compared.
def find_intersection(text_file_path_1: str, text_file_path_2: str) -> int:
    token_list_1 = A.tokenize(text_file_path_1)
    normalized_set_1 = {token.lower() for token in token_list_1}

    token_list_2 = A.tokenize(text_file_path_2)
    normalized_set_2 = {token.lower() for token in token_list_2}
    
    intersection = normalized_set_1 & normalized_set_2
    return len(intersection)


if __name__ == "__main__":
    try:
        print(find_intersection(sys.argv[1], sys.argv[2]))
    except IndexError:
        print("File names not provided.")

