#Luodun kassapäätteen rahamäärä ja myytyjen lounaiden määrä on oikea (rahaa 1000 euroa, lounaita myyty 0)
#(Huomaa, että luokka tallentaa rahamäärän sentteinä)
#Käteisosto toimii sekä edullisten että maukkaiden lounaiden osalta
#-Jos maksu riittävä: kassassa oleva rahamäärä kasvaa lounaan hinnalla ja vaihtorahan suuruus on oikea
#-Jos maksu on riittävä: myytyjen lounaiden määrä kasvaa
#-Jos maksu ei ole riittävä: kassassa oleva rahamäärä ei muutu, kaikki rahat palautetaan vaihtorahana ja myytyjen lounaiden määrässä ei muutosta
#seuraavissa testeissä tarvitaan myös Maksukorttia jonka oletetaan toimivan oikein
#Korttiosto toimii sekä edullisten että maukkaiden lounaiden osalta
#-Jos kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
#-Jos kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
#-Jos kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu, myytyjen lounaiden määrä muuttumaton ja palautetaan False
#-Kassassa oleva rahamäärä ei muutu kortilla ostettaessa
#Kortille rahaa ladattaessa kortin saldo muuttuu ja kassassa oleva rahamäärä kasvaa ladatulla summalla

import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassapaatteen_rahamaara_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_myytyjen_lounaiden_maara_on_oikea(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    #Käteisosto toimii sekä edullisten että maukkaiden lounaiden osalta
    def test_kassassa_oleva_rahamaara_kasvaa_lounaan_hinnalla_edullinen(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_kassassa_oleva_rahamaara_kasvaa_lounaan_hinnalla_maukas(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_vaihtorahan_suuruus_on_oikea_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(800), 400)

    def test_vaihtorahan_suuruus_on_oikea_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(480), 240)

    def test_myytyjen_lounaiden_maara_kasvaa_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(800), 400)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_myytyjen_lounaiden_maara_kasvaa_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(480), 240)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_maksu_ei_ole_riittava_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maksu_ei_ole_riittava_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    #Korttiosto toimii sekä edullisten että maukkaiden lounaiden osalta
    def test_kortilla_on_tarpeeksi_rahaa_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kortilla_on_tarpeeksi_rahaa_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kortilla_ei_ole_tarpeeksi_rahaa_maukas(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(Maksukortti(10)), False)
        self.assertEqual(self.kassapaate.maukkaat, 0) 

    def test_kortilla_ei_ole_tarpeeksi_rahaa_edullinen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(Maksukortti(10)), False)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortille_rahaa_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.maksukortti.saldo, 1100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_kortille_rahaa_ladattaessa_negatiivinen_summa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.maksukortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)




