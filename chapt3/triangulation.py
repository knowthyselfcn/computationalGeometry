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
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import numpy as np

class Triangluation(CoordWidget):
    def __init__(self):
        super(Triangluation, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Triangluation ')
        self.vertexs = []   #world  pos
        self.points = []    # screen pos
        self.polygon = None


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
        if e.buttons() & Qt.LeftButton :
            vertex = self.screenToWorld( e.pos())  # QPointF
            self.vertexs.append(vertex)
            self.points.append(e.pos())
            self.take_screenshot()
            self.makeConvexHull(self.vertexs)
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

    def makeConvexHull(self, vertexs):
        if len(vertexs) < 3:
            return
        self.vertexs.sort(key=lambda x: x.x())
        upper = [self.vertexs[0], self.vertexs[1]]
        for v in self.vertexs[2:len(self.vertexs)]:
            upper.append(v)
            while len(upper) > 2 and self.isRightTurn(upper[-3], upper[-2], upper[-1]):
                del upper[-2]
        lower = [self.vertexs[-1], self.vertexs[-2]]
        for v in reversed( self.vertexs[0:-3]):
            lower.append(v)
            while len(lower) > 2 and self.isRightTurn(lower[-3], lower[-2], lower[-1]):
                del lower[-2]
        del lower[0]
        upper.extend(lower)
        self.polygon = QPolygonF()
        for v in upper:
            self.polygon.append(v)

    def triangulate(self):
        vertice = []
        for v in self.vertexs:
            vertice.append([v.x(), v.y()])

        points = np.array(vertice)
        print points
        self.tri = Delaunay(points)
        plt.triplot(points[:, 0], points[:, 1], self.tri.simplices.copy())
        plt.plot(points[:, 0], points[:, 1], 'o')
        plt.show()

    def keyPressEvent(self, keyEvent):
        e = keyEvent
        if e.key() == Qt.Key_C:
            self.makeConvexHull(self.vertexs)
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
