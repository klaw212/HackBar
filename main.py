import sys
import os
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow

from PyQt6.QtWidgets import QApplication
from window import MainWindow

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())

