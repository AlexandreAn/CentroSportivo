from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
import os
from Dipendente import Dipendente

class VistaRicercaDipendente(QWidget):
    def __init__(self, on_dipendente_trovato, parent=None):
        super().__init__(parent)
        self.on_dipendente_trovato = on_dipendente_trovato
        self.setWindowTitle("Ricerca Dipendente")
        self.resize(400, 250)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Inserire i dati del dipendente"))

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        layout.addWidget(self.input_nome)

        self.input_cognome = QLineEdit()
        self.input_cognome.setPlaceholderText("Cognome")
        layout.addWidget(self.input_cognome)

        self.input_username = QComboBox()
        self.input_username.setEditable(True)
        self.input_username.setPlaceholderText("Oppure seleziona username")
        layout.addWidget(self.input_username)

        self.carica_usernames()

        self.btn_cerca = QPushButton("Cerca")
        self.btn_cerca.clicked.connect(self.cercaDipendente)
        layout.addWidget(self.btn_cerca)

        self.setLayout(layout)

    def carica_usernames(self):
        self.input_username.clear()
        if os.path.exists("Dati/Dipendenti.pickle"):
            dipendenti = Dipendente.getDipendenti()
            self.input_username.addItem("")  # Prima voce vuota per "nessuna selezione"
            for username in dipendenti.keys():
                self.input_username.addItem(username)

    def cercaDipendente(self):
        nome = self.input_nome.text().strip().lower()
        cognome = self.input_cognome.text().strip().lower()
        username = self.input_username.currentText().strip().lower()

        if not (username or (nome and cognome)):
            QMessageBox.warning(self, "Attenzione", "Inserisci username oppure nome e cognome.")
            return

        if not os.path.exists("Dati/Dipendenti.pickle"):
            QMessageBox.critical(self, "Errore", "Attualmente non ci sono dipendenti.")
            return

        self.dipendenti = Dipendente.getDipendenti()

        dipendente_trovato = None
        if username:
            dipendente_trovato = self.dipendenti.get(username)
        else:
            for s in self.dipendenti.values():
                if s.nome.lower() == nome and s.cognome.lower() == cognome:
                    dipendente_trovato = s
                    break

        if dipendente_trovato:
            self.on_dipendente_trovato(dipendente_trovato)
            self.close()
        else:
            QMessageBox.information(self, "Non trovato", "Nessun dipendente corrispondente ai dati inseriti.")
