#! /usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division

import sys, random
sys.path.append('/mypath/scriptlib')
from  coordWidget import CoordWidget
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform, QPolygonF
import numpy as np
import scipy.spatial import Delaynay


class Triangulation(CoordWidget):
    def __init__(self):
        super(Triangulation, self).__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Triangulation Test')


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
            pass
        self.lastPos = e.pos()
        self.update()

    def drawInWorld(self, qPainter):
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(255, 0, 0))
        qPainter.setPen(pen)


        old_transform = qPainter.worldTransform()
        pen.setWidth(5)
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.resetTransform()


        qPainter.setWorldTransform(old_transform)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Triangulation()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
