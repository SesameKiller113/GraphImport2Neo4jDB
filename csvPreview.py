from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPixmap
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QFrame, QApplication
)


class PreviewWindow(QWidget):
    def __init__(self, data_frame):
        super().__init__()
        self.setWindowTitle("CSV Data Preview")
        self.setGeometry(400, 200, 1200, 800)

        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Left layout for draggable texts
        self.left_layout = QGridLayout()
        layout.addLayout(self.left_layout)

        # Add draggable labels
        self.column_labels = {}
        self.add_draggable_labels(data_frame.columns)

        # Add "Add Box" button
        self.add_box_button = QPushButton("Add Box")
        self.add_box_button.setFixedHeight(50)
        layout.addWidget(self.add_box_button)
        self.add_box_button.clicked.connect(self.add_box)

        # Frame for dynamically added boxes
        self.box_area = QVBoxLayout()
        layout.addLayout(self.box_area)

        # Track column assignments in each box
        self.box_contents = []

    def add_draggable_labels(self, columns):
        """Add draggable labels for each column name"""
        for index, column in enumerate(columns):
            label = DraggableLabel(column, index, self)
            self.column_labels[index] = label
            row, col = divmod(index, 3)
            self.left_layout.addWidget(label, row, col)

    def add_box(self):
        """Add a new box (container) for dropping columns"""
        box = DropBox(len(self.box_contents))
        self.box_area.addWidget(box)
        self.box_contents.append([])
        box.dropped.connect(self.update_box_contents)

    def restore_label(self, label):
        """Restore label to its original position if not dropped in any box"""
        if label.index in self.column_labels and label.isVisible() is False:
            label.show()

    def update_box_contents(self, box_index, column_name, label):
        """Add label text to the correct box and move the label there"""
        if box_index < len(self.box_contents):
            self.box_contents[box_index].append(column_name)
            label.setParent(self.sender())  # 将标签移到框里
            label.show()  # 确保标签可见
            self.sender().layout.addWidget(label)
            print(f"Box {box_index} contents: {self.box_contents[box_index]}")


class DraggableLabel(QLabel):
    def __init__(self, text, index, parent):
        super().__init__(text)
        self.index = index
        self.parent = parent
        self.setFixedSize(120, 40)
        self.setStyleSheet(
            "background-color: #0a0a0a; color: white; border: 1px solid #aaa; padding: 5px; border-radius: 5px;"
        )
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def mouseMoveEvent(self, event):
        """Handle dragging of the label"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)

            pixmap = self.grab()
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            result = drag.exec(Qt.DropAction.MoveAction)
            if result != Qt.DropAction.MoveAction:
                self.parent.restore_label(self)


class DropBox(QFrame):
    dropped = pyqtSignal(int, str, DraggableLabel)

    def __init__(self, box_index):
        super().__init__()
        self.box_index = box_index
        self.setFrameShape(QFrame.Shape.Box)
        self.setMinimumHeight(100)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #f9f9f9; border: 2px dashed #aaa;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        """Allow drag operation if text data is available"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event and add label to box"""
        text = event.mimeData().text()
        source_label = event.source()
        event.acceptProposedAction()
        self.dropped.emit(self.box_index, text, source_label)



