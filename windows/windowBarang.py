from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *

class WindowBarang(QMainWindow):
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.mainLayout = QGridLayout()
        self.setWindowTitle("Barang")

        self.mainLayout.setVerticalSpacing(50)
        self.createTable()
        self.createInput()
        self.showData()

        widget = QWidget()
        widget.setLayout(self.mainLayout)
        self.setCentralWidget(widget)

    def load_data(self)->list:
        self.query.exec("SELECT * FROM barang")
        data = []
        while self.query.next():
            kode_barang = self.query.value(0)
            nama =  self.query.value(1)
            stok =  self.query.value(2)
            harga =  self.query.value(3)
            status =  self.query.value(4)
            data.append([kode_barang, nama, stok, harga, status])

        return data

    def showData(self):        
        self.data = self.load_data()

        if (len(self.data) > 16):
            self.table.setRowCount(len(self.data))
        self.table.clearContents()
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                newItem = QTableWidgetItem(str(self.data[i][j]))
                self.table.setItem(i,j , newItem)


    def createTable(self):
        self.table = QTableWidget(16, 5)
        self.headers = ["kode_barang", "Nama Barang", "Stok","Harga ", "status"]
        self.table.setHorizontalHeaderLabels(self.headers)
        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.table.clicked.connect(self.select)

        self.mainLayout.addWidget(self.table, 1,0)

    def createInput(self):
        groupBox = QGroupBox("Form")
        self.inputLayout = QGridLayout()
        self.inputLayout.setVerticalSpacing(10)
        self.inputLayout.setHorizontalSpacing(5)
        self.btnLayout = QHBoxLayout()
        self.btnLayout.setSpacing(10)
        groupBox.setLayout(self.inputLayout)

        self.lblNama = QLabel("Nama Barang")
        self.lblStok = QLabel("Srok")
        self.lblHarga = QLabel("Harga")
        self.lblStatus = QLabel("Status")

        self.inpNama = QLineEdit()
        self.inpStok = QLineEdit()
        self.inpHarga = QLineEdit()
        self.inpStatus = QComboBox()
        self.inpStatus.addItems(["aktif", "non aktif"])

        self.btnTambah = QPushButton("Tambah")
        self.btnEdit = QPushButton("Edit")
        self.btnHapus = QPushButton("Hapus")
        self.btnCancel = QPushButton("Cancel")
        self.btnRefresh = QPushButton("Refresh")

        self.btnTambah.setFixedWidth(80)
        self.btnTambah.clicked.connect(self.tambah)
        self.btnEdit.setFixedWidth(80)
        self.btnEdit.clicked.connect(self.edit)
        self.btnHapus.setFixedWidth(80)
        self.btnHapus.clicked.connect(self.hapus)
        self.btnCancel.setFixedWidth(80)
        self.btnCancel.clicked.connect(self.cancel)
        self.btnRefresh.setFixedWidth(80)
        self.btnRefresh.clicked.connect(self.refresh)

        self.inputLayout.addWidget(self.lblNama, 0, 0)
        self.inputLayout.addWidget(self.lblStok, 1, 0)
        self.inputLayout.addWidget(self.lblHarga, 2, 0)
        self.inputLayout.addWidget(self.lblStatus, 3, 0)

        self.inputLayout.addWidget(self.inpNama, 0, 1)
        self.inputLayout.addWidget(self.inpStok, 1, 1)
        self.inputLayout.addWidget(self.inpHarga, 2, 1)
        self.inputLayout.addWidget(self.inpStatus, 3, 1)

        self.inputLayout.addLayout(self.btnLayout, 4, 0, 1, 2) 

        self.btnLayout.addWidget(self.btnTambah)
        self.btnLayout.addWidget(self.btnEdit)
        self.btnLayout.addWidget(self.btnHapus)
        self.btnLayout.addWidget(self.btnCancel)
        self.btnLayout.addWidget(self.btnRefresh)
        self.btnLayout.addStretch()

        self.switchButton()

        self.mainLayout.addWidget(groupBox, 0, 0)

    def tambah(self):
        nama = self.inpNama.text()
        stok = self.inpStok.text()
        harga = self.inpHarga.text()
        status = self.inpStatus.currentText()
        
        self.query.exec(f"INSERT INTO `barang` (`kode_barang`, `nama`, `stok`, `harga`, `status`) VALUES (NULL, '{nama}', '{int(stok)}', '{int(harga)}', '{status}');")
        self.showData()
   
    def select(self):
        row = sorted(set(index.row() for index in self.table.selectedIndexes()))[0]
        try:
            data = self.data[row]
            self.kode_barang = data[0]
            self.inpNama.setText(data[1])
            self.inpStok.setText(str(data[2]))
            self.inpHarga.setText(str(data[3]))
            self.inpStatus.setCurrentText(str(data[4]))
            self.switchButton(False)
        except:
            self.clearInput()
            self.switchButton()

    def edit(self):
        nama = self.inpNama.text()
        stok = self.inpStok.text()
        harga = self.inpHarga.text()
        status = self.inpStatus.currentText()

        self.query.exec(f"UPDATE `barang` SET `nama` = '{nama}', `stok`={stok},`harga` = '{harga}', `status` = '{status}' WHERE `barang`.`kode_barang` = {self.kode_barang};")
        self.showData()
        self.clearInput()
        self.switchButton()

    def hapus(self):
        self.query.exec(f"DELETE FROM `barang` WHERE `barang`.`kode_barang` = {self.kode_barang}")
        self.showData()
        self.clearInput()
        self.switchButton()

    def cancel(self):
        self.kode_barang = None
        self.clearInput()
        self.switchButton()

    def switchButton(self, activeTambah=True):
        if activeTambah:
            self.btnTambah.setDisabled(False)
            self.btnEdit.setDisabled(True)
            self.btnHapus.setDisabled(True)
            self.btnCancel.setDisabled(True)
        else:
            self.btnTambah.setDisabled(True)
            self.btnEdit.setDisabled(False)
            self.btnHapus.setDisabled(False)
            self.btnCancel.setDisabled(False)

    def clearInput(self):
        self.inpNama.setText("")
        self.inpStok.setText("")
        self.inpHarga.setText("")
    
    def refresh(self):
        self.createTable()
        self.createInput()
        self.showData()
