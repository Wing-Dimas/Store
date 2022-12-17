from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *
from items import Items
from windows.windowDetailTransaksi import WindowDetailTransaksi
import numpy as np
from nota import Nota


class WindowTransaksi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.mainLayout = QGridLayout()
        self.setWindowTitle("Transaksi")

        self.mainLayout.setVerticalSpacing(50)
        self.createInput()
        self.createTotal()

        self.widget = QWidget()
        self.widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.widget)

    def load_data(self)->list:
        self.query.exec("SELECT * FROM barang WHERE status='aktif'")
        data = []
        while self.query.next():
            kode_barang = self.query.value(0)
            nama =  self.query.value(1)
            stok =  self.query.value(2)
            harga =  self.query.value(3)
            status =  self.query.value(4)
            data.append([kode_barang, nama, stok, harga, status])
        
        return data

    def createInput(self):
        barang = self.load_data()
        list_nama_barang = np.array(barang)[:, 1].tolist()
        groupBox = QGroupBox("Input Barang")
        self.inputBarangLayout = QGridLayout()
        groupBox.setLayout(self.inputBarangLayout)

        self.lblNamaBarang = QLabel("Nama Barang")
        self.lblQty = QLabel("Qty")

        self.inpNamaBarang = QComboBox()
        self.inpNamaBarang.addItems(list_nama_barang)
        self.inpQty = QLineEdit()

        self.btnTambah = QPushButton("Tambah")
        self.btnRefresh = QPushButton("Refresh")

        self.btnTambah.clicked.connect(self.tambah)
        self.btnRefresh.clicked.connect(self.refresh)

        # self.inputLayout.addWidget(self.btnRefresh, 0, 2)
        # self.inputLayout.addWidget(self.btnReset, 1, 2)
        # self.inputLayout.addWidget(groupBox, 2,0, 1, 3)

        self.inputBarangLayout.addWidget(self.lblNamaBarang, 0, 0)
        self.inputBarangLayout.addWidget(self.inpNamaBarang, 0, 1)
        self.inputBarangLayout.addWidget(self.lblQty, 1, 0)
        self.inputBarangLayout.addWidget(self.inpQty, 1, 1)
        self.inputBarangLayout.addWidget(self.btnTambah, 2, 0)
        self.inputBarangLayout.addWidget(self.btnRefresh, 2, 1)

        self.mainLayout.addWidget(groupBox, 0, 0)

    def createTotal(self):
        groupBox = QGroupBox("Form Pembayaran")
        self.pembayaranLayout = QGridLayout()
        self.pembayaranLayout.setVerticalSpacing(10)
        self.pembayaranLayout.setHorizontalSpacing(5)
        groupBox.setLayout(self.pembayaranLayout)


        self.lblTotal = QLabel("Total")
        self.inpTotal = QLabel("0")
        self.lblBayar = QLabel("Bayar")
        self.lblKembalian = QLabel("Kembalian")
        self.kembalian = QLabel("0")
        
        self.inpBayar = QLineEdit()
        
        self.btnBayar = QPushButton("Bayar")
        self.btnBayar.clicked.connect(self.pembayaran)

        self.pembayaranLayout.addWidget(self.lblTotal, 0,0)
        self.pembayaranLayout.addWidget(self.inpTotal, 0,1)
        self.pembayaranLayout.addWidget(self.lblBayar, 1, 0)
        self.pembayaranLayout.addWidget(self.inpBayar, 1, 1)
        self.pembayaranLayout.addWidget(self.btnBayar, 2, 1)
        self.pembayaranLayout.addWidget(self.lblKembalian, 3, 0)
        self.pembayaranLayout.addWidget(self.kembalian, 3, 1)

        self.mainLayout.addWidget(groupBox, 2, 0)

    def tambah(self):
        # get input
        namaBarang = self.inpNamaBarang.currentText()
        qty = int(self.inpQty.text())
        # check database
        self.query.exec(f"SELECT * FROM barang WHERE nama='{namaBarang}'")
        if self.query.next():
            kode_barang = self.query.value(0)
            nama =  self.query.value(1)
            stok =  self.query.value(2)
            harga =  self.query.value(3)
            status =  self.query.value(4)
            barang = [kode_barang, nama, stok, harga, status]
        
        # tambah keranjang
        self.tambahKeranjang(barang, qty)

    def tambahKeranjang(self, barang, qty):
        keranjang = Items.getItems()
        # cek over qty
        if barang[2] < qty: 
            msg = QMessageBox()
            msg.setText("Jumlah quantity melebihi batas stok barang")
            msg.exec()
            return
        # check name
        if(keranjang and barang[1] in np.array(keranjang)[:, 1].tolist()):
            # find index item in keranjang
            for i in range(len(keranjang)):
                if(barang[1] in keranjang[i]):
                    ind = i
                    break
            temp = keranjang[ind]
            # cek over qty
            if barang[2] < temp[2] + qty: 
                msg = QMessageBox()
                msg.setText("Jumlah quantity melebihi batas stok barang")
                msg.exec()
                return
            
            # update keranjang
            newQty = temp[2] + qty
            Items.replace(ind, [barang[0], barang[1], newQty, barang[3] ,newQty * barang[3]])
        else:
            Items.add([barang[0], barang[1], qty, barang[3], qty * barang[3]])
        
        # update total
        self.total = sum(np.array(Items.getItems())[:, 4].astype(np.int).tolist())
        self.inpTotal.setText(str(self.total))
        # update table
        WindowDetailTransaksi.trigger_add()

    def pembayaran(self):
        bayar = int(self.inpBayar.text())
        total = int(self.inpTotal.text())

        # cek jika kurang
        if bayar < total:
            msg = QMessageBox()
            msg.setText("Nominal pembayaran kurang")
            msg.exec()
            self.kembalian.setText("")
            return

        # 4. detail pemesanan
        items = Items.getItems()
        for item in items:
            self.query.exec(f"INSERT INTO transaksi('kode_barang', 'jumlah', 'total_harga') VALUES ({item[0]}, {item[2]}, {item[4]})")

        # tampilkan kembalian
        kembalian = bayar - total
        self.kembalian.setText(str(kembalian))
        msg = QMessageBox()
        msg.setText("Transaksi berhasil")
        msg.exec()
        Items.setBayar(bayar)
        Nota(bayar)
        # Items.clear()

    def refresh(self):
        Items.clear()
        Items.setBayar(0)
        self.createInput()
        self.inpTotal.setText("0")
        self.kembalian.setText("0")
        self.inpBayar.setText("")
