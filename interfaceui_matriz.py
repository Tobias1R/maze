# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceui_matriz.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1288, 759)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setContextMenuPolicy(Qt.NoContextMenu)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.groupBox.setMinimumSize(QSize(350, 0))
        self.groupBox.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.groupBox)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lb_info_entradas = QLabel(self.frame)
        self.lb_info_entradas.setObjectName(u"lb_info_entradas")
        self.lb_info_entradas.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.lb_info_entradas)

        self.lb_info_saidas = QLabel(self.frame)
        self.lb_info_saidas.setObjectName(u"lb_info_saidas")
        self.lb_info_saidas.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.lb_info_saidas)


        self.verticalLayout.addWidget(self.frame)

        self.controle_executa = QPushButton(self.groupBox)
        self.controle_executa.setObjectName(u"controle_executa")

        self.verticalLayout.addWidget(self.controle_executa)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButton = QToolButton(self.groupBox_2)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout_2.addWidget(self.toolButton)

        self.label222 = QLabel(self.groupBox_2)
        self.label222.setObjectName(u"label222")

        self.horizontalLayout_2.addWidget(self.label222)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.lb_resultado = QLabel(self.groupBox)
        self.lb_resultado.setObjectName(u"lb_resultado")

        self.verticalLayout.addWidget(self.lb_resultado)

        self.lb_progress = QLabel(self.groupBox)
        self.lb_progress.setObjectName(u"lb_progress")

        self.verticalLayout.addWidget(self.lb_progress)

        self.log = QPlainTextEdit(self.groupBox)
        self.log.setObjectName(u"log")
        self.log.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.log.sizePolicy().hasHeightForWidth())
        self.log.setSizePolicy(sizePolicy2)
        self.log.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout.addWidget(self.log)


        self.verticalLayout_2.addWidget(self.groupBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.widgetImagem = QWidget(Form)
        self.widgetImagem.setObjectName(u"widgetImagem")
        sizePolicy2.setHeightForWidth(self.widgetImagem.sizePolicy().hasHeightForWidth())
        self.widgetImagem.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.widgetImagem)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.horizontalLayout.addWidget(self.widgetImagem)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Apollo Teste 2", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Controles", None))
        self.lb_info_entradas.setText("")
        self.lb_info_saidas.setText("")
        self.controle_executa.setText(QCoreApplication.translate("Form", u"Resolver labirinto", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Carregar Labirinto", None))
        self.toolButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.label222.setText(QCoreApplication.translate("Form", u"Selecione arquivo com a matriz", None))
        self.lb_resultado.setText("")
        self.lb_progress.setText(QCoreApplication.translate("Form", u"LOG", None))
    # retranslateUi

