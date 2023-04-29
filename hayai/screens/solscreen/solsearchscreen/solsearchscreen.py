from typing import Optional

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from hayai.features.provider.delegates.filmdelegate import QFilmDelegate
from hayai.features.sol.viewmodels import QSolSearchViewModel
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.widgets.searchbar import QSearchbar

from ...screen import QScreen
from ..solfilmdetailscreen import QSolFilmDetailScreen

class QSolSearchScreen(QScreen):

    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._searchViewModel:  QSolSearchViewModel = QSolSearchViewModel()

        searchbar: QSearchbar = QSearchbar()

        view: QAutoFitView = QAutoFitView()
        view.setWrapping(True)
        view.setModel(self._searchViewModel.queriedFilms)
        view.setItemDelegate(QFilmDelegate())

        view.clicked.connect(self.onFilmClicked)
        searchbar.lineEditTextChanged.connect(self._searchViewModel.search)

        Layout: QVBoxLayout = QVBoxLayout()
        Layout.addWidget(searchbar)
        Layout.addWidget(view)
        Layout.setContentsMargins(0,0,0,0)
        Layout.setSpacing(0)
        self.setLayout(Layout)
        self.title = "Search"

    def onFilmClicked(self,index: QModelIndex):
        filmUrl: Optional[str] = index.siblingAtColumn(1).data()
        if filmUrl is not None and self.navigation is not None:
            screen: QScreen = QSolFilmDetailScreen(filmUrl)
            self.navigation.push(screen)
