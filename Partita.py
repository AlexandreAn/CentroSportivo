import os
import pickle




class Partita:

    def __init__(self):
        self.codice = 0 #attributo aggiunto per essere la chiave del dizionario
        self.data = None
        self.orarioInizio = None
        self.orarioFine= None
        self.campo = None
        self.socio = None
        self.orarioInizioOriginale = None
        self.orarioFineOriginale = None

    def createPartita(self, codice, data, orario_inizio, orario_fine, campo):
        self.codice = codice
        self.data = data
        self.orarioInizio = orario_inizio
        self.orarioFine = orario_fine
        self.orarioInizioOriginale = orario_inizio
        self.orarioFineOriginale = orario_fine
        self.campo = campo
        self.socio = None

        partite = Partita.getPartite()

        partite[codice] = self

        Partita.updatePartite(partite)


    def deletePartita(self):

        from Socio import Socio
        codice = self.codice
        partite = Partita.getPartite()

        if codice in partite:
            del partite[codice]

            Partita.updatePartite(partite)

        soci = Socio.getSoci()
        for s in soci.values():
            if codice in s.partitePrenotate:
                del s.partitePrenotate[codice]
        Socio.updateSoci(soci)

    def getInfoPartita(self):
        info = {
            "codice": self.codice,
            "data": self.data.strftime("%d/%m/%Y"),
            "campo": self.campo.name,
            "ora_inizio": self.orarioInizio.strftime("%H:%M"),
            "ora_fine": self.orarioFine.strftime("%H:%M"),
            "prenotato_da": self.socio.username if self.socio else "NESSUNO"
        }
        return info

    @staticmethod
    def getPartite():
        if os.path.exists("Dati/Partite.pickle"):
            with open("Dati/Partite.pickle", "rb") as f:
                return pickle.load(f)
        return {}

    @staticmethod
    def updatePartite(partite):
        with open("Dati/Partite.pickle", "wb") as f:
            pickle.dump(partite, f, pickle.HIGHEST_PROTOCOL)

    def calcolaCostoPartita(self):
        durata = (self.orarioFine - self.orarioInizio).total_seconds() / 60
        costo = round(durata * self.campo.value, 2)
        if self.socio is not None:  #aggiunta
            if self.socio.abbonato==True: #aggiunta
                costo = costo - (costo * 20 / 100) #aggiunta
        return costo
