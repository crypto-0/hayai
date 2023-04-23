from typing import Optional
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QWidget
from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal 

class QScreen(QFrame):
    created: pyqtSignal = pyqtSignal()
    started: pyqtSignal = pyqtSignal()
    stopped: pyqtSignal = pyqtSignal()
    destroyed: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._title: str = self.__class__.__name__

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self,title: str):
        if title:
            self._title = title

    def onCreated(self):
        self.created.emit()

    def onStart(self):
        self.started.emit()

    def onStop(self):
        self.stopped.emit()

    def onDestroy(self):
        self.destroyed.emit()

    def onBackButtonClicked(self):
        pass

class QScreenNavigationStack(QObject):
    popped: pyqtSignal = pyqtSignal()
    pushed: pyqtSignal = pyqtSignal()

    def __init__(self,root:Optional[QScreen] = None,parent: Optional[QObject] = None):
        super().__init__(parent=parent)
        self.rootScreen: Optional[QScreen] = root
        self.currentScreen: Optional[QScreen] = None
        self.screens: deque[QScreen] = deque()
        if root is not None:
            self.push(root)
            
    def push(self,screen: QScreen):
        if len(self.screens) == 0:
            self.root = screen
        self.currentScreen = screen
        self.pushed.emit()
        self.screens.append(screen)

    def pop(self):
        if len(self.screens) > 0:
            self.screens.pop()
            self.popped.emit()
        if len(self.screens) > 0:
            self.currentScreen = self.screens[-1]
        else:
            self.rootScreen = None
            self.currentScreen = None

        return self.currentScreen

    def popToRoot(self):
        while self.currentScreen != self.rootScreen:
            self.pop()

