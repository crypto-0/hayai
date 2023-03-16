from PyQt5.QtWidgets import QApplication
from hayai.screens import QWindow
import sys

def __hayai__():
    app = QApplication(sys.argv)
    window = QWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    __hayai__()

