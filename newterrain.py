import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex


class terrain(object):
    def __init__(self):  # terrain window setup
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setGeometry(0, 110, 800, 800)
        self.w.show()
        self.w.setWindowTitle('Terrain')
        self.w.setCameraPosition(distance=30, elevation=8)

        self.tmp = OpenSimplex()  # for perlin noise function (smoother heights)

        self.count = 1  # random constants
        self.y = range(-30, 33, self.count)
        self.x = range(-30, 33, self.count)
        self.sides = len(self.x)  # or y if they are not equal depending on desired size
        vertList = np.array([[x, y, self.tmp.noise2d(x=n/4 + .2, y=m/4 + .2)]for n, x in enumerate(self.x) for m, y in enumerate(self.y)], dtype=np.float32)
        thisgrid = gl.GLGridItem()  # generate mesh grid and add it to the window (w)
        thisgrid.scale(20, 20, 20)
        self.w.addItem(thisgrid)
        sides = []
        colors = []
        """
        This list append works by using n as the start + one step to the next intersection
        after that, we want to declare the next trigangle vertex at the bottom:
        here's a bad visual
         n+ystep___n
               |   |
               ____n+ystep+sides
        """

        for m in range(self.sides - 1):
            ystep = self.sides * m  # moves to next grid line
            for n in range(self.sides - 1):  # loop to generate verices
                sides.append([n + ystep, n + ystep + self.sides, n + ystep + self.sides + 1])
                sides.append([n + ystep, n + ystep + 1, n + ystep + self.sides + 1])
                colors.append([25, 25, 25, .3])
                colors.append([0, 0, 0, .3])
        sides = np.array(sides)
        peter = np.array(colors)
        self.mesh = gl.GLMeshItem(vertexes=vertList, faces=sides, faceColors=peter, smooth=True, drawEdges=False)
        self.mesh.setGLOptions('opaque')
        self.w.addItem(self.mesh)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    t = terrain()
    t.start()
