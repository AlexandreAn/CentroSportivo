import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from Socio import Socio
from VisteAmministratore.VistaHomeAmministratore import VistaHomeAmministratore
from VisteDipendente.VistaHomeDipendente import VistaHomeDipendente
from VisteLogin.VistaRegistrazioneSocio import VistaRegistrazioneSocio
from VisteSocio.VistaHomeSocio import VistaHomeSocio

class VistaLogin(QWidget):
    def __init__(self, parent=None):
        super(VistaLogin, self).__init__(parent)
        self.setWindowTitle("Login")
        self.resize(300, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username:"))
        self.usernameInput = QLineEdit()
        layout.addWidget(self.usernameInput)

        layout.addWidget(QLabel("Password:"))
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password) #oscura il testo
        layout.addWidget(self.passwordInput)

        self.labelDomanda = QLabel()
        self.labelDomanda.setVisible(False)
        layout.addWidget(self.labelDomanda)

        self.inputRispostaSicurezza = QLineEdit()
        self.inputRispostaSicurezza.setPlaceholderText("Rispondi alla domanda di sicurezza")
        self.inputRispostaSicurezza.setVisible(False)
        layout.addWidget(self.inputRispostaSicurezza)

        self.tentativi = 0  # contatore login falliti

        self.loginButton = QPushButton("Login")
        self.loginButton.clicked.connect(self.login)
        layout.addWidget(self.loginButton)
        layout.addStretch()
        self.registerButton = QPushButton("Registrati come Socio")
        self.registerButton.clicked.connect(self.registratiSocio)
        layout.addWidget(self.registerButton)

        self.setLayout(layout)

    def registratiSocio(self):
        self.vistaRegistrazione = VistaRegistrazioneSocio()
        self.vistaRegistrazione.show()

    def login(self):
        self.tentativi += 1
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not os.path.exists("Dati/data.json"):
            QMessageBox.critical(self, "Errore", "Nessun utente registrato.")
            return

        with open("Dati/data.json", "r") as f:
            utenti_data = json.load(f)

        for utente in utenti_data["utenti"]:
            if utente["username"] == username and utente["password"] == password:
                ruolo = utente["ruolo"]
                if ruolo == "amministratore":
                    self.hide()
                    self.vistaAmministratore = VistaHomeAmministratore()
                    self.vistaAmministratore.show()
                    self.tentativi = 0
                    return

                elif ruolo == "dipendente":
                    self.hide()
                    self.vistaDipendente = VistaHomeDipendente()
                    self.vistaDipendente.show()
                    self.tentativi = 0
                    return

                elif ruolo == "socio":
                    soci = Socio.getSoci()
                    socio = soci.get(username)
                    if socio:
                        self.hide()
                        self.vistaSocio = VistaHomeSocio(socio)
                        self.vistaSocio.show()
                        self.tentativi = 0
                        return
                    QMessageBox.critical(self, "Errore", "Dati socio non trovati.")
                    return

        if self.tentativi > 5:
            soci = Socio.getSoci()
            username = self.usernameInput.text()
            if username in soci:
                socio = soci[username]
                self.labelDomanda.setText(f"Domanda di sicurezza:\n{socio.domandaSicurezza}")
                self.labelDomanda.setVisible(True)
                self.inputRispostaSicurezza.setVisible(True)

                rispostaUtente = self.inputRispostaSicurezza.text().strip().lower()
                if rispostaUtente == socio.rispostaSicurezza.strip().lower():
                    messaggio = f"Accesso effettuato tramite domanda di sicurezza.\nRicorda: Username: {socio.username}, Password: {socio.password}"
                    socio.avvisi.append(messaggio)
                    self.salvaSocio(socio)
                    self.hide()
                    self.vistaSocio = VistaHomeSocio(socio)
                    self.vistaSocio.show()
                    return

        QMessageBox.critical(self, "Errore", "Username o password errati.")

    def salvaSocio(self, socio):
        import pickle
        soci = Socio.getSoci()
        soci[socio.username] = socio
        with open("Dati/Soci.pickle", "wb") as f:
            pickle.dump(soci, f, pickle.HIGHEST_PROTOCOL)


