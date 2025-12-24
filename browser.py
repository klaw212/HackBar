from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class Browser(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUrl(QUrl("https://www.google.com"))
