import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator
from datetime import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from Partita import Partita


class VistaGraficoPrenotazioni(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Numero prenotazioni per fascia oraria")
        self.setGeometry(200, 200, 800, 500)

        layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.aggiornaGrafico()

    def aggiornaGrafico(self):
        self.partite = Partita.getPartite()
        prenotate = []
        for p in self.partite.values():
            if p.socio is not None:
                prenotate.append(p)

        fasce_orarie = [
            (time(7, 0), time(8, 0)),
            (time(8, 0), time(9, 0)),
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(12, 0), time(13, 0)),
            (time(13, 0), time(14, 0)),
            (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)),
            (time(16, 0), time(17, 0)),
            (time(17, 0), time(18, 0)),
            (time(18, 0), time(19, 0)),
            (time(19, 0), time(20, 0)),
            (time(20, 0), time(21, 0)),
            (time(21, 0), time(22, 0)),
            (time(22, 0), time(23, 0)),
            (time(23, 0), time(0, 0))  # fino a mezzanotte
        ]

        etichette_fasce = [
            "7–8", "8–9", "9–10", "10–11", "11–12",
            "12–13", "13–14", "14–15", "15–16", "16–17",
            "17–18", "18–19", "19–20", "20–21", "21–22",
            "22–23", "23–00"
        ]

        conteggi = {}
        for fascia in etichette_fasce:
            conteggi[fascia] = 0

        for p in prenotate:
            inizio = p.orarioInizio.time()
            fine = p.orarioFine.time()

            for i, (fascia_inizio, fascia_fine) in enumerate(fasce_orarie):
                if fascia_fine == time(0, 0):
                    if inizio >= fascia_inizio or fine <= time(0, 0):
                        conteggi[etichette_fasce[i]] += 1
                else:
                    if inizio < fascia_fine and fine > fascia_inizio:
                        conteggi[etichette_fasce[i]] += 1

        y_labels = etichette_fasce
        x_values = []
        for f in y_labels:
            x_values.append(conteggi[f])

        ax = self.canvas.figure.subplots()
        ax.clear()
        ax.barh(y_labels, x_values, color='red')
        ax.set_xlabel("Num prenotazioni")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_title("Numero prenotazioni per fascia oraria")
        self.canvas.draw()
