import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QLineEdit,
                             QFrame, QGroupBox, QGridLayout, QMessageBox, QSplitter, QFileDialog,
                             QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from sales_analyzer import SalesAnalyzer
import pandas as pd

class SalesGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Analysis System - Sampath Food City")
        self.setGeometry(100, 100, 1500, 800)
        self.analyzer = SalesAnalyzer("Sales_data.csv")
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("Sales Analysis System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)

        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        file_frame = QFrame()
        file_layout = QHBoxLayout(file_frame)
        self.file_label = QLabel("Data File:")
        self.file_input = QLineEdit("sample_sales_data.csv")
        self.file_input.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)
        top_layout.addWidget(file_frame)

        filter_group = QGroupBox("Filters")
        filter_layout = QGridLayout(filter_group)

        self.branch_label = QLabel("Branch ID:")
        self.branch_input = QLineEdit()
        self.branch_input.setPlaceholderText("e.g., BR001 (optional)")
        filter_layout.addWidget(self.branch_label, 0, 0)
        filter_layout.addWidget(self.branch_input, 0, 1)

        self.year_label = QLabel("Year:")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g., 2023 (optional)")
        filter_layout.addWidget(self.year_label, 1, 0)
        filter_layout.addWidget(self.year_input, 1, 1)

        self.month_label = QLabel("Month:")
        self.month_input = QLineEdit()
        self.month_input.setPlaceholderText("e.g., 1 (optional)")
        filter_layout.addWidget(self.month_label, 2, 0)
        filter_layout.addWidget(self.month_input, 2, 1)

        top_layout.addWidget(filter_group)

        button_group = QGroupBox("Analysis Types")
        button_layout = QHBoxLayout(button_group)

        self.monthly_button = QPushButton("Monthly Sales")
        self.monthly_button.clicked.connect(lambda: self.run_analysis("monthly_sales"))
        button_layout.addWidget(self.monthly_button)

        self.price_button = QPushButton("Product Price")
        self.price_button.clicked.connect(lambda: self.run_analysis("price_analysis"))
        button_layout.addWidget(self.price_button)

        self.weekly_button = QPushButton("Weekly Sales")
        self.weekly_button.clicked.connect(lambda: self.run_analysis("weekly_sales"))
        button_layout.addWidget(self.weekly_button)

        self.preference_button = QPushButton("Product Preference")
        self.preference_button.clicked.connect(lambda: self.run_analysis("product_preference"))
        button_layout.addWidget(self.preference_button)

        self.distribution_button = QPushButton("Sales Distribution")
        self.distribution_button.clicked.connect(lambda: self.run_analysis("total_sales_distribution"))
        button_layout.addWidget(self.distribution_button)

        top_layout.addWidget(button_group)
        splitter.addWidget(top_widget)

        results_group = QGroupBox("Analysis Results")
        results_layout = QVBoxLayout(results_group)
        self.results_text_display = QTextEdit()
        self.results_text_display.setReadOnly(True)
        results_layout.addWidget(self.results_text_display)
        splitter.addWidget(results_group)

    def apply_styles(self):
        font = QFont("Arial", 10)
        self.setFont(font)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.WindowText, QColor("#333333"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#f5f5f5"))
        palette.setColor(QPalette.ToolTipBase, QColor("#ffffea"))
        palette.setColor(QPalette.ToolTipText, QColor("#333333"))
        palette.setColor(QPalette.Text, QColor("#333333"))
        palette.setColor(QPalette.Button, QColor("#4CAF50"))
        palette.setColor(QPalette.ButtonText, QColor("white"))
        palette.setColor(QPalette.BrightText, QColor("red"))
        palette.setColor(QPalette.Link, QColor("#2a82da"))
        palette.setColor(QPalette.Highlight, QColor("#3daee9"))
        palette.setColor(QPalette.HighlightedText, QColor("#000000"))
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            #title {
                font-size: 24px;
                font-weight: bold;
                color: #1a1a1a;
                padding: 10px;
            }
            QGroupBox {
                font-weight: bold;
                margin-top: 10px;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #e0e0e0;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                color: #333333;
            }
        """)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Sales Data CSV", "", "CSV Files (*.csv)")
        if file_name:
            self.file_input.setText(file_name)
            try:
                self.analyzer = SalesAnalyzer(file_name)
                QMessageBox.information(self, "Data Loaded", f"Successfully loaded data from {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error Loading Data", f"Failed to load data: {str(e)}")

    def run_analysis(self, analysis_type):
        branch_id = self.branch_input.text() if self.branch_input.text() else None
        year = int(self.year_input.text()) if self.year_input.text() else None
        month = int(self.month_input.text()) if self.month_input.text() else None

        try:
            result = pd.DataFrame()
            title = ""

            if analysis_type == "monthly_sales":
                result = self.analyzer.monthly_sales_analysis(branch_id, year, month)
                title = "Monthly Sales Analysis"
            elif analysis_type == "price_analysis":
                result = self.analyzer.price_analysis_by_product(branch_id, year, month)
                title = "Product Price Analysis"
            elif analysis_type == "weekly_sales":
                result = self.analyzer.weekly_sales_analysis(branch_id, year)
                title = "Weekly Sales Analysis"
            elif analysis_type == "product_preference":
                result = self.analyzer.product_preference_analysis(branch_id, year, month)
                title = "Product Preference Analysis"
            elif analysis_type == "total_sales_distribution":
                result = self.analyzer.total_sales_distribution_analysis(branch_id, year, month)
                title = "Total Sales Distribution Analysis"

            self.display_results(result, title)

        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", f"An error occurred during analysis: {str(e)}")

    def display_results(self, df, title):
        if df.empty:
            message = "No data found for the selected filters."
            self.results_text_display.setText(message)
            QMessageBox.information(self, "No Data", message)
            return

        # Format DataFrame to a string with increased column width
        formatted_df_string = df.to_string(
            index=False,
            justify='left',
            max_rows=None,
            max_colwidth=None,
            col_space=30 # Increased col_space further for better column width
        )

        # Add a clear header for the analysis type
        header = f"--- {title} ---\n"

        # Calculate a more accurate dashed line length based on the first line of the formatted DataFrame
        # This will be the header line of the DataFrame output by to_string()
        if not df.empty:
            header_line_from_df = formatted_df_string.split('\n')[0]
            dashed_line_length = len(header_line_from_df)
            dashed_line = "-" * dashed_line_length
        else:
            dashed_line = "-" * 50 # Default length if no data

        # Combine header, dashed lines, and the formatted DataFrame string
        full_output = header + dashed_line + "\n" + formatted_df_string + "\n" + dashed_line

        self.results_text_display.setText(full_output)

        # Update the group box title to show current analysis
        results_group = self.results_text_display.parent()
        if hasattr(results_group, 'setTitle'):
            results_group.setTitle(f"Analysis Results - {title}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SalesGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()