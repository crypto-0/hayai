from PyQt6.QtCore import  Q_ARG, QMetaObject, QModelIndex, QThread,  pyqtSignal
from PyQt6.QtWidgets import  QAbstractItemView,  QHBoxLayout, QVBoxLayout
from PyQt6.QtWidgets import QWidget
from typing import Optional 

from providers import Page, Provider, PageInfo
from hayai.features.qprovider import QProvider
from hayai.features.delegates.filmdelegate import QFilmDelegate
from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.autofitview import QAutoFitView
from hayai.features.widgets.titlenavbar import QTitleNavbar
from ..screen import QScreen

class QCategory(QScreen):
    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    changeGenerator: pyqtSignal = pyqtSignal(object)

    def __init__(self,category: str, provider: Provider, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._qprovider = QProvider(provider)
        self._qproviderThread: QThread = QThread()
        self._qprovider.moveToThread(self._qproviderThread)
        self._category = category
        self._pageInfo = PageInfo(1,1,True)

        self._categoryModel: QFilmListModel =QFilmListModel()

        titleNavbar: QTitleNavbar = QTitleNavbar(category)
        categoryView: QAutoFitView = QAutoFitView()
        categoryView.setWrapping(True)
        categoryView.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)
        categoryView.setSizeAdjustPolicy(QAbstractItemView.SizeAdjustPolicy.AdjustToContents)
        categoryView.setModel(self._categoryModel)
        categoryView.setItemDelegate(QFilmDelegate())
        categoryView.horizontalScrollBar().setEnabled(False)

        categoryView.clicked.connect(self.filmClicked)
        self._qprovider.page.connect(self.pageLoaded)
        self.stopped.connect(self._categoryModel.clear)
        self.started.connect(lambda :QMetaObject.invokeMethod(self._qprovider,"getCategory",Q_ARG(str,self._category),Q_ARG(int,1)))
        titleNavbar.forward.connect(self.nextPage)
        titleNavbar.back.connect(self.prevPage)

        categoryLayout: QVBoxLayout = QVBoxLayout()
        categoryLayout.addWidget(titleNavbar)
        categoryLayout.addWidget(categoryView)
        categoryLayout.setContentsMargins(0,0,0,0)
        categoryLayout.setSpacing(0)
        self.setLayout(categoryLayout)

        self.setObjectName("QCategory")
        self._qproviderThread.start()

    def pageLoaded(self,page: Page):
        self._pageInfo = page.pageInfo
        self._categoryModel.clear()
        self._categoryModel.appendRow(*page.films)

    def nextPage(self):
        if self._pageInfo.has_next_page:
            self._qprovider.getCategory(self._category,self._pageInfo.current_page + 1)

    def prevPage(self):
        if self._pageInfo.current_page > 1:
            self._qprovider.getCategory(self._category,self._pageInfo.current_page - 1)
    def onStart(self):
        self._pageInfo = PageInfo(1,1,True)

        return super().onStart()

    def onDestroy(self):
        self._qproviderThread.quit()
        self._qproviderThread.wait()
        return super().onDestroy()

