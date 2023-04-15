from typing import Optional
from PyQt6.QtCore import QModelIndex, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from hayai.features.qprovider import QProvider
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.delegates.filmdelegate import QFilmDelegate
from ..titlenavbar import QTitleNavbar

class QFilmRow(QFrame):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self,category: str,model: QFilmListModel,qprovider: QProvider,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self._model: QFilmListModel = model
        self._qprovider: QProvider = qprovider
        self._category: str = category

        categoryFrame: QFrame = QFrame()
        categoryFrame.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        titleNavbar: QTitleNavbar = QTitleNavbar(category)

        view: QAutoFitView = QAutoFitView()
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setItemDelegate(QFilmDelegate())
        view.setModel(model)


        titleNavbar.forward.connect(view.scrollRight)
        titleNavbar.back.connect(view.scrollLeft)
        view.clicked.connect(self.filmClicked)
        qprovider.page.connect(lambda page: self._model.appendRow(*page.films))


        filmRowLayout: QVBoxLayout = QVBoxLayout()
        filmRowLayout.addWidget(titleNavbar)
        filmRowLayout.addWidget(view)
        filmRowLayout.setContentsMargins(0,0,0,0)
        filmRowLayout.setSpacing(0)
        self.setLayout(filmRowLayout)

