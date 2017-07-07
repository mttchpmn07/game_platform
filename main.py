#!/usr/bin/env python3

"""Note to self Sprite(object) and Sprite() are the same in python 3"""

from PyQt5.QtCore import QRect, QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QLabel, QGraphicsItem, QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem)
from sprite import Link
from level import Level
from position import Position

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class Player:
    def __init__(self, parent=None, x=400, y=300, sprite=None,
                 level_max_x=4096-WINDOW_WIDTH, level_max_y=4096-WINDOW_HEIGHT,
                 level_min_x=WINDOW_WIDTH/2, level_min_y=WINDOW_HEIGHT/2):
        self.parent = parent
        self.pos = Position(pos=[x, y])
        self.vel = Position(pos=[0, 0])
        self.speed = 1
        self.sprite = sprite
        self.max_pos = Position(level_max_x, level_max_y)
        self.min_pos = Position(level_min_x, level_min_y)
        self.stamina = 100
        self.stamina_fade = 0
        if sprite is not None:
            self.sprite.move_sprite(self.pos)

        self.delay = 8
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate)
        self.timer.setInterval(self.delay)
        self.timer.start()

    def set_state(self, state):
        self.sprite.set_state(state)

    def state(self):
        return self.sprite.state

    def mov(self):
        print('Stamina : %f' % self.stamina)
        self.stamina += self.stamina_fade
        if self.stamina > 100:
            self.stamina = 100
        if self.stamina < 0:
            self.stamina = 0
            self.speed = 1
        self.pos = self.pos + self.vel
        if self.pos.x() < self.min_pos.x():
            self.pos.x(self.min_pos.x() + self.speed)
        if self.pos.y() < self.min_pos.y():
            self.pos.y(self.min_pos.y() + self.speed)
        if self.pos.x() > self.max_pos.x():
            self.pos.x(self.max_pos.x() - self.speed)
        if self.pos.y() > self.max_pos.y():
            self.pos.y(self.max_pos.y() - self.speed)

    def simulate(self):
        self.sprite.move_sprite(self.pos)
        self.mov()


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
        self.player = Player(self, 2048, 2048, Link(parent=self))

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
        self.centerOn(self.player.pos.x(), self.player.pos.y())
        self.m_scene.update()

    def get_angle(self, event):
        mouse_pos = Position(x=event.pos().x(), y=event.pos().y())
        mouse_pos = mouse_pos + self.player.pos - Position(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        # print('Player : %s' % self.player.pos)
        # print('Mouse : %s' % mouse_pos)
        # print('Angle : %f' % (self.player.pos < mouse_pos))
        return self.player.pos < mouse_pos

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Shift:
            self.player.speed = 5
            self.player.stamina_fade = -.1
        if event.isAutoRepeat() or self.mouse_down:
            return
        self.key_pressed = True
        if key == Qt.Key_Up or key == Qt.Key_W:
            # print('Pressed Up or W?')
            self.player.set_state('up')
            self.player.vel = Position(0, -self.player.speed)
        if key == Qt.Key_Down or key == Qt.Key_S:
            # print('Pressed Down or S?')
            self.player.set_state('down')
            self.player.vel = Position(0, self.player.speed)
        if key == Qt.Key_Left or key == Qt.Key_A:
            # print('Pressed Left or A?')
            self.player.set_state('left')
            self.player.vel = Position(-self.player.speed, 0)
        if key == Qt.Key_Right or key == Qt.Key_D:
            # print('Pressed Right or D?')
            self.player.set_state('right')
            self.player.vel = Position(self.player.speed, 0)
        if key == Qt.Key_Space:
            # print('Pressed Space?')
            if self.player.state() == 'static':
                self.player.set_state('blink')
            else:
                self.player.set_state('static')
        if key == Qt.Key_Escape:
            exit()
        #super(Demo, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_Shift:
            self.player.speed = 1
            self.player.stamina_fade = .1
        if event.isAutoRepeat() or self.mouse_down:
            return
        self.player.vel = Position(0, 0)
        # print('Keyboard released?')
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
        # print('Pressed mouse? : <%d, %d>' % (event.pos().x(), event.pos().y()))
        # print('Sprite Pos : <%d, %d>' % (self.player.pos.x(), self.player.pos.y()))
        self.mouse_down = True
        angle = self.get_angle(event)
        mouse_pos = Position(event.pos().x(), event.pos().y())
        mouse_pos = mouse_pos + self.player.pos - Position(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        vel = self.player.pos.get_unit(mouse_pos, self.player.speed)
        self.player.vel = vel
        print('Player : %s, Mouse : %s, Angle : %s' % (self.player.pos, mouse_pos, round(angle, 2)))
        print('Velocity : %s' % vel)
        if 240 < angle < 300 and self.player.state() != 'left':
            self.player.set_state('left')
        elif 60 < angle < 120 and self.player.state() != 'right':
            self.player.set_state('right')
        elif 120 <= angle <= 240 and self.player.state() != 'up':
            self.player.set_state('up')
        elif (angle >= 300 or angle <= 60) and self.player.state() != 'down':
            self.player.set_state('down')

    def mouseMoveEvent(self, event):
        if self.key_pressed:
            return
        angle = self.get_angle(event)
        # print(angle)
        if self.mouse_down:
            mouse_pos = Position(event.pos().x(), event.pos().y())
            mouse_pos = mouse_pos + self.player.pos - Position(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
            vel = self.player.pos.get_unit(mouse_pos, self.player.speed)
            self.player.vel = vel
            if 240 < angle < 300 and self.player.state() != 'left':
                self.player.set_state('left')
            elif 60 < angle < 120 and self.player.state() != 'right':
                self.player.set_state('right')
            elif 120 <= angle <= 240 and self.player.state() != 'up':
                self.player.set_state('up')
            elif (angle >= 300 or angle <= 60) and self.player.state() != 'down':
                self.player.set_state('down')
        else:
            if 240 < angle < 300 and self.player.state() != 'left_static':
                self.player.set_state('left_static')
            elif 60 < angle < 120 and self.player.state() != 'right_static':
                self.player.set_state('right_static')
            elif 120 <= angle <= 240 and self.player.state() != 'up_static':
                self.player.set_state('up_static')
            elif (angle >= 300 or angle <= 60) and self.player.state() != 'static':
                self.player.set_state('static')

    def mouseReleaseEvent(self, event):
        self.mouse_down = False
        self.player.vel = Position(0, 0)
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
