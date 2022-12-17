import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *

# WINDOWS
from windows.windowBarang import WindowBarang
from windows.windowTransaksi import WindowTransaksi
from windows.windowDetailTransaksi import WindowDetailTransaksi
from windows.windowHistory import WindowHistory

from nota import Nota
from items import Items

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(0,0,600,400)
        self.mdi = QMdiArea()
        self.mdi.setWindowTitle("STORE")

        self.init_db()
        self.init_ui()
        self.init_window()

        self.setCentralWidget(self.mdi)
        self.show()
        self.showMaximized()

    def init_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("store.db")
        self.db.open()

    def init_ui(self):
        menu_bar = self.menuBar()
        
        window = menu_bar.addMenu("Window")
        window.addAction("Barang")
        window.addAction("Transaksi")
        window.addAction("Detail Transaksi")
        window.addSeparator()
        window.addAction("Nota")
        window.addSeparator()
        window.addAction("History")

        mode = menu_bar.addMenu("Mode")
        mode.addAction("Cascade")
        mode.addAction("Tiled")

        window.triggered[QAction].connect(self.window_trigered)
        mode.triggered[QAction].connect(self.window_trigered)

    def init_window(self): 
        windows = [
            WindowDetailTransaksi(),
            WindowTransaksi(),
            WindowBarang(),
        ]
        for window in windows:
            self.mdi.addSubWindow(window)

    def window_trigered(self, p):
        if p.text() == "Barang":
            sub = WindowBarang()
            self.mdi.addSubWindow(sub)
            sub.show()
        elif p.text() == "Transaksi":
            sub = WindowTransaksi()
            self.mdi.addSubWindow(sub)
            sub.show()
        elif p.text() == "Detail Transaksi":
            sub = WindowDetailTransaksi()
            self.mdi.addSubWindow(sub)
            sub.show()
        elif p.text() == "Nota":
            sub = Nota(Items.getBayar())
            self.mdi.addSubWindow(sub)
            sub.show()
        elif p.text() == "History":
            sub = WindowHistory()
            self.mdi.addSubWindow(sub)
            sub.show()
        elif p.text() == "Cascade":
            self.mdi.cascadeSubWindows()
        elif p.text() == "Tiled":
            self.mdi.tileSubWindows()


if __name__ == "__main__":
    try :
        app = QApplication(sys.argv)
        app.setApplicationName("UAS")
        mainwindow = MainWindow()
        app.setWindowIcon(QIcon("favicon.ico"))
        app.exec()
        sys.exit(0)
    except NameError:
        print("Name Error")
    except SystemExit:
        print("exit")
    except Exception as e:
        print(e)
