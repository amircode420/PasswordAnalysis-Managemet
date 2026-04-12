# THIS IS FOR THE VAULT INTERFACE

from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem
)

from PyQt5.QtCore import Qt
import sqlite3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

class VaultInterface(QDialog):
    def __init__(self, master_password, parent = None):
        super().__init__(parent)
        self.master_password = master_password
        self.setWindowTitle("Password Vault")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: grey;")

        layout = QVBoxLayout()

        main_title = QLabel("Password Vault")
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setStyleSheet(f'''
                    QLabel{{
                        font-size: 20px;
                        color: white;
                        font-weight: bold;
                        font-style: italic;
                    }}''')
        layout.addWidget(main_title)
        layout.addStretch()

        # PASSWORD TABLE
        self.password_table = QTableWidget()
        self.password_table.setStyleSheet(f'''
                    QTableWidget{{
                        background-color: white;
                        color: black;
                    }}
                    QHeaderView::section{{
                        background-color: cyan;
                        border: 1px solid black;          
                    }}
                    QTableCornerButton::section{{
                        background-color: cyan;
                    }}
                    ''')
        self.password_table.setColumnCount(3)
        self.password_table.setHorizontalHeaderLabels(["Service", "Username/Email", "Password"]) # PASSWORD IS ENCRYPTED WHEN LOCKED, DECRYPTED WITH MASTER PASSWORD
        #self.password_table.setCornerButtonEnabled(False)
        # TO MAKE THE TABLE LABEL STRETCH OVER THE TABLE
        header = self.password_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        layout.addWidget(self.password_table)
        layout.addStretch()

        self.load_pass()

        # ADD CREDENTIALS
        creds_btn = QPushButton("Add Credentials")
        creds_btn.setStyleSheet(f'''
                    QPushButton{{
                        background-color: white;
                        color: black;
                        font-size: 14px;
                        padding: 5px;
                    }}
                    QPushButton:hover{{
                        background-color: green;
                    }}''')
        creds_btn.clicked.connect(self.add_btn)
        layout.addWidget(creds_btn)
        layout.addStretch()

        self.setLayout(layout)

    # ADDDIND CREDENTIALS WINDOW    
    def add_btn(self):
        print("this works")
        self.new_dialog = QDialog(self)
        self.new_dialog.setWindowTitle("Add Credentials")
        self.new_dialog.setFixedSize(400, 300)
        self.new_dialog.setStyleSheet("background-color: grey;")

        layout = QVBoxLayout()

        # SERVICE LABEL AND INPUT
        service_label = QLabel("Service:")
        service_label.setStyleSheet("color: white; font-weight: bold; font-size: 15px")
        layout.addWidget(service_label)
        
        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("Eg. FaceBook, Instragram..")
        self.service_input.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        layout.addWidget(self.service_input)
        layout.addStretch()
        
        # USER LABEL AND INPUT
        user_label = QLabel("Username/Emails:")
        user_label.setStyleSheet("color: white; font-weight: bold; font-size: 15px")
        layout.addWidget(user_label)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter Username or Email...")
        self.user_input.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        layout.addWidget(self.user_input)
        layout.addStretch()

        #PASSWORD LABEL AND INPUT
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: white; font-weight: bold; font-size: 15px")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Your Password...")
        self.password_input.setStyleSheet("background-color: white; color: black; font-size: 15px;")
        layout.addWidget(self.password_input)
        layout.addStretch()

        btn_layout = QHBoxLayout()

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_func)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)
        self.new_dialog.setLayout(layout)
        self.new_dialog.exec_()
    
    # SAVING THE CREDENTIALS FUNCTION
    def save_func(self):
        service = self.service_input.text()
        username = self.user_input.text()
        password = self.password_input.text()
        if not service or not password:
            QMessageBox.warning(self, "Error", "Please enter all information")
            return
        
        try:
            # ENCRYPTING PASSWORD
            encrypted_pass = self.encrypt_password(password)
            if encrypted_pass:
                conn = sqlite3.connect("vault.db")
                cur = conn.cursor()
                cur.execute('''
                    INSERT INTO Passwords (service, user_name, password) VALUEs (?, ?, ?)''', (service, username, encrypted_pass))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Success", "Credentials Added")
                # CLOSE AFTER SAVE
                self.new_dialog.accept()
                self.load_pass()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
    
    # ENCRYPTING PASSWORDS USING MASTER PASSWORD AS KEY
    def encrypt_password(self, password):
        try:
            salt = b'vault_encrypt_salt' # FIXED salt for key derivation
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
            f = Fernet(key)
            return f.encrypt(password.encode()).decode()
        except Exception as e:
            print(e)
    
    # LOADING AND DECRYPTING PASSWORDS FROM THE DATABASE TO THE TABLE
    def load_pass(self):
        try:
            conn = sqlite3.connect("vault.db")
            cur = conn.cursor()

            cur.execute("SELECT service, user_name, password FROM Passwords")
            passwords = cur.fetchall()
            conn.close()

            # SETTING THE TABLE ROW COUNT
            self.password_table.setRowCount(len(passwords))

            # POPULATE THE TABLE WITH THE DATA
            for row, (service, user_name, encrypted_pass) in enumerate(passwords):
                decrypted_pass = self.decrypt_password(encrypted_pass)

                # ADDING TO THE TABLE THE VALUES
                self.password_table.setItem(row, 0, QTableWidgetItem(service))
                self.password_table.setItem(row, 1, QTableWidgetItem(user_name))
                self.password_table.setItem(row, 2, QTableWidgetItem(decrypted_pass))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"failed to load credentials: {str(e)}")


    def decrypt_password(self, encrypted_password):
        try:
            salt = b'vault_encrypt_salt' # FIXED salt for key derivation
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.master_password.encode()))
            f = Fernet(key)
            return f.decrypt(encrypted_password.encode()).decode()
        except Exception as e:
            print(e)