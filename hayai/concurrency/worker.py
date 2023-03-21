import traceback, sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QRunnable
import sys

class WorkerSignals(QObject):
    finished: pyqtSignal = pyqtSignal()
    error: pyqtSignal = pyqtSignal(tuple)
    result: pyqtSignal = pyqtSignal(object)
    progress: pyqtSignal = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        #self.signals.destroyed.connect(self.exit)
        self.kwargs['progressSignal'] = self.signals.progress
        self.cancel = False

    @pyqtSlot()
    def run(self):
        try:
            result: object = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if not self.cancel:
                self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
            self.signals.deleteLater()

    def exit(self,member: str):
        sys.exit()

    def cancelResult(self):
        self.cancel = True
