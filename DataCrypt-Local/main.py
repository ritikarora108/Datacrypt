import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication
from ui import DataCryptApp

def main():
    app = QApplication(sys.argv)
    # Create and show the main application window
    main_window = DataCryptApp()
    main_window.show()

    app.processEvents()  # Ensure the splash screen is rendered

    sys.exit(app.exec())

if __name__ == '__main__':
    main() 