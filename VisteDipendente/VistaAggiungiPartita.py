import os
import pickle
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox

from Campo import Campo
from Partita import Partita


class VistaAggiungiPartita(QWidget):

    def __init__(self, parent=None):
        super(VistaAggiungiPartita, self).__init__(parent)
        self.v_layout = QVBoxLayout()
        self.qlines = {}
        self.add_info_text("codice", "Codice (numero intero)")
        self.add_info_text("data", "Data (GG/MM/AAAA) ")
        self.add_info_text("oraInizio", "Ora Inizio Partita (HH:MM)")
        self.add_info_text("oraFine", "Ora Fine Partita (HH:MM)")
        self.v_layout.addWidget(QLabel("Campo"))#fare classe enum per i campi e RadioButton
        self.radio1 = QRadioButton(Campo.Calcetto_Interno.name)
        self.radio2 = QRadioButton(Campo.Calcetto_Esterno.name)
        self.radio3 = QRadioButton(Campo.Padel_Interno.name)
        self.radio4 = QRadioButton(Campo.Padel_Esterno.name)
        self.v_layout.addWidget(self.radio1)
        self.v_layout.addWidget(self.radio2)
        self.v_layout.addWidget(self.radio3)
        self.v_layout.addWidget(self.radio4)

        btn_add = QPushButton("Aggiungi")
        btn_add.clicked.connect(self.aggiungiPartita)
        self.qlines["btn_add"] = btn_add #Perché?
        self.v_layout.addWidget(btn_add)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Aggiungi Partita")

    def add_info_text(self, nome, label):
        self.v_layout.addWidget(QLabel(label))
        current_text = QLineEdit(self)
        self.qlines[nome] = current_text
        self.v_layout.addWidget(current_text)

    def aggiungiPartita(self):
        for value in self.qlines.values():
            if isinstance(value, QLineEdit):
                if value.text() == "":
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisici tutte le informazioni richieste',  QMessageBox.Ok, QMessageBox.Ok)
                    return
        if not (self.radio1.isChecked() or self.radio2.isChecked() or self.radio3.isChecked() or self.radio4.isChecked()):
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisici tutte le informazioni richieste',
                                 QMessageBox.Ok, QMessageBox.Ok)
            return

        try:
            codice = int(self.qlines["codice"].text())
        except ValueError:
            QMessageBox.critical(self, "Errore", "Il codice deve essere un numero intero.")
            return



        partite = Partita.getPartite()
        if codice in partite:
            QMessageBox.critical(self, "Errore", f"Esiste già una partita con codice {codice}.")
            return



        try:
            data = datetime.strptime(self.qlines["data"].text(), '%d/%m/%Y')
            ora_inizio = datetime.strptime(self.qlines["oraInizio"].text(), '%H:%M')
            ora_fine = datetime.strptime(self.qlines["oraFine"].text(), '%H:%M')
        except ValueError:
            QMessageBox.critical(self, "Errore", "Formato data o ora non valido. Usa GG/MM/AAAA e HH:MM.")
            return

        if ora_fine <= ora_inizio:
            QMessageBox.critical(self, "Errore", "L'orario di fine deve essere successivo a quello di inizio.")
            return

        durata = datetime.combine(data, ora_fine.time()) - datetime.combine(data, ora_inizio.time())
        if durata < timedelta(hours=1):
            QMessageBox.critical(self, "Errore", "La partita deve durare almeno un'ora.")
            return

        if self.radio1.isChecked():
            campo = Campo.Calcetto_Interno
        elif self.radio2.isChecked():
            campo = Campo.Calcetto_Esterno
        elif self.radio3.isChecked():
            campo = Campo.Padel_Interno
        else:
            campo = Campo.Padel_Esterno

        #controllo sovrapposizioni
        nuovo_inizio = datetime.combine(data.date(), ora_inizio.time())
        nuovo_fine = datetime.combine(data.date(), ora_fine.time())

        for p in partite.values():
            if p.campo == campo and p.data.date() == data.date():
                inizio_esistente = datetime.combine(p.data, p.orarioInizio.time())
                fine_esistente = datetime.combine(p.data, p.orarioFine.time())

                if nuovo_inizio < fine_esistente and nuovo_fine > inizio_esistente:
                    QMessageBox.critical(
                        self,
                        "Errore",
                        f"Conflitto: il campo è già occupato dalle {p.orarioInizio.strftime('%H:%M')} "
                        f"alle {p.orarioFine.strftime('%H:%M')}."
                    )
                    return


        partita = Partita()
        try:


            data = datetime.strptime(self.qlines["data"].text(), '%d/%m/%Y')
            ora_inizio = datetime.strptime(self.qlines["oraInizio"].text(), '%H:%M')
            ora_fine = datetime.strptime(self.qlines["oraFine"].text(), '%H:%M')
            if self.radio1.isChecked():
                campo = Campo.Calcetto_Interno
            elif self.radio2.isChecked():
                campo = Campo.Calcetto_Esterno
            elif self.radio3.isChecked():
                campo = Campo.Padel_Interno
            else:
                campo = Campo.Padel_Esterno
            partita.createPartita(codice, data, ora_inizio, ora_fine, campo)
            QMessageBox.information(self, "Successo", "Partita aggiunta correttamente.")
        except:
            QMessageBox.critical(self, 'Errore', 'Controlla bene i dati inseriti', QMessageBox.Ok, QMessageBox.Ok )
            return
        self.close()








