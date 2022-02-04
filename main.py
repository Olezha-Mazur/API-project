import os
import sys
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow


class Yandex_Map_Window_Application(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.quit_btn.clicked.connect(self.quit)
        self.search_btn.clicked.connect(self.search)
        self.clear_current_search_btn.clicked.connect(self.clear_current_search)

    def clear_current_search(self):
        pass

    def search(self):
        print('Выполняется запрос на поиск')

    def quit(self):
        sys.exit(application.exec_())


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Yandex_Map_Window_Application()
    window.show()
    sys.exit(application.exec_())
