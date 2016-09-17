from solution_step import SolutionStep

from copy import copy, deepcopy

class SolverException(RuntimeError):
    pass

class LineOutOfRange(SolverException):
    pass

class IndexOutOfRange(SolverException):
    pass

class Solver(object):
    def __init__(self):
        self.step = 0
        self.type = "black"
        self.nonogram = None
        self.ss = None

    def solve(self, nonogram):
        self.nonogram = nonogram

        ss = SolutionStep(self.nonogram)
        self.ss = ss

        for i in xrange(10):
            self.execute_for_each_line(self.find_intersection)

        self.ss = None
        return ss.solution()

    def execute_for_each_line(self, func):
        x_size, y_size = self.ss.shape()
        space = self.nonogram.space_size()
        for i in xrange(y_size):
            layout, line = self.ss.row_layout_and_solution(i)
            print self.step
            if self.step == 49:
                pass
            if func(layout, line, space):
                print self.ss.solution()
            self.step += 1

        for i in xrange(x_size):
            layout, line = self.ss.col_layout_and_solution(i)
            print self.step
            if self.step == 49:
                pass
            if func(layout, line, space):
                print self.ss.solution()
            self.step += 1

    def find_intersection(self, layout, line, space):
        result_line = SolveMethod.find_intersection(layout, [int(i) for i in line], space)
        stepToGoal = False
        for i in xrange(len(result_line)):
            if result_line[i] is not None and line[i] != result_line[i]:
                line[i] = result_line[i]
                stepToGoal = True

        return stepToGoal


class SolveMethod(object):
    @staticmethod
    def cells_amount(layout, space):
        offsetFromEnd = 0
        if layout:
            offsetFromEnd = space * (len(layout) - 1)
            for v in layout:
                offsetFromEnd += v.value()

        return offsetFromEnd

    @staticmethod
    def __make_space_index(index1, index2):
        if index1:
            if index2:
                if index1.id() == index2.id():
                    raise SolverException()

                if index1.id() < index2.id():
                    return (index1, index2)
                else:
                    return (index2, index1)
            else:
                return (index1, None)
        else:
            if not index2:
                raise SolverException()

            return (index2, None)

    @staticmethod
    def find_nearest_pos(index, line, nextIndexExist):
        # TODO: color
        firstEmpty = None
        emptyCellsAmount = 0
        ps = None
        pe = None
        for i in xrange(len(line)):
            if line[i] == -1 and ps is None:
                if firstEmpty is None:
                    firstEmpty = i
                emptyCellsAmount += 1
            elif line[i] == index.color():
                if not ps:
                    ps = i
            elif ps:
                if not pe:
                    pe = i
                    break

        if emptyCellsAmount >= index.value() and nextIndexExist:
            return firstEmpty

        if not pe and ps:
            pe = len(line)

        if pe:
            if pe - ps > index.value():
                if nextIndexExist:
                    # it's mean we found another index, move back
                    pe = SolveMethod.find_nearest_pos(index, line[0:ps], nextIndexExist)
                else:
                    raise IndexOutOfRange

            return pe - index.value()

        return 0


    @staticmethod
    def fill_line(layout, line, space):
        """

        :param layout: [LayoutIndex, ..]
        :param line:  [0, 0, 0, 1, ]. 0 - undefined, value > 0 - it's a index of layout index
        :param space: size of space
        :return: [LayoutIndex] suitable line for this layout
        """
        if not layout:
            return [(None, None)] * len(line)

        # print line
        # print layout
        result = deepcopy(line)
        line_len = len(result)
        p = 0
        i = 0
        prev_index = None
        index = layout[0]
        next_index = layout[1] if (len(layout) > 1) else None
        while index:
            next_indexes = layout[i+1:]
            offsetFromEnd = SolveMethod.cells_amount(next_indexes, space) + space if next_indexes else 0

            offset_start_point = SolveMethod.find_nearest_pos(index, line[p:line_len - offsetFromEnd], next_indexes)
            if offset_start_point > 0:
                for v in xrange(p, p + offset_start_point):
                    result[v] = SolveMethod.__make_space_index(prev_index, index)
                p += offset_start_point

            # try suitable position for
            positionIsSuitable = False
            while not positionIsSuitable:
                if p + index.value() > line_len:
                    print line
                    print result
                    raise LineOutOfRange()

                positionIsSuitable = True
                pretend = result[p:p + index.value()]
                for v in pretend:
                    if not (v == -1 or v == index.color()):
                        positionIsSuitable = False
                        break

                if not positionIsSuitable:
                    result[p] = SolveMethod.__make_space_index(prev_index, index)
                    p += 1
                else:
                    for v in xrange(p, p + index.value()):
                        try:
                            result[v] = index
                        except:
                            pass

                    p += index.value()

            space = space if next_index is not None else len(result) - p
            for v in xrange(space):
                if next_index is not None and p > len(result):
                    raise LineOutOfRange()

                result[p] = SolveMethod.__make_space_index(index, next_index)
                p += 1

            i += 1
            prev_index = index
            index = next_index
            next_index = layout[i + 1] if len(layout) > (i + 1) else None


        return result

    @staticmethod
    def find_intersection(layout, line, space):
        forward_line = SolveMethod.fill_line(layout, line, space)
        reversed_line = SolveMethod.fill_line(list(reversed(layout)), list(reversed(line)), space)[::-1]

        result = [None] * len(line)
        for i in xrange(len(line)):
            if forward_line[i] == reversed_line[i]:
                # -1 - space
                result[i] = 0 if type(forward_line[i]) is tuple else reversed_line[i].color()

        return result
