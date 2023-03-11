from typing import Optional, Type

from PyQt5.QtCore import QSize, Qt, pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QFrame,  QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy


class QHeader(QFrame):
    searchButtonClicked: pyqtSignal = pyqtSignal()
    lightModeButtonClicked: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional['QWidget'] = None) -> None:
        super().__init__(parent)
    
        self.searchButton: QPushButton = QPushButton()
        self.searchButton.setObjectName("search-button")
        self.searchButton.setIcon(QIcon("hayai/widgets/header/assets/icons/search.png"))
        self.searchButton.setIconSize(QSize(25,25))
        self.searchButton.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Minimum)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.searchButton)
        self.headerLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.headerLayout.setContentsMargins(0,0,5,0)
        self.headerLayout.setSpacing(5)
        self.setLayout(self.headerLayout)

        self.setObjectName("QHeader")
        self.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        #self.setFixedHeight(60)

    @pyqtSlot(int)
    def headerButtonGroupClicked(self,id: int):
        if id == 1: self.searchButtonClicked.emit()
        elif id == 2: self.lightModeButtonClicked.emit()

        
