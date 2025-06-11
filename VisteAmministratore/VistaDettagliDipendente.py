from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class VistaDettagliDipendente(QWidget):
    def __init__(self, dipendente):
        super().__init__()
        self.setWindowTitle("Dettagli Dipendente")
        self.resize(500, 400)

        layout = QVBoxLayout()

        layout.addWidget(QLabel(f"Username: {dipendente.username}"))
        layout.addWidget(QLabel(f"Password: {dipendente.password}"))
        layout.addWidget(QLabel(f"Nome: {dipendente.nome}"))
        layout.addWidget(QLabel(f"Cognome: {dipendente.cognome}"))
        layout.addWidget(QLabel(f"Cellulare: {dipendente.cellulare}"))
        layout.addWidget(QLabel(f"Email: {dipendente.mail}"))

        self.setLayout(layout)