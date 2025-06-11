from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import os
from Socio import Socio
from VisteDipendente.VistaDettagliSocio import VistaDettagliSocio


class VistaVisualizzaListaSoci(QWidget):
    def __init__(self, parent=None):
        super(VistaVisualizzaListaSoci, self).__init__(parent)
        self.setWindowTitle("Lista Soci")
        self.resize(675, 400)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.caricaSoci()

    def caricaSoci(self):
        if not os.path.exists("Dati/Soci.pickle"):
            QMessageBox.warning(self, "Attenzione", "Nessun socio registrato.")
            return

        self.soci = Socio.getSoci()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nome", "Cognome", "Username", "Visualizza", "Elimina"])
        self.table.setRowCount(len(self.soci))

        for riga, socio in enumerate(self.soci.values()):
            info = socio.getInfoSocio()
            self.table.setItem(riga, 0, QTableWidgetItem(info["nome"]))
            self.table.setItem(riga, 1, QTableWidgetItem(info["cognome"]))
            self.table.setItem(riga, 2, QTableWidgetItem(info["username"]))

            btnVisualizza = QPushButton("Visualizza Dati")
            btnVisualizza.clicked.connect(lambda _, s=socio: self.visualizzaDettagliSocio(s))
            self.table.setCellWidget(riga, 3, btnVisualizza)

            btnElimina = QPushButton("Elimina")
            btnElimina.clicked.connect(lambda _, s=socio: self.eliminaSocio(s))
            self.table.setCellWidget(riga, 4, btnElimina)

    def eliminaSocio(self, socio):
        conferma = QMessageBox.question(self, "Conferma",
                                        "Vuoi davvero eliminare il socio ?",
                                        QMessageBox.Yes | QMessageBox.No)

        if conferma == QMessageBox.Yes:
            socio.deleteSocio()
            QMessageBox.information(self, "Successo", "Socio eliminato con successo.")
            self.caricaSoci()

    def visualizzaDettagliSocio(self, socio):
        self.vistaDettagli = VistaDettagliSocio(socio)
        self.vistaDettagli.show()
