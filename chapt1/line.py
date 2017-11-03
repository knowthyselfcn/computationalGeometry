#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, random
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import Qt
import numpy as np

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.line1 = [QtCore.QPoint(20, 40), QtCore.QPoint(250, 40)]     #[start, end]
        self.line2 = [QtCore.QPoint(250, 90), QtCore.QPoint(250, 340)]
        self.lastPos = QtCore.QPoint()
        self.initUI()
        
    def initUI(self):      
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Line Intersection Test')
        self.show()


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        # self.drawPoints(qp)
        self.drawLines(qp)
        qp.end()
        
    def drawPoints(self, qp):      
        qp.setPen(QtCore.Qt.red)
        size = self.size()        
        for i in range(1000):
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)

    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        l1 = self.line1
        l2 = self.line2
        qp.drawLine(l1[0].x(), l1[0].y(), l1[1].x(), l1[1].y())
        qp.drawLine(l2[0].x(), l2[0].y(), l2[1].x(), l2[1].y())
        # print(l1, l2)


    def mouseMoveEvent (self, me):
        l2 = self.line2
        delta = me.pos() - self.lastPos
        l2[0] = l2[0] + delta
        l2[1] = l2[1] + delta
        # print(me.pos())
        self.lastPos = me.pos()
        self.update()

    def mousePressEvent (self, pe):
        self.lastPos = pe.pos()
        self.update()


    def keyPressEvent (self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            sys.exit(0)

    def showInfo(self):
        pass

def main():    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
