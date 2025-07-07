from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QFileDialog, QLabel, QHBoxLayout, QDialogButtonBox, QInputDialog, QSpacerItem, QSizePolicy, QDialog
from PyQt6.QtGui import QFont, QClipboard, QPixmap 
from PyQt6.QtCore import Qt, QTimer
import sys
import os
from key_manager import generate_key_pair
from encryptor import encrypt_file
from decryptor import decrypt_file

class DataCryptApp(QWidget):
    def __init__(self):
        super().__init__()
        # Set the message box style globally
        self.setStyleSheet("""
            QMessageBox {
                background-color: #2C2F33;
                color: #FFFFFF;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 14px;
                min-width: 300px;
                min-height: 50px;
            }
            QMessageBox QPushButton {
                width: 100px;
                padding: 10px 20px;
                margin: 5px 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QMessageBox QPushButton[text="OK"], QMessageBox QPushButton[text="&Yes"] {
                background-color: #4CAF50;
                color: white;
                border: none;
            }
            QMessageBox QPushButton[text="OK"]:hover, QMessageBox QPushButton[text="&Yes"]:hover {
                background-color: #45a049;
            }
            QMessageBox QPushButton[text="&No"], QMessageBox QPushButton[text="Cancel"] {
                background-color: #FF5733;
                color: white;
                border: none;
            }
            QMessageBox QPushButton[text="&No"]:hover, QMessageBox QPushButton[text="Cancel"]:hover {
                background-color: #ff4122;
            }
            QMessageBox QDialogButtonBox {
                button-layout: 2;  /* Center the buttons */
            }
        """)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Datacrypt - Secure File Encryption")
        self.setGeometry(400, 150, 600, 400)
        self.setStyleSheet("background-color: #23272A; color: #FFFFFF;")
        
        layout = QVBoxLayout()
        
        # Add the logo at the header
        logo_label = QLabel(self)
        # Use sys._MEIPASS if running in a bundled executable.
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "logo.png")
        print(f"Loading logo from: {logo_path}")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            print(f"Logo file not found at: {logo_path}")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Add a title below the logo
        title = QLabel("🔒 DataCrypt - Secure File Storage", self)
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        self.file_label = QLabel("No file selected", self)
        self.file_label.setWordWrap(True)
        self.file_label.setStyleSheet("color: red;")
        layout.addWidget(self.file_label)
        
        self.public_key_label = QLabel("", self)
        self.public_key_label.setWordWrap(True)
        self.public_key_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.public_key_label)
        
        select_button_style = (
            "QPushButton {"
            "    background-color: #FF5733;"
            "    color: white;"
            "    border-radius: 10px;"
            "    padding: 12px;"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: #E04E2A;"
            "}"
        )
        
        encrypt_button_style = (
            "QPushButton {"
            "    background-color: #33B5E5;"
            "    color: white;"
            "    border-radius: 10px;"
            "    padding: 12px;"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: #2A9AC6;"
            "}"
            "QPushButton:disabled {"
            "    background-color: #7FB8D4;"
            "    color: #CCCCCC;"
            "}"
        )
        
        decrypt_button_style = (
            "QPushButton {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-radius: 10px;"
            "    padding: 12px;"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: #449D48;"
            "}"
            "QPushButton:disabled {"
            "    background-color: #8FBC91;"
            "    color: #CCCCCC;"
            "}"
        )
        
        generate_keys_button_style = (
            "QPushButton {"
            "    background-color: #FFC107;"
            "    color: white;"
            "    border-radius: 10px;"
            "    padding: 12px;"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: #E0A106;"
            "}"
        )
        
        # Create a horizontal layout for the select and deselect buttons
        file_selection_layout = QHBoxLayout()
        
        self.select_button = QPushButton("📂 Select File", self)
        self.select_button.setStyleSheet(select_button_style)
        self.select_button.clicked.connect(self.select_file)
        file_selection_layout.addWidget(self.select_button)
        
        deselect_button_style = (
            "QPushButton {"
            "    background-color: #808080;"
            "    color: white;"
            "    border-radius: 10px;"
            "    padding: 12px;"
            "    font-size: 15px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: #666666;"
            "}"
            "QPushButton:disabled {"
            "    background-color: #CCCCCC;"
            "    color: #808080;"
            "}"
        )
        
        self.deselect_button = QPushButton("❌ Remove File", self)
        self.deselect_button.setStyleSheet(deselect_button_style)
        self.deselect_button.clicked.connect(self.deselect_file)
        self.deselect_button.setEnabled(False)  # Initially disabled
        file_selection_layout.addWidget(self.deselect_button)
        
        layout.addLayout(file_selection_layout)
        
        # Create a horizontal layout for the encrypt and decrypt buttons
        button_layout = QHBoxLayout()
        
        self.encrypt_button = QPushButton("🔐 Encrypt File", self)
        self.encrypt_button.setStyleSheet(encrypt_button_style)
        self.encrypt_button.clicked.connect(self.encrypt_file)
        self.encrypt_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.encrypt_button)
        
        self.decrypt_button = QPushButton("🔓 Decrypt File", self)
        self.decrypt_button.setStyleSheet(decrypt_button_style)
        self.decrypt_button.clicked.connect(self.decrypt_file)
        self.decrypt_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.decrypt_button)
        
        layout.addLayout(button_layout)
        
        # Add the generate keys button and copy key button in sequence
        self.generate_keys_button = QPushButton("🔑 Generate ECDH Keys", self)
        self.generate_keys_button.setStyleSheet(generate_keys_button_style)
        self.generate_keys_button.clicked.connect(self.generate_keys)
        
        # Use the current file location to form paths for keys.
        keys_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys")
        public_key_path = os.path.join(keys_dir, "public_key.pem")
        private_key_path = os.path.join(keys_dir, "private_key.pem")
        print(f"Checking for public key at: {os.path.abspath(public_key_path)}")
        print(f"Checking for private key at: {os.path.abspath(private_key_path)}")
        
        # Check if keys already exist and disable the button if they do
        if os.path.exists(public_key_path) and os.path.exists(private_key_path):
            self.generate_keys_button.setEnabled(False)
            # Change the button style to make it more faded
            self.generate_keys_button.setStyleSheet(
                "QPushButton {"
                "    background-color: #B0B0B0;"  # Faded color
                "    color: #FFFFFF;"
                "    border-radius: 10px;"
                "    padding: 12px;"
                "    font-size: 15px;"
                "    font-weight: bold;"
                "}"
                "QPushButton:hover {"
                "    background-color: #A0A0A0;"  # Slightly darker on hover
                "}"
            )
        
        layout.addWidget(self.generate_keys_button)
        
        self.copy_key_button = QPushButton("📋 Show Public Key", self)
        self.copy_key_button.setStyleSheet(select_button_style)
        self.copy_key_button.clicked.connect(self.copy_public_key)
        layout.addWidget(self.copy_key_button)
        
        # Create a QLabel for the hint message
        self.hint_label = QLabel("", self)
        self.hint_label.setStyleSheet("color: green; font-size: 14px;")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setVisible(False)  # Initially hidden
        layout.addWidget(self.hint_label)  # Add it to the main layout
        
        self.setLayout(layout)
    
    def select_file(self):
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)", options=options)
        if file_name:
            self.file_label.setText(f"Selected: {file_name}")
            self.file_label.setStyleSheet("color: green;")
            self.selected_file = file_name
            self.encrypt_button.setEnabled(True)
            self.decrypt_button.setEnabled(True)
            self.deselect_button.setEnabled(True)  # Enable deselect button
        else:
            self.deselect_file()
    
    def deselect_file(self):
        """Clear the selected file and reset UI state"""
        self.file_label.setText("No file selected")
        self.file_label.setStyleSheet("color: red;")
        self.selected_file = None
        self.encrypt_button.setEnabled(False)
        self.decrypt_button.setEnabled(False)
        self.deselect_button.setEnabled(False)
    
    def encrypt_file(self):
        if hasattr(self, 'selected_file'):
            # Create the input dialog
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Recipient Public Key")
            dialog.setLabelText("Enter recipient's public key:")
            dialog.setFixedSize(400, 200)  # Set the desired size

            # Execute the dialog and get the input
            if dialog.exec() == QInputDialog.DialogCode.Accepted:
                public_key = dialog.textValue()
                if public_key:
                    # Proceed with file encryption using the provided public key
                    try:
                        encrypt_file(self.selected_file, public_key)
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Success")
                        msg.setText("File encrypted successfully!")
                        msg.setIcon(QMessageBox.Icon.Information)
                        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        reply = msg.exec()
                        
                        if reply == QMessageBox.StandardButton.Ok:
                            self.deselect_file()
                    except Exception as e:
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Error")
                        msg.setText(f"Encryption failed: {str(e)}")
                        msg.setIcon(QMessageBox.Icon.Warning)
                        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                        msg.exec()
                else:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Cancelled")
                    msg.setText("Encryption cancelled or no key provided.")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Warning")
            msg.setText("No file selected!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
    
    def decrypt_file(self):
        if hasattr(self, 'selected_file'):
            encrypted_file = self.selected_file
        else:
            options = QFileDialog.Option.ReadOnly
            encrypted_file, _ = QFileDialog.getOpenFileName(
                self,
                "Select Encrypted File",
                "",
                "Encrypted Files (*.enc)",
                options=options,
            )
            if not encrypted_file:
                msg = QMessageBox(self)
                msg.setWindowTitle("Warning")
                msg.setText("No file selected!")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                return

        key_file = encrypted_file.rsplit(".", 1)[0] + ".key"
        private_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys", "private_key.pem")

        if not os.path.exists(private_key_path):
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("ECDH keys not found. Please generate keys first.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        if not os.path.exists(key_file):
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(f"Key file not found: {key_file}")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        # Prompt for sender's public key
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Sender Public Key")
        dialog.setLabelText("Enter sender's public key:")
        dialog.setFixedSize(400, 200)
        if dialog.exec() == QInputDialog.DialogCode.Accepted:
            sender_public_key = dialog.textValue()
            if sender_public_key:
                try:
                    decrypt_file(encrypted_file, key_file, private_key_path, sender_public_key)
                except ValueError as e:
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Error")
                    msg.setText(f"Failed to decrypt: {str(e)}")
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
                    return
                msg = QMessageBox(self)
                msg.setWindowTitle("Success")
                msg.setText("File decrypted successfully!")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                reply = msg.exec()
                if reply == QMessageBox.StandardButton.Ok:
                    self.deselect_file()
            else:
                msg = QMessageBox(self)
                msg.setWindowTitle("Cancelled")
                msg.setText("Decryption cancelled or no key provided.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle("Cancelled")
            msg.setText("Decryption cancelled.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
    
    def generate_keys(self):
        if generate_key_pair():
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText("ECDH key pair generated successfully!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

            # Disable the button after keys are generated
            self.generate_keys_button.setEnabled(False)
            # Change the button style to make it more faded
            self.generate_keys_button.setStyleSheet(
                "QPushButton {"
                "    background-color: #B0B0B0;"  # Faded color
                "    color: #FFFFFF;"
                "    border-radius: 10px;"
                "    padding: 12px;"
                "    font-size: 15px;"
                "    font-weight: bold;"
                "}"
                "QPushButton:hover {"
                "    background-color: #A0A0A0;"  # Slightly darker on hover
                "}"
            )
    
    def copy_public_key(self):
        try:
            public_key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys", "public_key.pem")
            with open(public_key_path, "r") as f:
                pem = f.read()

            # Extract only the base64 key content (remove header/footer and whitespace)
            lines = pem.strip().splitlines()
            key_lines = [line for line in lines if not line.startswith('-----')]
            public_key = ''.join(key_lines)

            # Create a custom dialog
            dialog = QDialog(self)
            # dialog.setWindowTitle("Public Key")
            dialog.setFixedWidth(420)  # Set a smaller width for the dialog
            layout = QVBoxLayout(dialog)

            # Header label (navbar style)
            header = QLabel("Public Key")
            header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            header.setStyleSheet("background-color: #23272A; color: #33B5E5; padding: 10px;")
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(header)

            # Public key display (only the base64 key)
            key_label = QLabel(public_key)
            key_label.setStyleSheet("color: #FFFFFF; background-color: #2C2F33; padding: 10px;")
            key_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            key_label.setWordWrap(True)
            key_label.setFixedWidth(380)  # Set a smaller width for the label
            layout.addWidget(key_label)

            # Copy button
            button_layout = QHBoxLayout()
            copy_button = QPushButton("Copy")
            button_layout.addStretch()
            button_layout.addWidget(copy_button)
            button_layout.addStretch()
            layout.addLayout(button_layout)

            # Feedback label for copy action (reserve space with fixed height)
            copied_label = QLabel("")
            copied_label.setStyleSheet("color: green; font-size: 14px;")
            copied_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            copied_label.setFixedHeight(20)  # Reserve space so layout doesn't shift
            layout.addWidget(copied_label)

            def copy_to_clipboard():
                QApplication.clipboard().setText(public_key)
                copied_label.setText("COPIED")
                timer = QTimer(dialog)
                timer.setSingleShot(True)
                def clear_label():
                    if copied_label:
                        copied_label.setText("")
                timer.timeout.connect(clear_label)
                timer.start(2000)

            copy_button.clicked.connect(copy_to_clipboard)

            dialog.setLayout(layout)
            dialog.exec()

        except FileNotFoundError:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText("Public key file not found. Please generate keys first.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def closeEvent(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Exit")
        msg.setText("Are you sure you want to quit?")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        # Center the window relative to the main window
        msg.setStyleSheet(msg.styleSheet() + """
            QMessageBox {
                min-width: 400px;
                min-height: 150px;
            }
        """)
        
        # Ensure Yes is on the left and No on the right
        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        no_button = msg.button(QMessageBox.StandardButton.No)
        
        # Adjust button order
        button_box = msg.findChild(QDialogButtonBox)
        if button_box:
            button_box.setCenterButtons(True)
            layout = button_box.layout()
            layout.setSpacing(20)  # Add space between buttons
        
        reply = msg.exec()
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    
    # Create and display the splash screen
    try:
        print("Welcome the UI has started")
    except Exception:
        pass

    app.processEvents()  # Force the splash screen to render immediately.
    
    # Create the main application window
    main_window = DataCryptApp()
    main_window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()