from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
)
from PyQt6.QtCore import  Qt, pyqtSignal
from hayai.screens.solscreen import  QSolScreen
from hayai.widgets.titlebar import QStandardTitleBar

class QHayai(QMainWindow):

    stopped: pyqtSignal = pyqtSignal()
    started: pyqtSignal = pyqtSignal()
    destroyed: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()
        self.titlebar: QStandardTitleBar = QStandardTitleBar(self)
        solScreen: QSolScreen = QSolScreen()

        self.started.connect(solScreen.onStart)
        self.titlebar.backButtonClicked.connect(solScreen.onBackButtonClicked)

        self.setCentralWidget(solScreen)
        self.setMenuWidget(self.titlebar)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle("Hayai")
        self.statusBar()
        self.loadStylesheet()

    def onStart(self):
        self.started.emit()

    def loadStylesheet(self):
        with open("hayai/hayai.qss","r") as f:
            self.setStyleSheet(f.read())

