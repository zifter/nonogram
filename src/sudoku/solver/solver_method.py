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


class SolverPolicy(object):
    def __init__(self):
        pass