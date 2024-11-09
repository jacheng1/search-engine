# Part B: Intersection of two files
import PartA as A
import sys

def sorted_lists_intersection(list_a: list, list_b: list) -> list:
    """
    :params: 
        list_a - the first list of tokens
        list_b - the second list of tokens
    
    :return: 
        returns the intersection of lists A and B 
    """
    a_iter = 0
    b_iter = 0
    result = []

    while a_iter < len(list_a) and b_iter < len(list_b):
        if list_a[a_iter] < list_b[b_iter]:
            a_iter += 1
        elif list_a[a_iter] > list_b[b_iter]:
            b_iter += 1
        else:
            result.append(list_a[a_iter])
            a_iter += 1
            b_iter += 1
    
    return result

if __name__ == '__main__':
    text_file_1 = sys.argv[1]
    text_file_2 = sys.argv[2]

    file1_tokens = A.tokenize(text_file_1)
    file2_tokens = A.tokenize(text_file_2)

    # Sort the tokens before calling sort function
    file1_tokens.sort()
    file2_tokens.sort()

    intersection_list = sorted_lists_intersection(file1_tokens, file2_tokens)
    print(intersection_list)
    print(len(intersection_list))
    


    

