import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from Socio import Socio

class VistaRegistrazioneSocio(QWidget):
    def __init__(self, parent=None):
        super(VistaRegistrazioneSocio, self).__init__(parent)
        self.setWindowTitle("Registrazione Socio")
        self.resize(400, 300)
        self.layout = QVBoxLayout()
        self.qlines = {}
        # Campi da compilare
        self.add_info_text("nome", "Nome")
        self.add_info_text("cognome", "Cognome")
        self.add_info_text("username", "Username")
        self.add_info_text("password", "Password", password=True)
        self.add_info_text("cellulare", "Cellulare")
        self.add_info_text("mail", "Email")

        self.comboDomande = QComboBox()
        self.comboDomande.addItems([
            "Qual è il nome del tuo primo animale domestico?",
            "Qual è il cognome del tuo insegnante preferito?",
            "In quale città sei nato?",
            "Qual è il titolo del tuo libro preferito?",
            "Qual era il tuo soprannome da bambino?"
        ])
        self.layout.addWidget(QLabel("Domanda di sicurezza"))
        self.layout.addWidget(self.comboDomande)

        self.inputRisposta = QLineEdit()
        self.layout.addWidget(QLabel("Risposta di sicurezza"))
        self.layout.addWidget(self.inputRisposta)

        btn_registra = QPushButton("Registrati")
        btn_registra.clicked.connect(self.registraSocio)
        self.layout.addWidget(btn_registra)

        self.setLayout(self.layout)

    def add_info_text(self, nome, label, password=False):
        self.layout.addWidget(QLabel(label))
        qline = QLineEdit()
        if password:
            qline.setEchoMode(QLineEdit.Password)
        self.qlines[nome] = qline
        self.layout.addWidget(qline)

    def registraSocio(self):
        # Controllo campi vuoti
        for key, value in self.qlines.items():
            if value.text() == "":
                QMessageBox.critical(self, "Errore", f"Il campo '{key}' è obbligatorio")
                return

        # Verifica se username esiste già
        username = self.qlines["username"].text()
        if os.path.exists("Dati\data.json"):
            with open("Dati\data.json", "r") as f:
                datiUtenti = json.load(f)
                for utente in datiUtenti["utenti"]:
                    if utente["username"] == username:
                        QMessageBox.critical(self, "Errore", "Username già esistente")
                        return
        else:
            datiUtenti = {"utenti": []}

        risposta = self.inputRisposta.text().strip().lower()
        domanda = self.comboDomande.currentText()

        if not risposta:
            QMessageBox.critical(self, "Errore", "La risposta di sicurezza è obbligatoria")
            return
        if not domanda:
            QMessageBox.critical(self, "Errore", "La domanda di sicurezza è obbligatoria")
            return


        socio = Socio()
        password = self.qlines["password"].text()
        nome = self.qlines["nome"].text()
        cognome = self.qlines["cognome"].text()
        cellulare = self.qlines["cellulare"].text()
        mail = self.qlines["mail"].text()
        socio.createSocio(username, password, nome, cognome, cellulare, mail, domanda, risposta)

        # Salva su JSON
        nuovoUtente = {
            "username": username,
            "password": password,
            "ruolo": "socio",
            "risposta_sicurezza": risposta
        }
        datiUtenti["utenti"].append(nuovoUtente)

        with open("Dati\data.json", "w") as f:
            json.dump(datiUtenti, f, indent=4)

        QMessageBox.information(self, "Successo", "Registrazione completata!")
        self.close()
