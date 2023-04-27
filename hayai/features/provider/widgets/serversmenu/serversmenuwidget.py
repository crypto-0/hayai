from typing import List, Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QWidget, QMenu, QWidgetAction
from ...provider import VideoServer

class QServersMenu(QMenu):
    def __init__(self,servers: List[VideoServer],parent: Optional[QWidget] = None):
        super().__init__(parent)

        menuTitleLabel: QLabel = QLabel("select server".upper())
        menuTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        widgetAction: QWidgetAction = QWidgetAction(self)
        widgetAction.setDefaultWidget(menuTitleLabel)
        self.addAction(widgetAction)
        for server in servers:
            action: QAction = QAction(server.name,self)
            action.setData(server)
            self.addAction(action)
            self.addSeparator()
        self.loadStylesheet()

    def loadStylesheet(self):
        with open("hayai/features/provider/widgets/serversmenu/serversmenuwidget.qss","r") as f:
            self.setStyleSheet(f.read())

