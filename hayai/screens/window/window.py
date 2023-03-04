from typing import Optional
from PyQt5.QtWidgets import QGridLayout, QWidget
from hayai.widgets import QSidebar


class Window(QWidget):

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__()

        sidebar: QSidebar = QSidebar()

        windowLayout: QGridLayout = QGridLayout()
        windowLayout.addWidget(sidebar,0,0,1,1)
        windowLayout.setSpacing(0)
        windowLayout.setContentsMargins(0,0,0,0)
        self.setLayout(windowLayout)

        self.setMaximumSize(1920,1080)
        self.setObjectName("window")
        self.setWindowTitle("Hayai")
        self.loadStylesheet()

    def loadStylesheet(self):
        with open("hayai/screens/window/window.qss","r") as f:
            self.setStyleSheet(f.read())

        
