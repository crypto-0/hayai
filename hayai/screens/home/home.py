from typing import  Optional
from PyQt6.QtCore import Q_ARG, QMetaObject, QModelIndex, QThread, Qt, pyqtSignal

from PyQt6.QtWidgets import  QFrame, QHBoxLayout,  QScrollArea,  QSizePolicy, QVBoxLayout
from PyQt6.QtWidgets import QWidget
from providers import  Provider

from hayai.features.models.filmlist import QFilmListModel
from hayai.features.widgets.filmrow import QFilmRow
from hayai.features.qprovider import QProvider
from ..screen import QScreen

class QHome(QScreen):

    filmClicked: pyqtSignal = pyqtSignal(QModelIndex)
    def __init__(self,provider: Provider, parent: Optional[QWidget] = None ) -> None:
        super().__init__(parent=parent)

        self._qprovidersThread: QThread = QThread()

        scrollAreaFrame: QFrame = QFrame()

        scrollArea = QScrollArea()
        scrollArea.setObjectName("scroll-area")
        scrollArea.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        scrollArea.setWidget(scrollAreaFrame)
        scrollArea.horizontalScrollBar().setEnabled(False)
        scrollArea.verticalScrollBar().setEnabled(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setWidgetResizable(True)
        scrollArea.setContentsMargins(0,0,0,0)

        scrollAreaFrameLayout: QVBoxLayout = QVBoxLayout()
        for category in provider.available_home_categories:
            qprovider: QProvider = QProvider(provider)
            qprovider.moveToThread(self._qprovidersThread)
            self._qprovidersThread.finished.connect(qprovider.deleteLater)
            filmModel: QFilmListModel = QFilmListModel()
            filmRow: QFilmRow = QFilmRow(category,filmModel,qprovider,parent=self)
            filmRow.filmClicked.connect(self.filmClicked)
            self.started.connect(lambda category=category, qprovider= qprovider:QMetaObject.invokeMethod(qprovider,"getCategory",Q_ARG(str,category),Q_ARG(int,1)))
            self.stopped.connect(filmModel.clear)
            scrollAreaFrameLayout.addWidget(filmRow)

        scrollAreaFrameLayout.setContentsMargins(0,0,0,0)
        scrollAreaFrameLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scrollAreaFrameLayout.setSpacing(0)
        scrollAreaFrame.setLayout(scrollAreaFrameLayout)

        homeLayout: QHBoxLayout = QHBoxLayout()
        homeLayout.addWidget(scrollArea)
        homeLayout.setContentsMargins(0,0,0,0)
        homeLayout.setSpacing(0)
        self.setLayout(homeLayout)

        self.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.setObjectName("QHome")
        self._qprovidersThread.start()

    def onDestroy(self):
        self._qprovidersThread.quit()
        self._qprovidersThread.wait()
        return super().onDestroy()

