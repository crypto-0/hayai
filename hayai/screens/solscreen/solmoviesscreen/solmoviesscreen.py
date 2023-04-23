from PyQt6.QtCore import   QModelIndex,  pyqtSignal
from PyQt6.QtWidgets import   QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Optional 

from hayai.features.provider.delegates.filmdelegate import QFilmDelegate
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.sol.viewmodels import QSolMoviesViewModel
from ...screen import QScreen

class QSolMoviesScreen(QScreen):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)

    def __init__(self, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._moviesViewModel:  QSolMoviesViewModel = QSolMoviesViewModel()

        view: QAutoFitView = QAutoFitView()
        view.setWrapping(True)
        view.setModel(self._moviesViewModel.movies)
        view.setItemDelegate(QFilmDelegate())

        view.clicked.connect(self.filmClicked)

        Layout: QVBoxLayout = QVBoxLayout()
        Layout.addWidget(view)
        Layout.setContentsMargins(0,0,0,0)
        Layout.setSpacing(0)
        self.setLayout(Layout)
        self.title = "Movies"
