# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen tarkoituksena on tarjota käyttäjälle helppokäyttöinen työkalu PDF-tiedostojen käsittelyyn ja jakamiseen pienemmiksi tiedostoiksi. Käyttäjä voi ladata tiedostoja joko pudottamalla tiedoston käyttöliittymään tai valitsemalla tiedoston manuaalisesti tietokoneeltaan.

## Käyttäjät

Sovelluksessa on vain yhdenlaisia käyttäjiä, joten erillisiä käyttäjärooleja ei ole määritelty.

## Suunnitellut toiminnallisuudet

### Perusversio

- Käyttäjä voi lisätä tiedoston sovellukseen joko drag-and-drop -toimintoa tai valitsemalla tiedoston tietokoneeltaan. - ✅ **Tehty**
- Sovellus tarkistaa tiedoston kelvollisuuden. ✅ **Tehty**
- Ladatun tiedoston nimi ja perustiedot näytetään käyttöliittymässä. ✅ **Tehty**
- Käyttäjä voi valita ladatun tiedoston ja jakaa sen useiksi pienemmiksi tiedostoiksi määriteltyjen sivuvälien perusteella. ✅ **Tehty**
- Käyttäjä voi tallentaa jaetut tiedostot takaisin tietokoneelleen. ✅ **Tehty**

### Jatkokehitysideat

- Mahdollisuus automaattisesti nimetä jaetut tiedostot käyttäjän määrittelemän mallin mukaisesti.
- Jaettujen tiedostojen esikatselutoiminto ennen tallennusta.
- Mahdollisuus hallita ladattujen tiedostojen historiaa.
- OCR-toiminnallisuuden lisääminen ja hyödyntäminen automaatioissa.

## Käyttöliittymäluonnos

### Päänäkymä

- Yksinkertainen käyttöliittymä, jossa voidaan lisätä tiedosto joko:
    - Drag-and-drop toiminallisuuden avulla
  - "Valitse tiedosto" -painike
- Kun tiedosto on ladattu, käyttöliittymä näyttää tiedoston perustiedot ja mahdollisuuden suorittaa tiedoston jakaminen.
- Käyttöliittymä tarjoaa selkeän näkymän jaettujen tiedostojen tallentamiselle.

### Tiedoston käsittelyn näkymä

- Näyttää tiedoston esikatselun ja sivujen määrän.
- Mahdollistaa sivuvälien määrittelyn jaettaville tiedostoille.
- "Jaa tiedosto" -painike aloittaa jakamisen.