# -*- encoding: utf-8 -*-

import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import glob
#http://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
import json

class Classificator(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.load_images()
        self.i = 0
        self.i_max = len(self.image_list)
        #PictureBox
        self.pic = QLabel(self)
        self.pic.setGeometry(10, 10, 500, 500)
        if (self.i < self.i_max):
            self.pic.setPixmap(QPixmap(self.image_list[self.i]).scaled(500, 500))
        else:
            self.pic.setPixmap(QPixmap("logo.jpg").scaled(500, 500))

        # Label
        self.label1 = QLabel(self)
        self.label1.move(520, 10)
        self.label1.setText("Новый тег")

        #Textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(520, 30)
        self.textbox.resize(280, 20)

        # Button save tag
        self.button = QPushButton('Добавить', self)
        self.button.move(520, 50)
        self.button.clicked.connect(self.on_click_save_tag)

        # Button refresh tag
        self.button = QPushButton('Обновить', self)
        self.button.move(600, 50)
        self.button.clicked.connect(self.refreshUI)

        # Button refresh tag
        self.button = QPushButton('Сохранить', self)
        self.button.move(10, 520)
        self.button.clicked.connect(self.save_result)

        #Read&Create checkboxes from json
        if os.path.isfile("tags.json"):
            self.read_checkboxes()
            self.create_checkboxes()

        self.setGeometry(300, 300, 810, 700)
        self.setWindowTitle('Classificator')
        self.show()

    @pyqtSlot()
    def on_click_save_tag(self):
        textboxValue = self.textbox.text()
        self.textbox.clear()
        self.checkboxes.append(str(textboxValue))
        self.save_checkboxes()

    @pyqtSlot()
    def save_result(self):
        file = self.image_list[self.i].replace("data", "data_info").replace(".jpg", ".json")

        k = 0
        out_mas = []

        with open(file, 'w', encoding='utf8') as outfile:
            json.dump(out_mas, outfile)

        self.i += 1
        for widget in self.widgets:
            if(widget.checkState() > 0):
                out_mas.append(self.checkboxes[k])
                print(self.checkboxes[k])
            k+=1
        os.replace(self.image_list[self.i - 1], self.image_list[self.i - 1].replace("data", "data_old"))
        if(self.i<self.i_max):
            self.pic.setPixmap(QPixmap(self.image_list[self.i-1]).scaled(500, 500))
            self.textbox.setText("")
        else:
            self.pic.setPixmap(QPixmap("logo.jpg").scaled(500, 500))
            QMessageBox.question(self, 'Message', "Снимки закончились!", QMessageBox.Ok,
                                 QMessageBox.Ok)

    @pyqtSlot()
    def refreshUI(self):
        self.close()
        super().__init__()
        self.initUI()

    def load_images(self):
        self.image_list = []
        for filename in glob.glob('data/*.jpg'):  # assuming gif
            self.image_list.append(filename)
        print(self.image_list)

    def create_checkboxes(self):
        print("Loaded tags: " + str(self.checkboxes))
        y_ch = 10
        x_ch = 550
        self.widgets = []
        for chbx in self.checkboxes:
            self.checkbox = QCheckBox(chbx, self)
            self.checkbox.move(y_ch, x_ch)
            self.checkbox.setObjectName(chbx)
            self.widgets.append(self.checkbox)
            x_ch += 20
            if(x_ch >= 690):
                y_ch += 200
                x_ch = 550

    def save_checkboxes(self):
        with open("tags.json", 'w', encoding='utf8') as outfile:
            json.dump(self.checkboxes, outfile)

    def read_checkboxes(self):
        with open("tags.json", 'r', encoding='utf8') as infile:
            text = infile.read()
        self.checkboxes = json.loads(text)

    def clearLayout(self):
        if self.layout() is not None:
            old_layout = self.layout()
            for i in reversed(range(old_layout.count())):
                old_layout.itemAt(i).widget().setParent(None)
            import sip
            sip.delete(old_layout)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Classificator()
    sys.exit(app.exec_())