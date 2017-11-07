#! /usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division
import sys, random
sys.path.append('../')
from PyQt4.QtCore import QPoint, QPointF, QLine, QLineF
from PyQt4.QtGui import QColor, QMatrix, QTransform
import numpy as np
from bintrees import BinaryTree, AVLTree

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

# return QPointF
def lineIntersectTest( qLineF1, qLineF2):
    a1 = (qLineF1.y1() - qLineF1.y2())/(qLineF1.x1() - qLineF1.x2())
    b1 = qLineF1.y1() - a1 * qLineF1.x1()
    a2 = (qLineF2.y1() - qLineF2.y2()) / (qLineF2.x1() - qLineF2.x2())
    b2 = qLineF2.y1() - a2 * qLineF2.x1()
    a = np.array([[a1, -1 ], [a2, -1]])
    b = np.array([-b1, -b2])
    x = np.linalg.solve(a, b)
    p = QPointF(x[0], x[1])
    if pointInSegment(p, qLineF1) and pointInSegment(p, qLineF2):
        return p
    else:
        return None


def handleEventPoint(p):    # QPointF
    pass

def getSegByp(k, v):
    pass

#
# S : segment list
def findIntersections(S):
    T = AVLTree()
    Q = []  # event queue with [QPointF, lineId]
    for i, l in enumerate(S):
        Q.append([l.p1(), i, "l"])  # l : left, r : right, c : center
        Q.append([l.p2(), i, "r"])
    while Q:    # stops if Q = []
        p = Q[0][0]
        Q.pop(0)
        # handleEventPoint(p)
        Up = [p]
        Lp = []
        Segs = []
        T.foreach(lambda k, v: print k, v;if v[0] == p: Segs.append(v[0]) )




