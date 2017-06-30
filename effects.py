#!/usr/bin/env python3

import math

from PyQt5.QtCore import QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView)


class ObjProto(QGraphicsEllipseItem):
    def __init__(self, posX=0, posY=0, radX=50, radY=50):
        super().__init__(posX, posY, radX, radY)
        self.posX = 0
        self.posY = 0

    def move(self, velX, velY):
        self.posX += velX
        self.posY += velY


class Lighting(QGraphicsView):
    def __init__(self, parent=None):
        super(Lighting, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QGraphicsScene()
        self.m_lightSource = None
        self.m_items = []

        self.setScene(self.m_scene)

        self.setupScene()

        timer = QTimer(self)
        timer.timeout.connect(self.animate)
        timer.setInterval(30)
        timer.start()

        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

    def setupScene(self):
        self.m_scene.setSceneRect(-300, -200, 600, 460)

        linearGrad = QLinearGradient(QPointF(-100, -100), QPointF(100, 100))
        linearGrad.setColorAt(0, QColor(255, 255, 255))
        linearGrad.setColorAt(1, QColor(192, 192, 255))
        self.setBackgroundBrush(linearGrad)

        radialGrad = QRadialGradient(30, 30, 30)
        radialGrad.setColorAt(0, Qt.yellow)
        radialGrad.setColorAt(0.2, Qt.yellow)
        radialGrad.setColorAt(1, Qt.transparent)

        pixmap = QPixmap(60, 60)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radialGrad)
        painter.drawEllipse(0, 0, 60, 60)
        painter.end()

        self.m_lightSource = self.m_scene.addPixmap(pixmap)
        self.m_lightSource.setZValue(2)


        for i in range(-2, 3):
            for j in range(-2, 3):
                if (i + j) & 1:
                    item = QGraphicsEllipseItem(0, 0, 50, 50)
                else:
                    item = QGraphicsRectItem(0, 0, 50, 50)

                item.setPen(QPen(Qt.black, 1))
                item.setBrush(QBrush(Qt.white))

                effect = QGraphicsDropShadowEffect(self)
                effect.setBlurRadius(8)
                item.setGraphicsEffect(effect)
                item.setZValue(1)
                item.setPos(i * 80, j * 80)
                #self.m_scene.addItem(item)
                #self.m_items.append(item)

        proto = ObjProto(0, 0, 50, 50)
        proto.setPen(QPen(Qt.white, 1))
        proto.setBrush(QBrush(Qt.black))
        proto.setPos(80, 80)
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(8)
        proto.setGraphicsEffect(effect)
        proto.setZValue(1)

        self.m_items.append(proto)
        self.m_scene.addItem(proto)

    def animate(self):
        self.angle += (math.pi / 30)
        xs = 200 * math.sin(self.angle) - 40 + 25
        ys = 200 * math.cos(self.angle) - 40 + 25
        self.m_lightSource.setPos(xs, ys)

        for item in self.m_items:
            effect = item.graphicsEffect()

            delta = QPointF(item.x() - xs, item.y() - ys)
            effect.setOffset(QPointF(delta.toPoint() / 30))

            dd = math.hypot(delta.x(), delta.y())
            color = effect.color()
            color.setAlphaF(max(0.4, min(1 - dd / 200.0, 0.7)))
            effect.setColor(color)
            item.setPos(item.posX, item.posY)

        self.m_scene.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            print('Pressed Up or W?')
            for item in self.m_items:
                item.move(0, -10)
            #self.player.move(0, -10)
        if key == Qt.Key_Down or key == Qt.Key_S:
            print('Pressed Down or S?')
            for item in self.m_items:
                item.move(0, 10)
            #self.player.move(0, 10)
        if key == Qt.Key_Left or key == Qt.Key_A:
            print('Pressed Left or A?')
            for item in self.m_items:
                item.move(-10, 0)
            #self.player.move(-10, 0)
        if key == Qt.Key_Right or key == Qt.Key_D:
            print('Pressed Right or D?')
            for item in self.m_items:
                item.move(10, 0)
            #self.player.move(10, 0)
        if key == Qt.Key_Escape:
            exit()
        super(Lighting, self).keyPressEvent(event)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    lighting = Lighting()
    lighting.setWindowTitle("Lighting and Shadows")
    lighting.resize(640, 480)
    lighting.show()

    sys.exit(app.exec_())
