from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Campo import Campo
from Partita import Partita


class VistaPartitePrenotate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Distribuzione delle partite prenotate")
        self.setGeometry(150, 150, 600, 500)

        layout = QGridLayout()
        self.setLayout(layout)

        canvas, totale_label = self.creaGraficoDistribuzione()
        layout.addWidget(canvas, 0, 0)
        layout.addWidget(totale_label, 1, 0)

    def creaGraficoDistribuzione(self):
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        self.partite = Partita.getPartite()

        conteggio = {campo: 0 for campo in Campo}
        totale = 0

        for partita in self.partite.values():
            if partita.socio is not None:  # Solo partite prenotate
                conteggio[partita.campo] += 1
                totale += 1

        labels = []
        sizes = []

        for campo, num in conteggio.items():
            if num > 0:
                labels.append(campo.name.replace("_", " "))
                sizes.append(num)

        if not sizes:
            labels = ['Partite prenotate = 0']
            sizes = [1]
            ax.pie(sizes, labels=labels)
        else:
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        ax.set_title("Distribuzione partite prenotate rispetto ogni tipo di campo")
        ax.axis('equal')

        label = QLabel(f"Tot partite prenotate: {totale}")
        label.setStyleSheet("font-size: 14px; padding: 10px;")
        label.setAlignment(Qt.AlignCenter)
        
        return canvas, label
