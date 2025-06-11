from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import os

from Socio import Socio


class VistaRicercaSocio(QWidget):
    def __init__(self, on_socio_trovato, parent=None):

        #parametro on_socio_trovato: funzione da eseguire se il socio viene trovato

        super().__init__(parent)
        self.on_socio_trovato = on_socio_trovato
        self.setWindowTitle("Ricerca Socio")
        self.resize(400, 250)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Inserire i dati del socio"))

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        layout.addWidget(self.input_nome)

        self.input_cognome = QLineEdit()
        self.input_cognome.setPlaceholderText("Cognome")
        layout.addWidget(self.input_cognome)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Oppure username")
        layout.addWidget(self.input_username)

        self.btn_cerca = QPushButton("Cerca")
        self.btn_cerca.clicked.connect(self.cercaSocio)
        layout.addWidget(self.btn_cerca)

        self.setLayout(layout)

    def cercaSocio(self):
        nome = self.input_nome.text().strip().lower() #strip() rimuove spazi iniziali e finali
        cognome = self.input_cognome.text().strip().lower()
        username = self.input_username.text().strip().lower()

        if not (username or (nome and cognome)):
            QMessageBox.warning(self, "Attenzione", "Inserisci username oppure nome e cognome.")
            return

        if not os.path.exists("Dati/Soci.pickle"):
            QMessageBox.critical(self, "Errore", "Attualmente non ci sono soci.")
            return



        self.soci = Socio.getSoci()

        socio_trovato = None
        if username:
            socio_trovato = self.soci.get(username)
        else:
            soci_corrispondenti = [
                s for s in self.soci.values()
                if s.nome.lower() == nome and s.cognome.lower() == cognome
            ]

            if len(soci_corrispondenti) == 1:
                socio_trovato = soci_corrispondenti[0]
            elif len(soci_corrispondenti) > 1:
                from PyQt5.QtWidgets import QInputDialog

                usernames = [s.username for s in soci_corrispondenti]
                selected, ok = QInputDialog.getItem(
                    self,
                    "Seleziona Socio",
                    f"Sono stati trovati {len(soci_corrispondenti)} soci con lo stesso nome e cognome. Seleziona lo username:",
                    usernames,
                    editable=False
                )
                if ok and selected:
                    socio_trovato = self.soci.get(selected)
            else:
                socio_trovato = None

        if socio_trovato:
            self.on_socio_trovato(socio_trovato)
            self.close()
        else:
            QMessageBox.information(self, "Non trovato", "Nessun socio corrispondente ai dati inseriti.")

