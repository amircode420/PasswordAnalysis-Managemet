# PASSWORD GENERATOR

import secrets
import string
from PyQt5.QtWidgets import (
    QLineEdit, 
    QHBoxLayout, 
    QVBoxLayout, 
    QDialog, 
    QLabel, 
    QPushButton,
    QApplication,
    QMessageBox
)
from PyQt5.QtCore import Qt

class PasswordGenerator(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Password Generator Window")
        self.setFixedSize(450, 300)
        self.setStyleSheet("background-color: grey;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        #MAIN TITLE FOR THE WINDOW
        main_label = QLabel("Password Generator Window")
        main_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; font-style: italic")
        layout.addWidget(main_label, 0, Qt.AlignCenter)

        layout.addStretch()

        # INPUT FOR CHOOSING LENGTH
        len_container = QHBoxLayout()
        len_label = QLabel("Enter Desired Length: ")
        len_label.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        len_container.addWidget(len_label)

        self.len_input = QLineEdit("16")
        self.len_input.setStyleSheet(f'''
                        QLineEdit{{
                            background-color: white;
                            color: black;
                            font-size: 15px;
                        }}''')
        self.len_input.setFixedWidth(50)
        self.len_input.setMaxLength(2)
        len_container.addWidget(self.len_input)
        len_container.addStretch()
        layout.addLayout(len_container)

        layout.addSpacing(10)

        # Displaying the generated password
        pass_container = QHBoxLayout() # CONTAINER TO ADD
        self.pass_display = QLineEdit()
        self.pass_display.setReadOnly(True)
        self.pass_display.setStyleSheet(f"""
                QLineEdit{{
                    font-size: 15px;
                    background-color: white;
                    color: black;                     
                    padding: 5px;       }}
            """
        )
        self.pass_display.setPlaceholderText("Click Generate..")
        pass_container.addWidget(self.pass_display)

        # COPY BUTTON TO COPY THE PASSWORD TO CLIPBOARD
        copy_btn = QPushButton("Copy")
        copy_btn.setFixedSize(90, 40) # Smaller button size for copy
        copy_btn.setStyleSheet(f"""
                    QPushButton{{
                        background-color: white;
                        color: black;
                        font-size: 15px;
                               }}""")
        copy_btn.clicked.connect(self.copy_func)
        pass_container.addWidget(copy_btn)

        # GENERATE BUTTON
        gen_button = QPushButton("Generate")
        gen_button.setStyleSheet(f'''
                    QPushButton{{
                        background-color: white;
                        color: black;
                        font-size: 15px;
                    }}''')
        len_container.addWidget(gen_button)
        gen_button.clicked.connect(self.gen_func)


        layout.addLayout(pass_container)
        layout.addStretch()
        
    def gen_func(self):
        # GENERATE BUTTON FUNCTIONALITY
        try:
            length = int(self.len_input.text())
            if length < 8:
                length = 16
            if length > 32:
                length = 32
        
            # CHAR SET
            lowercase = string.ascii_lowercase 
            uppercase = string.ascii_uppercase
            digits = string.digits
            specials = "!@#$%^&*()_==+{}[]|\'':;<>,.?/"

            all_char = lowercase + uppercase + digits + specials

            #generate using secrets
            password = ''.join(secrets.choice(all_char) for _ in range(length))
            self.pass_display.setText(password)

        except Exception as e:
            QMessageBox.warning(self, "Length Error", "Please enter a valid character length")
            lenght = 16

        '''
        # CHAR SET
        lowercase = string.ascii_lowercase 
        uppercase = string.ascii_uppercase
        digits = string.digits
        specials = "!@#$%^&*()_==+{}[]|\'':;<>,.?/"

        all_char = lowercase + uppercase + digits + specials

        #generate using secrets
        password = ''.join(secrets.choice(all_char) for _ in range(length))
        self.pass_display.setText(password)
'''
    def copy_func(self):
        # COPY BUTTON FUNCTIONALTIY
        password = self.pass_display.text()
        if password:
            QApplication.clipboard().setText(password) # COPIED PASSWORD TO CLIPBOARD
            QMessageBox.information(self, "Notice", "Password Has been Copied to Clipboard!")
        print("this works")
