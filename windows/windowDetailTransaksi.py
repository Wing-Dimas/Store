from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *
from PySide6.QtCore import *
from items import Items

class WindowDetailTransaksi(QMainWindow):
    __keranjang = Items.getItems()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.mainLayout = QGridLayout()
        self.timer = QTimer()
        self.setWindowTitle("Detail Transaksi")

        self.mainLayout.setVerticalSpacing(50)
        self.createTable()
        self.showData()
        self.update()

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)
        

    def update(self):
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

    
    def showData(self):
        self.table.clearContents()
        keranjang = WindowDetailTransaksi.__keranjang
        if (len(keranjang) > 11):
            self.table.setRowCount(len(keranjang))

        if keranjang:
            for i in range(len(keranjang)):
                for j in range(0, len(keranjang[0]) - 1):
                    newItem = QTableWidgetItem(str(keranjang[i][j + 1]))
                    self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(11, 4)
        self.headers = ["Nama Barang", "Qty", "Harga", "Sub Total"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.mainLayout.addWidget(self.table, 0,0)
        

    def refresh(self):
        self.showData()

    @staticmethod
    def trigger_add():
        WindowDetailTransaksi.__keranjang = Items.getItems()
