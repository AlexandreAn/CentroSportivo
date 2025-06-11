import json
import os.path
import pickle
from datetime import datetime
from Partita import Partita


class Socio:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.nome = ""
        self.cognome = ""
        self.cellulare = ""
        self.mail = ""
        self.abbonamento = None #istanza (singola e non collezione) di abbonamento
        self.abbonato = False  # il socio viene istanziato di default sempre non abbonato ovviamente
        self.partitePrenotate = {}
        self.avvisi = []
        self.domandaSicurezza = ""
        self.rispostaSicurezza = ""

    def createSocio(self, username, password, nome, cognome, cellulare, mail, domanda, risposta): #non ho bisogno di indicare l'attributo abbonato
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.cellulare = cellulare
        self.mail = mail
        self.partitePrenotate = {}
        self.avvisi = []
        self.domandaSicurezza = domanda
        self.rispostaSicurezza = risposta

        soci = Socio.getSoci()

        soci[username] = self

        Socio.updateSoci(soci)

    def deleteSocio(self):


        username = self.username

        if self.abbonamento:
            self.abbonamento.deleteAbbonamento()

        # elimina dal JSON
        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
            data["utenti"] = [u for u in data["utenti"] if u["username"] != username]
            with open("Dati/data.json", "w") as f:
                json.dump(data, f, indent=4)

        # Elimina dal Pickle

        soci = Socio.getSoci()
        if username in soci:
            del soci[username]

        Socio.updateSoci(soci)

        # Libera le partite
        partite = Partita.getPartite()
        for p in partite.values():
            if p.socio and p.socio.username == username:
                p.socio = None
                p.orarioInizio = p.orarioInizioOriginale
                p.orarioFine = p.orarioFineOriginale

        Partita.updatePartite(partite)

    def getInfoSocio(self):
        return {
            "username": self.username,
            "nome": self.nome,
            "cognome": self.cognome,
            "cellulare": self.cellulare,
            "mail": self.mail,
            "abbonato": self.abbonato
        }

    @staticmethod
    def getSoci():
        if os.path.exists("Dati/Soci.pickle"):
            with open("Dati/Soci.pickle", "rb") as f:
                return pickle.load(f)
        return {}

    @staticmethod
    def updateSoci(soci):
        with open("Dati/Soci.pickle", "wb") as f:
            pickle.dump(soci, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def aggiornaStatoAbbonamenti():
        soci = Socio.getSoci()
        oggi = datetime.now().date()

        for socio in soci.values():
            abbonamento = socio.abbonamento

            if abbonamento and abbonamento.dataInizio and abbonamento.dataScadenza:
                data_inizio = abbonamento.dataInizio.date()
                data_scadenza = abbonamento.dataScadenza.date()

                if oggi >= data_scadenza:
                    abbonamento.deleteAbbonamento()  #l'abbonamento se è scaduto lo eliminiamo dal sistema
                elif oggi >= data_inizio:
                    socio.abbonato = True
                else:
                    socio.abbonato = False

        Socio.updateSoci(soci)



