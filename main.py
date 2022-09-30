import sys
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)
        self.show()
        self.textEdit_dec.textChanged.connect(self.update_bin)
        self.textEdit_dec.textChanged.connect(self.update_hex)
        for i in range(10):
            btn = self.findChild(QtWidgets.QPushButton, f"pushButton_{i}")
            btn.clicked.connect(self.clk_evt_btn_create(i))

    def clk_evt_btn_create(self, num):
        def clk_evt_btn():
            text = self.textEdit_dec.toPlainText()
            text += str(num)
            self.textEdit_dec.setPlainText(text)
        return clk_evt_btn

    def update_bin(self):
        text = self.textEdit_dec.toPlainText()
        try:
            itext = int(text)
        except ValueError:
            itext = 0
        txt = f"{itext:016b}"
        self.textEdit_bin.setPlainText(f"0b{txt[:8]}'{txt[8:]}")

    def update_hex(self):
        text = self.textEdit_dec.toPlainText()
        try:
            itext = int(text)
        except ValueError:
            itext = 0
        txt = f"{itext:08X}"
        self.textEdit_hex.setPlainText(f"0x{txt[:4]}'{txt[4:]}")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
