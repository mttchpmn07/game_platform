from math import atan2, sin, cos, pi, sqrt


class Position:
    def __init__(self, x=0.0, y=0.0, pos=None):
        assert type(x) is int or float
        assert type(y) is int or float
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

    def get_unit(self, direct, mag):
        angle = self < direct
        ret = Position(0.0, 0.0)
        # print('Angle : %f' % (angle % 90))
        if 0 <= angle < 90:
            ret.x(round(mag * abs(sin(angle / 180 * pi)), 2))
            ret.y(round(mag * abs(cos(angle / 180 * pi)), 2))
        elif 90 <= angle < 180:
            ret.x(round(mag * abs(sin((angle / 180 * pi) % 90)), 2))
            ret.y(round(-mag * abs(cos((angle / 180 * pi) % 90)), 2))
        elif 180 <= angle < 270:
            ret.x(round(-mag * abs(sin((angle / 180 * pi) % 90)), 2))
            ret.y(round(-mag * abs(cos((angle / 180 * pi) % 90)), 2))
        else:
            ret.x(round(-mag * abs(sin((angle / 180 * pi) % 90)), 2))
            ret.y(round(mag * abs(cos((angle / 180 * pi) % 90)), 2))
        return ret

    def __add__(self, other):
        return Position(pos=[self.pos[0] + other.pos[0], self.pos[1] + other.pos[1]])

    def __sub__(self, other):
        return Position(pos=[self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]])

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
        # print(str(self.pos))
        return '<' + str(round(self.pos[0], 2)) + ', ' + str(round(self.pos[1], 2)) + '>'


def main():
    pos0 = Position(0.0, 0.0)
    pos1 = Position(0.0, 1.0)
    pos2 = Position(1.0, 1.0)
    pos3 = Position(1.0, 0.0)
    pos4 = Position(1.0, -1.0)
    pos5 = Position(0.0, -1.0)
    pos6 = Position(-1.0, -1.0)
    pos7 = Position(-1.0, 0.0)
    pos8 = Position(-1.0, 1.0)
    pos0 = pos0 + Position(1.0, 1.0)
    pos1 = pos1 + Position(1.0, 1.0)
    pos2 = pos2 + Position(1.0, 1.0)
    pos3 = pos3 + Position(1.0, 1.0)
    pos4 = pos4 + Position(1.0, 1.0)
    pos5 = pos5 + Position(1.0, 1.0)
    pos6 = pos6 + Position(1.0, 1.0)
    pos7 = pos7 + Position(1.0, 1.0)
    pos8 = pos8 + Position(1.0, 1.0)
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
    unit1 = pos0.get_unit(pos1, 1)
    unit2 = pos0.get_unit(pos2, 1)
    unit3 = pos0.get_unit(pos3, 1)
    unit4 = pos0.get_unit(pos4, 1)
    unit5 = pos0.get_unit(pos5, 1)
    unit6 = pos0.get_unit(pos6, 1)
    unit7 = pos0.get_unit(pos7, 1)
    unit8 = pos0.get_unit(pos8, 1)
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
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos1, unit1))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos2, unit2))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos3, unit3))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos4, unit4))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos5, unit5))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos6, unit6))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos7, unit7))
    print('Unit for %s in %s direction with magnitude 1 is %s' % (pos0, pos8, unit8))


if __name__ == '__main__':
    main()
