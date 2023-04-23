from typing import Optional
from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QSizePolicy, QStyledItemDelegate, QVBoxLayout, QWidget
from hayai.features.widgets.autofitview import QAutoFitView
from .rownavbar import QRowNavbar

class QRowView(QFrame):

    itemClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self,category: str,model: QAbstractItemModel,delegate: Optional[QStyledItemDelegate] = None, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        categoryFrame: QFrame = QFrame()
        categoryFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        rowNavbar: QRowNavbar = QRowNavbar(category)

        view: QAutoFitView = QAutoFitView()
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        if delegate is not None:
            view.setItemDelegate(delegate)
        view.setModel(model)


        rowNavbar.forward.connect(view.scrollRight)
        rowNavbar.back.connect(view.scrollLeft)
        view.clicked.connect(self.itemClicked)

        rowViewLayout: QVBoxLayout = QVBoxLayout()
        rowViewLayout.addWidget(rowNavbar)
        rowViewLayout.addWidget(view)
        rowViewLayout.setContentsMargins(0,0,0,0)
        rowViewLayout.setSpacing(0)
        self.setLayout(rowViewLayout)


