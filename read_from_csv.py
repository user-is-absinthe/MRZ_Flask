import sys


def main():
    path = 'data.txt'
    my_matrix = open_matrix(path)
    print(my_matrix)
    if not good_matrix(my_matrix):
        sys.exit(1)
    else:
        print('Matrix is good.')
    pass


def good_matrix(matrix_str):
    len_prev = 0
    for i in range(len(matrix_str)):
        if i == 0:
            len_prev = len(matrix_str[i])
            continue
        len_now = len(matrix_str[i])
        if len_now != len_prev:
            return False
        len_prev = len_now
    return True


def open_matrix(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = [i.strip() for i in lines]
    return lines


if __name__ == '__main__':
    main()
