from nonogram.solution_step import SolutionStep
from nonogram.base.solution import SolutionPrinter

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

        goal = True
        while goal:
            goal = self.execute_for_each_line(self.find_intersection)

        self.ss = None
        return ss.solution()

    def apply(self, type, r):
        for i, index in r:
            if SolutionStep.ROW == type:
                self.ss.set_row(i, index)
            else:
                self.ss.set_col(i, index)

    def execute_for_each_line(self, func):
        stepToGoal = False
        x_size, y_size = self.ss.shape()
        space = self.nonogram.space_size()
        for i in xrange(y_size):
            layout, line = self.ss.row_layout(i), self.ss.row_lineup(i)
            print self.step
            r = func(layout, line, space)
            self.apply(SolutionStep.ROW, r)
            if r:
                print SolutionPrinter.pretty_string(self.ss.solution(), selected_row=i)
                stepToGoal = r or stepToGoal
            self.step += 1

        for i in xrange(x_size):
            layout, line = self.ss.col_layout(i), self.ss.col_lineup(i)
            print self.step
            r = func(layout, line, space)
            self.apply(SolutionStep.COL, r)
            if r:
                print SolutionPrinter.pretty_string(self.ss.solution(), selected_column=i)
                stepToGoal = r or stepToGoal
            self.step += 1

        return stepToGoal

    def find_intersection(self, layout, line, space):
        result_line = SolveMethod.find_intersection(layout, line, space)

        r = dict()
        for i in xrange(len(result_line)):
            if result_line[i] is not None and line[i] != result_line[i]:
                r[i] = result_line[i]

        return r


