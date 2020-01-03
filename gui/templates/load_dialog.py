# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_load_dialog(object):
    def setupUi(self, load_dialog):
        load_dialog.setObjectName("load_dialog")
        load_dialog.resize(429, 159)
        self.gridLayout = QtWidgets.QGridLayout(load_dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.load_categories_text = QtWidgets.QLineEdit(load_dialog)
        self.load_categories_text.setObjectName("load_categories_text")
        self.gridLayout.addWidget(self.load_categories_text, 0, 1, 1, 1)
        self.load_categories_label = QtWidgets.QLabel(load_dialog)
        self.load_categories_label.setObjectName("load_categories_label")
        self.gridLayout.addWidget(self.load_categories_label, 0, 0, 1, 1)
        self.load_products_button = QtWidgets.QToolButton(load_dialog)
        self.load_products_button.setObjectName("load_products_button")
        self.gridLayout.addWidget(self.load_products_button, 1, 2, 1, 1)
        self.load_operations_label = QtWidgets.QLabel(load_dialog)
        self.load_operations_label.setObjectName("load_operations_label")
        self.gridLayout.addWidget(self.load_operations_label, 2, 0, 1, 1)
        self.load_products_text = QtWidgets.QLineEdit(load_dialog)
        self.load_products_text.setObjectName("load_products_text")
        self.gridLayout.addWidget(self.load_products_text, 1, 1, 1, 1)
        self.load_operations_button = QtWidgets.QToolButton(load_dialog)
        self.load_operations_button.setObjectName("load_operations_button")
        self.gridLayout.addWidget(self.load_operations_button, 2, 2, 1, 1)
        self.load_button = QtWidgets.QDialogButtonBox(load_dialog)
        self.load_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.load_button.setOrientation(QtCore.Qt.Horizontal)
        self.load_button.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.load_button.setCenterButtons(True)
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 4, 0, 1, 3)
        self.load_operations_text = QtWidgets.QLineEdit(load_dialog)
        self.load_operations_text.setObjectName("load_operations_text")
        self.gridLayout.addWidget(self.load_operations_text, 2, 1, 1, 1)
        self.load_categories_button = QtWidgets.QToolButton(load_dialog)
        self.load_categories_button.setObjectName("load_categories_button")
        self.gridLayout.addWidget(self.load_categories_button, 0, 2, 1, 1)
        self.load_products_label = QtWidgets.QLabel(load_dialog)
        self.load_products_label.setObjectName("load_products_label")
        self.gridLayout.addWidget(self.load_products_label, 1, 0, 1, 1)
        self.load_error = QtWidgets.QLabel(load_dialog)
        self.load_error.setText("")
        self.load_error.setObjectName("load_error")
        self.gridLayout.addWidget(self.load_error, 3, 0, 1, 3)

        self.retranslateUi(load_dialog)
        QtCore.QMetaObject.connectSlotsByName(load_dialog)

    def retranslateUi(self, load_dialog):
        _translate = QtCore.QCoreApplication.translate
        load_dialog.setWindowTitle(_translate("load_dialog", "Wczytywanie danych"))
        self.load_categories_label.setText(_translate("load_dialog", "Kategorie"))
        self.load_products_button.setText(_translate("load_dialog", "..."))
        self.load_operations_label.setText(_translate("load_dialog", "Operacje"))
        self.load_operations_button.setText(_translate("load_dialog", "..."))
        self.load_categories_button.setText(_translate("load_dialog", "..."))
        self.load_products_label.setText(_translate("load_dialog", "Produkty"))

