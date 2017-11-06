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

def pointInLine(qPointF, qLineF):
    from sympy import Point, Line, Segment, Rational
    p1 = Point(qPointF.x(), qPointF.y())
    l = Line(Point(qLineF.x1(), qLineF.y1()), Point(qLineF.x2(), qLineF.y2()))
    point2d = l.projection(p1)
    return QPointF(point2d[0], point2d[1])

#@ return Boolean
def pointInSegment(qPointF, qLineF):
    length = qLineF.length()
    newLength = QLineF(qLineF.p1() , qPointF).length() + QLineF(qLineF.p2() , qPointF).length()
    dist = newLength - length
    res = False
    if  dist > sys.float_info.epsilon:
        res = False
    else:
        res = True
    return res

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
            x = self.lineIntersectTest(self.line1, self.line2)
            self.crossPoint = QPointF(x[0], x[1])
        super(LineWidget, self).mouseMoveEvent(e)


    def lineIntersectTest(self, qLineF1, qLineF2):
        a1 = (qLineF1.y1() - qLineF1.y2())/(qLineF1.x1() - qLineF1.x2())
        b1 = qLineF1.y1() - a1 * qLineF1.x1()
        a2 = (qLineF2.y1() - qLineF2.y2()) / (qLineF2.x1() - qLineF2.x2())
        b2 = qLineF2.y1() - a2 * qLineF2.x1()
        a = np.array([[a1, -1 ], [a2, -1]])
        b = np.array([-b1, -b2])
        x = np.linalg.solve(a, b)
        return x

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
        pen.setColor(QColor.fromRgb(0, 0, 255))
        qPainter.setPen(pen)
        qPainter.drawLine(self.line2)
        projectedPointWorld = pointInLine(self.screenToWorld(self.lastPos), self.line1)
        qPainter.drawPoint(self.worldToScreen(projectedPointWorld))
        if None != self.crossPoint:
            pen.setColor(QColor.fromRgb(0, 255, 0))
            qPainter.setPen(pen)
            qPainter.drawPoint(self.worldToScreen(self.crossPoint))
            self.intersected = pointInSegment(self.crossPoint, self.line1)
            if self.intersected:
                self.showInfo(qPainter, "intersected ")

def main():    
    app = QtGui.QApplication(sys.argv)
    ex = LineWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
