import json
import os.path
import pickle


class Dipendente:

    def __init__(self):
        self.username = ""
        self.password = ""
        self.nome = ""
        self.cognome = ""
        self.cellulare = ""
        self.mail = ""

    def createDipendente(self, username, password, nome, cognome, cellulare, mail):#funzione CRUD che utilizzerà l'amministratore
        self.username = username
        self.password = password
        self.nome = nome
        self.cognome = cognome
        self.cellulare = cellulare
        self.mail = mail

        dipendenti = Dipendente.getDipendenti()
        dipendenti[username] = self
        Dipendente.updateDipendenti(dipendenti)

        nuovo_utente = {
            "username": username,
            "password": password,
            "ruolo": "dipendente",
        }

        if os.path.isfile('Dati\data.json'):
            with open('Dati\data.json', 'r') as f:
                utenti_data = json.load(f)
        else:
            utenti_data = {"utenti": []}


        utenti_data["utenti"].append(nuovo_utente)

        with open('Dati\data.json', 'w') as f:
            json.dump(utenti_data, f, indent=4)


    def deleteDipendente(self):


        username = self.username

        # Elimina dal JSON
        if os.path.exists("Dati/data.json"):
            with open("Dati/data.json", "r") as f:
                data = json.load(f)
            lista_utenti = []
            for utente in data["utenti"]:
                if utente["username"] != username:
                    lista_utenti.append(utente)
            data["utenti"] = lista_utenti

            with open("Dati/data.json", "w") as f:
                json.dump(data, f, indent=4)

        # Elimina dal Pickle
        dipendenti = Dipendente.getDipendenti()
        if username in dipendenti:
            del dipendenti[username]
        Dipendente.updateDipendenti(dipendenti)

    @staticmethod
    def getDipendenti():
        if os.path.exists("Dati/Dipendenti.pickle"):
            with open("Dati/Dipendenti.pickle", "rb") as f:
                return pickle.load(f)
        return {}

    @staticmethod
    def updateDipendenti(dipendenti):
        with open("Dati/Dipendenti.pickle", "wb") as f:
            pickle.dump(dipendenti, f, pickle.HIGHEST_PROTOCOL)




















