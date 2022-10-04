import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from operator import add, sub, mul, floordiv


class Ui(QtWidgets.QMainWindow):
    operations_dict = {add:"sum", sub:"sub", mul:"mul", floordiv:"div", None:"result"}
    keys_dict = {
        Qt.Key_0:"0",
        Qt.Key_1:"1",
        Qt.Key_2:"2",
        Qt.Key_3:"3",
        Qt.Key_4:"4",
        Qt.Key_5:"5",
        Qt.Key_6:"6",
        Qt.Key_7:"7",
        Qt.Key_8:"8",
        Qt.Key_9:"9",
        Qt.Key_A:"A",
        Qt.Key_B:"B",
        Qt.Key_C:"C",
        Qt.Key_D:"D",
        Qt.Key_E:"E",
        Qt.Key_F:"F",
        Qt.Key_Slash:"div",
        Qt.Key_Plus:"sum",
        Qt.Key_Minus:"sub",
        Qt.Key_Asterisk:"mul",
        Qt.Key_Backspace:"backspace",
        Qt.Key_Enter:"result",
        Qt.Key_Return:"result",
        Qt.Key_Escape:"clear",
        Qt.Key_Delete:"clear_entry"
    }

    def __init__(self):
        super().__init__()
        uic.loadUi('calc.ui', self)
        # container for intermidiate result of arifmetic
        self.arifmetic_result = None
        # container sor saving last arifmetic operation
        self.current_ariphmetic_operation = None
        # log fot output to log-field
        self.text_log = ""
        # show main window
        self.show()
        # flag pointing to need clearing text field by next entry
        self.new_write_flag = True
        # init inactive palette
        self.palInactive = QPalette()
        self.palInactive.setColor(QPalette.Base, Qt.white)
        # init active palette
        self.palActive = QPalette()
        self.palActive.setColor(QPalette.Base, Qt.green)
        # dict to match text fields by b/d/c text browsers
        self.labels_dict = {self.textEdit_hex: self.label_hex, self.textEdit_dec: self.label_dec, self.textEdit_bin: self.label_bin}
        # list text fields to switching select current text field
        self.inputs_list = [self.textEdit_bin, self.textEdit_dec, self.textEdit_hex]
        # connecting number-buttons
        self.all_num_signals_connect()
        # connecting select empty
        self.textEdit_bin.selectionChanged.connect(self.select_inp_bin)
        self.textEdit_dec.selectionChanged.connect(self.select_inp_dec)
        self.textEdit_hex.selectionChanged.connect(self.select_inp_hex)
        self.textEdit_bin.selectionChanged.connect(self.paint_textFields)
        self.textEdit_dec.selectionChanged.connect(self.paint_textFields)
        self.textEdit_hex.selectionChanged.connect(self.paint_textFields)
        # signals ariphmetic buttons connection
        self.pushButton_sum.clicked.connect(self.ariphmetic_create(add))
        self.pushButton_sub.clicked.connect(self.ariphmetic_create(sub))
        self.pushButton_mul.clicked.connect(self.ariphmetic_create(mul))
        self.pushButton_div.clicked.connect(self.ariphmetic_create(floordiv))
        self.pushButton_result.clicked.connect(self.ariphmetic_create(None))
        # signals buttons C and CE
        self.pushButton_clear.clicked.connect(self.clk_C_btn)
        self.pushButton_clear_entry.clicked.connect(self.clk_CE_btn)
        # pointer to one of three text fields objects
        self.current_handler = self.textEdit_dec
        # start clearing select field
        self.current_handler.setPlainText("0")
        # init functions dict to match with button signals
        self.functions_dict = {i: self.clk_evt_btn_create(i) for i in "0123456789ABCDEF"}
        # add entries of arifmetic operations
        self.functions_dict.update({key: self.ariphmetic_create(op) for op, key in self.operations_dict.items()})
        # add entries of other keys
        self.functions_dict.update({"clear": self.clk_C_btn, "clear_entry":self.clk_CE_btn, "backspace":self.clk_backspace_btn})
        # stand on of active field
        self.paint_textFields()

        # create signals for all input
        for key, func in self.functions_dict.items():
            btn = self.findChild(QtWidgets.QPushButton, f"pushButton_{key}")
            if btn is not None:
                btn.clicked.connect(func)
        self.setChildrenFocusPolicy(Qt.NoFocus)

    # ???
    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)

    # def to performing the function of tracking keyboard
    def keyPressEvent(self, event):
        offset = 0
        key = self.keys_dict.get(event.key())
        if key is not None:
            self.functions_dict[key]()
        elif event.key() == Qt.Key_Up:
            offset = -1
        elif event.key() == Qt.Key_Down:
            offset = 1
        if offset:
            index = self.inputs_list.index(self.current_handler)
            index += offset
            index %= len(self.inputs_list)
            self.current_handler = self.inputs_list[index]
            self.paint_textFields()

    # def to stad out current field of non-current
    def paint_textFields(self):
        for edit, label in self.labels_dict.items():
            if edit == self.current_handler:
                label.setPalette(self.palActive)
            else:
                label.setPalette(self.palInactive)

    # def to creating
    def clk_evt_btn_create(self, num):
        def clk_evt_btn():
            if self.new_write_flag == True:
                self.new_write_flag = False
                self.set_all_notation(0)
                text = str(num)
            else:
                text = self.current_handler.toPlainText()
                text += str(num)
            self.current_handler.setPlainText(text)
        return clk_evt_btn

    # def to creating functions from arifmetic buttons
    def ariphmetic_create(self, operator):
        def ar_handler():
            self.aripfmetic_operations(operator)
        return ar_handler

    # replace separators in string, convert non-decimal value to decimal and return int
    def recieve_value(self, input):
        input = input.replace(' ', '')
        try:
            if self.current_handler == self.textEdit_bin:
                itext = int(input, base=2)
            if self.current_handler == self.textEdit_hex:
                itext = int(input, base=16)
            if self.current_handler == self.textEdit_dec:
                itext = int(input, base=10)
            return itext
        except ValueError:
            itext = 0
            return 0

    # def to connect all signals of text entries
    def all_num_signals_connect(self):
        self.textEdit_dec.textChanged.connect(self.output_update)
        self.textEdit_bin.textChanged.connect(self.output_update)
        self.textEdit_hex.textChanged.connect(self.output_update)

    # def to disconnect all signals of text entries
    def all_num_signals_disconnect(self):
        self.textEdit_dec.textChanged.disconnect(self.output_update)
        self.textEdit_bin.textChanged.disconnect(self.output_update)
        self.textEdit_hex.textChanged.disconnect(self.output_update)

    # def to get current number in text-editor and add input num from buttons to the end
    def output_update(self):
        text = self.current_handler.toPlainText()
        itext = self.recieve_value(text)
        self.select_notation_and_set(itext)

    # def to set values to not-current editors
    def select_notation_and_set(self, itext):
        self.all_num_signals_disconnect()
        if self.current_handler != self.textEdit_dec: self.set_dec(itext)
        if self.current_handler != self.textEdit_bin: self.set_bin(itext)
        if self.current_handler != self.textEdit_hex: self.set_hex(itext)
        self.all_num_signals_connect()

    # def to set values to current editor
    def set_current_notation(self, itext):
        self.all_num_signals_disconnect()
        if self.current_handler == self.textEdit_dec: self.set_dec(itext)
        if self.current_handler == self.textEdit_bin: self.set_bin(itext)
        if self.current_handler == self.textEdit_hex: self.set_hex(itext)
        self.all_num_signals_connect()

    # def to set valuet to all editors
    def set_all_notation(self, itext):
        self.all_num_signals_disconnect()
        self.set_dec(itext)
        self.set_bin(itext)
        self.set_hex(itext)
        self.all_num_signals_connect()

    # def to output decimal-formating text
    def set_dec(self, itext):
        self.textEdit_dec.setPlainText(f"{itext}")

    # def to output binary-formating text
    def set_bin(self, itext):
        sout = f"{itext:032b}"
        self.textEdit_bin.setPlainText(f"{sout[:8]} {sout[8:16]} {sout[16:24]} {sout[24:32]}")

    # def to output hexadecimal-formating text
    def set_hex(self, itext):
        sout = f"{itext:08X}"
        self.textEdit_hex.setPlainText(f"{sout[:2]} {sout[2:4]} {sout[4:6]} {sout[6:]}")

    # def to connection with signal clicked of buttons sum, sub, mul, dev, result
    def aripfmetic_operations(self, operation):
        # get text by active input entry and convert to int
        text = self.current_handler.toPlainText()
        itext = self.recieve_value(text)
        # first input number need to pull on result and not execute arifmetic operations
        if not self.arifmetic_result:
            self.arifmetic_result = itext
        # all next pushes of arifmetic buttons execute arifmetic operations
        else:
            self.arifmetic_result = self.current_ariphmetic_operation(self.arifmetic_result, itext)
        self.text_log += str(itext) + " "
        self.current_ariphmetic_operation = operation
        self.text_log += self.operations_dict[self.current_ariphmetic_operation] + " "

        if self.current_ariphmetic_operation is None:
            self.text_log += str(self.arifmetic_result) + "\n"
            self.arifmetic_result = None

        self.new_write_flag = True
        self.textEdit_log.setPlainText(self.text_log)

    # def to connection with signal selectChange of decimal entry
    def select_inp_bin(self):
        self.current_handler = self.textEdit_bin
    # def to connection with signal selectChange of binary entry
    def select_inp_dec(self):
        self.current_handler = self.textEdit_dec
    # def to connection with signal selectChange of hex entry
    def select_inp_hex(self):
        self.current_handler = self.textEdit_hex

    # def to connection with signal of C-button
    def clk_C_btn(self):
        self.arifmetic_result = None
        self.current_ariphmetic_operation = None
        self.text_log = ""
        self.textEdit_log.setPlainText(self.text_log)
        self.clk_CE_btn()

    # def to connection with signal of CE-button
    def clk_CE_btn(self):
        self.new_write_flag = True
        self.set_all_notation(0)

    # def to connection with signal of backspace-button
    def clk_backspace_btn(self):
        text = self.current_handler.toPlainText()
        text = text[:-1]
        itext = self.recieve_value(text)
        self.set_all_notation(itext)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
