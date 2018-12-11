import sys


def main():
    # path = 'data.txt'
    path = 'C:\\Users\Worker\Pycharm\Pycharm_project\MRZ_Flask\static\\true_chromatic\\temp_matrix.txt'
    # my_matrix = open_matrix(path)
    # print(my_matrix)
    # if not good_matrix(my_matrix):
    #     sys.exit(1)
    # else:
    #     print('Matrix is good.')
    # pass
    print(open_alien_matrix(path=path))


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
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        return ['1', '12']
    lines = [i.strip() for i in lines]
    while True:
        try:
            lines.remove('')
        except ValueError:
            break
    return lines


def open_alien_matrix(path):
    matrix_str = open_matrix(path=path)
    if good_matrix(matrix_str=matrix_str):
        return matrix_str
    else:
        return 'bad'


if __name__ == '__main__':
    main()
