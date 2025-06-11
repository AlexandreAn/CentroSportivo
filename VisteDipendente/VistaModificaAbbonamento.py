from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
from datetime import datetime
from Abbonamento import Abbonamento
from Socio import Socio

class VistaModificaAbbonamento(QWidget):
    def __init__(self, abbonamento, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Abbonamento")
        self.resize(400, 200)

        self.abbonamento = abbonamento

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Codice: {self.abbonamento.codice}"))
        layout.addWidget(QLabel(f"Socio: {self.abbonamento.socio.username if self.abbonamento.socio else 'N/D'}"))



        layout.addWidget(QLabel("Nuova data inizio abbonamento"))
        self.input_inizio = QDateEdit()
        self.input_inizio.setCalendarPopup(True)
        self.input_inizio.setDisplayFormat("dd/MM/yyyy")
        self.input_inizio.setDate(
            QDate(self.abbonamento.dataInizio.year, self.abbonamento.dataInizio.month, self.abbonamento.dataInizio.day))
        layout.addWidget(self.input_inizio)

        layout.addWidget(QLabel("Nuova data scadenza abbonamento"))
        self.input_scadenza = QDateEdit()
        self.input_scadenza.setCalendarPopup(True)
        self.input_scadenza.setDisplayFormat("dd/MM/yyyy")
        self.input_scadenza.setDate(QDate(self.abbonamento.dataScadenza.year, self.abbonamento.dataScadenza.month,
                                          self.abbonamento.dataScadenza.day))
        layout.addWidget(self.input_scadenza)

        self.btn_salva = QPushButton("Salva modifiche")
        self.btn_salva.clicked.connect(self.salvaModifiche)
        layout.addWidget(self.btn_salva)

        self.setLayout(layout)

    def salvaModifiche(self):
        data_inizio_str = self.input_inizio.text().strip()
        data_scadenza_str = self.input_scadenza.text().strip()

        try:
            data_inizio = datetime.strptime(data_inizio_str, "%d/%m/%Y")
            data_scadenza = datetime.strptime(data_scadenza_str, "%d/%m/%Y")
        except ValueError:
            QMessageBox.critical(self, "Errore", "Formato data non valido. Usa GG/MM/AAAA.")
            return

        if data_inizio > data_scadenza:
            QMessageBox.critical(self, "Errore", "La data di inizio non può essere successiva a quella di scadenza.")
            return

        #applica modifiche
        self.abbonamento.dataInizio = data_inizio
        self.abbonamento.dataScadenza = data_scadenza

        #salva il dizionario abbonamenti aggiornato
        abbonamenti = Abbonamento.getAbbonamenti()
        abbonamenti[self.abbonamento.codice] = self.abbonamento
        Abbonamento.updateAbbonamenti(abbonamenti)

        #ricalcola stato abbonato del socio
        socio = self.abbonamento.socio
        if socio:
            oggi = datetime.now().date()
            if oggi >= data_scadenza.date():
                self.abbonamento.deleteAbbonamento()
            elif oggi >= data_inizio.date():
                socio.abbonato = True
            else:
                socio.abbonato = False

            #salva socio aggiornato
            soci = Socio.getSoci()
            if socio.username in soci:
                soci[socio.username] = socio
                Socio.updateSoci(soci)

        QMessageBox.information(self, "Successo", "Abbonamento modificato correttamente.")
        self.close()
