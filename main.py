import requests
import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def request_map_image(x, y, zoom, size):
    req = 'https://static-maps.yandex.ru/1.x/'
    req += '?ll=' + str(x) + ',' + str(y)
    req += '&spn=' + str(zoom[0]) + ',' + str(zoom[1])
    req += '&size=' + str(size[0]) + ',' + str(size[1])
    req += '&l=sat'
    response = requests.get(req)
    return req, response, response.content


def request_map_objects(name):
    req = "http://geocode-maps.yandex.ru/1.x/"
    req += '?apikey=' + API_KEY
    req += "&geocode=" + name
    req += "&format=json"
    response = requests.get(req)
    if not response:
        return req, False, None
    json = response.json()
    return req, True, json["response"]["GeoObjectCollection"]["featureMember"]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle('API-Project')
        self.search_btn.clicked.connect(self.run)
        self.quit_btn.clicked.connect(self.quit)

    def quit(self):
        sys.exit(0)

    def run(self):
        if self.latitude_input.text() and self.longitude_input.text():
            latitude = self.latitude_input.text()
            longitude = self.longitude_input.text()
            try:
                zoom = float(self.zoom_input.text())
            except:
                zoom = 1.0
        else:
            return
        req, response, content = request_map_image(latitude, longitude, (zoom, zoom), (573, 430))

        if not response:
            print("Ошибка выполнения запроса: " + req)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(content)
            self.pixmap = pixmap
            self.image = QLabel(self)
            self.image.resize(573, 430)
            self.image.move(10, 10)
            self.image.setPixmap(self.pixmap)
            self.image.show()
        except Exception as e:
            print('Exception: ' + str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())