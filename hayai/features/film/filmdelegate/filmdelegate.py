from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtWidgets import QComboBox, QItemDelegate, QStyleOption, QStyledItemDelegate, QWidget
from typing import Optional

class QFilmDelegate(QItemDelegate):

    def __init__(self, parent ) -> None:
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: 'QStyleOption', index: QModelIndex) -> QWidget:
        editor = QComboBox()
        print("here in ed")
        return editor

    def setEditorData(self, editor,index) -> None:
        value = index.model().data(index,Qt.UserRole)
        editor.setCurrentIndex(value)
        
        
