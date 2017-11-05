#! /usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division
from  coordWidget import CoordWidget
import sys, random
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
        
    def drawInWorld(self, qPainter):
        pen = qPainter.pen()


        old_transform = qPainter.worldTransform()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.resetTransform()
        crossPoint = self.worldToScreen(QPointF(0.2, 0.4))
        qPainter.drawPoint(crossPoint)
        qPainter.setWorldTransform(old_transform)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Test()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
