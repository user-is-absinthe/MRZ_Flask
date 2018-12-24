# import load_from_file
from methods import func_load_from_file

import numpy as np
from matplotlib import pyplot


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
            return 1
        # y(k+1), w(k+1)
        array_of_y += hv_func  # y(k+1)
        weight_vector = np.dot(matrix_v_lamp, array_of_y)
        k += 1
    pass


def nsko(path_to_data=None, path_to_img=None):
    if path_to_data is None:
        return 1

    array_of_x, array_of_classes = func_load_from_file.load_for_nsko(path_to_data)

    answered = additional_constructions(ar_x=array_of_x, ar_cl=array_of_classes)

    if path_to_img is not None:
        if len(array_of_x[0]) == 3:  # or len(array_of_x) == 3:
            # figure = pyplot.figure()
            temp = list()
            for x in array_of_x:
                # pyplot.plot(x[0], x[1], style='r-')
                pyplot.scatter(x[0], x[1])
                temp.append(x[0])

            max_x = max(temp)
            min_x = min(temp)
            list_x = [i for i in np.arange(min_x, max_x, 0.1)]
            list_y = [answered[2]*x**2 + answered[1]*x + answered[0] for x in list_x]

            pyplot.plot(list_x, list_y)

        elif len(array_of_x[0]) == 4:
            pass

        pyplot.show()
        pass

    return answered


def my_split(arr, n):
    k, m = divmod(len(arr), n)
    return [arr[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def generator(amount_of_vectors=2, len_vectors=2, amount_of_classes=2, path=None):
    if amount_of_classes > amount_of_vectors:
        return 1

    vectors = [list(np.random.rand(len_vectors)) for i in range(amount_of_vectors)]

    temp = [i for i in range(amount_of_vectors)]
    classes = my_split(temp, amount_of_classes)
    for index_class, m_class in enumerate(classes):
        for index in range(len(m_class)):
            m_class[index] = index_class

    list_of_classes = list()
    for temp_class in classes:
        list_of_classes += temp_class

    for index, vector in enumerate(vectors):
        vector.append(list_of_classes[index])

    if path is None:
        return vectors
    else:
        with open(path, 'w') as file:
            for vector in vectors:
                for number in vector:
                    file.write(str(number) + ' ')
                file.write('\n')


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

    # test_path = '/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/static/nsko/input_file.txt'
    # array_of_X, array_of_classes = load_from_file.load_for_nsko(path)
    #
    # to_test = additional_constructions(ar_x=array_of_X, ar_cl=array_of_classes)
    # to_test = nsko(test_path)
    # print(to_test)

    path = '/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/static/nsko/test.txt'
    generator(
        amount_of_vectors=4,
        len_vectors=2,
        amount_of_classes=2,
        path=path
    )
    print(nsko(path_to_data=path, path_to_img=1))