class SolveMethod(object):
    class VAL:
        UNDEFINED = -1,
        SPACE = 0,

    @staticmethod
    def layout_min_size(layout, space, plusOneSpace=False):
        offsetFromEnd = 0
        if layout:
            offsetFromEnd = space * (len(layout) - int(not plusOneSpace) )
            for v in layout:
                offsetFromEnd += v.value()

        return offsetFromEnd

    @staticmethod
    def get_suitable_line_up(index, line, space):
        if index.value() > len(line):
            raise LineOutOfRange

        r = []

        firstPosOfIndex = len(line)
        for i in xrange(len(line)-index.value() + 1):
            if line[i] == index:
                firstPosOfIndex = i + index.value()
                break

        for i in xrange(0, firstPosOfIndex - index.value() + 1):
            positionIsSuitable = True
            for v in line[i:i+index.value()]:
                if not (v == -1 or v == index):
                    positionIsSuitable = False
                    break

            nextCells = line[i+index.value():i+index.value() + space]
            for v in nextCells:
                if v not in (-1, 0):
                    positionIsSuitable = False
                    break

            if positionIsSuitable:
                pretend = deepcopy(line)
                for v in xrange(i, i+index.value()):
                    pretend[v] = index
                r.append(pretend)

        return r

    @staticmethod
    def merge_lineups(lineups):
        r = deepcopy(lineups[0])
        for i in xrange(1, len(lineups)):
            for j in xrange(len(r)):
                if r[j] != lineups[i][j]:
                    r[j] = None

        return r

    @staticmethod
    def __make_space_index(index1, index2):
        if index1:
            if index2:
                if index1.id() == index2.id():
                    raise SolverException("Check indexes in you tests!")

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
    def get_minimum_offset(index, line, space):
        if index.value() > len(line):
            raise LineOutOfRange

        offset = 0
        suitableCells = 0
        for i in xrange(len(line)):
            if line[i] == -1 or line[i] == index:
                suitableCells += 1
            elif line[i] == 0:
                suitableCells = 0
            elif line[i] != index:
                raise SolverException("Cross with other color")

            if suitableCells >= index.value():
                spaceOk = True
                for j in xrange(space):
                    if i+j+1 >= len(line):
                        break

                    v = line[i+j+1]
                    if not(v == -1 or v == 0):
                        spaceOk = False
                        break

                if spaceOk:
                    offset = i + space + 1
                    break


        return offset

    @staticmethod
    def get_offset_from_end(layout, line, space):
        if not layout:
            return (0, [])

        info = {}
        offset = 0
        newLayout = []
        r = SolveMethod.fill_line(list(reversed(layout)), list(reversed(line)), space)
        firstIndex = layout[0]
        for i in xrange(len(r)):
            if r[i] == firstIndex:
                offset = i+1
            if r[i] not in info:
                info[r[i]] =  0
            info[r[i]] += 1

        for i in xrange(len(layout)):
            index = layout[i]
            if info[index] == index.value():
                newLayout = layout[i+1:]
                break

        offset += space

        return (offset, newLayout)

    @staticmethod
    def get_offset_from_start(index, line, nextIndexExist):
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
            elif line[i] == index:
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
                    pe = SolveMethod.get_offset_from_start(index, line[0:ps], nextIndexExist)
                else:
                    raise IndexOutOfRange

            return pe - index.value()

        return 0


    @staticmethod
    def fill_line(layout, line, space):
        """

        :param layout: [LayoutIndex, ..]
        :param line:  [li, li, li, 1, ]
        :param space: size of space
        :return: [LayoutIndex] suitable line for this layout
        """
        if not layout:
            return [(None, None)] * len(line)

        print line
        print layout
        result = deepcopy(line)
        line_len = len(result)
        p = 0
        i = 0
        prev_index = None
        index = layout[0]
        next_index = layout[1] if (len(layout) > 1) else None
        while index:
            nextLayout = layout[i+1:]
            endLine = line[p + SolveMethod.get_minimum_offset(index, line[p:], space):]
            (offsetFromEnd, nextLayout) = SolveMethod.get_offset_from_end(nextLayout, endLine, space)
            offsetFromeStart = SolveMethod.get_offset_from_start(index, line[p:line_len - offsetFromEnd], len(nextLayout) != 0)
            if offsetFromeStart > 0:
                for v in xrange(p, p + offsetFromeStart):
                    result[v] = SolveMethod.__make_space_index(prev_index, index)
                p += offsetFromeStart

            currentLineForIndex = line[p:line_len - offsetFromEnd]
            suitableLineUps = SolveMethod.get_suitable_line_up(index, currentLineForIndex, space)

            if not suitableLineUps:
                raise SolverException("Suitable line up doesn't found: %s = %s" % (index, currentLineForIndex))

            indexStarted = False
            lineUp = suitableLineUps[0]
            offset = 0
            while offset < len(lineUp):
                if lineUp[offset] == index:
                    result[p + offset] = index
                    indexStarted = True
                else:
                    if lineUp[offset] in (-1, 0) and not indexStarted:
                        result[p + offset] = SolveMethod.__make_space_index(prev_index, index)

                    if indexStarted:
                        break

                offset += 1

            p += offset

            mergedLineups = None
            spaceSize = space
            if next_index is None:
                mergedLineups = SolveMethod.merge_lineups(suitableLineUps)[offset:]
                spaceSize = len(result) - p

            # if line[p-1] == index.color():
            #     for v in xrange(space):
            #         result[p] = SolveMethod.__make_space_index(index, next_index)
            #         p += 1
            #
            #     spaceSize -= space

            for v in xrange(spaceSize):
                if next_index is not None and p > len(result):
                    raise LineOutOfRange()

                if result[p] == 0 or next_index is not None or (mergedLineups is not None and mergedLineups[v] == -1):
                    result[p] = SolveMethod.__make_space_index(index, next_index)
                else:
                    result[p] = None

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
            if forward_line[i] == reversed_line[i] and reversed_line[i] is not None:
                # -1 - space
                result[i] = 0 if type(forward_line[i]) is tuple else forward_line[i]

        return result
