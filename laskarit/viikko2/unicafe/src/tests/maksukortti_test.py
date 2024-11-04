#Tee valmiiseen, tiedostossa src/tests/maksukortti_test.py sijaitsevaan, TestMaksukortti-testiluokkaan testit, jotka testaavat ainakin seuraavia asioita:

#Kortin saldo alussa oikein
#Rahan lataaminen kasvattaa saldoa oikein

#Rahan ottaminen toimii:
##Saldo vähenee oikein, jos rahaa on tarpeeksi
##Saldo ei muutu, jos rahaa ei ole tarpeeksi
##Metodi palauttaa True, jos rahat riittivät ja muuten False

import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")    

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 11.00 euroa")

    def test_saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 9.00 euroa")

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_metodi_palauttaa_true_jos_rahat_riittivät(self):
        palaute = self.maksukortti.ota_rahaa(100)
        self.assertEqual(palaute, True)

    def test_metodi_palauttaa_false_jos_rahat_eivat_riita(self):
        palaute = self.maksukortti.ota_rahaa(1100)
        self.assertEqual(palaute, False)