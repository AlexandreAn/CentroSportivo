import json
import os
import shutil
import pickle
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QMessageBox
from PyQt5.QtCore import QTime, QTimer
from Abbonamento import Abbonamento
from Partita import Partita
from Socio import Socio


class VistaGestioneBackup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestione Backup")
        self.resize(400, 250)

        self.orarioBackupAutomatico = self.caricaOrarioBackup()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Seleziona un'opzione:"))

        self.btn_imposta_ora = QPushButton("Imposta ora backup automatico")
        self.btn_imposta_ora.clicked.connect(self.impostaOraBackupAutomatico)
        layout.addWidget(self.btn_imposta_ora)

        self.btn_backup_now = QPushButton("Effettua backup")
        self.btn_backup_now.clicked.connect(self.salvaBackup)
        layout.addWidget(self.btn_backup_now)

        self.btn_ripristina = QPushButton("Carica backup")
        self.btn_ripristina.clicked.connect(self.caricaBackup)
        layout.addWidget(self.btn_ripristina)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.controllaBackup)
        self.timer.start(60000)

    def caricaOrarioBackup(self):
        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
                orario = data.get("orario_backup")
                if orario:
                    ore, minuti = map(int, orario.split(":"))
                    return QTime(ore, minuti)
        return None

    def salvaOrarioBackup(self, orario: QTime):
        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
        else:
            data = {}

        data["orario_backup"] = orario.toString("HH:mm")

        with open("Dati/data.json", "w") as f:
            json.dump(data, f, indent=4)

    def impostaOraBackupAutomatico(self):
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())

        def conferma():
            self.orarioBackupAutomatico = self.time_edit.time()
            self.salvaOrarioBackup(self.orarioBackupAutomatico)
            QMessageBox.information(self, "Backup automatico attivato",
                                    f"Backup sarà eseguito ogni giorno alle {self.orarioBackupAutomatico.toString('HH:mm')}")
            self.time_window.close()

        self.time_window = QWidget()
        self.time_window.setWindowTitle("Orario Backup")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Scegli l'orario del backup automatico"))
        layout.addWidget(self.time_edit)

        btn_conferma = QPushButton("Conferma")
        btn_conferma.clicked.connect(conferma)
        layout.addWidget(btn_conferma)

        self.time_window.setLayout(layout)
        self.time_window.show()

    def controllaBackup(self):
        if self.orarioBackupAutomatico:
            ora_attuale = QTime.currentTime()
            if ora_attuale.hour() == self.orarioBackupAutomatico.hour() and \
               ora_attuale.minute() == self.orarioBackupAutomatico.minute():
                self.salvaBackup()
                QMessageBox.information(self, "Backup automatico",
                                        f"Backup eseguito alle {self.orarioBackupAutomatico.toString('HH:mm')}.")



    def salvaBackup(self):
        if not os.path.exists("Backup"):
            os.makedirs("Backup")

        partite = Partita.getPartite()
        soci = Socio.getSoci()
        abbonamenti = Abbonamento.getAbbonamenti()

        self.copiaDatiPartite(partite)
        self.copiaDatiSoci(soci)
        self.copiaDatiAbbonamenti(abbonamenti)

        QMessageBox.information(self, "Backup completato",
                                "Backup salvato con successo nella cartella 'Backup'.")

    def caricaBackup(self):
        sorgente = "Backup"
        destinazione = "Dati"

        if not os.path.exists(sorgente):
            QMessageBox.warning(self, "Errore", "La cartella Backup non esiste.")
            return

        file_ripristinati = []
        for file in os.listdir(sorgente):
            if file.endswith(".pickle"):
                shutil.copy2(os.path.join(sorgente, file),
                             os.path.join(destinazione, file))
                file_ripristinati.append(file)

        QMessageBox.information(self, "Ripristino completato",
                                 f"Backup ripristinato correttamente.\nFile sovrascritti: {', '.join(file_ripristinati)}")

    def copiaDatiPartite(self, partite):
        with open("Backup/Partite.pickle", "wb") as f:
            pickle.dump(partite, f, pickle.HIGHEST_PROTOCOL)

    def copiaDatiSoci(self, soci):
        with open("Backup/Soci.pickle", "wb") as f:
            pickle.dump(soci, f, pickle.HIGHEST_PROTOCOL)

    def copiaDatiAbbonamenti(self, abbonamenti):
        with open("Backup/Abbonamenti.pickle", "wb") as f:
            pickle.dump(abbonamenti, f, pickle.HIGHEST_PROTOCOL)


