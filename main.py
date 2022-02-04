import requests
import sys
from PyQt5 import uic

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)  
        self.setWindowTitle('API-Project')
        self.search_btn.clicked.connect(self.run)

    def run(self):
        if self.geo_width_input.text() and self.geo_height_input.text():
            latitude = self.geo_width_input.text()
            longitude = self.geo_height_input.text()
        else:
            self.close()
        map_request = f"https://static-maps.yandex.ru/1.x/?ll={latitude},{longitude}&spn=0.016457,0.00619&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap('map.png')
        self.image = QLabel(self)
        self.image.resize(573, 430)
        self.image.move(10, 10)
        self.image.setPixmap(self.pixmap)
        self.image.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())