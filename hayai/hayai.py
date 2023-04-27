from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
)
from PyQt6.QtCore import  Qt, pyqtSignal, qInstallMessageHandler
from hayai.screens.solscreen import  QSolScreen
from hayai.features.widgets.titlebar import QStandardTitleBar

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
        qInstallMessageHandler(self.handler)

    def onStart(self):
        self.started.emit()

    def handler(self,msgType,context,string):
        pass
    def loadStylesheet(self):
        with open("hayai/hayai.qss","r") as f:
            self.setStyleSheet(f.read())



