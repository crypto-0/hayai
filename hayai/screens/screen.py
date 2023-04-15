from typing import Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QWidget

class QScreen(QFrame):
    stopped: pyqtSignal = pyqtSignal()
    started: pyqtSignal = pyqtSignal()
    destroyed: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)

    def onStart(self):
        self.started.emit()

    def onStop(self):
        self.stopped.emit()

    def onDestroy(self):
        self.destroyed.emit()

