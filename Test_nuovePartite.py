import unittest
from datetime import datetime
from Campo import Campo
from Partita import Partita
from Socio import Socio

class ProvePartite(unittest.TestCase):
    def setUp(self):
        self.partita1=Partita()
        self.partita1.createPartita(123, "25/09/2025","18:00","20:00", Campo.Calcetto_Interno.value)
        self.socio1=Socio()
        self.socio2=Socio()
        self.socio1.createSocio("Ciccio1","password", "prova", "prova", "prova", "prova@outlook.it", "è una prova?", "sì è una prova")
        self.socio1.abbonato=True
        self.socio2.createSocio("Ciccio2","password", "prova", "prova", "prova", "prova@outlook.it", "è una prova?", "sì è una prova")
        self.socio2.abbonato=False

    def _aggiornaCosto(self, socio, costo):
        if socio.abbonato:
            costoAggiornato = costo-(costo*20/100)
            return costoAggiornato
        return costo


    def test_crea_distruggi_partita(self):
        partite= Partita.getPartite()
        self.assertIsNotNone(partite)
        self.assertIn(123, partite)
        self.partita1.deletePartita()
        partite= Partita.getPartite()
        self.assertNotIn(123, partite)

    def test_costo(self):

        orario_inizio = datetime.strptime(self.partita1.orarioInizio, "%H:%M")
        orario_fine = datetime.strptime(self.partita1.orarioFine, "%H:%M")
        durata_minuti = (orario_fine - orario_inizio).seconds / 60
        costo = round(durata_minuti * self.partita1.campo, 2)
        costoAtteso = 144.00
        self.assertAlmostEqual(costo, costoAtteso, places=2)



    def test_costoAbbonato(self):
        orario_inizio = datetime.strptime(self.partita1.orarioInizio, "%H:%M")
        orario_fine = datetime.strptime(self.partita1.orarioFine, "%H:%M")
        durata_minuti = (orario_fine - orario_inizio).seconds / 60
        costo = round(durata_minuti * self.partita1.campo, 2)
        costoCalcolato= self._aggiornaCosto(self.socio1, costo)
        self.assertIsNot(costo, costoCalcolato)
        print(costo)
        print(costoCalcolato)



if __name__ == '__main__':
    unittest.main()
