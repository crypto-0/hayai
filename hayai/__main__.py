from PyQt6.QtWidgets import QApplication
from hayai.hayai import QHayai
import sys

def __hayai__():
    app = QApplication(sys.argv)

    hayai = QHayai()
    hayai.show()
    hayai.onStart()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    __hayai__()

