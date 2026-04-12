# PASSWORD VAULT LOGIC

from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PyQt5.QtCore import Qt
import sqlite3
import os
import hashlib
import secrets
from core.vault_interface import VaultInterface

class PasswordVault(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        if self.vault_check():
            self.vault_login()
        else:
            self.vault_setup()

    # TO CHECK IF VAULT HAS BEEN SETUP
    def vault_check(self):
        if not os.path.exists("vault.db"):
            return False
        
        try:
            conn = sqlite3.connect("vault.db")
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) from PasswordDatabase")
            count = cur.fetchone()[0]
            conn.close()
            return count > 0    
        except:
            False
    # MAIN SETUP IF THE VAULT DOESN'T EXIST
    def vault_setup(self):
        self.setWindowTitle("Encrypted Vault - Setup")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: grey;")

        layout = QVBoxLayout()
        
        # MAIN TITLE LABEL
        main_title = QLabel("Create Master Password")
        main_title.setStyleSheet(f'''
                        QLabel{{
                        color: white; 
                        font-weight: bold; 
                        font-size: 15px;}}
                        ''')
        layout.addWidget(main_title, 0, Qt.AlignCenter)

        layout.addStretch()

        # MASTER PASSWORD INPUT
        self.master_pwd = QLineEdit()
        self.master_pwd.setEchoMode(QLineEdit.Password)
        self.master_pwd.setPlaceholderText("Enter Master Password....")
        self.master_pwd.setStyleSheet(f'''
                        QLineEdit{{
                            background-color: white;
                            color: black;
                            font-size: 14px;
                        }}''')
        layout.addWidget(self.master_pwd)

        # CONFIRM PASSWORD INPUT
        self.confirm_pwd = QLineEdit()
        self.confirm_pwd.setEchoMode(QLineEdit.Password)
        self.confirm_pwd.setPlaceholderText("Confirm Master Password....")
        self.confirm_pwd.setStyleSheet(f'''
                        QLineEdit{{
                            background-color: white;
                            color: black;
                            font-size: 14px;
                        }}''')
        layout.addWidget(self.confirm_pwd)
        
        layout.addStretch()

        # "CREATE VAULT" BUTTON
        create_vault = QPushButton("Create Vault..")
        create_vault.clicked.connect(self.create_func)
        layout.addWidget(create_vault)

        self.setLayout(layout)
    
    # VAULT LOGIN FUNCTIONALITY
    def vault_login(self):
        self.setWindowTitle("Encrypted Vault - Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: grey")

        layout = QVBoxLayout()

        main_title = QLabel("Vault Login Window")
        main_title.setStyleSheet(f'''
                        QLabel{{
                            font-size: 20px;
                            color: white;
                            font-weight : bold;
                            font-style: italic;
                        }}''')
        main_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(main_title)
        layout.addStretch()

        layout.addSpacing(20)

        self.master_input = QLineEdit()
        self.master_input.setEchoMode(QLineEdit.Password)
        self.master_input.setStyleSheet(f'''
                                QLineEdit{{
                                    background-color: white;
                                    color: black;
                                    font-size: 13px;
                                    padding: 5px;
                                }}''')
        self.master_input.setPlaceholderText("Enter Master Password....")
        layout.addWidget(self.master_input)
        layout.addStretch()

        unlock_button = QPushButton("Unlock Vault")
        unlock_button.setStyleSheet(f'''
                        QPushButton{{
                            background-color: white;
                            color: black;
                            font-weight: bold;
                            font-size: 14px;
                        }}
                        QPushButton:hover{{
                            background-color: lime;
                        }}''')
        
        unlock_button.clicked.connect(self.verify_login)
        layout.addWidget(unlock_button)
        layout.addStretch()


        self.setLayout(layout)

    def create_func(self):
        # CREATE THE VAULT
        master = self.master_pwd.text()
        confirm = self.confirm_pwd.text()

        if not master or not confirm:
            QMessageBox.warning(self, "Error", "Please Fill Both Input Fields...")
            return
        if master != confirm:
            QMessageBox.warning(self, "Error", "Passwords Dont Match, Please Try Again!")
            return
        
        if len(master) < 8:
            QMessageBox.warning(self, "Error", "Master Password should be 8+ characters (Use the Password Generator to generate a Strong Password for the Vault)")
            return
    
        # SALT FOR PASSWORD 
        salt = secrets.token_hex(16) 
        # HASHING and SALTING MASTER PASSWORD USING HASHLIB and SECRETS
        hash_pwd = hashlib.sha256((master + salt).encode()).hexdigest()

        # CREATE SQLITE DATABASE
        conn = sqlite3.connect("vault.db")
        curr = conn.cursor()

        curr.execute('''
                CREATE TABLE PasswordDataBase (
                    id INTEGER PRIMARY KEY,
                    hash_password TEXT NOT NULL,
                    salt TEXT NOT NULL)
                ''')
        
        # STORE HASH and SALT INTO DATABASE
        curr.execute("INSERT INTO PasswordDataBase (hash_password, salt) VALUES (?, ?)", (hash_pwd, salt))

        # CREATE THE CREDENTIAL PASSWORD TABLE FOR STORING PASSWORDS
        curr.execute('''
            CREATE TABLE Passwords(
                id INTEGER PRIMARY KEY,
                service TEXT NOT NULL,
                user_name TEXT, 
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Vault Has been Created Successfully!")
        self.close()
    
    # VERIFY PASSWORD ON LOGIN METHOD
    def verify_login(self):
        user_input = self.master_input.text()

        if not user_input:
            QMessageBox.warning(self, "Error", "Please Enter Password...")
            return        
        try:
            conn = sqlite3.connect("vault.db")
            cur = conn.cursor()

            cur.execute("SELECT hash_password, salt from PasswordDataBase LIMIT 1")
            res = cur.fetchone()
            conn.close()

            try:
                if not res:
                    QMessageBox.warning(self, "Error", "Password Not Found, Try Again")
                    self.master_input.clear()
                    return
            except Exception as e:
                print(e)

            live_hash, live_salt =  res

            new_hash = hashlib.sha256((user_input + live_salt).encode()).hexdigest()

            if new_hash == live_hash:
                QMessageBox.information(self, "Success", "Vault Unlocked!")
                self.master_pwd = user_input 
                self.close()

                interface = VaultInterface(user_input, self.parent())
                interface.exec_()
            else:
                QMessageBox.warning(self, "error", "Wrong Password, Try Again")
                self.master_input.clear()
                return
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login Failed: {str(e)}")