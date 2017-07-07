from math import atan2, pi


class Position:
    def __init__(self, x=0, y=0, pos=None):
        assert type(x) is int
        assert type(y) is int
        if pos is None:
            self.pos = [x, y]
        else:
            if type(pos) is Position:
                self.pos = [pos.x(), pos.y()]
            else:
                self.pos = pos

    def x(self, x=None):
        if x is None:
            return self.pos[0]
        else:
            self.pos[0] = x

    def y(self, y=None):
        if y is None:
            return self.pos[1]
        else:
            self.pos[1] = y

    def set(self, pos=None):
        if pos is not None:
            if type(pos) is Position:
                self.pos = [pos.x(), pos.y()]
            else:
                self.pos = pos

    def __add__(self, other):
        return Position(pos=[self.pos[0] + other.pos[0], self.pos[1] + other.pos[1]])

    def __mul__(self, other):
        return self.pos[0] * other.pos[0] + self.pos[1] * other.pos[1]

    def __lt__(self, other):
        diff_x = other.pos[0] - self.pos[0]
        diff_y = other.pos[1] - self.pos[1]
        angle = atan2(diff_x, diff_y) * 180 / pi
        if angle < 0:
            angle += 360
        return angle

    def __str__(self):
        #print(str(self.pos))
        return '<' + str(self.pos[0]) + ', ' + str(self.pos[1]) + '>'


def main():
    pos0 = Position(0, 0)
    pos1 = Position(0, 1)
    pos2 = Position(1, 1)
    pos3 = Position(1, 0)
    pos4 = Position(1, -1)
    pos5 = Position(0, -1)
    pos6 = Position(-1, -1)
    pos7 = Position(-1, 0)
    pos8 = Position(-1, 1)
    ans1 = pos0 < pos1
    ans2 = pos0 < pos2
    ans3 = pos0 < pos3
    ans4 = pos0 < pos4
    ans5 = pos0 < pos5
    ans6 = pos0 < pos6
    ans7 = pos0 < pos7
    ans8 = pos0 < pos8
    ans9 = pos1 + pos2
    ans10 = pos3 * pos4
    print('%s < %s = %s' % (pos0, pos1, ans1))
    print('%s < %s = %s' % (pos0, pos2, ans2))
    print('%s < %s = %s' % (pos0, pos3, ans3))
    print('%s < %s = %s' % (pos0, pos4, ans4))
    print('%s < %s = %s' % (pos0, pos5, ans5))
    print('%s < %s = %s' % (pos0, pos6, ans6))
    print('%s < %s = %s' % (pos0, pos7, ans7))
    print('%s < %s = %s' % (pos0, pos8, ans8))
    print('%s + %s = %s' % (pos1, pos2, ans9))
    print('%s * %s = %s' % (pos3, pos4, ans10))


if __name__ == '__main__':
    main()
