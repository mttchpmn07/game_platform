#!/usr/bin/env python3

import math

from PyQt5.QtCore import QRect, QPointF, Qt, QTimer
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPen, QPainter,
                         QPixmap, QRadialGradient)
from PyQt5.QtWidgets import (QLabel, QGraphicsItem, QApplication, QFrame, QGraphicsDropShadowEffect,
                             QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem)


class ProtoObj(object):
    def __init__(self, posX=0, posY=0, radX=30, radY=30, parent=None):
        super().__init__()
        self.posX = posX
        self.posY = posY
        self.radX = radX
        self.radY = radY
        self.parent = parent
        self.ellipse = QGraphicsEllipseItem(posX, posY, radX, radY)
        self.sheet = QPixmap('linkEdit.png')
        self.stand = []
        self.step = 0
        self.state = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.setInterval(1000)
        self.animation_timer.start()

    def initObj(self):
        self.ellipse.setPos(self.posX, self.posY)
        self.ellipse.setPen(QPen(Qt.transparent, 1))
        self.ellipse.setBrush(QBrush(Qt.darkGreen))
        self.ellipse.setZValue(0)
        self.ellipse.setOpacity(1)
        effect = QGraphicsDropShadowEffect(self.parent)
        effect.setBlurRadius(15)
        effect.setColor(Qt.black)
        self.ellipse.setGraphicsEffect(effect)
        self.stand.append(self.sheet.copy(10, 15, 100, 120))
        self.stand.append(self.sheet.copy(130, 15, 100, 120))
        self.stand.append(self.sheet.copy(250, 15, 100, 120))
        self.pix = self.parent.m_scene.addPixmap(self.stand[0])
        self.pix.setPos(self.posX, self.posY)
        self.pix.setOffset(-20, -56)
        self.pix.setZValue(2)
        self.pix.setScale(1)

    def getObj(self):
        return [self.ellipse]

    def moveObj(self, velX, velY):
        self.posX += velX
        self.posY += velY
        self.pix.setPos(self.posX, self.posY)

    def animate(self):
        if self.state == 0:
            self.step += 1
            if self.step > 2:
                self.step = 0
            'standing'
            #self.pix = self.parent.m_scene.addPixmap(self.stand[self.step])
            self.pix.setPixmap(self.stand[self.step])
            self.pix.setPos(self.posX, self.posY)
            #self.pix.setOffset(-20, -70)
            self.pix.setZValue(2)



class Lighting(QGraphicsView):
    def __init__(self, parent=None):
        super(Lighting, self).__init__(parent)

        self.angle = 0.0
        self.m_scene = QGraphicsScene()
        self.m_lightSource = None
        self.m_items = []

        self.setScene(self.m_scene)

        self.setupScene()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.setInterval(30)
        self.timer.start()

        self.setRenderHint(QPainter.Antialiasing)
        self.setFrameStyle(QFrame.NoFrame)

    def setupScene(self):
        self.m_scene.setSceneRect(-300, -200, 600, 460)

        linearGrad = QLinearGradient(QPointF(-100, -100), QPointF(100, 100))
        linearGrad.setColorAt(0, Qt.darkGreen)#QColor(255, 255, 255))
        linearGrad.setColorAt(1, Qt.green)#QQColor(192, 192, 255))
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

        self.proto = ProtoObj(0, 0, 50, 50, self)
        self.proto.initObj()

        #self.m_items.append(self.proto.getObj()[0])
        self.m_scene.addItem(self.proto.getObj()[0])
        #self.m_scene.addItem(self.proto.getObj()[1])

    def animate(self):
        self.angle += (math.pi / 30)
        xs = 200 * math.sin(self.angle) - 40 + 25
        ys = 200 * math.cos(self.angle) - 40 + 25
        self.m_lightSource.setPos(xs, ys)

        item = self.proto.getObj()[0]
        effect = item.graphicsEffect()

        delta = QPointF(item.x() - xs, item.y() - ys)
        effect.setOffset(QPointF(delta.toPoint() / 30))

        dd = math.hypot(delta.x(), delta.y())
        color = effect.color()
        color.setAlphaF(max(0.4, min(1 - dd / 200.0, 0.7)))
        effect.setColor(color)
        item.setPos(self.proto.posX, self.proto.posY)
        #self.proto.animate(0)
        #self.proto.pix.setPos(self.proto.posX, self.proto.posY)
        self.m_scene.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up or key == Qt.Key_W:
            #print('Pressed Up or W?')
            self.proto.moveObj(0, -10)
            #self.player.move(0, -10)
        if key == Qt.Key_Down or key == Qt.Key_S:
            #print('Pressed Down or S?')
            self.proto.moveObj(0, 10)
            #self.player.move(0, 10)
        if key == Qt.Key_Left or key == Qt.Key_A:
            #print('Pressed Left or A?')
            self.proto.moveObj(-10, 0)
            #self.player.move(-10, 0)
        if key == Qt.Key_Right or key == Qt.Key_D:
            #print('Pressed Right or D?')
            self.proto.moveObj(10, 0)
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
