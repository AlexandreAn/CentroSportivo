from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class VistaDettagliSocio(QWidget):
    def __init__(self, socio):
        super().__init__()
        self.setWindowTitle("Dettagli Socio")
        self.socio = socio
        self.resize(500, 400)

        layout = QVBoxLayout()


        info = self.socio.getInfoSocio()
        layout.addWidget(QLabel(f"Username: {info['username']}"))
        layout.addWidget(QLabel(f"Nome: {info['nome']}"))
        layout.addWidget(QLabel(f"Cognome: {info['cognome']}"))
        layout.addWidget(QLabel(f"Cellulare: {info['cellulare']}"))
        layout.addWidget(QLabel(f"Email: {info['mail']}"))
        layout.addWidget(QLabel(f"Abbonato: {info['abbonato']}"))

        layout.addWidget(QLabel("Partite prenotate:"))

        lista = QListWidget()
        if self.socio.partitePrenotate:
            for p in self.socio.partitePrenotate.values():
                lista.addItem(f"{p.data.strftime('%d/%m/%Y')} - {p.campo.name} "
                              f"({p.orarioInizio.strftime('%H:%M')} - {p.orarioFine.strftime('%H:%M')})")
        else:
            lista.addItem("Nessuna prenotazione.")

        layout.addWidget(lista)
        self.setLayout(layout)
