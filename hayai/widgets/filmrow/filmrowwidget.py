from typing import Optional
from PyQt6.QtCore import QModelIndex, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget
from providers import Page
from hayai.widgets.autofitview import QAutoFitView
from hayai.models.filmlist import QFilmListModel
from hayai.delegates.filmdelegate import QFilmDelegate
from hayai.widgets import QTitleNavbar

class QFilmRow(QFrame):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self,category: str,model: QFilmListModel, parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

        self._model: QFilmListModel = model
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

        filmRowLayout: QVBoxLayout = QVBoxLayout()
        filmRowLayout.addWidget(titleNavbar)
        filmRowLayout.addWidget(view)
        filmRowLayout.setContentsMargins(0,0,0,0)
        filmRowLayout.setSpacing(0)
        self.setLayout(filmRowLayout)

    def onPageLoaded(self,page: Page):
        if page.films:
            self._model.appendRow(*page.films)


