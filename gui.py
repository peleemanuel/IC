import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interactive Map')
        self.setGeometry(100, 100, 800, 600)
        web_view = QWebEngineView(self)
        web_view.load(QUrl("http://localhost:5000/"))
        self.setCentralWidget(web_view)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
