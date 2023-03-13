from typing import Optional
from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtGui import  QIcon, QPixmap
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

class QSearchbar(QFrame):
    lineEditTextChanged: pyqtSignal = pyqtSignal(str)
    lineEditFocusGained: pyqtSignal = pyqtSignal()
    

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        searchLabel: QLabel = QLabel()
        searchLabel.setPixmap(QPixmap("hayai/widgets/sidebar/assets/icons/search.png"))
        searchLabel.setPixmap(searchLabel.pixmap().scaled(16,16))

        searchLineEdit: QLineEdit = QLineEdit()
        searchLineEdit.setPlaceholderText("Quick search")
        searchLineEdit.setFrame(False)
        searchLineEdit.setAutoFillBackground(False)
        searchLineEdit.installEventFilter(self)

        clearButton: QPushButton = QPushButton()
        clearButton.setIcon(QIcon("hayai/widgets/sidebar/assets/icons/clear.png"))

        clearButton.clicked.connect(searchLineEdit.clear)
        searchLineEdit.textChanged.connect(self.lineEditTextChanged)

        searchbarLayout: QHBoxLayout = QHBoxLayout()
        searchbarLayout.addWidget(searchLabel)
        searchbarLayout.addWidget(searchLineEdit)
        searchbarLayout.addWidget(clearButton)
        searchbarLayout.setContentsMargins(0,0,0,0)
        searchbarLayout.setSpacing(0)
        self.setLayout(searchbarLayout)

        self.setObjectName("QSearchbar")

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn and isinstance(obj, QLineEdit):#pyright: ignore
            self.lineEditFocusGained.emit()
        return super().eventFilter(obj, event)


