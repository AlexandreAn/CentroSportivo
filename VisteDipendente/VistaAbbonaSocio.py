
from datetime import datetime

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
from Socio import Socio
from Abbonamento import Abbonamento


class VistaAbbonaSocio(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowTitle("Abbona Socio")
        self.resize(400, 250)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Inserire lo username del socio"))
        self.input_username = QLineEdit()
        layout.addWidget(self.input_username)



        layout.addWidget(QLabel("Inserire la data di inizio dell'abbonamento"))
        self.input_dataInizio = QDateEdit()
        self.input_dataInizio.setCalendarPopup(True)
        self.input_dataInizio.setDisplayFormat("dd/MM/yyyy")
        self.input_dataInizio.setDate(QDate.currentDate())  # default oggi
        layout.addWidget(self.input_dataInizio)

        layout.addWidget(QLabel("Inserire la data di scadenza dell'abbonamento"))
        self.input_dataScadenza = QDateEdit()
        self.input_dataScadenza.setCalendarPopup(True)
        self.input_dataScadenza.setDisplayFormat("dd/MM/yyyy")
        self.input_dataScadenza.setDate(QDate.currentDate())
        layout.addWidget(self.input_dataScadenza)


        layout.addWidget(QLabel("Inserire il codice dell'abbonamento"))
        self.input_codice = QLineEdit()
        layout.addWidget(self.input_codice)


        self.btn_cerca = QPushButton("Abbona")

        self.btn_cerca.clicked.connect(self.abbonaSocio)
        layout.addWidget(self.btn_cerca)

        self.setLayout(layout)

    def abbonaSocio(self):
        username = self.input_username.text().strip()

        data_inizio_str = self.input_dataInizio.date().toString("dd/MM/yyyy")
        data_scadenza_str = self.input_dataScadenza.date().toString("dd/MM/yyyy")
        codice_str = self.input_codice.text().strip()

        #controllo campi vuoti
        if not all([username, data_inizio_str, data_scadenza_str, codice_str]):
            QMessageBox.critical(self, "Errore", "Tutti i campi sono obbligatori.")
            return

        #controllo data
        try:
            data_inizio = datetime.strptime(data_inizio_str, "%d/%m/%Y")
            data_scadenza = datetime.strptime(data_scadenza_str, "%d/%m/%Y")
        except ValueError:
            QMessageBox.critical(self, "Errore", "Formato data non valido. Usa GG/MM/AAAA.")
            return

        if data_inizio > data_scadenza:
            QMessageBox.critical(self, "Errore", "La data di inizio non può essere successiva a quella di scadenza.")
            return

        #controllo codice univoco
        try:
            codice = int(codice_str)
        except ValueError:
            QMessageBox.critical(self, "Errore", "Il codice deve essere un numero intero.")
            return

        abbonamenti = Abbonamento.getAbbonamenti()
        if codice in abbonamenti:
            QMessageBox.critical(self, "Errore", f"Esiste già un abbonamento con codice {codice}.")
            return

        #controllo socio già abbonato
        soci = Socio.getSoci()
        socio = soci.get(username)
        if not socio:
            QMessageBox.critical(self, "Errore", f"Nessun socio trovato con username '{username}'.")
            return



        for abbonamento in abbonamenti.values():
            if abbonamento.socio and abbonamento.socio.username == socio.username:
                QMessageBox.critical(self, "Errore", "Questo socio ha già un abbonamento attivo.")
                return

        nuovo_abbonamento = Abbonamento()
        nuovo_abbonamento.createAbbonamento(codice, data_inizio, data_scadenza, socio)

        socio.abbonamento = nuovo_abbonamento

        if data_inizio.date() <= datetime.now().date() <= data_scadenza.date():
            socio.abbonato = True
        else:
            socio.abbonato = False

        soci[username] = socio
        Socio.updateSoci(soci)

        QMessageBox.information(self, "Successo", "Abbonamento creato e assegnato correttamente.")
        self.close()




