#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, random
sys.path.append('../')
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QWidget
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt5.QtGui import QColor, QTransform, QPolygonF
from  coordWidget import CoordWidget
import numpy as np
from tools import pointInLine, pointInSegment, lineIntersectTest

class LineWidget(CoordWidget):
    
    def __init__(self):
        super(LineWidget, self).__init__()
        self.line1 = QLineF(QPointF(-0.4, -0.2), QPointF(-0.1, 0.3))
        self.line2 = QLineF(QPointF(0.2, 0.1), QPointF(0.4, -0.3))
        self.lastPos = QtCore.QPoint()

        self.intersected = False
        self.crossPoint = None

    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.LeftButton:
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)  # QPointF
            self.line2.translate(translation)
            p = lineIntersectTest(self.line1, self.line2)
            if None != p:
                self.crossPoint = p
            else :
                self.crossPoint = None
                self.intersected = False
        super(LineWidget, self).mouseMoveEvent(e)

    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor( QColor.fromRgb(255, 0, 0) )
        qPainter.setPen(pen)
        qPainter.drawLine(self.line1)
        qPainter.drawLine(self.line2)

    def drawInScreen(self, qPainter):
        self.msgCnt = 0
        self.showInfo(qPainter, "Blue point: the intersection point")
        self.showInfo(qPainter, "Green point: the projected point of the the mouse")
        pen = qPainter.pen()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 255, 0))
        qPainter.setPen(pen)
        qPainter.drawLine(self.line2)
        projectedPointWorld = pointInLine(self.screenToWorld(self.lastPos), self.line1)
        qPainter.drawPoint(self.worldToScreen(projectedPointWorld))
        if None != self.crossPoint:
            pen.setColor(QColor.fromRgb(0, 0, 255))
            qPainter.setPen(pen)
            qPainter.drawPoint(self.worldToScreen(self.crossPoint))
            self.intersected = pointInSegment(self.crossPoint, self.line1)
            if self.intersected:
                self.showInfo(qPainter, "intersected ")

def main():    
    app = QtWidgets.QApplication(sys.argv)
    ex = LineWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
