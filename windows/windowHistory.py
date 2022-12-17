from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *

class WindowHistory(QMainWindow):
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.mainLayout = QGridLayout()
        self.setWindowTitle("History")

        self.mainLayout.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    def load_data(self)->list:
        self.query.exec("SELECT * FROM transaksi")
        data = []
        while self.query.next():
            kode_transaksi = self.query.value(0)
            kode_barang =  self.query.value(1)
            jumlah =  self.query.value(2)
            total_harga =  self.query.value(3)
            data.append([kode_transaksi, kode_barang, jumlah, total_harga])

        return data

    def showData(self):        
        self.table.clearContents()
        self.data = self.load_data()

        if (len(self.data) > 16):
            self.table.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(16, 4)
        self.headers = ["kode_transaksi", "kode_barang", "Stok","Jumlah ", "Total Harga"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)

        self.mainLayout.addWidget(self.table, 1,0)

    def createInput(self):
        self.btnRefresh = QPushButton("Refresh")

        self.btnRefresh.clicked.connect(self.refresh)

        self.mainLayout.addWidget(self.btnRefresh)

    def refresh(self):
        self.showData()