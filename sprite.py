#!/usr/bin/env python3

"""Note to self Sprite(object) and Sprite() are the same in python 3"""

import math

from PyQt5.QtCore import QRect, QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QLabel, QGraphicsItem, QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem)


class Sprite():
    def __init__(self, x=0, y=0, sheet=None, parent=None, width=None, height=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.width = width
        self.height = height
        self.sheet = QPixmap(sheet)
        self.pix = None
        self.states = {'static':
                           {'pix'   : [],
                            'delay' : 1000}}
        self.state = 'static'
        self.step = 0

        self.delay = 50
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(self.delay)
        self.timer.start()

    def set_sheet(self, sheet):
        self.sheet = QPixmap(sheet)

    def set_static(self, x=0, y=0, x_shift=None, y_shift=None, x_offset=0, y_offset=0,
                   z=1, scale=1):
        if x_offset is None or y_offset is None:
            self.states['static']['pix'].append(self.sheet)
        else:
            self.states['static']['pix'].append(self.sheet.copy(x, y, x_shift, y_shift))
        self.pix = self.parent.m_scene.addPixmap(self.states['static']['pix'][0])
        self.pix.setPos(self.x, self.y)
        self.pix.setOffset(x_offset, y_offset)
        self.pix.setZValue(z)
        self.pix.setScale(scale)

    def move_sprite(self, velX, velY):
        self.x += velX
        self.y += velY
        self.pix.setPos(self.x, self.y)

    def set_state(self, state):
        self.state = state
        self.timer.setInterval(self.states[state]['delay'])
        self.step = 0
        self.pix.setPixmap(self.states[state]['pix'][self.step])

    def add_state(self, name, maps=[], delay=50):
        self.states[name] = {}
        self.states[name]['pix'] = maps
        self.states[name]['delay'] = delay

    def animate(self):
        self.step += 1
        if self.step >= len(self.states[self.state]['pix']):
            self.step = 0
        #print('step:', self.step)
        self.pix.setPixmap(self.states[self.state]['pix'][self.step])


class Link(Sprite):
    def __init__(self, x=0, y=0, parent=None, width=None, height=None):
        super().__init__(x=0, y=0, sheet='linkEdit.png', parent=parent, width=width, height=height)


class Demo(QGraphicsView):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QGraphicsScene()
        self.m_lightSource = None
        self.m_items = []
        self.m_sprites = []

        self.setScene(self.m_scene)

        self.setup_scene()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(30)
        self.timer.start()

        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

    def setup_scene(self):
        self.m_scene.setSceneRect(-300, -200, 600, 460)

        linear_grad = QLinearGradient(QPointF(-100, -100), QPointF(100, 100))
        linear_grad.setColorAt(0, QColor(255, 255, 255))
        linear_grad.setColorAt(1, QColor(192, 192, 255))
        self.setBackgroundBrush(linear_grad)

        link = Link(x=0, y=0, parent=self)
        self.m_sprites.append(Sprite(0, 0, sheet='linkEdit.png', parent=self))
        self.m_sprites[0].set_static(0, 0, 120, 130, -60, -65)

        # Add state blink
        pix = []
        for i in range(15):
            pix.append(self.m_sprites[0].sheet.copy(0, 0, 120, 130))
        for i in range(1, 3):
            pix.append(self.m_sprites[0].sheet.copy(120*i, 130*0, 120, 130))
        self.m_sprites[0].add_state('blink', pix, 80)

        # Add state down
        pix = []
        for i in range(10):
            pix.append(self.m_sprites[0].sheet.copy(120*i, 130*4, 120, 130))
        self.m_sprites[0].add_state('down', pix, 80)

        # Add state left
        pix = []
        for i in range(10):
            pix.append(self.m_sprites[0].sheet.copy(120*i, 130*5, 120, 130))
        self.m_sprites[0].add_state('left', pix, 80)

        # Add state up
        pix = []
        for i in range(10):
            pix.append(self.m_sprites[0].sheet.copy(120*i, 130*6, 120, 130))
        self.m_sprites[0].add_state('up', pix, 80)

        # Add state right
        pix = []
        for i in range(10):
            pix.append(self.m_sprites[0].sheet.copy(120*i, 130*7, 120, 130))
        self.m_sprites[0].add_state('right', pix, 80)

    def animate(self):
        #for sprite in self.m_sprites:
        #    sprite.update()
        self.m_scene.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            print('Pressed Up or W?')
            self.m_sprites[0].set_state('up')
        if key == Qt.Key_Down or key == Qt.Key_S:
            print('Pressed Down or S?')
            self.m_sprites[0].set_state('down')
        if key == Qt.Key_Left or key == Qt.Key_A:
            print('Pressed Left or A?')
            self.m_sprites[0].set_state('left')
        if key == Qt.Key_Right or key == Qt.Key_D:
            print('Pressed Right or D?')
            self.m_sprites[0].set_state('right')
        if key == Qt.Key_Space:
            print('Pressed Space?')
            if self.m_sprites[0].state == 'static':
                self.m_sprites[0].set_state('blink')
            else:
                self.m_sprites[0].set_state('static')
        if key == Qt.Key_Escape:
            exit()
        super(Demo, self).keyPressEvent(event)


def main():
    import sys

    app = QApplication(sys.argv)

    demo = Demo()
    demo.setWindowTitle("Demo Sprite")
    demo.resize(640, 480)
    demo.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
