from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import os
import json
from Dipendente import Dipendente


class VistaModificaDipendente(QWidget):
    def __init__(self, dipendente, parent=None):
        super(VistaModificaDipendente, self).__init__(parent)
        self.dipendente = dipendente

        self.setWindowTitle("Modifica Dipendente")
        self.resize(400, 300)

        layout = QVBoxLayout()

        self.input_username = QLineEdit()
        self.input_username.setText(dipendente.username)
        self.input_username.setDisabled(True)

        self.input_password = QLineEdit()
        self.input_password.setText(dipendente.password)
        self.input_password.setEchoMode(QLineEdit.Password)

        self.input_nome = QLineEdit()
        self.input_nome.setText(dipendente.nome)

        self.input_cognome = QLineEdit()
        self.input_cognome.setText(dipendente.cognome)

        self.input_cellulare = QLineEdit()
        self.input_cellulare.setText(dipendente.cellulare)

        self.input_mail = QLineEdit()
        self.input_mail.setText(dipendente.mail)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.input_username)

        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.input_password)

        layout.addWidget(QLabel("Nome:"))
        layout.addWidget(self.input_nome)

        layout.addWidget(QLabel("Cognome:"))
        layout.addWidget(self.input_cognome)

        layout.addWidget(QLabel("Cellulare:"))
        layout.addWidget(self.input_cellulare)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.input_mail)

        self.btn_conferma = QPushButton("Conferma Modifiche")
        self.btn_conferma.clicked.connect(self.salvaModifiche)
        layout.addWidget(self.btn_conferma)

        self.setLayout(layout)

    def salvaModifiche(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        cellulare = self.input_cellulare.text().strip()
        mail = self.input_mail.text().strip()

        if not all([password, nome, cognome, cellulare, mail]):
            QMessageBox.critical(self, "Errore", "I campi obbligatori non possono essere vuoti.")
            return

        self.dipendente.password = password
        self.dipendente.nome = nome
        self.dipendente.cognome = cognome
        self.dipendente.cellulare = cellulare
        self.dipendente.mail = mail

        dipendenti = Dipendente.getDipendenti()
        dipendenti[username] = self.dipendente
        Dipendente.updateDipendenti(dipendenti)

        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
            for utente in data["utenti"]:
                if utente["username"] == username:
                    utente["password"] = password
                    utente["nome"] = nome
                    utente["cognome"] = cognome
                    break
            with open("Dati/data.json", "w") as f:
                json.dump(data, f, indent=4)

        QMessageBox.information(self, "Successo", "Dati aggiornati correttamente.")
        self.close()
