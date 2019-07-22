import sys
import utilsNew
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from contextlib import redirect_stdout
from queue import Queue

# This was originally supposed to gui for the whole project that could give a
# graphical interface to every aspect of the project, but I later realized that
# only a few things were actually made easier and more convenient with a gui, 
# So, this file is deprecated and replaced by plotgui.py



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'SRCFD graphical utility'
        self.left = 80
        self.top = 80
        self.width = 800
        self.height = 500
        self.masterFileList = []
        self.hrsavepth = ""
        self.lrsavepth = ""
        self.output = ""
        self.log = QTextEdit(self)
        self.log.move(185, 300)
        self.log.resize(600,150)
        self.log.setStyleSheet("background-color:black; color: green;")
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.lrsavepathtxt = QLineEdit(self)
        self.lrsavepathtxt.setText("enter low res save path here")
        self.lrsavepathtxt.move(185, 190)
        self.lrsavepathtxt.resize(500, 30)

        setlrButton = QPushButton("set", self)
        setlrButton.move(695,190)
        setlrButton.resize(90,30)
        setlrButton.clicked.connect(self.setlr)

        self.hrsavepathtxt = QLineEdit(self)
        self.hrsavepathtxt.setText("enter high res save path here")
        self.hrsavepathtxt.move(185, 235)
        self.hrsavepathtxt.resize(500, 30)

        sethrButton = QPushButton("set", self)
        sethrButton.move(695,235)
        sethrButton.resize(90,30)
        sethrButton.clicked.connect(self.sethr)

        buildButton = QPushButton("buildall", self)
        buildButton.move(20,10)
        buildButton.resize(150,75)
        buildButton.clicked.connect(self.build)

        saveButton = QPushButton("save as h5", self)
        saveButton.move(20,100)
        saveButton.resize(150,75)
        saveButton.clicked.connect(self.save)

        anim2dButton = QPushButton("plot and animate 2d data", self)
        anim2dButton.move(20,190)
        anim2dButton.resize(150,75)
        anim2dButton.clicked.connect(self.anim2d)

        anim3dButton = QPushButton("plot and animate 3d data", self)
        anim3dButton.move(20,280)
        anim3dButton.resize(150,75)
        anim3dButton.clicked.connect(self.anim3d)

        build3dButton = QPushButton("build 3d data from 2d", self)
        build3dButton.move(20,370)
        build3dButton.resize(150,75)
        build3dButton.clicked.connect(self.build3d)

        drop = CustomLabel('Drop here.', self)
        drop.move(185,10)
        drop.resize(600,165)

        area = QScrollArea(self)
        area.move(185, 10)
        area.resize(600,165)
        area.setWidget(drop)


        self.show()


    @pyqtSlot()
    def build(self):
        if len(self.masterFileList) < 1:
            pass

    @pyqtSlot()
    def save(self):
        pass

    @pyqtSlot()
    def anim2d(self):
        pass

    @pyqtSlot()
    def anim3d(self):
        pass

    @pyqtSlot()
    def build3d(self):
        pass

    @pyqtSlot()
    def setlr(self):
        self.lrSavepth = self.lrsavepathtxt.text()
        self.output += "low res save path set to \"" + self.lrSavepth + "\"\n"
        self.log.setText(self.output)

    @pyqtSlot()
    def sethr(self):
        self.hrSavepth = self.hrsavepathtxt.text()
        self.output += "high res save path set to \"" + self.hrSavepth + "\"\n"
        self.log.setText(self.output)


class CustomLabel(QLabel):

    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()
    def dropEvent(self, e):

        lst = [i.replace("file:///","") + \
                                "\n" for i in e.mimeData().text().split("\n")]
        self.setText("".join(lst))
        print(len(lst))
        print(lst[0])
        if self.size().height() < len(lst)*14:
            self.resize(self.size().width(), len(lst)*14)
        ex.masterFileList = lst




app = QApplication(sys.argv)
app.setStyle("Fusion")
ex = App()
ex.show()


app.exec_()
