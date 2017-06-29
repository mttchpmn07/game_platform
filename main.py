import sys

from time import sleep
from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPen)
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsItem, QGraphicsView, QGraphicsScene
from PyQt5.uic import loadUi


class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi('main_window.ui')
        self.setWindowTitle("Graphics Test")
        self.view = graphics_view()
        self.setCentralWidget(self.view)
        self.view.init_scene()


class graphics_view(QGraphicsView):
    def __init__(self):
        super(graphics_view, self).__init__()
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.world = world()
        self.player = player()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            #print('Pressed Up or W?')
            self.player.move(0, -10)
        if key == Qt.Key_Down or key == Qt.Key_S:
            #print('Pressed Down or S?')
            self.player.move(0, 10)
        if key == Qt.Key_Left or key == Qt.Key_A:
            #print('Pressed Left or A?')
            self.player.move(-10, 0)
        if key == Qt.Key_Right or key == Qt.Key_D:
            #print('Pressed Right or D?')
            self.player.move(10, 0)
        if key == Qt.Key_Escape:
            exit()
        self.update_scene()
        super(graphics_view, self).keyPressEvent(event)

    def init_scene(self):
        self.scene = QGraphicsScene(0, 0, 800, 600, self)
        self.scene.addItem(self.world)
        self.scene.addItem(self.player)
        self.setScene(self.scene)

    def update_scene(self):
        self.scene.update()


class position(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'


class world(QGraphicsItem):
    def __init__(self):
        super(world, self).__init__()
        self.boundingRect()

    def boundingRect(self):
        return QRectF(0, 0, 800, 600)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.black)


class player(QGraphicsItem):
    def __init__(self):
        super(player, self).__init__()
        self.boundingRect()
        self.pos = position(x=400, y=300)

    def boundingRect(self):
        return QRectF(0, 0, 30, 30)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.blue)
        painter.drawEllipse(QRectF(self.pos.x, self.pos.y, 30, 30))

    def move(self, velX, velY):
        self.pos.x += velX
        self.pos.y += velY


def main():
    app = QApplication(sys.argv)
    win = main_window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
