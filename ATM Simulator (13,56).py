# ATM SIMULATOR 

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ATM(QWidget):
    def __init__(self):
        super().__init__()

        # basic data ─ just one user for demo
        self.bal = 5000            # starting balance
        self.pin = "1234"          # default pin

        self.setWindowTitle("ATM – Mini Project")
        self.setGeometry(200, 120, 380, 350)
        self.setStyleSheet("background:#e6f2ff;")
        self.build_ui()

    # build all widgets in one go (kept it simple)
    def build_ui(self):
        self.v = QVBoxLayout()

        self.head = QLabel("ATM Simulator")
        self.head.setFont(QFont("Arial", 16, QFont.Bold))
        self.head.setAlignment(Qt.AlignCenter)
        self.v.addWidget(self.head)

        # pin entry
        self.pin_edit = QLineEdit()
        self.pin_edit.setEchoMode(QLineEdit.Password)
        self.pin_edit.setPlaceholderText("Enter PIN")
        self.v.addWidget(self.pin_edit)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)
        self.v.addWidget(self.login_btn)

        # action buttons – disabled until login ok
        self.btn_bal  = QPushButton("Check Balance")
        self.btn_dep  = QPushButton("Deposit")
        self.btn_wd   = QPushButton("Withdraw")
        self.btn_chg  = QPushButton("Change PIN")
        self.btn_exit = QPushButton("Exit")

        for b in (self.btn_bal, self.btn_dep, self.btn_wd, self.btn_chg, self.btn_exit):
            b.setEnabled(False)
            self.v.addWidget(b)

        # connect
        self.btn_bal.clicked.connect(self.show_bal)
        self.btn_dep.clicked.connect(self.do_dep)
        self.btn_wd.clicked.connect(self.do_wd)
        self.btn_chg.clicked.connect(self.do_chg)
        self.btn_exit.clicked.connect(self.close)

        self.setLayout(self.v)

    # --- helpers ----------------------------------------------------------
    def enable_actions(self, flag):
        self.btn_bal.setEnabled(flag)
        self.btn_dep.setEnabled(flag)
        self.btn_wd.setEnabled(flag)
        self.btn_chg.setEnabled(flag)
        self.btn_exit.setEnabled(flag)

    # check pin
    def check_login(self):
        if self.pin_edit.text() == self.pin:
            QMessageBox.information(self, "OK", "Logged in!")
            self.pin_edit.setDisabled(True)
            self.login_btn.setDisabled(True)
            self.enable_actions(True)
        else:
            QMessageBox.critical(self, "Oops", "Wrong PIN")

    # balance
    def show_bal(self):
        QMessageBox.information(self, "Balance", "₹{}".format(self.bal))

    # deposit
    def do_dep(self):
        amt, ok = QInputDialog.getInt(self, "Deposit", "Amount:")
        if ok and amt > 0:
            self.bal += amt
            QMessageBox.information(self, "Done", "Deposited ₹{}".format(amt))
        else:
            QMessageBox.warning(self, "Error", "Invalid amount!")

    # withdraw
    def do_wd(self):
        amt, ok = QInputDialog.getInt(self, "Withdraw", "Amount:")
        if ok:
            if amt <= self.bal:
                self.bal -= amt
                QMessageBox.information(self, "Done", "Withdrawn ₹{}".format(amt))
            else:
                QMessageBox.warning(self, "Err", "Not enough balance")

    # change pin + force re-login
    def do_chg(self):
        new_pin, ok = QInputDialog.getText(self, "Change PIN", "New PIN (digits only):")
        if ok and new_pin.isdigit() and new_pin.strip():
            self.pin = new_pin.strip()
            QMessageBox.information(self, "Success", "PIN changed. Login again.")
            # logout
            self.enable_actions(False)
            self.pin_edit.setEnabled(True)
            self.pin_edit.clear()
            self.login_btn.setEnabled(True)
        else:
            QMessageBox.warning(self, "Invalid", "PIN must be numeric.")


# run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ATM()
    win.show()
    sys.exit(app.exec_())

