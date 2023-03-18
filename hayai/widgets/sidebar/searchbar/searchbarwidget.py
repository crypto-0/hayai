from typing import Optional
from PyQt5.QtCore import QEvent, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import  QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

class QSearchbar(QFrame):
    lineEditTextChanged: pyqtSignal = pyqtSignal(str)
    lineEditFocusGained: pyqtSignal = pyqtSignal()
    

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(500)

        searchLabel: QLabel = QLabel()
        searchLabel.setPixmap(QPixmap("hayai/widgets/sidebar/assets/icons/search.png"))
        searchLabel.setPixmap(searchLabel.pixmap().scaled(16,16))

        self.searchLineEdit: QLineEdit = QLineEdit()
        self.searchLineEdit.setFixedHeight(30)
        self.searchLineEdit.setPlaceholderText("Quick search")
        self.searchLineEdit.setFrame(False)
        self.searchLineEdit.setAutoFillBackground(False)
        self.searchLineEdit.installEventFilter(self)

        clearButton: QPushButton = QPushButton()
        clearButton.setIcon(QIcon("hayai/widgets/sidebar/assets/icons/clear.png"))

        clearButton.clicked.connect(self.searchLineEdit.clear)
        self.timer.timeout.connect(self.__emitEditedText)
        self.searchLineEdit.textChanged.connect(self.__startEditTimeout)


        searchbarLayout: QHBoxLayout = QHBoxLayout()
        searchbarLayout.addWidget(searchLabel)
        searchbarLayout.addWidget(self.searchLineEdit)
        searchbarLayout.addWidget(clearButton)
        searchbarLayout.setContentsMargins(0,0,0,0)
        searchbarLayout.setSpacing(0)
        self.setLayout(searchbarLayout)

        self.setObjectName("QSearchbar")

    def __startEditTimeout(self):
        self.timer.start()
    
    def __emitEditedText(self):
        self.timer.stop()
        self.lineEditTextChanged.emit(self.searchLineEdit.text())

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn and isinstance(obj, QLineEdit):#pyright: ignore
            self.lineEditFocusGained.emit()
        return super().eventFilter(obj, event)


