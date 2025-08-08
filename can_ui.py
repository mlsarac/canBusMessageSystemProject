from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QTextEdit
)
from PyQt5.QtWidgets import QApplication
import sys

class CANMessageSenderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J1939 CAN Message Sender")
        self.resize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Message selection
        msg_layout = QHBoxLayout()
        msg_label = QLabel("Message:")
        self.msg_combo = QComboBox()
        self.msg_combo.addItem("Select")
        msg_layout.addWidget(msg_label)
        msg_layout.addWidget(self.msg_combo)

        # Signal selection
        sig_layout = QHBoxLayout()
        sig_label = QLabel("Signal:")
        self.sig_combo = QComboBox()
        self.sig_combo.addItem("Select")
        sig_layout.addWidget(sig_label)
        sig_layout.addWidget(self.sig_combo)

        # Signal value input (text and combo)
        val_layout = QHBoxLayout()
        val_label = QLabel("Value:")
        self.val_input = QLineEdit()
        self.val_combo = QComboBox()
        self.val_combo.hide()  # default hidden
        self.unit_label = QLabel("")  # Unit label added
        self.range_label = QLabel("")  # Range label added
        val_layout.addWidget(val_label)
        val_layout.addWidget(self.val_input)
        val_layout.addWidget(self.val_combo)
        val_layout.addWidget(self.unit_label)
        val_layout.addWidget(self.range_label)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.view_btn = QPushButton("View Encoded Message")
        self.send_btn = QPushButton("Send Message")
        btn_layout.addWidget(self.view_btn)
        btn_layout.addWidget(self.send_btn)

        # Message output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        layout.addLayout(msg_layout)
        layout.addLayout(sig_layout)
        layout.addLayout(val_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.output_display)

        self.setLayout(layout)

