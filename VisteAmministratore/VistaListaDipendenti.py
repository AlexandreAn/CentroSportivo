from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import os
from Dipendente import Dipendente
from VisteAmministratore.VistaDettagliDipendente import VistaDettagliDipendente
from VisteAmministratore.VistaModificaDipendente import VistaModificaDipendente


class VistaListaDipendenti(QWidget):
    def __init__(self, parent=None):
        super(VistaListaDipendenti, self).__init__(parent)
        self.setWindowTitle("Lista Dipendenti")
        self.resize(800, 400)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout) 
        self.caricaDipendenti()

    def caricaDipendenti(self):
        if not os.path.exists("Dati/Dipendenti.pickle"):
            QMessageBox.warning(self, "Attenzione", "Nessun dipendente registrato.")
            return

        self.dipendenti = Dipendente.getDipendenti()

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nome", "Cognome", "Username", "Visualizza", "Modifica", "Elimina"])
        self.table.setRowCount(len(self.dipendenti))


        for riga, dipendente in enumerate(self.dipendenti.values()): #values() restituisce i valori ignorando le chiavi
            self.table.setItem(riga, 0, QTableWidgetItem(dipendente.nome)) #enumerate aggiunge un indice a ogni elemento dell'iterabile
            self.table.setItem(riga, 1, QTableWidgetItem(dipendente.cognome))
            self.table.setItem(riga, 2, QTableWidgetItem(dipendente.username))

            btn_visualizza = QPushButton("Visualizza Dati")

            btn_visualizza.clicked.connect(lambda _, d=dipendente: self.visualizzaDatiDipendente(d))
            # i : separano i parametri dall'espressione da restituire. _ serve per ignorare un parametro che PyQt passa in automatico con connect

            self.table.setCellWidget(riga, 3, btn_visualizza)



            btn_modifica = QPushButton("Modifica Dati")
            btn_modifica.clicked.connect(lambda _, d=dipendente: self.modificaDatiDipendente(d))
            self.table.setCellWidget(riga, 4, btn_modifica)

            btn_elimina = QPushButton("Elimina")

            btn_elimina.clicked.connect(lambda _, d=dipendente: self.eliminaDipendente(d))

            self.table.setCellWidget(riga, 5, btn_elimina)



    def eliminaDipendente(self, dipendente):

        conferma = QMessageBox.question(self, "Conferma",
                                        "Vuoi davvero eliminare il dipendente ?",
                                        QMessageBox.Yes | QMessageBox.No)

        if conferma == QMessageBox.Yes:

            dipendente.deleteDipendente()

            QMessageBox.information(self, "Successo", "Dipendente eliminato con successo.")
            self.caricaDipendenti()

    def visualizzaDatiDipendente(self, dipendente):
        self.vista_dettagli = VistaDettagliDipendente(dipendente)
        self.vista_dettagli.show()

    def modificaDatiDipendente(self, dipendente):
        self.vista_modifica = VistaModificaDipendente(dipendente)
        self.vista_modifica.show()



