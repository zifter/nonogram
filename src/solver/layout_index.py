from base.solution import Solution

class LayoutIndex(object):
    uid = 1000
    def __init__(self, value, color=1):
        self._id = LayoutIndex.__getId()
        self._color = color
        self._value = value
        self._done = False

    @staticmethod
    def __getId():
        LayoutIndex.uid += 1
        return LayoutIndex.uid

    def __repr__(self):
        return "<%s, %s, %s>" % (self.value(), self.color(), self.id())

    def __str__(self):
        return "<%s, %s, %s>" % (self.value, self._id, self._color)

    def value(self):
        return self._value

    def color(self):
        return self._color

    def id(self):
        return self._id

    def cross_out(self):
        self._done = True

    def is_crossed_out(self):
        return self._done

    def is_none(self):
        return self._id == -1

    def is_spase(self):
        return self._id == 0

    def __eq__(self, other):
        return type(other) is LayoutIndex and not self.is_spase() and not self.is_none() and self._id == other._id

    def __ne__(self, other):
        return not self.__eq__(other)


class SmartTuple(object):
    def __init__(self, v1=None, v2=None):
        self.v = [v1, v2]

    def test_eq1(self, v):
        return self.v[0] == v or self.v[1] == v

    def tuple_eq1(self, st):
        return self.test_eq1(st[0]) or self.test_eq1(st[1])

    def tuple_eq2(self, st):
        return self[0] == st[0] and self[1] == st[1] or \
            self[0] == st[1] and self[1] == st[0]

    def __getitem__(self, item):
        return self.v[item]

    def __setitem__(self, key, value):
        return self.v.__setitem__(key, value)

    def __repr__(self):
        return "%s" % str(self.v)

    def __str__(self):
        return "%s" % str(self.v)


class SoftTuple(SmartTuple):
    def __eq__(self, other):
        if type(other) in (SmartTuple, tuple):
            return self.tuple_eq1(other)

        return self.test_eq1(other)

class SolutionCell(SoftTuple):
    def __init__(self):
        self.v = [-1, -1]


class StrictTuple(SmartTuple):
    def __eq__(self, other):
        if type(other) in (SmartTuple, tuple):
            return self.tuple_eq2(other)

        raise RuntimeError("Something goes wrong %s" % str(other))