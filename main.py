import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from VisteLogin.VistaLogin import VistaLogin


if __name__ == "__main__":
    from Socio import Socio

    Socio.aggiornaStatoAbbonamenti()
    app = QApplication(sys.argv)
    app.setStyle("Windows")
    app.setFont(QFont("Calibri", 10))
    login = VistaLogin()
    login.show()
    sys.exit(app.exec_())





