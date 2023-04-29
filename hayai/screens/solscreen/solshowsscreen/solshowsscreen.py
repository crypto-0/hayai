from typing import Optional

from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

from hayai.features.provider.delegates.filmdelegate import QFilmDelegate
from hayai.features.sol.viewmodels import QSolShowsViewModel
from hayai.features.widgets.autofitview import QAutoFitView

from ...screen import QScreen
from ..solfilmdetailscreen import QSolFilmDetailScreen

class QSolShowsScreen(QScreen):

    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._showsViewModel:  QSolShowsViewModel = QSolShowsViewModel()

        view: QAutoFitView = QAutoFitView()
        view.setWrapping(True)
        view.setModel(self._showsViewModel.shows)
        view.setItemDelegate(QFilmDelegate())

        view.clicked.connect(self.onFilmClicked)

        Layout: QVBoxLayout = QVBoxLayout()
        Layout.addWidget(view)
        Layout.setContentsMargins(0,0,0,0)
        Layout.setSpacing(0)
        self.setLayout(Layout)
        self.title = "Shows"

    def onFilmClicked(self,index: QModelIndex):
        filmUrl: Optional[str] = index.siblingAtColumn(1).data()
        if filmUrl is not None and self.navigation is not None:
            screen: QScreen = QSolFilmDetailScreen(filmUrl)
            self.navigation.push(screen)
