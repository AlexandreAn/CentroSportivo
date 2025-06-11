from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from Dipendente import Dipendente  #assicurati che il percorso sia corretto

class VistaAggiungiDipendente(QWidget):
    def __init__(self, parent=None):
        super(VistaAggiungiDipendente, self).__init__(parent)

        self.setWindowTitle("Aggiungi Dipendente")
        self.resize(400, 300)

        layout = QVBoxLayout()

        # Etichette e campi di input
        self.input_username = QLineEdit()
        self.input_password = QLineEdit()
        self.input_nome = QLineEdit()
        self.input_cognome = QLineEdit()
        self.input_cellulare = QLineEdit()
        self.input_mail = QLineEdit()

        self.input_password.setEchoMode(QLineEdit.Password)

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

        # Pulsante conferma
        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.clicked.connect(self.aggiungiDipendente)
        layout.addWidget(self.btn_conferma)

        self.setLayout(layout)

    def aggiungiDipendente(self):
        import os
        import json

        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        cellulare = self.input_cellulare.text().strip()
        mail = self.input_mail.text().strip()

        #controllo campi obbligatori
        if not all([username, password, nome, cognome, cellulare, mail]):
            QMessageBox.critical(self, "Errore", "Compila tutti i campi obbligatori.")
            return

        #controllo su JSON
        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
                for utente in data.get("utenti", []):
                    if utente["username"] == username:
                        QMessageBox.critical(self, "Errore", "Username già esistente nel sistema.")
                        return

        #controllo su Pickle 
        if os.path.exists("Dati/Dipendenti.pickle"):
            dipendenti = Dipendente.getDipendenti()
            if username in dipendenti:
                QMessageBox.critical(self, "Errore", "Username già registrato tra i dipendenti.")
                return

        # crea il dipendente
        try:
            dip = Dipendente()
            dip.createDipendente(username, password, nome, cognome, cellulare, mail)
            QMessageBox.information(self, "Successo", "Dipendente aggiunto correttamente.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore durante la creazione: {str(e)}")
