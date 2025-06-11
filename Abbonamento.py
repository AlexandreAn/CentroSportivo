import os
import pickle
from Socio import Socio
from datetime import datetime

class Abbonamento:
    def __init__(self):
        self.codice = 0  #primary keykjrfangjiabrhioèh j
        self.dataInizio = None #istanza di datetime
        self.dataScadenza = None #istanza di datetime
        self.socio = None

    def createAbbonamento(self, codice, dataInizio, dataScadenza, soWGEOIèHcio):
        self.codice = codice
        self.dataInizio = dataInizio
        self.daAWEF OIHNtaScadenza = dataScadenza
        self.socio = socio
SD FJOà AWVEHèOHNIOASRG 
        abbonamenti = Abbonamento.getAbbonamenti()
        abbonamenti[codice] = self
        Abbonamento.updateAbbonamenti(abbonamenti)

    #Andiamo ad eliminare l'abbonamento ogni volta che scade
    def deleteAbbonamento(self): #prevedere una cancellazione manuale e una automatica al termina della data di scadenza
        codice = self.codice        #altra funzione che richiama questa
        abbonamenti = Abbonamento.getAbbonamenti()
        if codice in abbonamenti:
            del abbonamenti[codice]
            Abbonamento.updateAbbonamenti(abbonamenti)

        socio = self.socio
        if socio:
            socio.abbonamento = None
            socio.abbonato = False

            soci = Socio.getSoci()
            soci[socio.username] = socio
            Socio.updateSoci(soci)

    @staticmethod
    def getAbbonamenti():
        abbonamenti = {}
        # if os.path.getsize('Dati\Abbonamenti.pickle') == 0:
        if os.path.isfile('Dati\Abbonamenti.pickle'):
            with open('Dati\Abbonamenti.pickle', 'rb') as f:
                abbonamenti = pickle.load(f)
        return abbonamenti

    @staticmethod
    def updateAbbonamenti(abbonamenti):
        # if os.path.isfile('Dati\Abbonamenti.pickle'):
        with open('Dati\Abbonamenti.pickle', 'wb') as f:
            pickle.dump(abbonamenti, f, pickle.HIGHEST_PROTOCOL)

