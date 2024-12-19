import json
import sys
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox
)
from importGraph import startImport

class ImportPageWindow(QWidget):
    def __init__(self, box_contents):
        super().__init__()
        self.preview_window = None
        self.box_contents = box_contents
        self.current_index = 0
        self.node_name_input = None  # To store the node name input field
        self.node_relation_input = None  # To store the node relation input
        self.property_key_checkboxes = {}  # Store checkboxes for property keys
        self.setWindowTitle("Import CSV to Neo4j")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(400, 200, 1200, 800)

        # Main vertical layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setSpacing(20)

        # Dictionary to store input fields for the current set of variables
        self.current_inputs = {}

        # "Next Node" button
        self.add_box_button = QPushButton("Next Node")
        self.add_box_button.setFixedHeight(50)
        self.add_box_button.setFixedWidth(120)
        self.add_box_button.setStyleSheet("background-color: #0a6df0; color: white;")
        self.main_layout.addWidget(self.add_box_button, 0, Qt.AlignmentFlag.AlignRight)
        self.add_box_button.clicked.connect(self.next_node)

        # Display the first content set
        self.display_box_content()

        # Store input data for json file
        self.data = []

    def clear_current_fields(self):
        def clear_layout(layout):
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item and item.widget() and item.widget() != self.add_box_button:
                    widget = item.widget()
                    widget.setParent(None)
                    widget.deleteLater()
                    layout.takeAt(i)
                elif item and item.layout():
                    clear_layout(item.layout())
                    layout.removeItem(item)

        clear_layout(self.main_layout)
        self.current_inputs.clear()
        self.property_key_checkboxes.clear()

    def display_box_content(self):
        self.clear_current_fields()

        if 0 <= self.current_index < len(self.box_contents):
            current_content = self.box_contents[self.current_index]
            if len(current_content) == 0:
                self.next_node()
                return

            node_layout = QVBoxLayout()
            node_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Node Name Label and Input Field
            node_name = QLabel("Node Name:")
            node_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
            node_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            node_layout.addWidget(node_name)

            self.node_name_input = QLineEdit()
            self.node_name_input.setPlaceholderText("Enter Node Name")
            self.node_name_input.setFixedWidth(400)
            self.node_name_input.setFixedHeight(50)
            self.node_name_input.setStyleSheet(
                "font-size: 20px; padding: 10px; border: 2px solid #aaa; border-radius: 8px;"
            )
            node_layout.addWidget(self.node_name_input)

            if self.current_index < len(self.box_contents) - 1:
                self.node_relation_input = QLineEdit()
                self.node_relation_input.setPlaceholderText("Enter Relation")
                self.node_relation_input.setFixedWidth(400)
                self.node_relation_input.setFixedHeight(50)
                self.node_relation_input.setStyleSheet(
                    "font-size: 20px; padding: 10px; border: 2px solid #aaa; border-radius: 8px;"
                )
                node_layout.addWidget(self.node_relation_input)

            self.main_layout.insertLayout(0, node_layout)

            for var_name in current_content:
                h_layout = QHBoxLayout()
                h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

                var_label = QLabel(f"{var_name}:")
                var_label.setStyleSheet("font-size: 16px; font-weight: bold;")

                line_edit_1 = QLineEdit()
                line_edit_1.setPlaceholderText("Enter English Variable Name")
                line_edit_1.setMinimumHeight(30)
                line_edit_1.setFixedWidth(300)

                checkbox = QCheckBox("Property Key")
                checkbox.setFixedHeight(30)

                h_layout.addWidget(var_label)
                h_layout.addWidget(line_edit_1)
                h_layout.addWidget(checkbox)
                h_layout.addStretch()

                self.main_layout.insertLayout(self.main_layout.count() - 1, h_layout)

                self.current_inputs[var_name] = line_edit_1
                self.property_key_checkboxes[var_name] = checkbox
        else:
            self.close()

    def collect_input_data(self):
        data = {}
        if self.node_name_input:
            data["Node Name"] = self.node_name_input.text().strip()
        if self.current_index < len(self.box_contents) - 1 and self.node_relation_input:
            data["Relation"] = self.node_relation_input.text().strip()

        for var_name, line_edit in self.current_inputs.items():
            value = line_edit.text().strip()
            if self.property_key_checkboxes[var_name].isChecked():
                data["Property Key"] = var_name
            data[var_name] = value

        return data

    def next_node(self):
        current_data = self.collect_input_data()
        self.data.append(current_data)
        print("Current data:", current_data)

        self.current_index += 1
        if self.current_index < len(self.box_contents):
            self.display_box_content()
        else:
            with open("data_cache.json", "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            startImport()
            self.close()

