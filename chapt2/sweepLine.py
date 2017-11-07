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
from PyQt4.QtGui import QColor, QMatrix, QTransform
import numpy as np



class Test(CoordWidget):
    
    def __init__(self):
        super(Test, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Test')

        self.qLineFs = []
        self.tmpPoint = None    # QPointF

    def mousePressEvent(self, qMousePressEvent):
        e = qMousePressEvent
        if e.buttons() & Qt.LeftButton :
            vertex = self.screenToWorld( e.pos())  # QPointF
            if None != self.tmpPoint:
                self.qLineFs.append(QLineF(self.screenToWorld(self.tmpPoint), self.screenToWorld(e.pos())))
                self.tmpPoint = None
            else:
                self.tmpPoint = e.pos()

            # self.points.append(e.pos())
            # self.take_screenshot()
            # self.makeConvexHull(self.vertexs)
        self.lastPos = e.pos()
        self.update()
        
    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(0, 0, 0))
        # pen.setWidth()
        qPainter.setPen(pen)
        for l in self.qLineFs:
            qPainter.drawLines(l)

    def drawInScreen(self, qPainter):
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
