#! /usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division

import sys, random
sys.path.append('../')
from  coordWidget import CoordWidget
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform, QPolygonF
import numpy as np


class PolyTest(CoordWidget):
    def __init__(self):
        super(PolyTest, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Polygon Intersectin Test')
        self.qPolygon1 = QPolygonF([QPointF(0.1, 0), QPointF(0.3, 0.1), QPointF(0.5, 0.3), QPointF(0.37, 0.5), QPointF(0.05, 0.1) ])
        self.qPolygon2 = QPolygonF([QPointF(-0.05, 0.1),  QPointF(-0.37, 0.5), QPointF(-0.5, 0.3),  QPointF(-0.3, 0.1), QPointF(-0.1, 0)])
        self.qPolygon3 = QPolygonF()

    # override super，多边形无需填充
    def preDraw(self, qPainter):
        qPainter.save()
        qPainter.setWorldTransform(self.getWorldToScreenTransform())
        pen = qPainter.pen()
        pen.setCosmetic(True)
        qPainter.setPen(pen)
        brush = QtGui.QBrush()
        brush.setColor(QColor.fromRgb(255, 0, 0))
        # brush.setStyle(Qt.SolidLine)       #
        qPainter.setBrush(brush)

    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.RightButton :
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)
            self.scene_translation_ = self.scene_translation_ + translation
        elif e.buttons() & Qt.LeftButton:
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos) #QPointF
            self.qPolygon1.translate(translation)
        self.lastPos = e.pos()
        self.update()

    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(255, 0, 0))
        qPainter.setPen(pen)
        qPainter.drawConvexPolygon(self.qPolygon1)

        pen.setColor(QColor.fromRgb(0, 0, 255))
        qPainter.setPen(pen)
        qPainter.drawConvexPolygon(self.qPolygon2)

        self.qPolygon3 = self.qPolygon1.intersected(self.qPolygon2)

        brush = qPainter.brush()
        brush.setColor(QColor.fromRgb(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        qPainter.setBrush(brush)
        qPainter.drawConvexPolygon(self.qPolygon3)

        old_transform = qPainter.worldTransform()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.resetTransform()
        crossPoint = self.worldToScreen(QPointF(0.2, 0.4))

        qPainter.setWorldTransform(old_transform)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = PolyTest()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
