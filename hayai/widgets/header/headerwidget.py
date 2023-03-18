from typing import Optional, Type

from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QAbstractButton, QFrame, QLabel,  QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy


class QHeader(QFrame):
    searchButtonClicked: pyqtSignal = pyqtSignal()
    lightModeButtonClicked: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent)
    
        self.currentScreenLabel: QLabel =QLabel("Home")

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.currentScreenLabel)
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.headerLayout.setContentsMargins(5,0,5,0)
        self.headerLayout.setSpacing(10)
        self.setLayout(self.headerLayout)

        self.setObjectName("QHeader")
        #self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        self.setFixedHeight(40)

    def setCurrentScreenTitle(self,screenName: str):
        self.currentScreenLabel.setText(screenName)


        
