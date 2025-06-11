from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

class VistaConfermaEliminazioneDipendente(QWidget):
    def __init__(self, dipendente):
        super().__init__()
        self.dipendente = dipendente
        self.setWindowTitle("Conferma Eliminazione")
        self.resize(400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Nome: {dipendente.nome}"))
        layout.addWidget(QLabel(f"Cognome: {dipendente.cognome}"))
        layout.addWidget(QLabel(f"Username: {dipendente.username}"))

        btn_elimina = QPushButton("Elimina Definitivamente")
        btn_elimina.setStyleSheet("color: red; font-weight: bold")
        btn_elimina.clicked.connect(self.elimina)
        layout.addWidget(btn_elimina)

        self.setLayout(layout)

    def elimina(self):
        self.dipendente.deleteDipendente()
        QMessageBox.information(self, "Eliminato", f" Dipendente'{self.dipendente.username}' eliminato con successo.")
        self.close()