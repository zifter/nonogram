import math

class SolverMethod(object):
    @staticmethod
    def line_layout(line):
        undefined = []
        defined = []
        for i in line:
            if i == 0:
                undefined.append(i)
            else:
                defined.append(i)

        return defined, undefined

    @staticmethod
    def belonged_box(x, y, matrix, shape):
        start_x = int(math.floor(x / shape[0])) * shape[0]
        start_y = int(math.floor(y / shape[1])) * shape[1]

        return matrix.sub_matrix(start_x, start_y, shape)


class SolverPolicy(object):
    def __init__(self):
        pass