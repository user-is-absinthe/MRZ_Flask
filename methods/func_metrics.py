import numpy


def evklid_lenght(vector_1, vector_2, arguments=0):
    if len(vector_1) != len(vector_2):
        print('Lenght vector A != lenght vector B.')
        return -1
    temp_list = []
    for i in range(len(vector_1)):
        temp_list.append((vector_1[i] - vector_2[i]) ** 2)
    return (sum(temp_list))**0.5


def mannhetn_lenght(vector_1, vector_2, arguments=0):
    if len(vector_1) != len(vector_2):
        print('Lenght vector A != lenght vector B.')
        return -1
    temp_list = []
    for i in range(len(vector_1)):
        temp_list.append(abs(vector_1[i] - vector_2[i]))
    return sum(temp_list)


def rem_metr(vector_1, vector_2, arguments=0):
    if len(vector_1) != len(vector_2):
        print('Lenght vector A != lenght vector B.')
        return -1
    temp_list = []
    for i in range(len(vector_1)):
        temp_list.append(abs(vector_1[i] - vector_2[i]))
    return max(temp_list)


def minkovskiy(vector_1, vector_2, p_t):
    if len(vector_1) != len(vector_2) or p_t == 0:
        print('Lenght vector A != lenght vector B or p == zero.')
        return -1
    temp_list = []
    for i in range(len(vector_1)):
        temp_list.append((vector_1[i] - vector_2[i]) ** p_t)
    return (sum(temp_list))**(1 / p_t)


def camber_metr(vector_1, vector_2, arguments=0):
    if len(vector_1) != len(vector_2):
        print('Lenght vector A != lenght vector B.')
        return -1
    temp_list = []
    for i in range(len(vector_1)):
        temp_list.append(abs(vector_1[i] - vector_2[i]) / (abs(vector_1[i]) + abs(vector_2[i])))
    return sum(temp_list)


# def mohave(vector_1, vector_2, matrix):
#    if len(vector_1) != len(vector_2) or len(matrix) != len(vector_2) or len(matrix[0]) != len(vector_2):
#        print('Lenght vector A != lenght vector B or matrix not sqare.')
#        return -1
#    matrix = numpy.array(matrix)
#    matrix_minus_one = matrix.
    

def to_centr(many_vectors, one_vector, name, arguments=0):
    many_vectors = numpy.array(many_vectors)
    centr = many_vectors.sum(0)
    
    if name == 'evklid_lenght':
        return evklid_lenght(centr, one_vector)
    elif name == 'mannhetn_lenght':
        return mannhetn_lenght(centr, one_vector)
    elif name == 'rem_metr':
        return rem_metr(centr, one_vector)
    elif name == 'minkovskiy':
        return minkovskiy(centr, one_vector, arguments)
    elif name == 'camber_metr':
        return camber_metr(centr, one_vector)
    
    
def nearly(many_vectors, one_vector, name, arguments=0):
    many_vectors = numpy.array(many_vectors)
    dist = []
    if name == 'evklid_lenght':
        name = evklid_lenght
    elif name == 'mannhetn_lenght':
        name = mannhetn_lenght
    elif name == 'rem_metr':
        name = rem_metr
    elif name == 'minkovskiy':
        name = minkovskiy
    elif name == 'camber_metr':
        name = camber_metr
    for i in many_vectors:
        dist.append(name(one_vector, i, arguments))
    return min(dist)
    

def etalon(etalons_vectors, one_vector, name, arguments=0):
    return nearly(etalons_vectors, one_vector, name, arguments=0)


# def nearly_max(many_vectors, one_vector, arguments=0):
#    pass


def all_metrics(p_eqval, vector_b, vector_a):
    vector_a = numpy.array(vector_a)
    vector_b = numpy.array(vector_b)

    answered = dict()

    if isinstance(vector_a[0], numpy.ndarray):
        # a - matrix
        answered['to_centr_evklid_lenght'] = to_centr(vector_a, vector_b, 'evklid_lenght')
        answered['to_centr_mannhetn_lenght'] = to_centr(vector_a, vector_b, 'mannhetn_lenght')
        answered['to_centr_rem_metr'] = to_centr(vector_a, vector_b, 'rem_metr')
        answered['to_centr_minkovskiy'] = to_centr(vector_a, vector_b, 'minkovskiy', p_eqval)
        answered['to_centr_camber_metr'] = to_centr(vector_a, vector_b, 'camber_metr')

        answered['nearly_evklid_lenght'] = nearly(vector_a, vector_b, 'evklid_lenght')
        answered['nearly_mannhetn_lenght'] = nearly(vector_a, vector_b, 'mannhetn_lenght')
        answered['nearly_rem_metr'] = nearly(vector_a, vector_b, 'rem_metr')
        answered['nearly_minkovskiy'] = nearly(vector_a, vector_b, 'minkovskiy', p_eqval)
        answered['nearly_camber_metr'] = nearly(vector_a, vector_b, 'camber_metr')
    else:
        # a - vector
        answered['evklid_lenght'] = evklid_lenght(vector_a, vector_b)
        answered['mannhetn_lenght'] = mannhetn_lenght(vector_a, vector_b)
        answered['rem_metr'] = rem_metr(vector_a, vector_b)
        answered['minkovskiy'] = minkovskiy(vector_a, vector_b, p_eqval)
        answered['camber_metr'] = camber_metr(vector_a, vector_b)

    return answered


# def read_data(filename='./input_file/data_lenght.txt'):
#     file = open(filename, 'r')
#     data = file.read()
#     data = data.split('\n')
#     if data[-1] == '':
#         data.pop(-1)
#     ar = data[0].split(' ')
#     br = data[1].split(' ')
#     pr = data[2]
#     matrixr = data[3:]
#     file.close()
#     return ar, br, pr, matrixr


def read_data(path):
    with open(path, 'r') as file:
        data = file.readlines()

    data = [i.strip() for i in data]

    p = float(data[0])
    vector_a = [float(i) for i in data[1].split(', ')]

    temp = data[2:]
    if len(temp) == 1:
        vector_b = [float(i) for i in data[2].split(', ')]
    else:
        vector_b = list()
        for line in temp:
            vector_b.append([float(i) for i in line.split(', ')])

    return p, numpy.array(vector_a), numpy.array(vector_b)


if __name__ == '__main__':
    # a = [1, 2, 3]
    # b = [3, 2, 1]
    # p = 4
    # matrix = [[1, 2, 3],
    #           [4, 5, 6],
    #           [7, 8, 9]]
    # [a, b, p, matrix] = read_data()
    # b = a
    
    # print(evklid_lenght(a, b))
    # print(mannhetn_lenght(a, b))
    # print(rem_metr(a, b))
    # print(minkovskiy(a, b, p))
    # print(camber_metr(a, b))
    # print('\n')
    #
    # print(to_centr(matrix, b, 'evklid_lenght'))
    # print(to_centr(matrix, b, 'mannhetn_lenght'))
    # print(to_centr(matrix, b, 'rem_metr'))
    # print(to_centr(matrix, b, 'minkovskiy', p))
    # print(to_centr(matrix, b, 'camber_metr'))
    # print('\n')
    #
    # print(nearly(matrix, b, 'evklid_lenght'))
    # print(nearly(matrix, b, 'mannhetn_lenght'))
    # print(nearly(matrix, b, 'rem_metr'))
    # print(nearly(matrix, b, 'minkovskiy', p))
    # print(nearly(matrix, b, 'camber_metr'))

    print(read_data('/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/static/metrics/test.txt'))
