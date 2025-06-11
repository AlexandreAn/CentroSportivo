from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from Socio import Socio
from Dipendente import Dipendente
from Abbonamento import Abbonamento

class VistaAltreStatistiche(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Altre statistiche")
        self.resize(330, 150)

        layout = QVBoxLayout()

        num_soci = len(Socio.getSoci())
        num_dipendenti = len(Dipendente.getDipendenti())
        num_abbonamenti = len(Abbonamento.getAbbonamenti())

        table = QTableWidget()
        table.setRowCount(3)
        table.setColumnCount(2)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)

        table.setItem(0, 0, QTableWidgetItem("Soci registrati"))
        table.setItem(0, 1, QTableWidgetItem(str(num_soci)))
        table.setItem(1, 0, QTableWidgetItem("Dipendenti registrati"))
        table.setItem(1, 1, QTableWidgetItem(str(num_dipendenti)))
        table.setItem(2, 0, QTableWidgetItem("Abbonamenti registrati"))
        table.setItem(2, 1, QTableWidgetItem(str(num_abbonamenti)))

        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.resizeColumnsToContents()
        table.setAlternatingRowColors(True)

        layout.addWidget(table)
        self.setLayout(layout)
