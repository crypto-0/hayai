from PyQt6.QtCore import QEvent,QPointF, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from .titlebarbuttons import SvgTitleBarButton

from .titlebarbuttons import (CloseButton, MaximizeButton, MinimizeButton,PngTitleBarButton,
                                 TitleBarButton)


class QTitleBar(QFrame):
    """ Title bar with minimize, maximum and close button """

    def __init__(self, parent):
        super().__init__(parent)
        self.oldPosition: int = 0
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self.hBoxLayout = QHBoxLayout(self)
        self._isDoubleClickEnabled = True

        self.resize(200, 32)
        self.setFixedHeight(32)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft) #pyright: ignore
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.minBtn)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignmentFlag.AlignRight)

        # connect signal to slot
        window: QWidget = self.window()
        self.minBtn.clicked.connect(window.showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.closeBtn.clicked.connect(self.closeWindow)

        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.Type.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False

        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        """ Toggles the maximization state of the window """
        if event.button() != Qt.MouseButton.LeftButton or not self._isDoubleClickEnabled:
            return

        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if  not self.canDrag(e.pos()):
            return
        delta = QPointF(e.globalPosition() - self.oldPosition)
        window = self.window()
        window.move(int(window.x() + delta.x()), int(window.y() + delta.y()))
        self.oldPosition = e.globalPosition()


    def mousePressEvent(self, e):
        if not self.canDrag(e.pos()):
            return
        self.oldPosition = e.globalPosition()

    def __toggleMaxState(self):
        """ Toggles the maximization state of the window and change icon """
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def _isDragRegion(self, pos):
        """ Check whether the position belongs to the area where dragging is allowed """
        width = 0
        
        for button in self.findChildren(TitleBarButton):
            if isinstance(button,TitleBarButton) and  button.isVisible():
                width += button.width()

        return 0 < pos.x() < self.width() - width

    def _hasButtonPressed(self):
        """ whether any button is pressed """
        for btn in self.findChildren(TitleBarButton):
            if isinstance(btn,TitleBarButton) and  btn.isPressed():
                return True
        return False


    def canDrag(self, pos):
        """ whether the position is draggable """
        return self._isDragRegion(pos) and not self._hasButtonPressed()

    def setDoubleClickEnabled(self, isEnabled):
        """ whether to switch window maximization status when double clicked
        Parameters
        ----------
        isEnabled: bool
            whether to enable double click
        """
        self._isDoubleClickEnabled = isEnabled

    def closeWindow(self):
        self.window().close()


class QStandardTitleBar(QTitleBar):
    """ Title bar with icon and title """
    backButtonClicked: pyqtSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.backButton: PngTitleBarButton = PngTitleBarButton("hayai/features/widgets/titlebar/assets/left.png",self)
        self.backButton.setFixedSize(20,20)
        self.hBoxLayout.insertSpacing(0, 5)
        self.hBoxLayout.insertWidget(0, self.backButton, 0, Qt.AlignmentFlag.AlignLeft)
        self.titleLabel = QLabel("hayai",self)
        self.titleLabel.setStyleSheet(" QLabel{ background: transparent;font: 16px 'Segoe UI'; padding: 0 4px;color: #a1acbc } ")

        self.backButton.clicked.connect(self.backButtonClicked)
        self.window().windowTitleChanged.connect(self.setTitle)

        self.hBoxLayout.insertWidget(1, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

