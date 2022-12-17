import sys
import csv
import sqlite3
from math import sin, cos, pi, sqrt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMessageBox, QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog, QTableWidget
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtWidgets import QLabel, QLineEdit, QLCDNumber
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import QPoint, Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.f1 = False
        self.f2 = False
        self.save = []
        self.history = []
        self.hello = QMessageBox(self)
        self.hello.setText('Здравствуйте, уважаемый пользователь!')
        self.hello.exec()
        self.initUI()

    def initUI(self):
        con = sqlite3.connect("figure.db")
        self.setGeometry(300, 300, 700, 800)
        self.setWindowTitle('Фигурное рисование')

        #self.table2()

        self.button_1 = QPushButton(self)
        self.button_1.move(20, 40)
        self.button_1.setText("Выберите фигуру для рисования")
        self.button_1.setStyleSheet('QPushButton {background-color: #FFF0F5}')
        self.button_1.clicked.connect(self.run)

        self.button_2 = QPushButton(self)
        self.button_2.move(20, 80)
        self.button_2.setText("Очистить доску")
        self.button_2.setStyleSheet('QPushButton {background-color: #FFF0F5}')
        self.button_2.clicked.connect(self.clear)

        self.error = QLabel(self)
        self.error.setText("")
        self.error.resize(500, 80)
        self.error.move(30, 115)

        self.desk = QLabel(self)
        self.desk.setText("ДОСКА ДЛЯ РИСОВАНИЯ:")
        self.desk.move(400, 170)

        #для квадрата
        self.sq = QLabel(self)
        self.sq.setText("КВАДРАТ")
        self.sq.move(350, 10)

        self.size1sq = QLabel(self)
        self.size1sq.setText("сторона:")
        self.size1sq.move(350, 40)

        self.size2sq = QLineEdit(self)
        self.size2sq.move(420, 40)
        self.size2sq.resize(70, 20)

        self.rgbsq = QLabel(self)
        self.rgbsq.setText("цвет:")
        self.rgbsq.move(350, 70)

        self.r1sq = QLabel(self)
        self.r1sq.setText("R:")
        self.r1sq.move(400, 70)

        self.r2sq = QLineEdit(self)
        self.r2sq.move(420, 70)
        self.r2sq.resize(50, 20)

        self.g1sq = QLabel(self)
        self.g1sq.setText("G:")
        self.g1sq.move(480, 70)

        self.g2sq = QLineEdit(self)
        self.g2sq.move(500, 70)
        self.g2sq.resize(50, 20)

        self.b1sq = QLabel(self)
        self.b1sq.setText("B:")
        self.b1sq.move(560, 70)

        self.b2sq = QLineEdit(self)
        self.b2sq.move(580, 70)
        self.b2sq.resize(50, 20)

        self.xysq = QLabel(self)
        self.xysq.setText("координаты:")
        self.xysq.move(350, 100)

        self.x1sq = QLabel(self)
        self.x1sq.setText("x:")
        self.x1sq.move(460, 100)

        self.x2sq = QLineEdit(self)
        self.x2sq.move(480, 100)
        self.x2sq.resize(50, 20)

        self.y1sq = QLabel(self)
        self.y1sq.setText("y:")
        self.y1sq.move(540, 100)

        self.y2sq = QLineEdit(self)
        self.y2sq.move(560, 100)
        self.y2sq.resize(50, 20)

        self.buttonsq = QPushButton(self)
        self.buttonsq.move(350, 120)
        self.buttonsq.setText("Создать")
        self.buttonsq.clicked.connect(self.drawsq)

        self.buttonsq2 = QPushButton(self)
        self.buttonsq2.move(500, 120)
        self.buttonsq2.setText("Сохранить")
        self.buttonsq2.clicked.connect(self.savesq)

        self.sq.hide()
        self.size1sq.hide()
        self.size2sq.hide()
        self.rgbsq.hide()
        self.r1sq.hide()
        self.r2sq.hide()
        self.g1sq.hide()
        self.g2sq.hide()
        self.b1sq.hide()
        self.b2sq.hide()
        self.xysq.hide()
        self.x1sq.hide()
        self.x2sq.hide()
        self.y1sq.hide()
        self.y2sq.hide()
        self.buttonsq.hide()
        self.buttonsq2.hide()

        #ДЛЯ КРУГА
        self.ci = QLabel(self)
        self.ci.setText("КРУГ")
        self.ci.move(350, 10)

        self.size1ci = QLabel(self)
        self.size1ci.setText("диаметр:")
        self.size1ci.move(350, 40)

        self.size2ci = QLineEdit(self)
        self.size2ci.move(420, 40)
        self.size2ci.resize(70, 20)

        self.rgbci = QLabel(self)
        self.rgbci.setText("цвет:")
        self.rgbci.move(350, 70)

        self.r1ci = QLabel(self)
        self.r1ci.setText("R:")
        self.r1ci.move(400, 70)

        self.r2ci = QLineEdit(self)
        self.r2ci.move(420, 70)
        self.r2ci.resize(50, 20)

        self.g1ci = QLabel(self)
        self.g1ci.setText("G:")
        self.g1ci.move(480, 70)

        self.g2ci = QLineEdit(self)
        self.g2ci.move(500, 70)
        self.g2ci.resize(50, 20)

        self.b1ci = QLabel(self)
        self.b1ci.setText("B:")
        self.b1ci.move(560, 70)

        self.b2ci = QLineEdit(self)
        self.b2ci.move(580, 70)
        self.b2ci.resize(50, 20)

        self.xyci = QLabel(self)
        self.xyci.setText("координаты:")
        self.xyci.move(350, 100)

        self.x1ci = QLabel(self)
        self.x1ci.setText("x:")
        self.x1ci.move(460, 100)

        self.x2ci = QLineEdit(self)
        self.x2ci.move(480, 100)
        self.x2ci.resize(50, 20)

        self.y1ci = QLabel(self)
        self.y1ci.setText("y:")
        self.y1ci.move(540, 100)

        self.y2ci = QLineEdit(self)
        self.y2ci.move(560, 100)
        self.y2ci.resize(50, 20)

        self.buttonci = QPushButton(self)
        self.buttonci.move(350, 120)
        self.buttonci.setText("Создать")
        self.buttonci.clicked.connect(self.drawci)

        self.buttonci2 = QPushButton(self)
        self.buttonci2.move(500, 120)
        self.buttonci2.setText("Сохранить")
        self.buttonci2.clicked.connect(self.saveci)

        self.ci.hide()
        self.size1ci.hide()
        self.size2ci.hide()
        self.rgbci.hide()
        self.r1ci.hide()
        self.r2ci.hide()
        self.g1ci.hide()
        self.g2ci.hide()
        self.b1ci.hide()
        self.b2ci.hide()
        self.xyci.hide()
        self.x1ci.hide()
        self.x2ci.hide()
        self.y1ci.hide()
        self.y2ci.hide()
        self.buttonci.hide()
        self.buttonci2.hide()

        #для прямоугольника
        self.re = QLabel(self)
        self.re.setText("ПРЯМОУГОЛЬНИК")
        self.re.move(350, 10)

        self.size1re = QLabel(self)
        self.size1re.setText("длина:")
        self.size1re.move(350, 40)

        self.size2re = QLineEdit(self)
        self.size2re.move(420, 40)
        self.size2re.resize(70, 20)

        self.size3re = QLabel(self)
        self.size3re.setText("высота:")
        self.size3re.move(500, 40)

        self.size4re = QLineEdit(self)
        self.size4re.move(570, 40)
        self.size4re.resize(70, 20)

        self.rgbre = QLabel(self)
        self.rgbre.setText("цвет:")
        self.rgbre.move(350, 70)

        self.r1re = QLabel(self)
        self.r1re.setText("R:")
        self.r1re.move(400, 70)

        self.r2re = QLineEdit(self)
        self.r2re.move(420, 70)
        self.r2re.resize(50, 20)

        self.g1re = QLabel(self)
        self.g1re.setText("G:")
        self.g1re.move(480, 70)

        self.g2re = QLineEdit(self)
        self.g2re.move(500, 70)
        self.g2re.resize(50, 20)

        self.b1re = QLabel(self)
        self.b1re.setText("B:")
        self.b1re.move(560, 70)

        self.b2re = QLineEdit(self)
        self.b2re.move(580, 70)
        self.b2re.resize(50, 20)

        self.xyre = QLabel(self)
        self.xyre.setText("координаты:")
        self.xyre.move(350, 100)

        self.x1re = QLabel(self)
        self.x1re.setText("x:")
        self.x1re.move(460, 100)

        self.x2re = QLineEdit(self)
        self.x2re.move(480, 100)
        self.x2re.resize(50, 20)

        self.y1re = QLabel(self)
        self.y1re.setText("y:")
        self.y1re.move(540, 100)

        self.y2re = QLineEdit(self)
        self.y2re.move(560, 100)
        self.y2re.resize(50, 20)

        self.buttonre = QPushButton(self)
        self.buttonre.move(350, 120)
        self.buttonre.setText("Создать")
        self.buttonre.clicked.connect(self.drawre)

        self.buttonre2 = QPushButton(self)
        self.buttonre2.move(500, 120)
        self.buttonre2.setText("Сохранить")
        self.buttonre2.clicked.connect(self.savere)

        self.re.hide()
        self.size1re.hide()
        self.size2re.hide()
        self.size3re.hide()
        self.size4re.hide()
        self.rgbre.hide()
        self.r1re.hide()
        self.r2re.hide()
        self.g1re.hide()
        self.g2re.hide()
        self.b1re.hide()
        self.b2re.hide()
        self.xyre.hide()
        self.x1re.hide()
        self.x2re.hide()
        self.y1re.hide()
        self.y2re.hide()
        self.buttonre.hide()
        self.buttonre2.hide()

        #для треугольника
        self.tr = QLabel(self)
        self.tr.setText("ТРЕУГОЛЬНИК")
        self.tr.move(350, 10)

        self.size1tr = QLabel(self)
        self.size1tr.setText("сторона:")
        self.size1tr.move(350, 40)

        self.size2tr = QLineEdit(self)
        self.size2tr.move(420, 40)
        self.size2tr.resize(70, 20)

        self.rgbtr = QLabel(self)
        self.rgbtr.setText("цвет:")
        self.rgbtr.move(350, 70)

        self.r1tr = QLabel(self)
        self.r1tr.setText("R:")
        self.r1tr.move(400, 70)

        self.r2tr = QLineEdit(self)
        self.r2tr.move(420, 70)
        self.r2tr.resize(50, 20)

        self.g1tr = QLabel(self)
        self.g1tr.setText("G:")
        self.g1tr.move(480, 70)

        self.g2tr = QLineEdit(self)
        self.g2tr.move(500, 70)
        self.g2tr.resize(50, 20)

        self.b1tr = QLabel(self)
        self.b1tr.setText("B:")
        self.b1tr.move(560, 70)

        self.b2tr = QLineEdit(self)
        self.b2tr.move(580, 70)
        self.b2tr.resize(50, 20)

        self.xytr = QLabel(self)
        self.xytr.setText("координаты:")
        self.xytr.move(350, 100)

        self.x1tr = QLabel(self)
        self.x1tr.setText("x:")
        self.x1tr.move(460, 100)

        self.x2tr = QLineEdit(self)
        self.x2tr.move(480, 100)
        self.x2tr.resize(50, 20)

        self.y1tr = QLabel(self)
        self.y1tr.setText("y:")
        self.y1tr.move(540, 100)

        self.y2tr = QLineEdit(self)
        self.y2tr.move(560, 100)
        self.y2tr.resize(50, 20)

        self.buttontr = QPushButton(self)
        self.buttontr.move(350, 120)
        self.buttontr.setText("Создать")
        self.buttontr.clicked.connect(self.drawtr)

        self.buttontr2 = QPushButton(self)
        self.buttontr2.move(500, 120)
        self.buttontr2.setText("Сохранить")
        self.buttontr2.clicked.connect(self.savetr)

        self.tr.hide()
        self.size1tr.hide()
        self.size2tr.hide()
        self.rgbtr.hide()
        self.r1tr.hide()
        self.r2tr.hide()
        self.g1tr.hide()
        self.g2tr.hide()
        self.b1tr.hide()
        self.b2tr.hide()
        self.xytr.hide()
        self.x1tr.hide()
        self.x2tr.hide()
        self.y1tr.hide()
        self.y2tr.hide()
        self.buttontr.hide()
        self.buttontr2.hide()

        # для n-угольника
        self.po = QLabel(self)
        self.po.setText("-УГОЛЬНИК")
        self.po.move(400, 10)

        self.n2po = QLineEdit(self)
        self.n2po.move(350, 10)
        self.n2po.resize(50, 20)

        self.size1po = QLabel(self)
        self.size1po.setText("сторона:")
        self.size1po.move(350, 40)

        self.size2po = QLineEdit(self)
        self.size2po.move(420, 40)
        self.size2po.resize(70, 20)

        self.rgbpo = QLabel(self)
        self.rgbpo.setText("цвет:")
        self.rgbpo.move(350, 70)

        self.r1po = QLabel(self)
        self.r1po.setText("R:")
        self.r1po.move(400, 70)

        self.r2po = QLineEdit(self)
        self.r2po.move(420, 70)
        self.r2po.resize(50, 20)

        self.g1po = QLabel(self)
        self.g1po.setText("G:")
        self.g1po.move(480, 70)

        self.g2po = QLineEdit(self)
        self.g2po.move(500, 70)
        self.g2po.resize(50, 20)

        self.b1po = QLabel(self)
        self.b1po.setText("B:")
        self.b1po.move(560, 70)

        self.b2po = QLineEdit(self)
        self.b2po.move(580, 70)
        self.b2po.resize(50, 20)

        self.xypo = QLabel(self)
        self.xypo.setText("координаты:")
        self.xypo.move(350, 100)

        self.x1po = QLabel(self)
        self.x1po.setText("x:")
        self.x1po.move(460, 100)

        self.x2po = QLineEdit(self)
        self.x2po.move(480, 100)
        self.x2po.resize(50, 20)

        self.y1po = QLabel(self)
        self.y1po.setText("y:")
        self.y1po.move(540, 100)

        self.y2po = QLineEdit(self)
        self.y2po.move(560, 100)
        self.y2po.resize(50, 20)

        self.buttonpo = QPushButton(self)
        self.buttonpo.move(350, 120)
        self.buttonpo.setText("Создать")
        self.buttonpo.clicked.connect(self.drawpo)

        self.buttonpo2 = QPushButton(self)
        self.buttonpo2.move(500, 120)
        self.buttonpo2.setText("Сохранить")
        self.buttonpo2.clicked.connect(self.savepo)

        self.po.hide()
        self.n2po.hide()
        self.size1po.hide()
        self.size2po.hide()
        self.rgbpo.hide()
        self.r1po.hide()
        self.r2po.hide()
        self.g1po.hide()
        self.g2po.hide()
        self.b1po.hide()
        self.b2po.hide()
        self.xypo.hide()
        self.x1po.hide()
        self.x2po.hide()
        self.y1po.hide()
        self.y2po.hide()
        self.buttonpo.hide()
        self.buttonpo2.hide()

    def clear(self):
        self.f, ok_pressed = QInputDialog.getItem(
            self, "Стирание", "Вы точно хотите очистить доску?",
            ("да", "нет"), 0, False)
        if ok_pressed:
            if self.f == "да":
                self.f2 = True
            else:
                self.f2 = False

    def clear2(self, qp):
        self.history = []
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(0, 200, 700, 800)

    def run(self):
        self.f1 = True
        self.figure, ok_pressed = QInputDialog.getItem(
            self, "Выберите фигуру для рисования", "ФИГУРА",
            ("квадрат", "круг", "прямоугольник", "треугольник", "n-угольник"), 0, False)

        if ok_pressed:
            if self.figure == "квадрат":
                self.sq.show()
                self.size1sq.show()
                self.size2sq.show()
                self.rgbsq.show()
                self.r1sq.show()
                self.r2sq.show()
                self.g1sq.show()
                self.g2sq.show()
                self.b1sq.show()
                self.b2sq.show()
                self.xysq.show()
                self.x1sq.show()
                self.x2sq.show()
                self.y1sq.show()
                self.y2sq.show()
                self.buttonsq.show()
                self.buttonsq2.show()

                self.ci.hide()
                self.size1ci.hide()
                self.size2ci.hide()
                self.rgbci.hide()
                self.r1ci.hide()
                self.r2ci.hide()
                self.g1ci.hide()
                self.g2ci.hide()
                self.b1ci.hide()
                self.b2ci.hide()
                self.xyci.hide()
                self.x1ci.hide()
                self.x2ci.hide()
                self.y1ci.hide()
                self.y2ci.hide()
                self.buttonci.hide()
                self.buttonci2.hide()

                self.re.hide()
                self.size1re.hide()
                self.size2re.hide()
                self.size3re.hide()
                self.size4re.hide()
                self.rgbre.hide()
                self.r1re.hide()
                self.r2re.hide()
                self.g1re.hide()
                self.g2re.hide()
                self.b1re.hide()
                self.b2re.hide()
                self.xyre.hide()
                self.x1re.hide()
                self.x2re.hide()
                self.y1re.hide()
                self.y2re.hide()
                self.buttonre.hide()
                self.buttonre2.hide()

                self.tr.hide()
                self.size1tr.hide()
                self.size2tr.hide()
                self.rgbtr.hide()
                self.r1tr.hide()
                self.r2tr.hide()
                self.g1tr.hide()
                self.g2tr.hide()
                self.b1tr.hide()
                self.b2tr.hide()
                self.xytr.hide()
                self.x1tr.hide()
                self.x2tr.hide()
                self.y1tr.hide()
                self.y2tr.hide()
                self.buttontr.hide()
                self.buttontr2.hide()

                self.po.hide()
                self.n2po.hide()
                self.size1po.hide()
                self.size2po.hide()
                self.rgbpo.hide()
                self.r1po.hide()
                self.r2po.hide()
                self.g1po.hide()
                self.g2po.hide()
                self.b1po.hide()
                self.b2po.hide()
                self.xypo.hide()
                self.x1po.hide()
                self.x2po.hide()
                self.y1po.hide()
                self.y2po.hide()
                self.buttonpo.hide()
                self.buttonpo2.hide()

            if self.figure == "круг":
                self.ci.show()
                self.size1ci.show()
                self.size2ci.show()
                self.rgbci.show()
                self.r1ci.show()
                self.r2ci.show()
                self.g1ci.show()
                self.g2ci.show()
                self.b1ci.show()
                self.b2ci.show()
                self.xyci.show()
                self.x1ci.show()
                self.x2ci.show()
                self.y1ci.show()
                self.y2ci.show()
                self.buttonci.show()
                self.buttonci2.show()

                self.sq.hide()
                self.size1sq.hide()
                self.size2sq.hide()
                self.rgbsq.hide()
                self.r1sq.hide()
                self.r2sq.hide()
                self.g1sq.hide()
                self.g2sq.hide()
                self.b1sq.hide()
                self.b2sq.hide()
                self.xysq.hide()
                self.x1sq.hide()
                self.x2sq.hide()
                self.y1sq.hide()
                self.y2sq.hide()
                self.buttonsq.hide()
                self.buttonsq2.hide()

                self.re.hide()
                self.size1re.hide()
                self.size2re.hide()
                self.size3re.hide()
                self.size4re.hide()
                self.rgbre.hide()
                self.r1re.hide()
                self.r2re.hide()
                self.g1re.hide()
                self.g2re.hide()
                self.b1re.hide()
                self.b2re.hide()
                self.xyre.hide()
                self.x1re.hide()
                self.x2re.hide()
                self.y1re.hide()
                self.y2re.hide()
                self.buttonre.hide()
                self.buttonre2.hide()

                self.tr.hide()
                self.size1tr.hide()
                self.size2tr.hide()
                self.rgbtr.hide()
                self.r1tr.hide()
                self.r2tr.hide()
                self.g1tr.hide()
                self.g2tr.hide()
                self.b1tr.hide()
                self.b2tr.hide()
                self.xytr.hide()
                self.x1tr.hide()
                self.x2tr.hide()
                self.y1tr.hide()
                self.y2tr.hide()
                self.buttontr.hide()
                self.buttontr2.hide()

                self.po.hide()
                self.n2po.hide()
                self.size1po.hide()
                self.size2po.hide()
                self.rgbpo.hide()
                self.r1po.hide()
                self.r2po.hide()
                self.g1po.hide()
                self.g2po.hide()
                self.b1po.hide()
                self.b2po.hide()
                self.xypo.hide()
                self.x1po.hide()
                self.x2po.hide()
                self.y1po.hide()
                self.y2po.hide()
                self.buttonpo.hide()
                self.buttonpo2.hide()

            if self.figure == "прямоугольник":
                self.re.show()
                self.size1re.show()
                self.size2re.show()
                self.size3re.show()
                self.size4re.show()
                self.rgbre.show()
                self.r1re.show()
                self.r2re.show()
                self.g1re.show()
                self.g2re.show()
                self.b1re.show()
                self.b2re.show()
                self.xyre.show()
                self.x1re.show()
                self.x2re.show()
                self.y1re.show()
                self.y2re.show()
                self.buttonre.show()
                self.buttonre2.show()

                self.sq.hide()
                self.size1sq.hide()
                self.size2sq.hide()
                self.rgbsq.hide()
                self.r1sq.hide()
                self.r2sq.hide()
                self.g1sq.hide()
                self.g2sq.hide()
                self.b1sq.hide()
                self.b2sq.hide()
                self.xysq.hide()
                self.x1sq.hide()
                self.x2sq.hide()
                self.y1sq.hide()
                self.y2sq.hide()
                self.buttonsq.hide()
                self.buttonsq2.hide()

                self.ci.hide()
                self.size1ci.hide()
                self.size2ci.hide()
                self.rgbci.hide()
                self.r1ci.hide()
                self.r2ci.hide()
                self.g1ci.hide()
                self.g2ci.hide()
                self.b1ci.hide()
                self.b2ci.hide()
                self.xyci.hide()
                self.x1ci.hide()
                self.x2ci.hide()
                self.y1ci.hide()
                self.y2ci.hide()
                self.buttonci.hide()
                self.buttonci2.hide()

                self.tr.hide()
                self.size1tr.hide()
                self.size2tr.hide()
                self.rgbtr.hide()
                self.r1tr.hide()
                self.r2tr.hide()
                self.g1tr.hide()
                self.g2tr.hide()
                self.b1tr.hide()
                self.b2tr.hide()
                self.xytr.hide()
                self.x1tr.hide()
                self.x2tr.hide()
                self.y1tr.hide()
                self.y2tr.hide()
                self.buttontr.hide()
                self.buttontr2.hide()

                self.po.hide()
                self.n2po.hide()
                self.size1po.hide()
                self.size2po.hide()
                self.rgbpo.hide()
                self.r1po.hide()
                self.r2po.hide()
                self.g1po.hide()
                self.g2po.hide()
                self.b1po.hide()
                self.b2po.hide()
                self.xypo.hide()
                self.x1po.hide()
                self.x2po.hide()
                self.y1po.hide()
                self.y2po.hide()
                self.buttonpo.hide()
                self.buttonpo2.hide()

            if self.figure == "треугольник":
                self.tr.show()
                self.size1tr.show()
                self.size2tr.show()
                self.rgbtr.show()
                self.r1tr.show()
                self.r2tr.show()
                self.g1tr.show()
                self.g2tr.show()
                self.b1tr.show()
                self.b2tr.show()
                self.xytr.show()
                self.x1tr.show()
                self.x2tr.show()
                self.y1tr.show()
                self.y2tr.show()
                self.buttontr.show()
                self.buttontr2.show()

                self.sq.hide()
                self.size1sq.hide()
                self.size2sq.hide()
                self.rgbsq.hide()
                self.r1sq.hide()
                self.r2sq.hide()
                self.g1sq.hide()
                self.g2sq.hide()
                self.b1sq.hide()
                self.b2sq.hide()
                self.xysq.hide()
                self.x1sq.hide()
                self.x2sq.hide()
                self.y1sq.hide()
                self.y2sq.hide()
                self.buttonsq.hide()
                self.buttonsq2.hide()

                self.ci.hide()
                self.size1ci.hide()
                self.size2ci.hide()
                self.rgbci.hide()
                self.r1ci.hide()
                self.r2ci.hide()
                self.g1ci.hide()
                self.g2ci.hide()
                self.b1ci.hide()
                self.b2ci.hide()
                self.xyci.hide()
                self.x1ci.hide()
                self.x2ci.hide()
                self.y1ci.hide()
                self.y2ci.hide()
                self.buttonci.hide()
                self.buttonci2.hide()

                self.re.hide()
                self.size1re.hide()
                self.size2re.hide()
                self.size3re.hide()
                self.size4re.hide()
                self.rgbre.hide()
                self.r1re.hide()
                self.r2re.hide()
                self.g1re.hide()
                self.g2re.hide()
                self.b1re.hide()
                self.b2re.hide()
                self.xyre.hide()
                self.x1re.hide()
                self.x2re.hide()
                self.y1re.hide()
                self.y2re.hide()
                self.buttonre.hide()
                self.buttonre2.hide()

                self.po.hide()
                self.n2po.hide()
                self.size1po.hide()
                self.size2po.hide()
                self.rgbpo.hide()
                self.r1po.hide()
                self.r2po.hide()
                self.g1po.hide()
                self.g2po.hide()
                self.b1po.hide()
                self.b2po.hide()
                self.xypo.hide()
                self.x1po.hide()
                self.x2po.hide()
                self.y1po.hide()
                self.y2po.hide()
                self.buttonpo.hide()
                self.buttonpo2.hide()

            if self.figure == "n-угольник":
                self.po.show()
                self.n2po.show()
                self.size1po.show()
                self.size2po.show()
                self.rgbpo.show()
                self.r1po.show()
                self.r2po.show()
                self.g1po.show()
                self.g2po.show()
                self.b1po.show()
                self.b2po.show()
                self.xypo.show()
                self.x1po.show()
                self.x2po.show()
                self.y1po.show()
                self.y2po.show()
                self.buttonpo.show()
                self.buttonpo2.show()

                self.sq.hide()
                self.size1sq.hide()
                self.size2sq.hide()
                self.rgbsq.hide()
                self.r1sq.hide()
                self.r2sq.hide()
                self.g1sq.hide()
                self.g2sq.hide()
                self.b1sq.hide()
                self.b2sq.hide()
                self.xysq.hide()
                self.x1sq.hide()
                self.x2sq.hide()
                self.y1sq.hide()
                self.y2sq.hide()
                self.buttonsq.hide()
                self.buttonsq2.hide()

                self.ci.hide()
                self.size1ci.hide()
                self.size2ci.hide()
                self.rgbci.hide()
                self.r1ci.hide()
                self.r2ci.hide()
                self.g1ci.hide()
                self.g2ci.hide()
                self.b1ci.hide()
                self.b2ci.hide()
                self.xyci.hide()
                self.x1ci.hide()
                self.x2ci.hide()
                self.y1ci.hide()
                self.y2ci.hide()
                self.buttonci.hide()
                self.buttonci2.hide()

                self.re.hide()
                self.size1re.hide()
                self.size2re.hide()
                self.size3re.hide()
                self.size4re.hide()
                self.rgbre.hide()
                self.r1re.hide()
                self.r2re.hide()
                self.g1re.hide()
                self.g2re.hide()
                self.b1re.hide()
                self.b2re.hide()
                self.xyre.hide()
                self.x1re.hide()
                self.x2re.hide()
                self.y1re.hide()
                self.y2re.hide()
                self.buttonre.hide()
                self.buttonre2.hide()

                self.tr.hide()
                self.size1tr.hide()
                self.size2tr.hide()
                self.rgbtr.hide()
                self.r1tr.hide()
                self.r2tr.hide()
                self.g1tr.hide()
                self.g2tr.hide()
                self.b1tr.hide()
                self.b2tr.hide()
                self.xytr.hide()
                self.x1tr.hide()
                self.x2tr.hide()
                self.y1tr.hide()
                self.y2tr.hide()
                self.buttontr.hide()
                self.buttontr2.hide()

    def drawsq(self):
        try:
            int(self.size2sq.text())
            int(self.r2sq.text())
            int(self.g2sq.text())
            int(self.b2sq.text())
            int(self.x2sq.text())
            int(self.y2sq.text())
        except Exception:
            self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nвсе данные должны являться \nцелыми числами")
        try:
            a = "1"
            self.er = 0
            if (self.size2sq.text() == "" or self.r2sq.text() == "" or
                    self.g2sq.text() == "" or self.b2sq.text() == "" or
                    self.x2sq.text() == "" or self.y2sq.text() == ""):
                self.er = 1
                a += "a"
            elif int(self.size2sq.text()) <= 0:
                self.er = 3
                a += "a"
            elif (int(self.r2sq.text()) < 0 or int(self.r2sq.text()) > 255 or
                  int(self.g2sq.text()) < 0 or int(self.g2sq.text()) > 255 or
                  int(self.b2sq.text()) < 0 or int(self.b2sq.text()) > 255):
                self.er = 4
                a += "a"
            elif int(self.x2sq.text()) < 0 or int(self.y2sq.text()) < 0:
                self.er = 5
                a += "a"
            b = int(a)
        except Exception:
            if self.er == 1:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nне все данные заполнены")
            elif self.er == 3:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nразмер фигуры не может иметь \nотрицательное значение или \nравняться нулю")
            elif self.er == 4:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nr, g, b должны быть в диапозоне \nот 0 до 255")
            elif self.er == 5:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкоординаты должны быть >= 0")
        else:
            self.error.setText("")
            self.flag = True
            self.repaint()
            self.er = 0

    def drawci(self):
        try:
            int(self.size2ci.text())
            int(self.r2ci.text())
            int(self.g2ci.text())
            int(self.b2ci.text())
            int(self.x2ci.text())
            int(self.y2ci.text())
        except Exception:
            self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nвсе данные должны являться \nцелыми числами")
        try:
            a = "1"
            self.er = 0
            if (self.size2ci.text() == "" or self.r2ci.text() == "" or
                    self.g2ci.text() == "" or self.b2ci.text() == "" or
                    self.x2ci.text() == "" or self.y2ci.text() == ""):
                self.er = 1
                a += "a"
            elif int(self.size2ci.text()) <= 0:
                self.er = 3
                a += "a"
            elif (int(self.r2ci.text()) < 0 or int(self.r2ci.text()) > 255 or
                  int(self.g2ci.text()) < 0 or int(self.g2ci.text()) > 255 or
                  int(self.b2ci.text()) < 0 or int(self.b2ci.text()) > 255):
                self.er = 4
                a += "a"
            elif int(self.x2ci.text()) < 0 or int(self.y2ci.text()) < 0:
                self.er = 5
                a += "a"
            b = int(a)
        except Exception:
            if self.er == 1:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nне все данные заполнены")
            elif self.er == 3:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nразмер фигуры не может иметь \nотрицательное значение или \nравняться нулю")
            elif self.er == 4:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nr, g, b должны быть в диапозоне \nот 0 до 255")
            elif self.er == 5:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкоординаты должны быть >= 0")
        else:
            self.error.setText("")
            self.flag = True
            self.repaint()
            self.er = 0

    def drawre(self):
        try:
            int(self.size2re.text())
            int(self.size4re.text())
            int(self.r2re.text())
            int(self.g2re.text())
            int(self.b2re.text())
            int(self.x2re.text())
            int(self.y2re.text())
        except Exception:
            self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nвсе данные должны являться \nцелыми числами")
        try:
            a = "1"
            self.er = 0
            if (self.size2re.text() == "" or self.size4re.text() == "" or
                    self.r2re.text() == "" or self.g2re.text() == "" or
                    self.b2re.text() == "" or self.x2re.text() == "" or self.y2re.text() == ""):
                self.er = 1
                a += "a"
            elif int(self.size2re.text()) <= 0 or int(self.size4re.text()) <= 0:
                self.er = 3
                a += "a"
            elif (int(self.r2re.text()) < 0 or int(self.r2re.text()) > 255 or
                  int(self.g2re.text()) < 0 or int(self.g2re.text()) > 255 or
                  int(self.b2re.text()) < 0 or int(self.b2re.text()) > 255):
                self.er = 4
                a += "a"
            elif int(self.x2re.text()) < 0 or int(self.y2re.text()) < 0:
                self.er = 5
                a += "a"
            b = int(a)
        except Exception:
            if self.er == 1:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nне все данные заполнены")
            elif self.er == 3:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nразмер фигуры не может иметь \nотрицательное значение или \nравняться нулю")
            elif self.er == 4:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nr, g, b должны быть в диапозоне \nот 0 до 255")
            elif self.er == 5:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкоординаты должны быть >= 0")
        else:
            self.error.setText("")
            self.flag = True
            self.repaint()
            self.er = 0

    def drawtr(self):
        try:
            int(self.size2tr.text())
            int(self.r2tr.text())
            int(self.g2tr.text())
            int(self.b2tr.text())
            int(self.x2tr.text())
            int(self.y2tr.text())
        except Exception:
            self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nвсе данные должны являться \nцелыми числами")
        try:
            a = "1"
            self.er = 0
            if (self.size2tr.text() == "" or self.r2tr.text() == "" or self.g2tr.text() == "" or
                    self.b2tr.text() == "" or self.x2tr.text() == "" or self.y2tr.text() == ""):
                self.er = 1
                a += "a"
            elif int(self.size2tr.text()) <= 0:
                self.er = 3
                a += "a"
            elif (int(self.r2tr.text()) < 0 or int(self.r2tr.text()) > 255 or
                  int(self.g2tr.text()) < 0 or int(self.g2tr.text()) > 255 or
                  int(self.b2tr.text()) < 0 or int(self.b2tr.text()) > 255):
                self.er = 4
                a += "a"
            elif int(self.x2tr.text()) < 0 or int(self.y2tr.text()) < 0:
                self.er = 5
                a += "a"
            b = int(a)
        except Exception:
            if self.er == 1:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nне все данные заполнены")
            elif self.er == 3:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nразмер фигуры не может иметь \nотрицательное значение или \nравняться нулю")
            elif self.er == 4:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nr, g, b должны быть в диапозоне \nот 0 до 255")
            elif self.er == 5:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкоординаты должны быть >= 0")
        else:
            self.error.setText("")
            self.flag = True
            self.repaint()
            self.er = 0

    def drawpo(self):
        try:
            int(self.size2po.text())
            int(self.n2po.text())
            int(self.r2po.text())
            int(self.g2po.text())
            int(self.b2po.text())
            int(self.x2po.text())
            int(self.y2po.text())
        except Exception:
            self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nвсе данные должны являться \nцелыми числами")
        try:
            a = "1"
            self.er = 0
            if (self.size2po.text() == "" or self.n2po.text() == "" or self.r2po.text() == "" or self.g2po.text() == "" or
                    self.b2po.text() == "" or self.x2po.text() == "" or self.y2po.text() == ""):
                self.er = 1
                a += "a"
            elif int(self.n2po.text()) <= 2:
                self.er = 2
                a += "a"
            elif int(self.size2po.text()) <= 0:
                self.er = 3
                a += "a"
            elif (int(self.r2po.text()) < 0 or int(self.r2po.text()) > 255 or
                  int(self.g2po.text()) < 0 or int(self.g2po.text()) > 255 or
                  int(self.b2po.text()) < 0 or int(self.b2po.text()) > 255):
                self.er = 4
                a += "a"
            elif int(self.x2po.text()) < 0 or int(self.y2po.text()) < 0:
                self.er = 5
                a += "a"
            b = int(a)
        except Exception:
            if self.er == 1:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nне все данные заполнены")
            elif self.er == 2:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкол-во сторон должно быть >= 3")
            elif self.er == 3:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nразмер фигуры не может иметь \nотрицательное значение или \nравняться нулю")
            elif self.er == 4:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nr, g, b должны быть в диапозоне \nот 0 до 255")
            elif self.er == 5:
                self.error.setText("СООБЩЕНИЕ ОБ ОШИБКЕ: \nкоординаты должны быть >= 0")
        else:
            self.error.setText("")
            self.flag = True
            self.repaint()
            self.er = 0

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 200, 700, 800)
        painter.drawLine(0, 200, 700, 200)
        painter.drawLine(300, 0, 300, 200)
        painter.setBrush(QColor(216, 191, 216))
        painter.drawRect(0, 0, 300, 200)
        painter.setBrush(QColor(176, 196, 222))
        painter.drawRect(300, 0, 400, 200)
        qp = QPainter()
        qp.begin(self)
        if self.f1:
            self.draw(qp)
        if self.f2:
            self.clear2(qp)
            self.f2 = False
        #if self.f3:
            #self.table2()
        if self.flag:
            if self.figure == "квадрат":
                self.drawsq1(qp)
            if self.figure == "круг":
                self.drawci1(qp)
            if self.figure == "прямоугольник":
                self.drawre1(qp)
            if self.figure == "треугольник":
                self.drawtr1(qp)
            if self.figure == "n-угольник":
                self.drawpo1(qp)
        qp.end()

    def draw(self, qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        #else:
            #qp.setBrush(QColor(255, 255, 255))
            #qp.drawRect(0, 200, 700, 800)

    def drawsq1(self, qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        if self.flag:
            x = int(self.x2sq.text())
            y = int(self.y2sq.text())
            R = int(self.r2sq.text())
            G = int(self.g2sq.text())
            B = int(self.b2sq.text())
            qp.setBrush(QColor(R, G, B))
            qp.drawRect(x, y + 200, int(self.size2sq.text()), int(self.size2sq.text()))
        self.flag = False
        self.history.append(["квадрат", int(self.size2sq.text()), R, G, B, x, y])

    def drawci1(self, qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        if self.flag:
            x = int(self.x2ci.text())
            y = int(self.y2ci.text())
            R = int(self.r2ci.text())
            G = int(self.g2ci.text())
            B = int(self.b2ci.text())
            qp.setBrush(QColor(R, G, B))
            qp.drawEllipse(x, y + 200, int(self.size2ci.text()), int(self.size2ci.text()))
        self.flag = False
        self.history.append(["круг", int(self.size2ci.text()), R, G, B, x, y])

    def drawre1(self, qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        if self.flag:
            x = int(self.x2re.text())
            y = int(self.y2re.text())
            R = int(self.r2re.text())
            G = int(self.g2re.text())
            B = int(self.b2re.text())
            qp.setBrush(QColor(R, G, B))
            qp.drawRect(x, y + 200, int(self.size2re.text()), int(self.size4re.text()))
        self.flag = False
        self.history.append(["прямоугольник", int(self.size2re.text()), int(self.size4re.text()), R, G, B, x, y])

    def drawtr1(self, qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        R = int(self.r2tr.text())
        G = int(self.g2tr.text())
        B = int(self.b2tr.text())
        if self.flag:
            x = int(self.x2tr.text())
            y = int(self.y2tr.text())
            s = int(self.size2tr.text())
            rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
            nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                      rad * sin(i * 2 * pi / 3 + pi / 2))
                     for i in range(3)]
            nodes2 = [QPoint(int(node[0] + x),
                       int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
            points = QPolygon(nodes2)
            qp.setBrush(QColor(R, G, B))
            qp.drawPolygon(points)
        self.flag = False
        self.history.append(["треугольник", s, R, G, B, x, y])

    def drawpo1(self,qp):
        if self.history:
            for elem in self.history:
                if elem[0] == "квадрат":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawRect(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "круг":
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawEllipse(int(elem[5]), int(elem[6]) + 200, int(elem[1]), int(elem[1]))
                elif elem[0] == "прямоугольник":
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawRect(int(elem[6]), int(elem[7]) + 200, int(elem[1]), int(elem[2]))
                elif elem[0] == "треугольник":
                    x = int(elem[5])
                    y = int(elem[6])
                    s = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / 3)))
                    nodes = [(rad * cos(i * 2 * pi / 3 + pi / 2),
                              rad * sin(i * 2 * pi / 3 + pi / 2))
                             for i in range(3)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / 3)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[2]), int(elem[3]), int(elem[4])))
                    qp.drawPolygon(points)
                elif elem[0] == "n-угольник":
                    x = int(elem[6])
                    y = int(elem[7])
                    s = int(elem[2])
                    n = int(elem[1])
                    rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
                    nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                              rad * sin(i * 2 * pi / n + pi / 2))
                             for i in range(n)]
                    nodes2 = [QPoint(int(node[0] + x),
                                     int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
                    points = QPolygon(nodes2)
                    qp.setBrush(QColor(int(elem[3]), int(elem[4]), int(elem[5])))
                    qp.drawPolygon(points)
        R = int(self.r2po.text())
        G = int(self.g2po.text())
        B = int(self.b2po.text())
        if self.flag:
            x = int(self.x2po.text())
            y = int(self.y2po.text())
            s = int(self.size2po.text())
            n = int(self.n2po.text())
            rad = s / sqrt(2 * (1 - cos(2 * pi / n)))
            nodes = [(rad * cos(i * 2 * pi / n + pi / 2),
                      rad * sin(i * 2 * pi / n + pi / 2))
                     for i in range(n)]
            nodes2 = [QPoint(int(node[0] + x),
                       int(y - node[1] + s / sqrt(2 * (1 - cos(2 * pi / n)))) + 200) for node in nodes]
            points = QPolygon(nodes2)
            qp.setBrush(QColor(R, G, B))
            qp.drawPolygon(points)
        self.flag = False
        self.history.append(["n-угольник", n, s, R, G, B, x, y])

    def savesq(self):
        col = ["фигура", "размер", "цвет", "координаты"]
        with open('figure.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';')
            writer.writerow(col)
            line = []
            line.append("квадрат")
            line.append(int(self.size2sq.text()))
            line.append((int(self.r2sq.text()), int(self.g2sq.text()), int(self.b2sq.text())))
            line.append((int(self.x2sq.text()), int(self.y2sq.text())))
            self.save.append(line)
            for elem in self.save:
                writer.writerow(elem)
        con = sqlite3.connect("figure.db")
        cur = con.cursor()
        cur.execute(f"""insert into Figures(figure, size, R, G, B, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    ('квадрат', int(self.size2sq.text()), int(self.r2sq.text()), int(self.g2sq.text()),
                    int(self.b2sq.text()), int(self.x2sq.text()), int(self.y2sq.text())))
        con.commit()
        cur.close()
        con.close()

        #self.table2()


    def saveci(self):
        col = ["фигура", "размер", "цвет", "координаты"]
        with open('figure.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';')
            writer.writerow(col)
            line = []
            line.append("круг")
            line.append(int(self.size2ci.text()))
            line.append((int(self.r2ci.text()), int(self.g2ci.text()), int(self.b2ci.text())))
            line.append((int(self.x2ci.text()), int(self.y2ci.text())))
            self.save.append(line)
            for elem in self.save:
                writer.writerow(elem)
        con = sqlite3.connect("figure.db")
        cur = con.cursor()
        cur.execute(f"""insert into Figures(figure, size, R, G, B, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    ('круг', int(self.size2ci.text()), int(self.r2ci.text()), int(self.g2ci.text()),
                     int(self.b2ci.text()), int(self.x2ci.text()), int(self.y2ci.text())))
        con.commit()
        cur.close()
        con.close()

        #self.table2()

    def savere(self):
        col = ["фигура", "размер", "цвет", "координаты"]
        self.rectsize = str(self.size2re.text() + "*" + self.size4re.text())
        with open('figure.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';')
            writer.writerow(col)
            line = []
            line.append("прямоугольник")
            line.append(self.rectsize)
            line.append((int(self.r2re.text()), int(self.g2re.text()), int(self.b2re.text())))
            line.append((int(self.x2re.text()), int(self.y2re.text())))
            self.save.append(line)
            for elem in self.save:
                writer.writerow(elem)
        con = sqlite3.connect("figure.db")
        cur = con.cursor()
        cur.execute(f"""insert into Figures(figure, size, R, G, B, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    ('прямоугольник', self.rectsize, int(self.r2re.text()), int(self.g2re.text()),
                     int(self.b2re.text()), int(self.x2re.text()), int(self.y2re.text())))
        con.commit()
        cur.close()
        con.close()

        #self.table2()

    def savetr(self):
        col = ["фигура", "размер", "цвет", "координаты"]
        with open('figure.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';')
            writer.writerow(col)
            line = []
            line.append("треугольник")
            line.append(int(self.size2tr.text()))
            line.append((int(self.r2tr.text()), int(self.g2tr.text()), int(self.b2tr.text())))
            line.append((int(self.x2tr.text()), int(self.y2tr.text())))
            self.save.append(line)
            for elem in self.save:
                writer.writerow(elem)
        con = sqlite3.connect("figure.db")
        cur = con.cursor()
        cur.execute(f"""insert into Figures(figure, size, R, G, B, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    ('треугольник', int(self.size2tr.text()), int(self.r2tr.text()), int(self.g2tr.text()),
                     int(self.b2tr.text()), int(self.x2tr.text()), int(self.y2tr.text())))
        con.commit()
        cur.close()
        con.close()

        #self.table2()

    def savepo(self):
        col = ["фигура", "размер", "цвет", "координаты"]
        with open('figure.csv', 'w', newline='', encoding="utf8") as f:
            writer = csv.writer(
                f, delimiter=';')
            writer.writerow(col)
            line = []
            line.append(f"{int(self.n2po.text())}-угольник")
            line.append(int(self.size2po.text()))
            line.append((int(self.r2po.text()), int(self.g2po.text()), int(self.b2po.text())))
            line.append((int(self.x2po.text()), int(self.y2po.text())))
            self.save.append(line)
            for elem in self.save:
                writer.writerow(elem)
        con = sqlite3.connect("figure.db")
        cur = con.cursor()
        cur.execute(f"""insert into Figures(figure, size, R, G, B, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (f"{int(self.n2po.text())}-угольник", int(self.size2po.text()), int(self.r2po.text()), int(self.g2po.text()),
                     int(self.b2po.text()), int(self.x2po.text()), int(self.y2po.text())))
        con.commit()
        cur.close()
        con.close()

        #self.table2()

    #def table2(self):
        #self.table = QTableWidget(self)
        #self.table.resize(480, 800)
        #self.table.move(701, 0)
        #self.table_list = []
        #self.table.setColumnCount(7)
        #con = sqlite3.connect("figure.db")
        #cur = con.cursor()
        #result = cur.execute(f"""SELECT figure, size, R, G, B, x, y FROM Figures""").fetchall()
        #for i, elem in enumerate(result):
            #self.table.setRowCount(
                #self.table.rowCount() + 1)
            #for j, el in enumerate(elem):
               #self.table.setItem(i, j, QTableWidgetItem(el))
            #self.table.setItem(i, 2, QTableWidgetItem(''))
        #self.table.resizeColumnsToContents()
        #self.table.setHorizontalHeaderLabels(['figure', 'size', 'R', 'G', 'B', 'x', 'y'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
