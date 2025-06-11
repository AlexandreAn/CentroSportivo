from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QPushButton, QSizePolicy
from VisteAmministratore.VistaGestioneDipendenti import VistaGestioneDipendenti
from VisteAmministratore.VistaStatistiche import VistaStatistiche
from PyQt5.QtWidgets import QWidget


class VistaHomeAmministratore(QWidget):

    def __init__(self, parent=None):
        super(VistaHomeAmministratore, self).__init__(parent)
        
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.get_generic_button("Gestione Dipendenti", self.gestisciDipendenti), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Visualizza Statistiche", self.visualizzaStatistiche), 0, 1)
        grid_layout.addWidget(self.get_generic_button("Log-out", self.goLogout), 1, 0, 2, Qt.AlignHCenter)

        self.setLayout(grid_layout)
        self.resize(500,400)
        self.setWindowTitle("Benvenuto")

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(on_click)
        return button

    def gestisciDipendenti(self):
        self.vista_gestione_dipendenti = VistaGestioneDipendenti()
        self.vista_gestione_dipendenti.show()


    def visualizzaStatistiche(self):
        self.vista_statistiche = VistaStatistiche()
        self.vista_statistiche.show()

    def goLogout(self):
        from VisteLogin.VistaLogin import VistaLogin
        self.login_view = VistaLogin()
        self.login_view.show()
        self.close()


