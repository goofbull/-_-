# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(696, 700)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)

        self.accuracy = QLabel(self.centralwidget)
        self.accuracy.setObjectName(u"accuracy")

        self.gridLayout.addWidget(self.accuracy, 7, 0, 1, 1)

        self.ShowDataButton = QPushButton(self.centralwidget)
        self.ShowDataButton.setObjectName(u"ShowDataButton")

        self.gridLayout.addWidget(self.ShowDataButton, 1, 0, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 8, 1, 1, 1)

        self.ShowDiagramsButton = QPushButton(self.centralwidget)
        self.ShowDiagramsButton.setObjectName(u"ShowDiagramsButton")

        self.gridLayout.addWidget(self.ShowDiagramsButton, 1, 1, 1, 1)

        self.precision = QLabel(self.centralwidget)
        self.precision.setObjectName(u"precision")

        self.gridLayout.addWidget(self.precision, 9, 0, 1, 1)

        self.recall = QLabel(self.centralwidget)
        self.recall.setObjectName(u"recall")

        self.gridLayout.addWidget(self.recall, 7, 1, 1, 1)

        self.ShowResultButton = QPushButton(self.centralwidget)
        self.ShowResultButton.setObjectName(u"ShowResultButton")

        self.gridLayout.addWidget(self.ShowResultButton, 3, 0, 1, 1)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")

        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 2)

        self.ShowReportButton = QPushButton(self.centralwidget)
        self.ShowReportButton.setObjectName(u"ShowReportButton")

        self.gridLayout.addWidget(self.ShowReportButton, 6, 2, 1, 1)

        self.MetricsText = QLabel(self.centralwidget)
        self.MetricsText.setObjectName(u"MetricsText")

        self.gridLayout.addWidget(self.MetricsText, 5, 0, 1, 1)

        self.SaveButton = QPushButton(self.centralwidget)
        self.SaveButton.setObjectName(u"SaveButton")

        self.gridLayout.addWidget(self.SaveButton, 3, 2, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 1, 1, 1)

        self.filename = QLineEdit(self.centralwidget)
        self.filename.setObjectName(u"filename")

        self.gridLayout.addWidget(self.filename, 0, 1, 1, 1)

        self.InputFilenameButton = QPushButton(self.centralwidget)
        self.InputFilenameButton.setObjectName(u"InputFilenameButton")

        self.gridLayout.addWidget(self.InputFilenameButton, 0, 0, 1, 1)

        self.f1_score = QLabel(self.centralwidget)
        self.f1_score.setObjectName(u"f1_score")

        self.gridLayout.addWidget(self.f1_score, 9, 1, 1, 1)

        self.Result = QLabel(self.centralwidget)
        self.Result.setObjectName(u"Result")

        self.gridLayout.addWidget(self.Result, 3, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Accuracy:", None))
        self.accuracy.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ShowDataButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0432\u0435\u0441\u0442\u0438 \u0434\u0430\u043d\u043d\u044b\u0435", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"F1 Score:", None))
        self.ShowDiagramsButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0433\u0440\u0430\u0444\u0438\u043a\u0438", None))
        self.precision.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.recall.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ShowResultButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
        self.ShowReportButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u043e\u0442\u0447\u0435\u0442", None))
        self.MetricsText.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0442\u0440\u0438\u043a\u0438 \u043e\u0446\u0435\u043d\u043a\u0438:", None))
        self.SaveButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Precision:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Recall:", None))
        self.InputFilenameButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0432\u0435\u0441\u0442\u0438 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0444\u0430\u0439\u043b\u0430", None))
        self.f1_score.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.Result.setText(QCoreApplication.translate("MainWindow", u"-", None))
    # retranslateUi

