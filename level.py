import json
import random


from PyQt5.QtCore import QPointF, Qt, QTimer
from PyQt5.QtGui import (QColor, QLinearGradient, QPainter, QPixmap)
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsScene, QGraphicsView)

TILE_SIZE = 64
TILE_COUNT = 64
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Tile:
    def __init__(self, sheet=None, x=0, y=0, x_shift=TILE_SIZE, y_shift=TILE_SIZE):
        self.sheet = sheet
        self.x = x
        self.y = y
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.pix = QPixmap(self.sheet).copy(self.x, self.y, self.x_shift, self.y_shift)

    def get_pix(self):
        return self.pix

    def serialize(self):
        return [self.sheet, self.x, self.y, self.x_shift, self.y_shift]


class Level:
    def __init__(self, parent=None, fp=None, size=64, level=None):
        self.parent = parent
        self.fp = fp
        self.size = size
        self.level = level
        if fp is not None and level is None:    # We have a file path, but aren't provided a level, we need to load one
            self.level = self.load()
        elif fp is not None:                    # We have a file path and a level, we save our level
            self.save()
        else:                                   # We don't have a file path or a level, we load the default level
            self.fp = 'assets/level.txt'
            self.level = self.load()
        self.draw()

    def save(self):
        with open(self.fp, 'w') as file:
            json.dump(self.level, file)

    def load(self):
        with open(self.fp, 'r') as file:
            return json.load(file)

    def draw(self):
        for i, row in enumerate(self.level['base']):
            for j, tile in enumerate(row):
                if isinstance(tile, list):
                    #print(64*j, 64*i, tile[0], tile[1], tile[2], tile[3], tile[4])
                    pix = self.parent.m_scene.addPixmap(QPixmap(tile[0]).copy(tile[1], tile[2], tile[3], tile[4]))
                    pix.setPos(64*j, 64*i)
                    pix.setZValue(0)
        for i, row in enumerate(self.level['foliage']):
            for j, tile in enumerate(row):
                if isinstance(tile, list):
                    #print(64*j, 64*i, tile[0], tile[1], tile[2], tile[3], tile[4])
                    pix = self.parent.m_scene.addPixmap(QPixmap(tile[0]).copy(tile[1], tile[2], tile[3], tile[4]))
                    pix.setPos(64*j, 64*i)
                    pix.setZValue(1)
        for i, row in enumerate(self.level['object']):
            for j, tile in enumerate(row):
                if isinstance(tile, list):
                    for obj in tile:
                        #print(64*j, 64*i, obj[0], obj[1], obj[2], obj[3], obj[4])
                        pix = self.parent.m_scene.addPixmap(QPixmap(obj[0]).copy(obj[1], obj[2], obj[3], obj[4]))
                        pix.setPos(64*j, 64*i)
                        pix.setZValue(2)


class Demo(QGraphicsView):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.m_scene = QGraphicsScene()
        self.m_lightSource = None
        self.m_items = []
        self.m_sprites = []

        self.setScene(self.m_scene)
        self.setup_scene()
        self.view_center = [WINDOW_WIDTH/2/WINDOW_WIDTH*4096, WINDOW_HEIGHT/2/WINDOW_HEIGHT*4096]
        self.centerOn(self.view_center[0], self.view_center[1])
        #print(self.view_center)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(30)
        self.timer.start()

        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

        self.mouse_down = False
        self.setMouseTracking(True)

        self.key_pressed = False
        self.shift = False

        ran_foliage = lambda x: 0 if x < .75 else ['assets/tree.png', 0, 0, 64, 64]
        ran_obj = lambda x: 0 if x < .9 else [['assets/ore.png', 0, 0, 64, 64]]
        level = {'base': [[['assets/grass.png', 0, 0, 64, 64] for i in range(64)] for j in range(64)],
                 'foliage': [[ran_foliage(random.uniform(0, 1)) for i in range(64)] for j in range(64)],
                 'object': [[ran_obj(random.uniform(0, 1)) for i in range(64)] for j in range(64)],
                 'tilted': [[0 for i in range(16)] for j in range(16)],
                 'walkable': [[True for i in range(16)] for j in range(16)]}
        self.level = Level(self, fp='assets/level_test.txt', level=level)

    def setup_scene(self):
        self.m_scene.setSceneRect(0, 0, 4096, 4096)

        linear_grad = QLinearGradient(QPointF(-100, -100), QPointF(100, 100))
        linear_grad.setColorAt(0, QColor(255, 255, 255))
        linear_grad.setColorAt(1, QColor(192, 192, 255))
        self.setBackgroundBrush(linear_grad)

    def animate(self):
        self.centerOn(self.view_center[0], self.view_center[1])
        self.m_scene.update()

    def keyPressEvent(self, event):
        key = event.key()
        self.key_pressed = True
        if key == Qt.Key_Shift:
            self.shift = True
        if key == Qt.Key_Up or key == Qt.Key_W:
            #print('Pressed Up or W?')
            if self.shift:
                self.view_center = [self.view_center[0], self.view_center[1] - 50]
            else:
                self.view_center = [self.view_center[0], self.view_center[1] - 10]
        if key == Qt.Key_Down or key == Qt.Key_S:
            #print('Pressed Down or S?')
            if self.shift:
                self.view_center = [self.view_center[0], self.view_center[1] + 50]
            else:
                self.view_center = [self.view_center[0], self.view_center[1] + 10]
        if key == Qt.Key_Left or key == Qt.Key_A:
            #print('Pressed Left or A?')
            if self.shift:
                self.view_center = [self.view_center[0] - 50, self.view_center[1]]
            else:
                self.view_center = [self.view_center[0] - 10, self.view_center[1]]
        if key == Qt.Key_Right or key == Qt.Key_D:
            #print('Pressed Right or D?')
            if self.shift:
                self.view_center = [self.view_center[0] + 50, self.view_center[1]]
            else:
                self.view_center = [self.view_center[0] + 10, self.view_center[1]]
        if key == Qt.Key_Space:
            print('view_x: %d, view_y: %d' % (self.view_center[0], self.view_center[1]))
        if key == Qt.Key_Escape:
            exit()
        #super(Demo, self).keyPressEvent(event)

    def mousePressEvent(self, event):
        mouse_x = int(event.pos().x()/WINDOW_WIDTH*4096)
        mouse_y = int(event.pos().y()/WINDOW_HEIGHT*4096)
        #print(event.pos().x(), mouse_x)
        #print(event.pos().y(), mouse_y)
        self.view_center = [mouse_x, mouse_y]
        self.mouse_down = True
        super(Demo, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mouse_down:
            mouse_x = int(event.pos().x()/WINDOW_WIDTH*4096)
            mouse_y = int(event.pos().y()/WINDOW_HEIGHT*4096)
            # print(event.pos().x(), mouse_x)
            # print(event.pos().y(), mouse_y)
            self.view_center = [mouse_x, mouse_y]
        super(Demo, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        super(Demo, self).mouseReleaseEvent(event)

    def keyReleaseEvent(self, event):
        key = event.key()
        self.key_pressed = False
        if key == Qt.Key_Shift:
            self.shift = False

def main():
    import sys

    app = QApplication(sys.argv)

    demo = Demo()
    demo.setWindowTitle("Demo Map Explorer")
    demo.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    demo.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
