import os


def fix_path(wrecked_path):
    path_list = wrecked_path.split('/')
    points_index = path_list.index('..')
    path_list.pop(points_index)
    path_list.pop(points_index - 1)
    return_str = ''
    for i in path_list:
        return_str += i + '/'
    return return_str[:len(return_str) - 1]


def get_path():
    return os.path.dirname(__file__)


if __name__ == '__main__':
    print('/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/methods/../data/true_chromatic/monochromgraph.png')
    print(fix_path('/Users/owl/Pycharm/PycharmProjects/MRZ_Flask/methods/../data/true_chromatic/monochromgraph.png'))
