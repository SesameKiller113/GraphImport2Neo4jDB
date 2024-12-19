import sys
import pandas as pd
from PyQt6.QtGui import QIcon
from py2neo import Graph, Node
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
)


class CSVToNeo4jApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Import CSV to Neo4j")
        self.setWindowIcon(QIcon("icon.png"))
        self.initUI()

    def initUI(self):
        # Set window size and title
        self.setWindowTitle("CSV to Neo4j Importer")
        self.setGeometry(300, 300, 500, 150)

        # Create file path label
        self.label = QLabel("CSV File Path:", self)
        self.label.move(20, 20)

        # Create file path input field
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setGeometry(120, 20, 250, 25)

        # Create "Browse" button
        self.browse_btn = QPushButton("Browse", self)
        self.browse_btn.setGeometry(380, 20, 80, 25)
        self.browse_btn.clicked.connect(self.select_file)

        # Create "Import" button
        self.import_btn = QPushButton("Import to Neo4j", self)
        self.import_btn.setGeometry(200, 70, 120, 40)
        self.import_btn.clicked.connect(self.import_to_neo4j)

    def select_file(self):
        """Open a file dialog to select a CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            self.file_path_input.setText(file_path)

    def import_to_neo4j(self):
        """Import data from the selected CSV file to Neo4j"""
        file_path = self.file_path_input.text()
        if not file_path:
            QMessageBox.critical(self, "Error", "Please select a CSV file!")
            return

        try:
            # Load the CSV file into a DataFrame
            data = pd.read_csv(file_path)

        except Exception as e:
            # Show an error message if the import fails
            QMessageBox.critical(self, "Error", f"Failed to import data: {str(e)}")


def main():
    """Main function to initialize the application"""
    app = QApplication(sys.argv)
    main_window = CSVToNeo4jApp()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
