#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# bochica                                                                      #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a GNU Privacy Guard encryption-decryption graphical user     #
# interface.                                                                   #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help               display help message
    --version                display version and exit
    -v, --verbose            verbose logging
    -s, --silent             silent
    -u, --username=USERNAME  username
    --keysender=KEY          recipient key [default: none]
    --keyrecipient=KEY       recipient key [default: none]
"""

name    = "bochica"
version = "2017-01-31T0155Z"
logo    = None

import docopt
import logging
import os
import sys
import time

import propyte
from PyQt5.QtWidgets import (
    QApplication,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QWidget
)
import shijian

def main(options):

    global program
    program = propyte.Program(
        options = options,
        name    = name,
        version = version,
        logo    = logo
    )
    global log
    from propyte import log

    global key_sender
    global key_recipient
    key_sender    = None if options["--keysender"].lower() == "none" else options["--keysender"]
    key_recipient = None if options["--keyrecipient"].lower() == "none" else options["--keyrecipient"]

    application = QApplication(sys.argv)
    interface = Interface()
    sys.exit(application.exec_())

class Interface(QWidget):
    
    def __init__(
        self
        ):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.height_window                  = 750
        self.width_window                   = 480
        self.position_x_window              = 0
        self.position_y_window              = 0

        self.position_x_button_encrypt      = 10
        self.position_y_button_encrypt      = 10

        self.position_x_button_decrypt      = 346
        self.position_y_button_decrypt      = 10

        self.position_x_label_recipient_key = 90
        self.position_y_label_recipient_key = 74

        self.position_x_text_recipient_key  = 178
        self.position_y_text_recipient_key  = 70

        self.position_x_label_sender_key    = 90
        self.position_y_label_sender_key    = 44

        self.position_x_text_sender_key     = 178
        self.position_y_text_sender_key     = 40

        self.position_x_label_passcode      = 90
        self.position_y_label_passcode      = 104

        self.position_x_text_passcode       = 178
        self.position_y_text_passcode       = 100

        self.width_button                   = 124

        self.width_text_box                 = 460
        self.height_text_box                = 300

        self.position_x_text_entry          = 10
        self.position_y_text_entry          = 130

        self.position_x_text_exit           = 10
        self.position_y_text_exit           = 440

        self.setWindowTitle(name)
        self.setGeometry(
            self.position_x_window,
            self.position_y_window,
            self.width_window,
            self.height_window
        )

        # button encrypt
        self.button_encrypt_message = QPushButton("encrypt", self)
        self.button_encrypt_message.move(
            self.position_x_button_encrypt,
            self.position_y_button_encrypt
        )
        self.button_encrypt_message.setFixedWidth(self.width_button)
        self.button_encrypt_message.clicked.connect(self.message_encrypt)

        # button decrypt
        self.button_decrypt_message = QPushButton("decrypt", self)
        self.button_decrypt_message.move(
            self.position_x_button_decrypt,
            self.position_y_button_decrypt
        )
        self.button_decrypt_message.setFixedWidth(self.width_button)
        self.button_decrypt_message.clicked.connect(self.message_decrypt)

        # label recipient key
        self.label_recipient_key = QLabel(self)
        self.label_recipient_key.move(
            self.position_x_label_recipient_key,
            self.position_y_label_recipient_key
        )
        self.label_recipient_key.setText("recipient key:")

        # text box recipient key
        self.text_recipient_key = QLineEdit(self)
        self.text_recipient_key.move(
            self.position_x_text_recipient_key,
            self.position_y_text_recipient_key
        )
        if key_recipient:
            self.text_recipient_key.setText(key_recipient)

        # label sender key
        self.label_sender_key = QLabel(self)
        self.label_sender_key.move(
            self.position_x_label_sender_key,
            self.position_y_label_sender_key
        )
        self.label_sender_key.setText("sender key:")

        # text box sender key
        self.text_sender_key = QLineEdit(self)
        self.text_sender_key.move(
            self.position_x_text_sender_key,
            self.position_y_text_sender_key
        )
        if key_sender:
            self.text_sender_key.setText(key_sender)

        # label passcode
        self.label_passcode = QLabel(self)
        self.label_passcode.move(
            self.position_x_label_passcode,
            self.position_y_label_passcode
        )
        self.label_passcode.setText("passcode:")

        # text box passcode
        self.text_passcode = QLineEdit(self)
        self.text_passcode.setEchoMode(QLineEdit.Password)
        self.text_passcode.move(
            self.position_x_text_passcode,
            self.position_y_text_passcode
        )

        # text entry box
        self.text_entry = QTextEdit(self)
        self.text_entry.move(
            self.position_x_text_entry,
            self.position_y_text_entry
        )
        self.text_entry.setFixedWidth(self.width_text_box)
        self.text_entry.setFixedHeight(self.height_text_box)

        # text exit box
        self.text_exit = QTextEdit(self)
        self.text_exit.move(
            self.position_x_text_exit,
            self.position_y_text_exit
        )
        self.text_exit.setFixedWidth(self.width_text_box)
        self.text_exit.setFixedHeight(self.height_text_box)

        self.show()

    def message_encrypt(self):

        command = "echo \"{text}\" | gpg --encrypt --armor --trust-model always -u {key_sender} -r {key_recipient}".format(
            text          = self.text_entry.toPlainText(),
            key_sender    = self.text_sender_key.text(),
            key_recipient = self.text_recipient_key.text()
        )
        log.debug(command)
        message_encrypted = shijian.engage_command(
            command = command
        ).decode("utf-8") 
        self.text_exit.setText("")
        self.text_exit.insertPlainText(str(message_encrypted))

    def message_decrypt(self):

        command = "echo \"{text}\" | gpg --decrypt --passphrase \"{passcode}\"".format(
            text     = self.text_entry.toPlainText(),
            passcode = self.text_passcode.text()
        )
        #log.debug(command) caution: security
        message_decrypted = shijian.engage_command(
            command = command
        ).decode("utf-8") 
        self.text_exit.setText("")
        self.text_exit.insertPlainText(str(message_decrypted))

    def closeEvent(
        self,
        event
        ):

        program.terminate()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
