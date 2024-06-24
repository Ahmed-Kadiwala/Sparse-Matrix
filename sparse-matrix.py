import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class MatrixApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matrix Representation")
        self.setGeometry(100, 100, 800, 600)  # Initial larger size
        self.setMinimumSize(600, 400)  # Minimum size for the window
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout(self.main_widget)
        
        self.initUI()

    def initUI(self):
        self.row_label = QLabel("Number of rows:")
        self.row_input = QLineEdit()
        
        self.col_label = QLabel("Number of columns:")
        self.col_input = QLineEdit()
        
        self.create_button = QPushButton("Create Matrix")
        self.create_button.clicked.connect(self.create_matrix)

        self.matrix_layout = QTableWidget()
        self.matrix_layout.horizontalHeader().setVisible(False)
        self.matrix_layout.verticalHeader().setVisible(False)
        self.matrix_layout.setShowGrid(True)
        self.matrix_layout.setStyleSheet("QTableWidget { background-color: #ffffff; border: 1px solid #cccccc; }")
        
        self.submit_button = QPushButton("Submit Matrix")
        self.submit_button.clicked.connect(self.submit_matrix)
        self.submit_button.setVisible(False)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.row_label)
        input_layout.addWidget(self.row_input)
        input_layout.addWidget(self.col_label)
        input_layout.addWidget(self.col_input)
        input_layout.addWidget(self.create_button)
        
        self.layout.addLayout(input_layout)
        self.layout.addWidget(self.matrix_layout)
        self.layout.addWidget(self.submit_button)

    def create_matrix(self):
        try:
            rows = int(self.row_input.text())
            cols = int(self.col_input.text())
            if rows <= 0 or cols <= 0:
                raise ValueError("Rows and columns must be positive integers.")
        except ValueError as e:
            print(f"Input Error: {e}")
            return
        
        self.matrix_layout.clear()
        self.matrix_layout.setRowCount(rows)
        self.matrix_layout.setColumnCount(cols)
        
        cell_width = 50  # Adjust cell width and height as needed
        cell_height = 30
        self.matrix_layout.horizontalHeader().setDefaultSectionSize(cell_width)
        self.matrix_layout.verticalHeader().setDefaultSectionSize(cell_height)
        
        for i in range(rows):
            for j in range(cols):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignCenter)
                self.matrix_layout.setItem(i, j, item)
        
        self.submit_button.setVisible(True)

    def submit_matrix(self):
        rows = self.matrix_layout.rowCount()
        cols = self.matrix_layout.columnCount()
        
        matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                value = self.matrix_layout.item(i, j).text()
                try:
                    element = int(value) if value else 0
                except ValueError:
                    print(f"Invalid value at ({i}, {j}): {value}")
                    return
                row.append(element)
            matrix.append(row)
        
        self.display_non_zero_elements(matrix, rows, cols)
    
    def display_non_zero_elements(self, matrix, rows, cols):
        non_zero_window = QMainWindow(self)
        non_zero_window.setWindowTitle("Matrix Info")
        non_zero_window.setGeometry(200, 200, 600, 400)
        
        central_widget = QWidget()
        non_zero_window.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        matrix_info_label = QLabel(f"Matrix Size: {rows}x{cols}")
        layout.addWidget(matrix_info_label)
        
        non_zero_count = 0
        zero_count = 0
        
        table_widget = QTableWidget()
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Row", "Column", "Value"])
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    table_widget.insertRow(non_zero_count)
                    table_widget.setItem(non_zero_count, 0, QTableWidgetItem(str(i)))
                    table_widget.setItem(non_zero_count, 1, QTableWidgetItem(str(j)))
                    table_widget.setItem(non_zero_count, 2, QTableWidgetItem(str(matrix[i][j])))
                    non_zero_count += 1
                else:
                    zero_count += 1
        
        layout.addWidget(table_widget)
        
        info_label = QLabel(f"Non-zero elements: {non_zero_count}  |  Zero elements: {zero_count}")
        layout.addWidget(info_label)
        
        non_zero_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MatrixApp()
    
    # Apply stylesheet for improved appearance
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0; /* Light gray background */
        }
        QWidget {
            background-color: #f0f0f0; /* Light gray background */
        }
        QLabel {
            font-size: 16px; /* Larger font size for labels */
            color: #333333; /* Dark gray text color */
        }
        QLineEdit, QPushButton {
            font-size: 16px; /* Larger font size for input fields and buttons */
            padding: 8px; /* Increased padding */
            border: 1px solid #cccccc; /* Light gray border */
        }
        QPushButton {
            background-color: #4CAF50; /* Green background color */
            color: white; /* White text color */
            border: none; /* No border */
            padding: 10px 20px; /* Larger padding */
            text-align: center; /* Center text */
            text-decoration: none; /* No underline */
            display: inline-block; /* Display as inline block */
            font-size: 16px; /* Larger font size */
            margin: 4px 2px; /* Margin */
            cursor: pointer; /* Pointer cursor */
            border-radius: 8px; /* Rounded corners */
        }
        QTableWidget {
            font-size: 14px; /* Smaller font size for matrix cells */
            border: 1px solid #cccccc; /* Light gray border */
        }
        QTableWidget::item:selected {
            background-color: #0078d7; /* Blue selected background color */
            color: white; /* White text color */
        }
    """)
    
    mainWin.show()
    sys.exit(app.exec_())
