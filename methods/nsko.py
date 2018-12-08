import load_from_file

import numpy as np


def heavy_side(vector):
    for i in range(len(vector)):
        if vector[i] <= 0:
            vector[i] = 0
    return vector


def additional_constructions(ar_x, ar_cl):
    array_of_y = np.ones((1, len(ar_x))).transpose()

    for i in range(len(ar_x)):
        ar_x[i].append(1 if ar_cl[i] == 0 else -1)

    matrix_v = 0
    for i in range(len(ar_x)):
        if i == 0:
            matrix_v = np.array(ar_x[i])
        else:
            matrix_v = np.vstack((matrix_v, ar_x[i]))
    v_t_v = np.dot(matrix_v.transpose(), matrix_v)
    v_t_v_1 = np.linalg.inv(v_t_v)
    matrix_v_lamp = np.dot(v_t_v_1, matrix_v.transpose())  # * array_of_y
    weight_vector = np.dot(matrix_v_lamp, array_of_y)
    k = 0  # iterations
    while True:
        hv_func = heavy_side(np.dot(matrix_v, weight_vector) - array_of_y)
        if (np.dot(matrix_v, weight_vector)).all() > 0:
            return weight_vector
        elif (np.dot(matrix_v, weight_vector) - array_of_y == 0).all() and hv_func != 0:
            # классы не разделимы
            print('Classes are not separable.')
            return -1
        # y(k+1), w(k+1)
        array_of_y += hv_func  # y(k+1)
        weight_vector = np.dot(matrix_v_lamp, array_of_y)
        k += 1
    pass


def nsko(path=None):
    if path is None:
        return 0

    array_of_X, array_of_classes = load_from_file.load_for_nsko(path)

    answered = additional_constructions(ar_x=array_of_X, ar_cl=array_of_classes)

    return answered


if __name__ == '__main__':

    # array_of_X, array_of_classes = [
    #     [1, 2],
    #     [0, 2],
    #     [-1, -3],
    #     [-3, -2]
    # ], [
    #     0,
    #     0,
    #     1,
    #     1
    # ]

    my_path = '/Users/owl/Pycharm/PycharmProjects/MRZ/NSKO/input_file.txt'
    # array_of_X, array_of_classes = load_from_file.load_for_nsko(path)
    #
    # to_test = additional_constructions(ar_x=array_of_X, ar_cl=array_of_classes)
    to_test = nsko(my_path)
    print(to_test)
