
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from contextlib import redirect_stdout
import plotter

# This is a drag and drop gui that allows for more intuitive and convenient use
# of the functions in plotter.py. The desired files can be dragged directly into
# the window and plotted or animated.



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'SRCFD graphical utility'
        self.left = 80
        self.top = 80
        self.width = 620
        self.height = 500
        self.masterFileList = []
        self.savepth = ""
        self.gifname = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.savepathtxt = QLineEdit(self)
        self.savepathtxt.setText("enter save path here")
        self.savepathtxt.move(10, 285)
        self.savepathtxt.resize(500, 30)

        setlrButton = QPushButton("set", self)
        setlrButton.move(520,285)
        setlrButton.resize(90,30)
        setlrButton.clicked.connect(self.setpath)

        self.gifnamebutton = QLineEdit(self)
        self.gifnamebutton.setText("enter gif name here")
        self.gifnamebutton.move(10, 325)
        self.gifnamebutton.resize(500, 30)

        setnameButton = QPushButton("set", self)
        setnameButton.move(520,325)
        setnameButton.resize(90,30)
        setnameButton.clicked.connect(self.setgifname)

        drop = CustomLabel('Drop here.', self)
        drop.move(10,10)
        drop.resize(600,265)

        area = QScrollArea(self)
        area.move(10, 10)
        area.resize(600,265)
        area.setWidget(drop)

        self.plot2dbutton = QPushButton("make 2D plots", self)
        self.plot2dbutton.move(10, 365)
        self.plot2dbutton.resize(100, 30)
        self.plot2dbutton.clicked.connect(self.do2d)

        self.plot3dbutton = QPushButton("make 3D plots", self)
        self.plot3dbutton.move(120, 365)
        self.plot3dbutton.resize(100, 30)
        self.plot3dbutton.clicked.connect(self.do3d)

        self.gifbutton = QPushButton("make gif", self)
        self.gifbutton.move(230, 365)
        self.gifbutton.resize(100, 30)
        self.gifbutton.clicked.connect(self.dogif)

        self.show()

    @pyqtSlot()
    def setpath(self):
        self.savepth = self.savepathtxt.text()
        print(self.savepth)

    @pyqtSlot()
    def setgifname(self):
        self.gifname = self.gifnamebutton.text()

    @pyqtSlot()
    def do2d(self):
        if len(self.masterFileList) < 1:
            pass
        plotter.plot2d(self.masterFileList, self.savepth)

    @pyqtSlot()
    def do3d(self):
        if len(self.masterFileList) < 1:
            pass
        color = QColorDialog.getColor().name()
        plotter.plot3d(self.masterFileList, self.savepth, color)

    @pyqtSlot()
    def dogif(self):
        if len(self.masterFileList) < 1:
            pass
        print("gif")
        plotter.makeGif(self.masterFileList, self.gifname)

class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()
    def dropEvent(self, e):

        lst = [i.replace("file:///","") + "\n" for i in e.mimeData().text().split("\n")]
        if len(lst) > 1:
            lst = lst[0:len(lst)-1]
        self.setText("".join(lst))
        print(len(lst))
        if self.size().height() < len(lst)*14:
            self.resize(self.size().width(), len(lst)*14)
        ex.masterFileList = lst


app = QApplication(sys.argv)
app.setStyle("Fusion")
ex = App()
ex.show()


app.exec_()
