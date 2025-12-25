from PyQt6.QtCore import QUrl
from urllib.parse import unquote


class BrowserController:
    def __init__(self, browser, url_bar):
        self.browser = browser
        self.url_bar = url_bar
        self.browser.urlChanged.connect(self.sync_url)

    def load(self, url: str):
        if not url:
            return
        if not url.startswith("http"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def sync_url(self, url):
        self.url_bar.setText(unquote(url.toString()))

    def inject(self, base_url: str, payload: str):
        self.browser.setUrl(QUrl(base_url + payload))
