from PyQt6.QtCore import Q_ARG, QMetaObject, QModelIndex, QThread, pyqtSignal
from PyQt6.QtWidgets import  QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Optional 
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.qprovider import QProvider
from hayai.features.delegates.filmdelegate import QFilmDelegate
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.widgets.searchbar import QSearchbar
from hayai.features.widgets.titlenavbar import QTitleNavbar
from providers import Page, Provider, PageInfo
from ..screen import QScreen

class QSearch(QScreen):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    lineEditTextChanged: pyqtSignal = pyqtSignal(str)
    changeGenerator: pyqtSignal = pyqtSignal(object)

    def __init__(self, provider: Provider, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._qprovider = QProvider(provider)
        self._qproviderThread: QThread = QThread()
        self._qprovider.moveToThread(self._qproviderThread)
        self._qproviderThread.finished.connect(self._qprovider.deleteLater)
        self._pageInfo = PageInfo(0,0,True)
        self._searchQuery: str = ""

        self.searchModel: QFilmListModel =QFilmListModel()

        titleNavbar: QTitleNavbar = QTitleNavbar("search")

        searchView: QAutoFitView = QAutoFitView()
        searchView.setWrapping(True)
        searchView.setModel(self.searchModel)
        searchView.setItemDelegate(QFilmDelegate())

        self.searchbar: QSearchbar = QSearchbar()

        searchView.clicked.connect(self.filmClicked)
        self.searchbar.lineEditTextChanged.connect(self.search)
        self._qprovider.page.connect(self.pageLoaded)
        titleNavbar.forward.connect(self.nextPage)
        titleNavbar.back.connect(self.prevPage)

        searchLayout: QVBoxLayout = QVBoxLayout()
        searchLayout.addWidget(titleNavbar)
        searchLayout.addWidget(self.searchbar)
        searchLayout.addWidget(searchView)
        searchLayout.setContentsMargins(0,0,0,0)
        searchLayout.setSpacing(0)
        self.setLayout(searchLayout)

        self.setObjectName("QSearch")
        self._qproviderThread.start()

    def search(self,query: str):
        self._searchQuery = query
        QMetaObject.invokeMethod(self._qprovider,"search",Q_ARG(str,query),Q_ARG(int,1))


    def pageLoaded(self,page: Page):
        self._pageInfo = page.pageInfo
        self.searchModel.clear()
        self.searchModel.appendRow(*page.films)

    def nextPage(self):
        if self._pageInfo.has_next_page:
            QMetaObject.invokeMethod(self._qprovider,"search",Q_ARG(str,self._searchQuery),Q_ARG(int,self._pageInfo.current_page + 1))

    def prevPage(self):
        if self._pageInfo.current_page > 1:
            QMetaObject.invokeMethod(self._qprovider,"search",Q_ARG(str,self._searchQuery),Q_ARG(int,self._pageInfo.current_page - 1))

    def onDestroy(self):
        self._qproviderThread.quit()
        self._qproviderThread.wait()
        return super().onDestroy()
