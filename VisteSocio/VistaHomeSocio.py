from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QSizePolicy
from PyQt5.QtCore import Qt
from VisteSocio.VistaAvvisiSocio import VistaAvvisiSocio
from VisteSocio.VistaPrenotazionePartite import VistaPrenotazionePartite

class VistaHomeSocio(QWidget):
    def __init__(self, socioAutenticato, parent=None):
        super(VistaHomeSocio, self).__init__(parent)
        self.socioAutenticato = socioAutenticato
        label= QLabel(f"Benvenuto {self.socioAutenticato.username}", self)
        label.setFont(QFont("Arial", 20))
        label.setGeometry(0, 0, 500, 100)
        label.setAlignment(Qt.AlignCenter)

        grid_layout = QGridLayout()
        grid_layout.addWidget(label, 0, 0, 1, 2)
        grid_layout.addWidget(self.get_generic_button("Prenota Campo", self.visualizzaTurniLiberi), 1, 0)
        grid_layout.addWidget(self.get_generic_button("Bacheca Avvisi", self.goBacheca), 1, 1)
        grid_layout.addWidget(self.get_generic_button("Logout", self.goLogout), 2, 0, 2, Qt.AlignHCenter)

        self.setLayout(grid_layout)
        self.resize(500,400)
        self.setWindowTitle("Benvenuto")

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        button.clicked.connect(on_click) 
        return button

    def visualizzaTurniLiberi(self):
        self.vistaPrenotaPartite = VistaPrenotazionePartite(self.socioAutenticato)
        self.vistaPrenotaPartite.show()

    def goLogout(self):
        from VisteLogin.VistaLogin import VistaLogin
        self.vistaLogin = VistaLogin()
        self.vistaLogin.show()
        self.close()

    def goBacheca(self):
        self.vistaAvvisi = VistaAvvisiSocio(self.socioAutenticato)
        self.vistaAvvisi.show()

