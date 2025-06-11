from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget

class VistaAvvisiSocio(QWidget):
    def __init__(self, socio):
        super().__init__()
        self.setWindowTitle("Bacheca Avvisi")
        self.resize(600, 300)
        layout = QVBoxLayout()
        self.socio = socio
        avvisi = QListWidget()

        for avviso in self.socio.avvisi:
            avvisi.addItem(avviso)

        layout.addWidget(QLabel("Avvisi recenti:"))
        layout.addWidget(avvisi)
        self.setLayout(layout)
