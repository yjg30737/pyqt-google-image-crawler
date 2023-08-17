import os, sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well


from PyQt5.QtGui import QFont, QIcon

from inputDialog import InputDialog
from loadingLbl import LoadingLabel
from script import get_image_from_google, get_languages
from notifier import NotifierWidget
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QListWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QSpacerItem, QSizePolicy, QWidget, QDialog, QListWidgetItem, QGroupBox, QFormLayout, QSpinBox, QComboBox, \
    QSystemTrayIcon, QAction, QMenu, QMessageBox
from PyQt5.QtCore import QThread, Qt, QCoreApplication

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))
QApplication.setWindowIcon(QIcon('logo.svg'))


class Thread(QThread):
    def __init__(self, text_arr: list, color: str, max_num: int):
        super(Thread, self).__init__()
        self.__text_arr = text_arr
        self.__color = color
        self.__max_num = max_num

    def run(self):
        try:
            for filename in self.__text_arr:
                get_image_from_google(filename, save_path=filename, color=self.__color, max_num=self.__max_num)
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__lang = get_languages()

    def __initUi(self):
        self.setWindowTitle('Google Image Crawler')

        self.__addBtn = QPushButton('Add')
        self.__delBtn = QPushButton('Delete')

        self.__addBtn.clicked.connect(self.__add)
        self.__delBtn.clicked.connect(self.__delete)

        self.__maxSpinBox = QSpinBox()
        self.__maxSpinBox.setRange(10, 1000)
        self.__colorCmbBox = QComboBox()
        self.__colorCmbBox.addItems(['color', 'blackandwhite', 'transparent', 'red', 'orange', 'yellow', 'green', 'teal',
                                     'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'])
        self.__langCmbBox = QComboBox()
        self.__langCmbBox.addItems(self.__lang.keys())

        lay = QFormLayout()
        lay.addRow('Maximum Images', self.__maxSpinBox)
        lay.addRow('Colors', self.__colorCmbBox)
        lay.addRow('Languages', self.__langCmbBox)

        settingGrpBox = QGroupBox('Settings (Parameters)')
        settingGrpBox.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(QLabel('Topics'))
        lay.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.MinimumExpanding))
        lay.addWidget(self.__addBtn)
        lay.addWidget(self.__delBtn)
        lay.setAlignment(Qt.AlignRight)
        lay.setContentsMargins(0, 0, 0, 0)

        menuWidget = QWidget()
        menuWidget.setLayout(lay)

        self.__listWidget = QListWidget()

        self.__runBtn = QPushButton('Start Crawling')
        self.__runBtn.clicked.connect(self.__run)
        self.__runBtn.setEnabled(False)

        self.__loadingLbl = LoadingLabel()

        lay = QVBoxLayout()
        lay.addWidget(settingGrpBox)
        lay.addWidget(menuWidget)
        lay.addWidget(self.__listWidget)
        lay.addWidget(self.__runBtn)
        lay.addWidget(self.__loadingLbl)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        self.__setTrayMenu()
        QApplication.setQuitOnLastWindowClosed(False)

    def __setTrayMenu(self):
        # background app
        menu = QMenu()

        action = QAction("Quit", self)
        action.setIcon(QIcon('close.svg'))

        action.triggered.connect(app.quit)

        menu.addAction(action)

        tray_icon = QSystemTrayIcon(app)
        tray_icon.setIcon(QIcon('logo.svg'))
        tray_icon.activated.connect(self.__activated)

        tray_icon.setContextMenu(menu)

        tray_icon.show()

    def __activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def __add(self):
        dialog = InputDialog('Add', '', self)
        reply = dialog.exec()
        if reply == QDialog.Accepted:
            text = dialog.getText()
            self.__listWidget.addItem(QListWidgetItem(text))
            self.__runBtn.setEnabled(True)

    def __delete(self):
        if self.__listWidget.currentItem():
            self.__listWidget.takeItem(self.__listWidget.currentRow())
            if self.__listWidget.count() == 0:
                self.__runBtn.setEnabled(False)

    def __run(self):
        text_arr = [self.__listWidget.item(idx).text() for idx in range(self.__listWidget.count())]
        color = self.__colorCmbBox.currentText()
        max_num = self.__maxSpinBox.value()
        self.__t = Thread(text_arr=text_arr, color=color, max_num=max_num)
        self.__t.started.connect(self.__started)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        self.__loadingLbl.setVisible(True)
        self.__loadingLbl.start()
        print('started')

    def __finished(self):
        if not self.isVisible():
            self.__notifierWidget = NotifierWidget(informative_text='Task Complete', detailed_text='Click this!')
            self.__notifierWidget.show()
            self.__notifierWidget.doubleClicked.connect(self.show)
        self.__loadingLbl.stop()
        self.__loadingLbl.setVisible(False)
        print('finished')

    def closeEvent(self, e):
        message = 'The window will be closed. Would you like to continue running this app in the background?'
        closeMessageBox = QMessageBox(self)
        closeMessageBox.setWindowTitle('Wait!')
        closeMessageBox.setText(message)
        closeMessageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = closeMessageBox.exec()
        # Yes
        if reply == 16384:
            e.accept()
        # No
        elif reply == 65536:
            app.quit()
        return super().closeEvent(e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())