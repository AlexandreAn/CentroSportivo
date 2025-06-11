

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox

from Socio import Socio
from VisteDipendente.VistaDettagliSocio import VistaDettagliSocio
from Partita import Partita
from VisteDipendente.VistaModificaPartita import VistaModificaPartita


class VistaVisualizzaListaPartite(QWidget):

    def __init__(self, parent=None):
        super(VistaVisualizzaListaPartite, self).__init__(parent)
        self.partite = Partita.getPartite()
        data_list = list(self.partite.values())  # Converte i valori del dizionario in una lista
        partite_ordinate = sorted(data_list, key=lambda partita:(partita.data, partita.orarioInizio))
        # funzione lambda per ordinare le partite per data e ora di inizio
        self.v_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["CODICE", "DATA", "CAMPO", "ORA INIZIO", "ORA FINE", "PRENOTATO DA", "MODIFICA", "CANCELLA"])
        self.table.setRowCount(len(partite_ordinate))



        for row, partita in enumerate(partite_ordinate):
            info = partita.getInfoPartita()

            self.table.setItem(row, 0, QTableWidgetItem(str(info["codice"])))
            self.table.setItem(row, 1, QTableWidgetItem(info["data"]))
            self.table.setItem(row, 2, QTableWidgetItem(info["campo"]))
            self.table.setItem(row, 3, QTableWidgetItem(info["ora_inizio"]))
            self.table.setItem(row, 4, QTableWidgetItem(info["ora_fine"]))

            if partita.socio:
                btn_socio = QPushButton(partita.socio.username)
                btn_socio.clicked.connect(lambda _, s=partita.socio: self.visualizzaDatiSocio(s))
                self.table.setCellWidget(row, 5, btn_socio)
            else:
                self.table.setItem(row, 5, QTableWidgetItem("NESSUNO"))

            #implementare dopo Cliente

            if partita.socio is None:
                btn_modifica = QPushButton("Modifica")
                btn_modifica.clicked.connect(lambda _, p=partita: self.modificaPartita(p))
                self.table.setCellWidget(row, 6, btn_modifica)
            else:
                disabled = QPushButton("Modifica")
                disabled.setEnabled(False)
                disabled.setStyleSheet("color: gray")
                self.table.setCellWidget(row, 6, disabled)

            btn_cancella = QPushButton("Cancella")
            btn_cancella.clicked.connect(lambda _, p=partita: self.eliminaPartita(p))
            self.table.setCellWidget(row, 7, btn_cancella)



        self.v_layout.addWidget(self.table)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Lista Partite")
        self.resize(1049, 300)

    def visualizzaDatiSocio(self, socio):
        self.vista_dettagli = VistaDettagliSocio(socio)
        self.vista_dettagli.show()

    def modificaPartita(self, partita):
        self.vista_modifica = VistaModificaPartita(partita)
        self.vista_modifica.show()
        self.close()

    def eliminaPartita(self, partita):
            if partita.socio:
                self.avvisaSocio(partita)


            partita.deletePartita()
            QMessageBox.information(self, "Partita eliminata",
                                    f"La partita con codice {partita.codice} è stata eliminata.")
            self.close()
            self.__init__()
            self.show()

    def avvisaSocio(self, partita):
        socio = partita.socio
        messaggio = f"La partita del {partita.data.strftime('%d/%m/%Y')} alle ore {partita.orarioInizio.strftime('%H:%M')} è stata cancellata dal centro sportivo."
        socio.avvisi.append(messaggio)

        soci = Socio.getSoci()
        soci[socio.username] = socio
        Socio.updateSoci(soci)





