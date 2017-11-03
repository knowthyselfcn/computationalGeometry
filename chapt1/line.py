#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, random
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform
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

        self.total_length = 0.9
        self.coordinate_system_lines_ = []
        self.coordinate_system_lines_.append(QPointF(-self.total_length, 0))
        self.coordinate_system_lines_.append(QPointF(self.total_length, 0))
        self.coordinate_system_lines_.append(QPointF(0, -self.total_length))
        self.coordinate_system_lines_.append(QPointF(0, self.total_length))

        self.scene_translation_ = QPointF()
        self.lastPos = QPoint()
        self.scene_size_ = 1.5

        self.show()
        
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

    def mouseMoveEvent (self, me):
        l2 = self.line2
        delta = me.pos() - self.lastPos
        l2[0] = l2[0] + delta
        l2[1] = l2[1] + delta
        self.lastPos = me.pos()
        self.update()

    def mousePressEvent (self, pe):
        self.lastPos = pe.pos()
        self.update()

    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.RightButton :
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)
            print(translation)
            self.scene_translation_ = self.scene_translation_ + translation

        self.update()


    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            sys.exit(0)

    def wheelEvent (self, e):   # QWheelEvent e
        old_world_pos_of_mouse = self.screenToWorld(e.pos())
        scale_factor = 1
        if e.delta() > 0 :
            scale_factor  = scale_factor * 11/10
        else :
            scale_factor = scale_factor * 10 / 11
        print scale_factor
        if scale_factor < 0:
            scale_factor = -scale_factor
        self.scene_size_ = self.scene_size_ * scale_factor

        new_screen_pos_of_mouse = self.worldToScreen(old_world_pos_of_mouse)
        self.scene_translation_ = self.scene_translation_ + self.screenToWorld(e.pos()) - self.screenToWorld(new_screen_pos_of_mouse)

        self.update()

    def drawCoord(self, painter):
        pen = QtGui.QPen()
        color = QColor.fromRgb(200, 200, 200)
        pen.setColor( color )
        painter.setPen(pen)
        painter.drawLines(self.coordinate_system_lines_ )
        old_transform = painter.worldTransform()
        painter.resetTransform()
        painter.setWorldTransform(old_transform)


    def getZoomFactor(self):
        return min(self.width() / self.scene_size_, self.height() / self.scene_size_)

    def getWorldToScreenTransform(self):
        logic_mat = QtGui.QMatrix(1, 0, 0, -1, self.width() / 2, self.height() / 2)   # QMatrix
        # 根据场景大小设置缩放系数
        zoom_factor = self.getZoomFactor()                       # float
        scale_mat = QtGui.QTransform.fromScale(zoom_factor, zoom_factor)     #QTransform
        # 根据平移向量设置平移变换
        tranalate_mat = QtGui.QTransform.fromTranslate(self.scene_translation_.x(), self.scene_translation_.y())   #QTransform
        # 总体变换
        return tranalate_mat * scale_mat * QTransform(logic_mat)

    def screenToWorld(self, qPoint):    #return QPointF
        worldPos = self.getWorldToScreenTransform().inverted()[0].map(QPointF(qPoint))
        return worldPos

    def worldToScreen(self, qPointF):
        screen = self.getWorldToScreenTransform().map(qPointF)    #QPointF
        return QPoint(screen.x(), screen.y())



    def showInfo(self):
        pass

    def preDraw(self, painter):
        painter.save()
        painter.setWorldTransform(self.getWorldToScreenTransform())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        brush = QtGui.QBrush()
        brush.setColor(QColor.fromRgb(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

    def postDraw(self, painter):
        painter.restore()

    def paintEvent(self, e):
        qp = QtGui.QPainter()   #this is the main QPainter
        qp.begin(self)

        self.preDraw(qp)

        self.drawLines(qp)
        self.drawCoord(qp)

        self.postDraw(qp)

        qp.end()

def main():    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
