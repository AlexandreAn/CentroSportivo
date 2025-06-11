from logging import setLogRecordFactory

from encodings.punycode import selective_find

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Partita import Partita
from Campo import Campo

class VistaGuadagnoPartite(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribuzione dei guadagni per campo")
        self.setGeometry(150, 150, 600, 500)

        layout = QGridLayout()
        self.setLayout(layout)

        canvas, guadagno_totale = self.creaGraficoTorta()
        layout.addWidget(canvas, 0, 0)
        layout.addWidget(guadagno_totale, 1, 0)

    def creaGraficoTorta(self):
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        self.partite = Partita.getPartite()
        guadagni = {campo: 0.0 for campo in Campo}
        totale = 0.0

        for partita in self.partite.values():
            if partita.socio is not None: 
                guadagno = partita.calcolaCostoPartita()
                guadagni[partita.campo] += guadagno
                totale += guadagno

        labels = []
        sizes = []

        for campo, valore in guadagni.items():
            if valore > 0:
                labels.append(campo.name.replace("_", " "))
                sizes.append(valore)

        if not sizes:
            labels = ['guadagno = 0']
            sizes = [1]
            ax.pie(sizes, labels=labels)
        else:
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

        ax.set_title("Distribuzione guadagni rispetto ogni campo")
        ax.axis('equal')

        label = QLabel(f"Guadgno totale: € {totale:.2f}")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 14px; padding: 10px;")

        return canvas, label
