import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QProgressBar,
    QTextEdit,
    QAction,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from core.analysis import PasswordAnalyzer
from core.generate_pwd import PasswordGenerator
from core.pwd_vault import PasswordVault

class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Analysis and Management Tool")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #899499; color: white;")
        self.password_analyzer = PasswordAnalyzer()
        self.generator = PasswordGenerator()
        self.main_vault = PasswordVault()

        # MAIN LAYOUT
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addStretch()
        layout = QHBoxLayout()
        layout.addStretch()
        layout2 = QVBoxLayout()
        #layout2.addStretch()
        
        # MAIN LABEL
        self.title_label = QLabel("Password Analysis and Mangement Tool")
        self.title_label.setStyleSheet("font-size: 25px; font-weight: bold; color: white;")
        layout2.addWidget(self.title_label, 0 , Qt.AlignCenter)

        layout2.addSpacing(10)

        # PASSWORD INPUT BOX
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(f'''QLineEdit{{
            font-size: 15px;
            color: black;
            background-color: white;
            padding-right: 30px;
            border: 2px solid;
            }}              
                            
            ''')
        self.password_input.setPlaceholderText("Enter password to analyze")
        #self.password_input.setMaxLength(72)
        self.password_input.setFixedWidth(300)

        '''
        # SHOW AND HIDE function
        self.show_pass = QAction("👁", self)
        self.show_pass.triggered.connect(self.show_func)
        self.password_input.addAction(self.show_pass, QLineEdit.TrailingPosition)
        '''

        layout2.addWidget(self.password_input, 0 , Qt.AlignCenter) 

        
        # ANALYZE BUTTON
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setStyleSheet(
            f'''
            QPushButton{{
            font-size: 20px;
            background-color: white;
            color: black;
            }}
            '''
        )
        self.analyze_btn.setFixedWidth(300)
        layout2.addWidget(self.analyze_btn, 0 , Qt.AlignCenter)
        self.analyze_btn.clicked.connect(self.analysis)

        '''
        # GENERATE PASSWORD BUTTON
        self.gen_pass_btn = QPushButton("Generate Password")
        self.gen_pass_btn.setFixedWidth(300)
        layout2.addWidget(self.gen_pass_btn, 0, Qt.AlignCenter)
        self.gen_pass_btn.clicked.connect(self.gen_pass)
        '''

        # PROGRESS COLOR BAR
        self.color_bar = QProgressBar()
        self.color_bar.setFixedWidth(300)
        self.color_bar.setTextVisible(False)
        layout2.addWidget(self.color_bar, 0, Qt.AlignCenter)

        self.password_input.textChanged.connect(self.color_bar_func)


        #RESULT LABEL
        self.res_label = QLabel("Analysis Results: ")
        self.res_label.setStyleSheet(f'''
                        QLabel{{
                            font-size: 18px;
                            font-weight: bold;
                            color: black;
                            
                        }}            
                        ''')
        layout2.addWidget(self.res_label, 0, Qt.AlignCenter)

        # RESULTS TEXTBOX
        self.res_text = QTextEdit()
        self.res_text.setPlaceholderText("Results will appear here...")
        self.res_text.setStyleSheet(f'''
            QTextEdit{{
                font-size: 15px;
                color: black;
                background-color: white;
            }}
        ''')
        self.res_text.setFixedHeight(250)
        self.res_text.setFixedWidth(400)
        self.res_text.setReadOnly(True)
        self.res_text.setLineWrapMode(QTextEdit.WidgetWidth)
        layout2.addWidget(self.res_text, 0, Qt.AlignCenter)
        layout2.addStretch()

         # Bottom Container for Buttons
        bottom_ctn = QHBoxLayout()

        # GENERATE PASSWORD BUTTON
        self.gen_pass_btn = QPushButton("Password Generator")
        self.gen_pass_btn.setStyleSheet(f'''
                                QPushButton{{
                                    background-color: white;
                                    color: black;
                                    font-size: 15px;
                                    font-weight: bold;
                                }}
                                QPushButton:hover{{
                                        background-color: #FFBF00;
                                }}''')
        bottom_ctn.addWidget(self.gen_pass_btn)
        self.gen_pass_btn.clicked.connect(self.gen_pass)

        bottom_ctn.addStretch()

        # VAULT BUTTON
        self.vault_btn = QPushButton("Password Vault")
        self.vault_btn.setStyleSheet(f'''
                    QPushButton{{
                            font-size: 15px;
                            font-weight: bold;
                            background-color: white;
                            color: black;
                    }}
                    QPushButton:hover{{
                            background-color: #CC5500;
                    }}
                        ''')
        self.vault_btn.clicked.connect(self.vault)
        bottom_ctn.addWidget(self.vault_btn)
         
        
        # Adding to the layouts
        main_layout.addLayout(layout)
        main_layout.addLayout(layout2)
        main_layout.addStretch()
        main_layout.addLayout(bottom_ctn)

    '''
    # SHOW and HIDE functionality
    def show_func(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal) # REVEALS PASSWORD
            self.show_pass.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_pass.setText("Show")
    '''

    # COLOR BAR FUCNTIONALITY
    def color_bar_func(self):
        try:
            password = self.password_input.text()
            if not password:
                self.color_bar.setValue(0)
                #self.color_bar.setStyleSheet()
                return
            
            analysis = self.password_analyzer.full_analysis(password)
            new_score = analysis['strength_score']
            print("Score: ", new_score)

            percentage = (new_score/4) * 100
            self.color_bar.setValue(int(percentage))
            print("Score Percentage: ", percentage)

            # ADD COLOR TO PROGESS BAR
            if new_score <= 1: # VERY WEAK AND WEAK COLOR
                color = "red"
            elif new_score == 2: # MEDIUM COLOR
                color = "yellow"
            else:  # STRONG AND VERY STRONG COLOR
                color = "green"
            
            self.color_bar.setStyleSheet(f'''
                        QProgressBar::chunk{{
                            background-color: {color};
                        }}''')
        except ValueError as e:
            QMessageBox.critical(self, "Error", "Password has too many characters (EXCEEDING LENGTH OF 72 CHARACTERS)")
            self.password_input.clear()

        # ANALYZE BUTTON FUNCTIONALITY
    def analysis(self):
        try:
            password = self.password_input.text()
            gui_output = self.password_analyzer.res_gui(password)

        
            all_res = "----BASIC TEST-----\n"
            all_res += f"{gui_output['strength_test']}\n"
            all_res += f"{gui_output['crack_time']}\n"
            all_res += f"{gui_output['warning']}\n"
            all_res += f"{gui_output['detailed_results']}\n"
            
            '''
            strength_text = gui_output['strength_text']
            crack_time = gui_output['crack_time']
            warning = gui_output['warning']
            detailed_res = gui_output['detailed_results']
            '''
            
            self.res_text.setText(all_res)

            print("This works")
        except Exception as e:
            QMessageBox.warning(self, "Notice!", "Please enter a Password first!")
            print(e)
    
    # GENERATOR BUTTON FUNCTIONALITY
    def gen_pass(self):
        dialog = PasswordGenerator()
        dialog.exec_()
        print("this works")

    # VAULT BUTTON FUNCTIONALITY
    def vault(self):
        dialog = PasswordVault()
        dialog.exec_()
        print("This works")

def main():
    app = QApplication(sys.argv)    
    window = PasswordManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()