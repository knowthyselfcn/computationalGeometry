#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys, random
from PyQt4.Qt import Qt
from PyQt4.QtGui import QApplication, QWidget
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform
# import numpy as np
from PIL import Image
import StringIO


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

class CoordWidget(QtGui.QWidget):
    
    def __init__(self):
        super(CoordWidget, self).__init__()
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
        self.lastPos = None
        self.scene_size_ = 1.5

        self.images = []   # save widget image to gif
        self.msgCnt = 0
        self.show()

    def mousePressEvent (self, pe):
        self.lastPos = pe.pos()
        self.update()

    # deal with general mouseMoveEvent, such as rightKey to move coord
    def mouseMoveEvent(self, e):
        newPos = e.pos()
        if (self.lastPos - newPos).manhattanLength() < 1:
            self.lastPos = newPos
            return
        if e.buttons() & Qt.RightButton :
            translation = self.screenToWorld(newPos) - self.screenToWorld(self.lastPos)
            self.scene_translation_ = self.scene_translation_ + translation
        # elif e.buttons() & Qt.LeftButton:
        self.lastPos = e.pos()
        self.update()

    # general event: escape to exit,
    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == Qt.Key_Escape:
            sys.exit(0)

    def wheelEvent (self, e):   # QWheelEvent e
        old_world_pos_of_mouse = self.screenToWorld(e.pos())
        scale_factor = 1
        if e.delta() > 0 :
            scale_factor = scale_factor * 10 / 11
        else:
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

    def showInfo(self, qPainter, qStr):
        self.msgCnt =  self.msgCnt + 1
        pen = qPainter.pen()
        pen.setColor(QColor.fromRgb(0, 0, 0))
        qPainter.setPen(pen)
        qPainter.drawText(QPoint(0, 15 * self.msgCnt ), qStr)

    # save QImage to PIL image
    def take_screenshot(self):
        qPixmap = QtGui.QPixmap.grabWindow(self.winId())
        qImage = qPixmap.toImage()
        qBuffer = QtCore.QBuffer()
        qBuffer.open(QtCore.QIODevice.ReadWrite)
        qImage.save(qBuffer, "PNG")
        strio = StringIO.StringIO()
        strio.write(qBuffer.data())
        qBuffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)
        self.images.append(pil_im)

    def saveGIF(self):
        img = self.images[0]
        img.save("aaaaaaaaaaaaaa.gif", optimize=True, save_all=True, append_images=self.images, quality=10)

    def preDraw(self, qPainter):
        qPainter.save()
        qPainter.setWorldTransform(self.getWorldToScreenTransform())
        pen = qPainter.pen()
        pen.setCosmetic(True)
        qPainter.setPen(pen)
        brush = QtGui.QBrush()
        brush.setColor(QColor.fromRgb(255, 0, 0))
        brush.setStyle(Qt.SolidPattern)       # 填充绘制的多边形区域
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

    # 这两个函数是为了子类override的。
    def drawInWorld(self, qPainter):
        pass

    def drawInScreen(self, qPainter):
        pass

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)   #this is the main QPainter
        # qp.begin(self)

        self.preDraw(qp)
        self.drawCoord(qp)

        self.drawInWorld(qp)

        self.postDraw(qp)

        self.drawInScreen(qp)


def main():    
    app = QtGui.QApplication(sys.argv)
    ex = CoordWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
