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
        Qt.Key_Delete:"clear_entry",
        Qt.Key_Left:"lshift",
        Qt.Key_Right:"rshift"
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
        # connecting select empty
        self.textEdit_bin.selectionChanged.connect(self.select_binary_field)
        self.textEdit_dec.selectionChanged.connect(self.select_decimal_field)
        self.textEdit_hex.selectionChanged.connect(self.select_hexadecimal_field)
        self.textEdit_bin.selectionChanged.connect(self.paint_textFields)
        self.textEdit_dec.selectionChanged.connect(self.paint_textFields)
        self.textEdit_hex.selectionChanged.connect(self.paint_textFields)
        # signals ariphmetic buttons connection
        self.pushButton_sum.clicked.connect(self.create_arifmetic_functions(add))
        self.pushButton_sub.clicked.connect(self.create_arifmetic_functions(sub))
        self.pushButton_mul.clicked.connect(self.create_arifmetic_functions(mul))
        self.pushButton_div.clicked.connect(self.create_arifmetic_functions(floordiv))
        self.pushButton_result.clicked.connect(self.create_arifmetic_functions(None))
        # signals buttons C and CE
        self.pushButton_clear.clicked.connect(self.click_C)
        self.pushButton_clear_entry.clicked.connect(self.click_CE)
        # pointer to one of three text fields objects
        self.current_handler = self.textEdit_dec
        # start clearing select field
        self.output_to_all_fields(0)
        # connected left anr right shift
        self.pushButton_lshift.clicked.connect(self.click_leftShift)
        self.pushButton_rshift.clicked.connect(self.click_rightShift)
        # init functions dict to match with button signals
        self.functions_dict = {i: self.click_button_event_create(i) for i in "0123456789ABCDEF"}
        # add entries of arifmetic operations
        self.functions_dict.update({key: self.create_arifmetic_functions(op) for op, key in self.operations_dict.items()})
        # add entries of other keys
        self.functions_dict.update({"clear": self.click_C, "clear_entry":self.click_CE, "backspace":self.click_backspace, "rshift":self.click_rightShift, "lshift":self.click_leftShift})
        # stand on of active field
        self.paint_textFields()

        # create signals for all input
        for key, func in self.functions_dict.items():
            btn = self.findChild(QtWidgets.QPushButton, f"pushButton_{key}")
            if btn is not None:
                btn.clicked.connect(func)
        self.setChildrenFocusPolicy(Qt.NoFocus)

    def setChildrenFocusPolicy(self, policy):
        """disconnect all changes of focus"""
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)
        recursiveSetChildFocusPolicy(self)

    def keyPressEvent(self, event):
        """performing the function of tracking keyboard"""
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

    def paint_textFields(self):
        """stad out current field of non-current"""
        for edit, label in self.labels_dict.items():
            if edit == self.current_handler:
                label.setPalette(self.palActive)
            else:
                label.setPalette(self.palInactive)

    def click_button_event_create(self, character):
        """creating"""
        def click_button_event():
            if self.new_write_flag == True:
                self.new_write_flag = False
                int_number = self.convert_string_to_int(character)
            else:
                existing_text = self.current_handler.toPlainText()
                int_number = self.convert_string_to_int(existing_text + character)
            self.output_to_all_fields(int_number)
        return click_button_event

    def create_arifmetic_functions(self, operator):
        """creating functions from arifmetic buttons"""
        def arifmetic_function():
            self.perform_aripfmetic_operation(operator)
        return arifmetic_function

    def convert_string_to_int(self, string_number):
        """replace separators in string, convert non-decimal value to decimal and return int"""
        string_number = string_number.replace(' ', '')
        try:
            if self.current_handler == self.textEdit_bin:
                int_number = int(string_number, base=2)
            if self.current_handler == self.textEdit_hex:
                int_number = int(string_number, base=16)
            if self.current_handler == self.textEdit_dec:
                int_number = int(string_number, base=10)
            return int_number
        except ValueError:
            int_number = 0
            return 0

    def update_fields(self):
        """get current number in text-editor and add input num from buttons to the end"""
        existing_text = self.current_handler.toPlainText()
        int_number = self.convert_string_to_int(existing_text)
        self.output_to_all_fields(int_number)

    def output_to_all_fields(self, int_number):
        """set valuet to all editors"""
        self.print_decimal(int_number)
        self.print_binary(int_number)
        self.print_hexadecimal(int_number)

    def print_decimal(self, itext):
        """output decimal-formating text"""
        self.textEdit_dec.setPlainText(f"{itext}")

    def print_binary(self, itext):
        """output binary-formating text"""
        sout = f"{itext:032b}"
        self.textEdit_bin.setPlainText(f"{sout[0:8]} {sout[8:16]} {sout[16:24]} {sout[24:32]}")

    def print_hexadecimal(self, itext):
        """output hexadecimal-formating text"""
        sout = f"{itext:08X}"
        self.textEdit_hex.setPlainText(f"{sout[:2]} {sout[2:4]} {sout[4:6]} {sout[6:]}")

    def perform_aripfmetic_operation(self, operation):
        """connection with signal clicked of buttons sum, sub, mul, dev, result"""
        # get text by active input entry and convert to int
        text = self.current_handler.toPlainText()
        itext = self.convert_string_to_int(text)
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
            self.output_to_all_fields(self.arifmetic_result)
            self.arifmetic_result = None

        self.new_write_flag = True
        self.textEdit_log.setPlainText(self.text_log)

    def select_binary_field(self):
        """connection with signal selectChange of decimal entry"""
        self.current_handler = self.textEdit_bin
    def select_decimal_field(self):
        """connection with signal selectChange of binary entry"""
        self.current_handler = self.textEdit_dec
    def select_hexadecimal_field(self):
        """connection with signal selectChange of hex entry"""
        self.current_handler = self.textEdit_hex

    def click_C(self):
        """connection with signal of C-button"""
        self.arifmetic_result = None
        self.current_ariphmetic_operation = None
        self.text_log = ""
        self.textEdit_log.setPlainText(self.text_log)
        self.click_CE()

    def click_CE(self):
        """connection with signal of CE-button"""
        self.new_write_flag = True
        self.output_to_all_fields(0)

    def click_backspace(self):
        """connection with signal of backspace-button"""
        text = self.current_handler.toPlainText()
        text = text[:-1]
        itext = self.convert_string_to_int(text)
        self.output_to_all_fields(itext)

    def click_leftShift(self):
        itext = int(self.current_handler.toPlainText())
        itext <<= 1
        itext &= 0xFFFFFFFF
        self.output_to_all_fields(itext)

    def click_rightShift(self):
        itext = int(self.current_handler.toPlainText())
        itext >>= 1
        itext &= 0xFFFFFFFF
        self.output_to_all_fields(itext)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
