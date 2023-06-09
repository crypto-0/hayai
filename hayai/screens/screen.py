from abc import ABC, abstractmethod
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QFrame, QWidget
from collections import deque
from PyQt6.QtCore import pyqtSignal 

class QScreen(QFrame):
    created: pyqtSignal = pyqtSignal()
    started: pyqtSignal = pyqtSignal()
    stopped: pyqtSignal = pyqtSignal()
    destroyed: pyqtSignal = pyqtSignal()

    def __init__(self,parent: Optional[QWidget] = None):
        super().__init__(parent=parent)
        self._title: str = self.__class__.__name__
        self._navigation: Optional[IScreenNavigation] = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,title: str):
        if title:
            self._title = title

    @property
    def navigation(self):
        return self._navigation

    @navigation.setter
    def navigation(self,navigation):
        self._navigation = navigation

    def onCreated(self):
        self.created.emit()

    def onStart(self):
        self.started.emit()

    def onStop(self):
        self.stopped.emit()

    def onDestroy(self):
        self.destroyed.emit()

class IScreenNavigation(QObject):

    def __init__(self,parent: Optional[QObject]):
        super().__init__(parent=parent)

    @abstractmethod
    def push(self,screen: QScreen):
        raise NotImplemented

    @abstractmethod
    def pop(self):
        raise NotImplemented

    @abstractmethod
    def popToRoot(self):
        raise NotImplemented
