from base.solution import Solution

class LayoutIndex(object):
    def __init__(self, value, id, color=1):
        self._id = id
        self._color = color
        self._value = value
        self._done = False

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