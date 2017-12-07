#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
pip install cython
pip install triangle-20170429-cp27-cp27m-win_amd64.whl   https://www.lfd.uci.edu/~gohlke/pythonlibs/#triangle
"""


from __future__ import division

import sys, random
sys.path.append('../')
from  coordWidget import CoordWidget
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform, QPolygonF
import matplotlib.pyplot as plt
import numpy as np

import triangle
import triangle.plot

class Triangluation(CoordWidget):
    def __init__(self):
        super(Triangluation, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Triangluation ')
        self.vertexs = []   #world  pos
        self.points = []    # screen pos
        self.polygon = QPolygonF()

        self.holeVertexs = []   #world  pos
        self.holePoints = []    # screen pos
        self.holePolygon = QPolygonF()

    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.RightButton :
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)
            self.scene_translation_ = self.scene_translation_ + translation
        elif e.buttons() & Qt.LeftButton:
            pass
        self.lastPos = e.pos()
        self.update()

    def mousePressEvent(self, qMousePressEvent):
        e = qMousePressEvent
        modifiers = QtGui.QApplication.keyboardModifiers()
        if e.buttons() & Qt.LeftButton:
            vertex = self.screenToWorld(e.pos())  # QPointF
            self.take_screenshot()
            if modifiers == QtCore.Qt.ControlModifier:
                self.holePoints.append(e.pos())
                self.holeVertexs.append(vertex)
                self.makeConvexHull(self.holeVertexs, self.holePolygon)
                if self.holePolygon.size() > 4:
                    self.holeVertexs = []
                    for i in xrange(self.holePolygon.size()):
                        self.holeVertexs.append( self.holePolygon.at(i))
            else:   # record a hole
                self.points.append(e.pos())
                self.vertexs.append(vertex)
                self.makeConvexHull(self.vertexs, self.polygon)
                if self.polygon.size() > 4:
                    self.vertexs = []
                    for i in xrange(self.polygon.size()):
                        self.vertexs.append( self.polygon.at(i))
        self.lastPos = e.pos()
        self.update()

    def isRightTurn(self, p0, p1, p2):
        v1x = p1.x() - p0.x()
        v1y = p1.y() - p0.y()
        v2x = p2.x() - p1.x()
        v2y = p2.y() - p1.y()
        if v1x * v2y - v1y * v2x > 0.0:
            return False
        else:
            return True

    def makeConvexHull(self, vertexs, polygon):
        vertexs.sort(key=lambda x: x.x())
        if len(vertexs) < 3:
            return
        upper = [vertexs[0], vertexs[1]]
        for v in vertexs[2:len(vertexs)]:
            upper.append(v)
            while len(upper) > 2 and self.isRightTurn(upper[-3], upper[-2], upper[-1]):
                del upper[-2]
        lower = [vertexs[-1], self.vertexs[-2]]
        for v in reversed(vertexs[0:-3]):
            lower.append(v)
            while len(lower) > 2 and self.isRightTurn(lower[-3], lower[-2], lower[-1]):
                del lower[-2]
        del lower[0]
        upper.extend(lower)
        polygon.clear()
        for v in upper:
            polygon.append(v)

    # http://www.cs.cmu.edu/~quake/triangle.html
    def triangulate(self):
        vertice = []
        for v in self.vertexs:
            vertice.append([v.x(), v.y()])
        points = np.array(vertice)
        holeVertice = []
        for v in self.holeVertexs:
            holeVertice.append([v.x(), v.y()])
        holePoints = np.array(holeVertice)
        A = dict(vertices=points, holes1=holePoints)
        B = triangle.triangulate(A, 'pqa') #
        triangle.plot.compare(plt, A, B)
        plt.show()

    def keyPressEvent(self, keyEvent):
        e = keyEvent
        if e.key() == Qt.Key_C:
            self.makeConvexHull(self.vertexs, self.polygon)
            self.makeConvexHull(self.holeVertexs, self.holePolygon)
        elif e.key() == Qt.Key_S:
            self.saveGIF()
        elif e.key() == Qt.Key_T:
            self.triangulate()
        super(Triangluation, self).keyPressEvent(keyEvent)

    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(255, 0, 0))
        qPainter.setPen(pen)

        # draw convex hull
        if None != self.polygon:
            qPainter.drawPolyline(self.polygon)

        pen.setColor(QColor.fromRgb(0, 255, 0))
        qPainter.setPen(pen)
        if None != self.holePolygon:
            qPainter.drawPolyline(self.holePolygon)

        pen.setColor(QColor.fromRgb(0, 0, 255))
        qPainter.setPen(pen)

    def drawInScreen(self, qPainter):
        pen = qPainter.pen()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.resetTransform()
        # draw selected points in screen
        for v in self.points:
            qPainter.drawPoint(v)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Triangluation()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
