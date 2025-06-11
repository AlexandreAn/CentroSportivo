from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer
from datetime import datetime
from Socio import Socio
from Partita import Partita

class VistaPrenotazionePartite(QWidget):
    def __init__(self, socioAutenticato, parent=None):
        super(VistaPrenotazionePartite, self).__init__(parent)
        self.socio = socioAutenticato
        self.partite = self.filtraPartite() #partite non prenotate o prenotate dal socio in questione
        self.setWindowTitle("Prenota una Partita")
        self.resize(925, 300)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["DATA", "CAMPO", "ORA INIZIO", "ORA FINE", "COSTO", "AZIONE", "CANCELLA"])
        self.table.setRowCount(len(self.partite))

        for row, partita in enumerate(self.partite):
            info = partita.getInfoPartita()
            self.table.setItem(row, 0, QTableWidgetItem(info["data"]))
            self.table.setItem(row, 1, QTableWidgetItem(info["campo"]))
            orarioInizio = QLineEdit(info["ora_inizio"])
            orarioFine = QLineEdit(info["ora_fine"])
            self.table.setCellWidget(row, 2, orarioInizio)
            self.table.setCellWidget(row, 3, orarioFine)
            self.aggiornaCosto(row, partita)

            if partita.socio is not None and partita.socio.username == self.socio.username:
                check = QPushButton("✅")
                check.setEnabled(False)
                check.setStyleSheet("color: green; font-weight: bold;")
                self.table.setCellWidget(row, 5, check)
                btn_cancella = QPushButton("Cancella")
                btn_cancella.setStyleSheet("color: red")
                btn_cancella.clicked.connect(lambda _, p=partita, r=row: self.cancellaPrenotazione(p, r))
                # _ per gestire il segnale click altrimenti non funziona
                self.table.setCellWidget(row, 6, btn_cancella)
            else:
                btn = QPushButton("Prenota")
                btn.clicked.connect(lambda _, p=partita, r=row: self.prenotaPartita(p, r))
                self.table.setCellWidget(row, 5, btn)

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.timerAggiornaCosti = QTimer(self)
        self.timerAggiornaCosti.timeout.connect(lambda: [
            self.aggiornaCosto(riga, partita)
            for riga, partita in enumerate(self.partite)
            if self.table.cellWidget(riga, 5) and isinstance(self.table.cellWidget(riga, 5),
                                                             QPushButton) and self.table.cellWidget(riga,
                                                                                                    5).text() == "Prenota"
        ])
        self.timerAggiornaCosti.start(1000)

    def filtraPartite(self):
        try:
            allPartite = Partita.getPartite()
            partiteFiltrate = []
            for partita in allPartite.values():
                if partita.socio is None or partita.socio.username == self.socio.username:
                    partiteFiltrate.append(partita)
            partiteOrdinate = sorted(partiteFiltrate, key=lambda p: (p.data, p.orarioInizio))
            return partiteOrdinate

        except:
            return []

    def aggiornaCosto(self, row, partita):
        try:
            inizioInserito = self.table.cellWidget(row, 2).text()
            fineInserita = self.table.cellWidget(row, 3).text()
            orarioInizio = datetime.strptime(inizioInserito, "%H:%M")
            orarioFine = datetime.strptime(fineInserita, "%H:%M")
            if orarioInizio < partita.orarioInizio or orarioFine > partita.orarioFine or orarioInizio >= orarioFine:
                self.table.setItem(row, 4, QTableWidgetItem("Errore: Orario non valido"))
                return

            if ((orarioFine - orarioInizio).seconds / 60) < 60.0:
                self.table.setItem(row, 4, QTableWidgetItem("Durata minima 1 ora"))
                return

            durataMinuti = (orarioFine - orarioInizio).seconds / 60
            costo = round(durataMinuti * partita.campo.value, 2)
            #Nel caso il socio fosse abbonato gli viene applicato lo sconto del 20% sul costo
            if self.socio.abbonato==True:
                costo=self.applicaSconto(costo)
            self.table.setItem(row, 4, QTableWidgetItem(f"{costo:.2f}€"))
        except:
            self.table.setItem(row, 4, QTableWidgetItem("Errore"))

    def applicaSconto(self,costo):
        return (costo - (costo * 20) / 100)

    def prenotaPartita(self, partita, row):
        try:
            inizioInserito = self.table.cellWidget(row, 2).text()
            fineInserita = self.table.cellWidget(row, 3).text()
            try:
                orarioInizio = datetime.strptime(inizioInserito, "%H:%M")
                orarioFine = datetime.strptime(fineInserita, "%H:%M")
            except ValueError:
                QMessageBox.warning(self, "Errore di Formato", "L'orario deve essere nel formato HH:MM (es. 14:30).")
                return

            if orarioInizio < partita.orarioInizio or orarioFine > partita.orarioFine or orarioInizio >= orarioFine:
                QMessageBox.warning(self, "Errore",
                                    "Orario non valido: Non rispetta l'orario disponibile.")
                return

            if ((orarioFine - orarioInizio).seconds / 60) < 60.0:
                QMessageBox.warning(self, "Errore", "La durata minima della prenotazione è di 1 ora.")
                return

            partita.orarioInizio = orarioInizio
            partita.orarioFine = orarioFine
            partita.socio = self.socio
            self.socio.partitePrenotate[partita.codice] = partita
            self.salvaPartite(partita)
            self.salvaSocio()
            check = QPushButton("✅")
            check.setEnabled(False)
            check.setStyleSheet("color: green; font-weight: bold;")
            self.table.setCellWidget(row, 5, check)
            btnCancella = QPushButton("Cancella")
            btnCancella.setStyleSheet("color: red")
            btnCancella.clicked.connect(lambda _, p=partita, r=row: self.cancellaPrenotazione(p, r))
            self.table.setCellWidget(row, 6, btnCancella)

        except Exception as e:
            QMessageBox.critical(self, "Errore prenotazione", f"Errore nella prenotazione:\n{e}")

    def cancellaPrenotazione(self, partita, row):
        try:
            partita.socio = None
            partita.orarioInizio = partita.orarioInizioOriginale
            partita.orarioFine = partita.orarioFineOriginale
            if partita.codice in self.socio.partitePrenotate:
                del self.socio.partitePrenotate[partita.codice]
            self.salvaPartite(partita)
            self.salvaSocio()
            orarioInizio = QLineEdit(partita.orarioInizio.strftime("%H:%M"))
            orarioFine = QLineEdit(partita.orarioFine.strftime("%H:%M"))
            self.table.setCellWidget(row, 2, orarioInizio)
            self.table.setCellWidget(row, 3, orarioFine)
            btn = QPushButton("Prenota")
            btn.clicked.connect(lambda _, p=partita, r=row: self.prenotaPartita(p, r))
            self.table.setCellWidget(row, 5, btn)
            self.table.setCellWidget(row, 6, None)
        except Exception as e:
            QMessageBox.critical(self, "Errore cancellazione", f"Errore durante la cancellazione:\n{e}")

    def salvaPartite(self, nuova_partita):
        partite = Partita.getPartite()
        partite[nuova_partita.codice] = nuova_partita
        Partita.updatePartite(partite)

    def salvaSocio(self):
        soci = Socio.getSoci()
        soci[self.socio.username] =self.socio
        Socio.updateSoci(soci)
