from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy

from VisteDipendente.VistaGestioneBackup import VistaGestioneBackup
from VisteDipendente.VistaGestionePartite import VistaGestionePartite
from VisteDipendente.VistaGestioneSoci import VistaGestioneSoci



class VistaHomeDipendente(QWidget):

    def __init__(self, parent=None):
        super(VistaHomeDipendente, self).__init__(parent) #creiamo una vista nuova, parent=None
        grid_layout = QGridLayout() #nella home abbiamo 4 bottoni disposti a griglia
        grid_layout.addWidget(self.get_generic_button("Gestione Partite", self.goPartite), 0, 0)
        grid_layout.addWidget(self.get_generic_button("Gestione Soci", self.goSoci), 0, 1)
        grid_layout.addWidget(self.get_generic_button("Backup", self.goBackup), 1, 0)
        grid_layout.addWidget(self.get_generic_button("Log-out", self.goLogout), 1, 1)
        self.setLayout(grid_layout)
        self.resize(500, 400)
        self.setWindowTitle("Benvenuto")
        #lo stile di default potrebbe dare problemi se si usa il mac, come impostare uno stile PyQt?

    def get_generic_button(self, titolo, on_click):
        button = QPushButton(titolo)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) #ridimensionamento finestra e bottone
        button.clicked.connect(on_click) #non gli piace connect
        return button

    def goSoci(self):
        self.vista_gestione_soci = VistaGestioneSoci()
        self.vista_gestione_soci.show()


    def goPartite(self):
        self.vista_gestione_partite = VistaGestionePartite()
        self.vista_gestione_partite.show()


    def goLogout(self):
        from VisteLogin.VistaLogin import VistaLogin #se lo faccio globale si crea un errore di import circolare
        self.vista_login = VistaLogin()
        self.vista_login.show()
        self.close()

    def goBackup(self):
        self.vista_backup = VistaGestioneBackup()
        self.vista_backup.show()



