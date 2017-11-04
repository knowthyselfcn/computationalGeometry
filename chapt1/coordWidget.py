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



class CoordWidget(QtGui.QWidget):
    
    def __init__(self):
        super(CoordWidget, self).__init__()
        self.line1 = QLineF(QPointF(-0.4, -0.2), QPointF(-0.1, 0.3))
        self.line2 = QLineF(QPointF(0.2, 0.1), QPointF(0.4, -0.3))
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

        self.scene_translation_ = QPointF(0, 0)
        self.lastPos = QPoint()
        self.scene_size_ = 1.5

        self.show()

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
            self.scene_translation_ = self.scene_translation_ + translation
        elif e.buttons() & Qt.LeftButton:
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos) #QPointF
            self.line2.translate(translation)
        self.lastPos = e.pos()
        self.update()


    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            sys.exit(0)

    def wheelEvent (self, e):   # QWheelEvent e
        old_world_pos_of_mouse = self.screenToWorld(e.pos())
        scale_factor = 1
        if e.delta() > 0 :
            scale_factor = scale_factor * 10 / 11
        else :
            scale_factor = scale_factor * 11 / 10
        if scale_factor < 0:
            scale_factor = -scale_factor
        self.scene_size_ = self.scene_size_ * scale_factor

        new_screen_pos_of_mouse = self.worldToScreen(old_world_pos_of_mouse)
        self.scene_translation_ = self.scene_translation_ + self.screenToWorld(e.pos()) - self.screenToWorld(new_screen_pos_of_mouse)

        self.update()

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

    def showInfo(self, qPainter):
        qPainter.drawText("hello")

    def preDraw(self, qPainter):
        qPainter.save()
        qPainter.setWorldTransform(self.getWorldToScreenTransform())
        pen = qPainter.pen()
        pen.setCosmetic(True)
        qPainter.setPen(pen)
        brush = QtGui.QBrush()
        brush.setColor(QColor.fromRgb(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        qPainter.setBrush(brush)

    def postDraw(self, painter):
        painter.restore()


    def drawCoord(self, qPainter):
        # pen = QtGui.QPen()
        pen = qPainter.pen()
        color = QColor.fromRgb(200, 200, 200)
        pen.setColor( color )
        qPainter.setPen(pen)
        qPainter.drawLines(self.coordinate_system_lines_ )


    def drawInWorld(self, qPainter):
        pass

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)   #this is the main QPainter
        # qp.begin(self)

        self.preDraw(qp)
        self.drawCoord(qp)

        self.drawInWorld(qp)

        self.postDraw(qp)


def main():    
    app = QtGui.QApplication(sys.argv)
    ex = CoordWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
