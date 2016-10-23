class Iterator(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def next(self):
        raise NotImplemented()


class IteratorLine(Iterator):
    def __init__(self, matrix):
        Iterator.__init__(self, matrix)
        self.currentIndex = 0

    def next(self):
        try:
            return self._value()
        finally:
            self.currentIndex += 1

    def _value(self):
        x, y = self.matrix.shape
        if self.currentIndex == (x + y):
            return None

        if self.currentIndex >= x:
            return self.matrix.column(self.currentIndex - x)
        else:
            return self.matrix.row(self.currentIndex)


class IteratorBoxToList(Iterator):
    def __init__(self, matrix, shape):
        Iterator.__init__(self, matrix)
        self.currentX = 0
        self.currentY = 0
        self.shape = shape

    def next(self):
        try:
            return self._value()
        finally:
            self.currentX += self.shape[0]
            if self.currentX >= self.matrix.shape[0]:
                self.currentX = 0
                self.currentY += self.shape[1]


    def _value(self):
        x, y = self.matrix.shape
        if self.currentY >= y or self.currentX >= x:
            return None

        return self.matrix.sub_matrix(self.currentX, self.currentY, self.shape).to_list()

