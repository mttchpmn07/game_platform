import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi('main_window.ui')


def main():
    app = QApplication(sys.argv)
    widget = main_window()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
