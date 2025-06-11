import unittest
from unittest.mock import MagicMock
from datetime import datetime,time
from Partita import Partita
from Campo import Campo

class ProvaPartita(unittest.TestCase):
    def _calcola_costo_partita(self, data_partita, orario_inizio_partita, orario_fine_partita, tipo_campo):

        dt_inizio = datetime.combine(data_partita, orario_inizio_partita)
        dt_fine = datetime.combine(data_partita, orario_fine_partita)

        if dt_fine <= dt_inizio:
            return 0.00

        durata_delta = dt_fine - dt_inizio
        durata_minuti = durata_delta.total_seconds() / 60

        # Accediamo direttamente a .value che contiene la tariffa al minuto
        tariffa_al_minuto = tipo_campo.value

        costo = round(durata_minuti * tariffa_al_minuto, 2)
        return costo

    def test_costo_calcetto_esterno_un_ora(self):
        data_test = datetime(2024, 1, 1).date()
        ora_inizio_test = time(16, 0)
        ora_fine_test = time(17, 0)
        campo_test = Campo.Calcetto_Esterno  # .value è 1.00 (o 1)

        # Costo atteso: 60 minuti * 1.00 €/min = 60.00 €
        costo_atteso = 60.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)

        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)

    def test_costo_calcetto_interno_un_ora_e_mezza(self):
        data_test = datetime(2024, 1, 1).date()
        ora_inizio_test = time(18, 0)
        ora_fine_test = time(19, 30)  # 90 minuti
        campo_test = Campo.Calcetto_Interno  # .value è 1.20

        # Costo atteso: 90 minuti * 1.20 €/min = 108.00 €
        costo_atteso = 108.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)

        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)

    def test_costo_padel_esterno_quarantacinque_minuti(self):
        data_test = datetime(2024, 1, 1).date()
        ora_inizio_test = time(10, 0)
        ora_fine_test = time(10, 45) # 45 minuti
        campo_test = Campo.Padel_Esterno # .value è 0.60

        # Costo atteso: 45 minuti * 0.60 €/min = 27.00 €
        costo_atteso = 27.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)
        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)

    def test_costo_padel_interno_due_ore(self):
        data_test = datetime(2024, 1, 1).date()
        ora_inizio_test = time(14, 0)
        ora_fine_test = time(16, 0) # 120 minuti
        campo_test = Campo.Padel_Interno # .value è 0.80

        # Costo atteso: 120 minuti * 0.80 €/min = 96.00 €
        costo_atteso = 96.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)
        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)


    def test_costo_durata_zero(self):
        data_test = datetime(2024, 1, 1).date()
        ora_inizio_test = time(10, 0)
        ora_fine_test = time(10, 0)
        campo_test = Campo.Calcetto_Esterno # Un campo qualsiasi

        costo_atteso = 0.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)
        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)

    def test_costo_orario_fine_prima_di_inizio(self):
        data_test = datetime(2024,1,1).date()
        ora_inizio_test = time(11,0)
        ora_fine_test = time(10,0)
        campo_test = Campo.Calcetto_Esterno

        costo_atteso = 0.00
        costo_calcolato = self._calcola_costo_partita(data_test, ora_inizio_test, ora_fine_test, campo_test)
        self.assertAlmostEqual(costo_calcolato, costo_atteso, places=2)



if __name__ == "__main__":
    unittest.main()
