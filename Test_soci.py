import unittest
from Socio import Socio

class ProvaSocio(unittest.TestCase):
    def test_aggiungi_socio(self):
        self.socio=Socio()
        self.socio.createSocio("Ciccio","password", "prova", "prova", "prova", "prova@outlook.it", "è una prova?", "sì è una prova")
        soci=Socio.getSoci()
        self.assertIsNotNone(soci)
        self.assertIn("Ciccio", soci)

    def test_elimina_socio(self):
        self.socio = Socio()
        self.socio.createSocio("Ciccio", "password", "prova", "prova", "prova", "prova@outlook.it", "è una prova?",
                               "sì è una prova")
        soci = Socio.getSoci()
        self.assertIsNotNone(soci)
        self.assertIn("Ciccio", soci)
        self.socio.deleteSocio()
        soci = Socio.getSoci()
        self.assertNotIn("Ciccio", soci)
if __name__ == "__main__":
    unittest.main()
