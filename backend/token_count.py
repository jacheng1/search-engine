import os

def count_unique_tokens(directory="partial-index"):
    unique_token_count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding="UTF-8") as file:
                unique_token_count += sum(1 for line in file)
    return unique_token_count


unique_token_count = count_unique_tokens()
print(f"Number of unique tokens: {unique_token_count}")