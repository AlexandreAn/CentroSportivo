from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QPushButton, QHBoxLayout)
from Abbonamento import Abbonamento

class VistaVisualizzaListaAbbonamenti(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizza abbonamenti")
        self.resize(550, 300)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Codice", "Data Inizio", "Data Scadenza", "Username Socio"])
        layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.btnModifica = QPushButton("Modifica abbonamento")
        self.btnElimina = QPushButton("Elimina abbonamento")
        self.btnModifica.clicked.connect(self.modificaAbbonamento)
        self.btnElimina.clicked.connect(self.eliminaAbbonamento)
        btn_layout.addWidget(self.btnModifica)
        btn_layout.addWidget(self.btnElimina)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.caricaDati()

    def caricaDati(self):
        self.abbonamenti = Abbonamento.getAbbonamenti()
        self.table.setRowCount(0)

        if not self.abbonamenti:
            QMessageBox.information(self, "Nota", "Nessun abbonamento trovato.")
            self.close()
            return

        self.table.setRowCount(len(self.abbonamenti))
        for riga, abb in enumerate(self.abbonamenti.values()):
            self.table.setItem(riga, 0, QTableWidgetItem(str(abb.codice)))
            self.table.setItem(riga, 1, QTableWidgetItem(abb.dataInizio.strftime("%d/%m/%Y")))
            self.table.setItem(riga, 2, QTableWidgetItem(abb.dataScadenza.strftime("%d/%m/%Y")))
            self.table.setItem(riga, 3, QTableWidgetItem(abb.socio.username if abb.socio else "N/D"))

    def getAbbonamentoSelezionato(self):
        selected = self.table.currentRow()
        if selected == -1:
            return None
        codice = int(self.table.item(selected, 0).text())
        return self.abbonamenti.get(codice)

    def eliminaAbbonamento(self):
        abb = self.getAbbonamentoSelezionato()
        if not abb:
            QMessageBox.warning(self, "Attenzione", "Seleziona un abbonamento dalla lista.")
            return
        conferma = QMessageBox.question(
            self, "Conferma", f"Vuoi davvero eliminare l'abbonamento {abb.codice}?",
            QMessageBox.Yes | QMessageBox.No)
        if conferma == QMessageBox.Yes:
            abb.deleteAbbonamento()
            self.caricaDati()

    def modificaAbbonamento(self):
        abb = self.getAbbonamentoSelezionato()
        if not abb:
            QMessageBox.warning(self, "Attenzione", "Seleziona un abbonamento da modificare.")
            return
        from VisteDipendente.VistaModificaAbbonamento import VistaModificaAbbonamento
        self.vistaModificaAbb = VistaModificaAbbonamento(abb)
        self.vistaModificaAbb.show()
        self.close()
