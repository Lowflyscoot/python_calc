import sys
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)
        self.sbin_output = ""
        self.sdec_output = ""
        self.shex_output = ""
        self.current_handler = self.textEdit_hex
        self.show()
        self.all_signals_connect()
        self.textEdit_dec.setPlainText("0")
        # self.pushButton_
        for i in range(10):
            btn = self.findChild(QtWidgets.QPushButton, f"pushButton_{i}")
            btn.clicked.connect(self.clk_evt_btn_create(i))

    def clk_evt_btn_create(self, num):
        def clk_evt_btn():
            text = self.current_handler.toPlainText()
            text += str(num)
            self.current_handler.setPlainText(text)
        return clk_evt_btn

    def check_input_correct(self, input):
        try:
            itext = int(input)
            # clear log window
            self.textEdit_log.setPlainText("")
            return itext
        except ValueError:
            itext = 0
            # print error to log window
            self.textEdit_log.setPlainText("incorrect input")
            return 0

    def all_signals_connect(self):
        self.textEdit_dec.textChanged.connect(self.output_update)
        self.textEdit_bin.textChanged.connect(self.output_update)
        self.textEdit_hex.textChanged.connect(self.output_update)

    def all_signals_disconnect(self):
        self.textEdit_dec.textChanged.disconnect(self.output_update)
        self.textEdit_bin.textChanged.disconnect(self.output_update)
        self.textEdit_hex.textChanged.disconnect(self.output_update)

    def output_update(self):
        text = self.current_handler.toPlainText()
        itext = self.check_input_correct(text)
        self.all_signals_disconnect()
        if self.current_handler != self.textEdit_dec: self.set_dec(itext)
        if self.current_handler != self.textEdit_bin: self.set_bin(itext)
        if self.current_handler != self.textEdit_hex: self.set_hex(itext)
        self.all_signals_connect()

    def set_dec(self, itext):
        self.textEdit_dec.setPlainText(f"{itext}")

    def set_bin(self, itext):
        sout = f"{itext:032b}"
        self.textEdit_bin.setPlainText(f"{sout[:8]} {sout[8:16]} {sout[16:24]} {sout[24:32]}")

    def set_hex(self, itext):
        sout = f"{itext:08X}"
        self.textEdit_hex.setPlainText(f"{sout[:2]} {sout[2:4]} {sout[4:6]} {sout[6:]}")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
