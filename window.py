from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QListWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget,
    QLabel, QLineEdit, QSpinBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from urllib.parse import unquote
from PyQt6.QtGui import QIcon

from payloads.payload_loader import load_payloads
from logger import log


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HackBar")
        self.resize(1400, 850)
        self.setWindowIcon(QIcon("hackbar.ico"))

        # ================= URL BAR =================
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(
            "https://target.com/page.php?id=1"
        )

        self.go_btn = QPushButton("GO")
        self.go_btn.clicked.connect(self.load_url)

        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("URL:"))
        top_bar.addWidget(self.url_bar)
        top_bar.addWidget(self.go_btn)

        # ================= BROWSER =================
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.sync_url_bar)
        self.browser.titleChanged.connect(
            lambda title: log("TITLE", title)
        )

        # ================= TABS =================
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_sql_tab(), "SQL")
        self.tabs.addTab(self.create_payload_tab("xss"), "XSS")
        self.tabs.addTab(self.create_payload_tab("lfi"), "LFI")
        self.tabs.addTab(self.create_payload_tab("rce"), "RCE")

        # ================= LAYOUT =================
        left_layout = QVBoxLayout()
        left_layout.addLayout(top_bar)
        left_layout.addWidget(self.tabs)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 4)
        main_layout.addWidget(self.browser, 6)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # ==================================================
    # URL HANDLING
    # ==================================================

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return

        if not url.startswith("http"):
            url = "https://" + url

        log("LOAD_URL", url)
        self.browser.setUrl(QUrl(url))

    def sync_url_bar(self, url: QUrl):
        decoded = unquote(url.toString())
        self.url_bar.setText(decoded)
        log("URL_CHANGED", decoded)

    # ==================================================
    # SQL TAB (SINGLE WINDOW + UNION SELECT)
    # ==================================================

    def create_sql_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # SQL payloads
        self.sql_list = QListWidget()
        self.sql_list.addItems(load_payloads("sql.txt"))

        add_sql_btn = QPushButton("ADD SQL PAYLOAD")
        add_sql_btn.clicked.connect(
            lambda: self.append_payload(self.sql_list)
        )

        # DIOS payloads
        self.dios_list = QListWidget()
        self.dios_list.addItems(load_payloads("dios.txt"))

        add_dios_btn = QPushButton("ADD DIOS PAYLOAD")
        add_dios_btn.clicked.connect(
            lambda: self.append_payload(self.dios_list)
        )

        # -------- UNION SELECT --------
        self.union_spin = QSpinBox()
        self.union_spin.setMinimum(1)
        self.union_spin.setMaximum(100)
        self.union_spin.setValue(3)

        union_btn = QPushButton("ADD UNION SELECT")
        union_btn.clicked.connect(self.append_union_payload)

        # Layout
        layout.addWidget(QLabel("SQL Payloads (sql.txt)"))
        layout.addWidget(self.sql_list)
        layout.addWidget(add_sql_btn)

        layout.addWidget(QLabel("DIOS Payloads (dios.txt)"))
        layout.addWidget(self.dios_list)
        layout.addWidget(add_dios_btn)

        layout.addWidget(QLabel("UNION SELECT column count"))
        layout.addWidget(self.union_spin)
        layout.addWidget(union_btn)

        widget.setLayout(layout)
        return widget

    # ==================================================
    # GENERIC PAYLOAD TABS
    # ==================================================

    def create_payload_tab(self, payload_type: str):
        widget = QWidget()
        layout = QVBoxLayout()

        payload_list = QListWidget()
        payload_list.addItems(
            load_payloads(f"{payload_type}.txt")
        )

        add_btn = QPushButton("ADD PAYLOAD")
        add_btn.clicked.connect(
            lambda: self.append_payload(payload_list)
        )

        layout.addWidget(
            QLabel(f"{payload_type.upper()} Payloads")
        )
        layout.addWidget(payload_list)
        layout.addWidget(add_btn)

        widget.setLayout(layout)
        return widget

    # ==================================================
    # PAYLOAD APPEND (NO EXECUTION)
    # ==================================================

    def append_payload(self, payload_list: QListWidget):
        item = payload_list.currentItem()
        if not item:
            return

        payload = item.text()
        current_url = self.url_bar.text()

        self.url_bar.setText(current_url + payload)
        log("PAYLOAD_APPENDED", payload)

    # ==================================================
    # UNION SELECT (AUTO GENERATED)
    # ==================================================

    def append_union_payload(self):
        count = self.union_spin.value()
        columns = ",".join(str(i) for i in range(1, count + 1))
        payload = f" UNION SELECT {columns}"

        current_url = self.url_bar.text()
        self.url_bar.setText(current_url + payload)

        log("UNION_APPENDED", payload)
