import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSql import *
from datetime import datetime
import random
from items import Items

class Nota(QMainWindow):

    def __init__(self, bayar=1000000):
        super().__init__()
        self.setGeometry(0,0,300,0)
        self.setWindowTitle("Nota")
        self.setMinimumWidth(340)
        self.setMaximumWidth(340)
        self.items = Items.getItems()
        
        main_layout = QVBoxLayout()

        # HEADING
        heading = QLabel("MyStore")
        heading.setAlignment(Qt.AlignCenter)
        myFont=QFont()
        myFont.setBold(True)
        heading.setFont(myFont)

        # date
        now = datetime.now()
        date    = QLabel("Tanggal             : " + now.strftime("%d-%m-%Y"))

        # NO transaksi
        no      = QLabel("kode transaksi : ID" + self.generateId())

        # table head
        table_head = QLabel("nama barang            Qty            Harga                  Sub Total")

        # setayout
        main_layout.addWidget(QLabel("====================================="))
        main_layout.addWidget(heading)
        main_layout.addWidget(QLabel("====================================="))
        main_layout.addWidget(date)
        main_layout.addWidget(no)
        main_layout.addWidget(QLabel("------------------------------------------------------------"))
        main_layout.addWidget(table_head)
        main_layout.addWidget(QLabel("------------------------------------------------------------"))

        total = 0
        for item in self.items:
            total += item[4]
            main_layout.addWidget(QLabel(f"{item[1]:20} {item[2]:13} {item[3]:20,} {item[4]:28,}"))
        main_layout.addWidget(QLabel("------------------------------------------------------------"))
        main_layout.addWidget(QLabel(f"Total {total:85,}"))
        main_layout.addWidget(QLabel(f"Bayar {bayar:84,}"))
        main_layout.addWidget(QLabel(f"Kemabalian {(bayar - total):73,}"))
        main_layout.addWidget(QLabel("------------------------------------------------------------"))
        main_layout.addWidget(QLabel("        Terima Kasih telah berbelanja di toko kami ^-^"))
        
        main_layout.addStretch()


        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        pixmap = widget.grab()

        # Save the QPixmap to an image file
        # pixmap.save("screenshot.png")
        pixmap.save(f"nota_{datetime.now().strftime('%Y%m%d')}.png", "png")  
        

    def generateId(self):
        s = ""
        for i in range(8):
            num = random.randint(0,9)
            s += str(num)
        return s

