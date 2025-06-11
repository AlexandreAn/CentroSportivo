from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class VistaConfermaEliminazioneSocio(QWidget):
    def __init__(self, socio):
        super().__init__()
        self.socio = socio
        self.setWindowTitle("Conferma Eliminazione")
        self.resize(400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Nome: {socio.nome}"))
        layout.addWidget(QLabel(f"Cognome: {socio.cognome}"))
        layout.addWidget(QLabel(f"Username: {socio.username}"))

        btn_elimina = QPushButton("Elimina Definitivamente")
        btn_elimina.setStyleSheet("color: red; font-weight: bold")
        btn_elimina.clicked.connect(self.elimina)
        layout.addWidget(btn_elimina)

        self.setLayout(layout)

    def elimina(self):
        self.socio.deleteSocio()
        QMessageBox.information(self, "Eliminato", f"Socio '{self.socio.username}' eliminato con successo.")
        self.close()
