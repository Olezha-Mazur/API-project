import requests
import sys
import math
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'

def limify(value, smallest, biggest, precision):
    p = 10 ** precision
    return int(max(smallest, min(biggest, value)) * p) / p

def makePoint(x, y, design, n):
    return {'x': x, 'y': y, 'design': design, 'n': n}


def request_map_image(x, y, zoom, size, points=[]):
    req = 'https://static-maps.yandex.ru/1.x/'
    req += '?ll=' + str(x) + ',' + str(y)
    req += '&spn=' + str(zoom[0]) + ',' + str(zoom[1])
    req += '&size=' + str(size[0]) + ',' + str(size[1])
    req += '&l=sat'
    if len(points) > 0:
        pt = ''
        for point in points:
            pt += str(point['x']) + ',' + str(point['y']) + ',' + \
                  point['design'] + str(point['n']) + '~'
        req += '&pt='+pt[:-1]
    response = requests.get(req)
    return req, response, response.content


def request_map_objects(name):
    req = "http://geocode-maps.yandex.ru/1.x/"
    req += '?apikey=' + API_KEY
    req += "&geocode=" + name
    req += "&format=json"
    response = requests.get(req)
    if not response:
        return req, response, None
    json = response.json()
    return req, response, json["response"]["GeoObjectCollection"]["featureMember"]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle('API-Project')
        self.image = QLabel(self)
        self.image.resize(573, 430)
        self.image.move(10, 10)
        self.search_btn.clicked.connect(self.run)
        self.quit_btn.clicked.connect(self.quit)
        self.latitude_input.setText("46.0156")
        self.longitude_input.setText("51.5373")
        self.zoom_input.setText("0.001")
        self.run(True)

    def quit(self):
        sys.exit(0)

    def keyPressEvent(self, e):
        zoom_keys = [16777239, 16777238]
        move_keys = [16777236, 16777235, 16777234, 16777237]
        k = e.key()
        zoom = float(self.zoom_input.text())
        if k in zoom_keys:
            zoom_factor = zoom / 2
            v = zoom_factor * (1 - 2 * zoom_keys.index(k))
            zoom = limify(zoom + v, 0.00001, 90, 5)
            self.zoom_input.setText(str(zoom))
            self.run(True)
        if k in move_keys:
            move_factor = zoom
            i = move_keys.index(k)
            dx = move_factor * (int((i == 0)) - int((i == 2)))
            dy = move_factor * (int((i == 1)) - int((i == 3)))
            nx = limify(float(self.latitude_input.text()) + dx, -179.99999, 179.99999, 5)
            ny = limify(float(self.longitude_input.text()) + dy, -86, 86, 5)
            self.latitude_input.setText(str(nx))
            self.longitude_input.setText(str(ny))
            self.run(True)


    def run(self, move=False):
        #self.grabKeyboard()
        if not move:
            place_name = self.place_name_input.text()
            req, response, result = request_map_objects(place_name)
            if response:
                GeoObject = result[0]["GeoObject"]
                coords = GeoObject["Point"]["pos"].split(' ')
                latitude, longitude = float(coords[0]), float(coords[1])
                self.latitude_input.setText(str(latitude))
                self.longitude_input.setText(str(longitude))
                zoom = float(self.zoom_input.text())
            else:
                print("Ошибка выполнения запроса: " + req)
                print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            if self.latitude_input.text() and self.longitude_input.text():
                latitude = self.latitude_input.text()
                longitude = self.longitude_input.text()
                try:
                    zoom = float(self.zoom_input.text())
                except:
                    zoom = 1.0
            else:
                return
        req, response, content = request_map_image(latitude, longitude, (zoom, zoom), (573, 430),
                                                   [makePoint(46.0156, 51.5373, 'pm2blm', 1)])

        if not response:
            print("Ошибка выполнения запроса: " + req)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        try:
            pixmap = QPixmap()
            pixmap.loadFromData(content)
            self.pixmap = pixmap
            self.image.setPixmap(self.pixmap)
            self.image.show()
        except Exception as e:
            print('Exception: ' + str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
