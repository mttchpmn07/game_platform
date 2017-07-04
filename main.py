#!/usr/bin/env python3

"""Note to self Sprite(object) and Sprite() are the same in python 3"""

import math

from PyQt5.QtCore import QRect, QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QLabel, QGraphicsItem, QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem)
from sprite import Link
from level import Level

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Player:
    def __init__(self, parent=None, x=400, y=300, sprite=None):
        self.parent = parent
        self.x = x
        self.y = y
        self.sprite = sprite
        if sprite is not None:
            self.sprite.move_sprite(self.x, self.y)

    def set_state(self, state):
        self.sprite.set_state(state)

    def state(self):
        return self.sprite.state

class Demo(QGraphicsView):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)
        #   Setup scene
        self.m_scene = QGraphicsScene()
        self.setScene(self.m_scene)
        self.setup_scene()
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        #   Set up entities (not attached to this term, but basically things like light sources, level, npcs)
        self.m_lightSource = None
        self.level = Level(self, fp='assets/level_test.txt')
        self.player = Player(self, WINDOW_WIDTH/2, WINDOW_HEIGHT/2, Link(parent=self))

        #   Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(30)
        self.timer.start()

        #   Render settings
        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

        #   Input management
        self.mouse_down = False
        self.setMouseTracking(True)
        self.key_pressed = False

    def setup_scene(self):
        self.m_scene.setSceneRect(0, 0, 4096, 4096)

        linear_grad = QLinearGradient(QPointF(-100, -100), QPointF(100, 100))
        linear_grad.setColorAt(0, QColor(255, 255, 255))
        linear_grad.setColorAt(1, QColor(192, 192, 255))
        self.setBackgroundBrush(linear_grad)

    def animate(self):
        self.m_scene.update()

    def get_angle(self, event):
        sprite_x = self.player.x
        sprite_y = self.player.y
        mouse_x = event.pos().x()
        mouse_y = event.pos().y()
        diff_x = mouse_x - sprite_x
        diff_y = mouse_y - sprite_y
        angle = math.atan2(diff_x, diff_y) * 180 / math.pi
        #print("sprite: <%d, %d>, mouse:<%d, %d>, angle:%f" % (sprite_x, sprite_y, mouse_x, mouse_y, angle))
        return angle

    def keyPressEvent(self, event):
        key = event.key()
        if event.isAutoRepeat() or self.mouse_down:
            return
        self.key_pressed = True
        if key == Qt.Key_Up or key == Qt.Key_W:
            #print('Pressed Up or W?')
            self.player.set_state('up')
        if key == Qt.Key_Down or key == Qt.Key_S:
            #print('Pressed Down or S?')
            self.player.set_state('down')
        if key == Qt.Key_Left or key == Qt.Key_A:
            #print('Pressed Left or A?')
            self.player.set_state('left')
        if key == Qt.Key_Right or key == Qt.Key_D:
            #print('Pressed Right or D?')
            self.player.set_state('right')
        if key == Qt.Key_Space:
            #print('Pressed Space?')
            if self.player.state() == 'static':
                self.player.set_state('blink')
            else:
                self.player.set_state('static')
        if key == Qt.Key_Escape:
            exit()
        super(Demo, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat() or self.mouse_down:
            return
        key = event.key()
        #print('Keyboard released?')
        if self.player.state() == 'left' and (key == Qt.Key_Left or key == Qt.Key_A):
            self.key_pressed = False
            self.player.set_state('left_static')
        if self.player.state() == 'right' and (key == Qt.Key_Right or key == Qt.Key_D):
            self.key_pressed = False
            self.player.set_state('right_static')
        if self.player.state() == 'down' and (key == Qt.Key_Down or key == Qt.Key_S):
            self.key_pressed = False
            self.player.set_state('static')
        if self.player.state() == 'up' and (key == Qt.Key_Up or key == Qt.Key_W):
            self.key_pressed = False
            self.player.set_state('up_static')

    def mousePressEvent(self, event):
        print('Pressed mouse? : <%d, %d>' % (event.pos().x(), event.pos().y()))
        print('Player Pos : <%d, %d>' % (self.player.x, self.player.y))
        self.mouse_down = True
        angle = self.get_angle(event)
        if -60 > angle > -120 and self.player.state() != 'left':
            self.player.set_state('left')
        if 60 < angle < 120 and self.player.state() != 'right':
            self.player.set_state('right')
        if -60 <= angle <= 60 and self.player.state() != 'down':
            self.player.set_state('down')
        if (angle <= -120 or angle >= 120) and self.player.state() != 'up':
            self.player.set_state('up')

    def mouseMoveEvent(self, event):
        if self.key_pressed:
            return
        angle = self.get_angle(event)
        if self.mouse_down:
            if -60 > angle > -120 and self.player.state() != 'left':
                self.player.set_state('left')
            if 60 < angle < 120 and self.player.state() != 'right':
                self.player.set_state('right')
            if -60 <= angle <= 60 and self.player.state() != 'down':
                self.player.set_state('down')
            if (angle <= -120 or angle >= 120) and self.player.state() != 'up':
                self.player.set_state('up')
        else:
            if -60 > angle > -120 and self.player.state() != 'left_static':
                self.player.set_state('left_static')
            if 60 < angle < 120 and self.player.state != 'right_static':
                self.player.set_state('right_static')
            if -60 <= angle <= 60 and self.player.state() != 'static':
                self.player.set_state('static')
            if (angle <= -120 or angle >= 120) and self.player.state() != 'up_static':
                self.player.set_state('up_static')

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        if self.player.state() == 'left':
            self.player.set_state('left_static')
        if self.player.state() == 'right':
            self.player.set_state('right_static')
        if self.player.state() == 'down':
            self.player.set_state('static')
        if self.player.state() == 'up':
            self.player.set_state('up_static')


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
