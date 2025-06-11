

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox

from Campo import Campo
from datetime import datetime, timedelta

from Partita import Partita


class VistaModificaPartita(QWidget):
    def __init__(self, partita, parent=None):
        super(VistaModificaPartita, self).__init__(parent)
        self.partita = partita
        self.v_layout = QVBoxLayout()
        self.qlines = {}

        # Campi di testo precompilati
        self.add_info_text("codice", "Codice", str(partita.codice), editable=False)
        self.add_info_text("data", "Data", partita.data.strftime("%d/%m/%Y"))
        self.add_info_text("oraInizio", "Ora Inizio", partita.orarioInizio.strftime("%H:%M"))
        self.add_info_text("oraFine", "Ora Fine", partita.orarioFine.strftime("%H:%M"))

        # Radio buttons campo
        self.v_layout.addWidget(QLabel("Campo"))

        self.radio1 = QRadioButton(Campo.Calcetto_Interno.name)
        self.radio2 = QRadioButton(Campo.Calcetto_Esterno.name)
        self.radio3 = QRadioButton(Campo.Padel_Interno.name)
        self.radio4 = QRadioButton(Campo.Padel_Esterno.name)
        self.v_layout.addWidget(self.radio1)
        self.v_layout.addWidget(self.radio2)
        self.v_layout.addWidget(self.radio3)
        self.v_layout.addWidget(self.radio4)
        #con un ciclo for che itera per ogni campo in Campo non appaiono tutti

        btn_modifica = QPushButton("Salva modifiche")
        btn_modifica.clicked.connect(self.salvaModifiche)
        self.v_layout.addWidget(btn_modifica)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Modifica Partita")

    def add_info_text(self, nome, label, default_value="", editable=True):
        self.v_layout.addWidget(QLabel(label))
        text_box = QLineEdit()
        text_box.setText(default_value)
        text_box.setReadOnly(not editable)
        self.qlines[nome] = text_box
        self.v_layout.addWidget(text_box)

    def salvaModifiche(self):
        try:
            for nome, campo in self.qlines.items():
                if campo.text().strip() == "":
                    QMessageBox.critical(self, "Errore", f"Il campo '{nome}' è obbligatorio.")
                    return

            data = datetime.strptime(self.qlines["data"].text(), '%d/%m/%Y')
            ora_inizio = datetime.strptime(self.qlines["oraInizio"].text(), '%H:%M')
            ora_fine = datetime.strptime(self.qlines["oraFine"].text(), '%H:%M')

            if ora_fine <= ora_inizio:
                QMessageBox.critical(self, "Errore", "L'orario di fine deve essere successivo a quello di inizio.")
                return

            durata = datetime.combine(data.date(), ora_fine.time()) - datetime.combine(data.date(), ora_inizio.time())
            if durata < timedelta(hours=1):
                QMessageBox.critical(self, "Errore", "La partita deve durare almeno un'ora.")
                return

            if not (
                    self.radio1.isChecked() or self.radio2.isChecked() or self.radio3.isChecked() or self.radio4.isChecked()):
                raise ValueError("Nessun campo selezionato")

            #carica il dizionario

            partite = Partita.getPartite()

            codice = int(self.qlines["codice"].text())

            nuovo_inizio = datetime.combine(data.date(), ora_inizio.time())
            nuovo_fine = datetime.combine(data.date(), ora_fine.time())

            if self.radio1.isChecked():
                campo = Campo.Calcetto_Interno
            elif self.radio2.isChecked():
                campo = Campo.Calcetto_Esterno
            elif self.radio3.isChecked():
                campo = Campo.Padel_Interno
            else:
                campo = Campo.Padel_Esterno

            for p in partite.values():
                if p.codice == codice:
                    continue  #salta la partita che si sta modificando

                if p.campo == campo and p.data.date() == data.date():
                    inizio_esistente = datetime.combine(p.data.date(), p.orarioInizio.time())
                    fine_esistente = datetime.combine(p.data.date(), p.orarioFine.time())

                    if nuovo_inizio < fine_esistente and nuovo_fine > inizio_esistente:
                        QMessageBox.critical(
                            self,
                            "Errore",
                            f"Il campo è già occupato dalle {p.orarioInizio.strftime('%H:%M')} "
                            f"alle {p.orarioFine.strftime('%H:%M')}."
                        )
                        return

            partita = partite.get(codice)
            if partita:
                partita.data = data
                partita.orarioInizio = ora_inizio
                partita.orarioFine = ora_fine
                partita.orarioInizioOriginale = ora_inizio
                partita.orarioFineOriginale = ora_fine
                partita.campo = campo



                Partita.updatePartite(partite)

                QMessageBox.information(self, "Successo", "Partita modificata con successo!")
                self.close()
            else:
                QMessageBox.critical(self, "Errore", "Partita non trovata.")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nei dati: {str(e)}")
