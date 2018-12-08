def load_for_nsko(path):
    with open(path, 'r') as file:
        lines = file.readlines()

        lines = [line.strip() for line in lines]
        lines = [[symbol for symbol in line.split(' ')] for line in lines]

        array_classes = [line.pop(-1) for line in lines]

        # print(lines, '\n', array_classes)
        lines = [[int(number) for number in line] for line in lines]
        array_classes = list(map(int, array_classes))
        return lines, array_classes


if __name__ == '__main__':
    print('\n\n\tTEST WORK MODE!', end='\n\n\n')
    print(load_for_nsko('input_file.txt'))
