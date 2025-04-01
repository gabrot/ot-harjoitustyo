# Käyttöohje

## Ohjelman käynnistäminen

Asenna ensin riippuvuudet komennolla:

```bash
poetry install
```

Käynnistä sen jälkeen sovellus komennolla:

```bash
poetry run invoke start
```

# Scanflow käyttöohje

Scanflow on työkalu, jolla voit jakaa PDF-tiedostoja pienempiin osiin joko tasaisesti määrätyn sivumäärän mukaan tai itse määrittelemiesi sivualueiden perusteella.

## Käyttöliittymä

Käyttöliittymä koostuu seuraavista osista:
- Tiedoston pudotusalue (tulossa myöhemmin)
- Tiedoston tiedot -kenttä
- Asetustilan valitsimet (Kiinteät alueet / Omat alueet)
- Sivualueiden määrittelykentät
- Jakamispainike
- Tilakenttä

## Tiedoston valitseminen

PDF-tiedoston voi valita kahdella eri tavalla:
1. **Raahaa ja pudota**: Raahaa PDF-tiedosto tiedostoselaimesta pudotusalueelle. **HUOM!** *Sovellus ei tällä hetkellä tue Raahaa ja pudota ominaisuutta*
2. **Valitse tiedosto**: Klikkaa pudotusaluetta tai "Valitse tiedosto" -painiketta, jolloin avautuu tiedoston valintaikkuna.

Kun tiedosto on valittu, näet tiedoston nimen ja sivumäärän "Tiedoston tiedot" -kohdassa.

## Asetustilan valinta

Sovelluksessa on kaksi eri tapaa määritellä, miten PDF jaetaan:

### 1. Kiinteät alueet

Tässä tilassa voit jakaa PDF-tiedoston osiin, joissa on tasainen määrä sivuja:

1. Valitse "Kiinteät alueet" asetustilaksi
2. Määritä sivujen määrä per tiedosto numerokenttään. **HUOM!**  *Sovellus jakaa PDF:n 2 sivun tiedostoihin valinnasta riippumatta.*
3. Näet inforuudussa, montako PDF-tiedostoa tullaan luomaan


### 2. Omat alueet

Tässä tilassa voit itse määritellä, mitkä sivut tulevat mihinkin tiedostoon:

1. Valitse "Omat alueet" asetustilaksi
2. Määritä ensimmäiselle alueelle alku- ja loppusivu
3. Lisää tarvittaessa uusia alueita "Lisää alue" -painikkeella
4. Voit määritellä useita alueita, jotka voivat olla päällekkäisiä tai epäjärjestyksessä

Jokaiselle alueelle määritellään:
- Mistä sivusta alue alkaa
- Mihin sivuun alue päättyy

Voit poistaa alueen (paitsi viimeisen) klikkaamalla alueen oikeassa yläkulmassa olevaa "×"-painiketta.

## PDF-tiedoston jakaminen

Kun olet valinnut tiedoston ja määritellyt haluamasi alueet:

1. Klikkaa "Jaa PDF" -painiketta
2. Valitse tallennushakemisto avautuvasta hakemistonvalintaikkunasta
3. Ohjelma luo uudet PDF-tiedostot valittuun hakemistoon ja ilmoittaa tilakenttään, montako tiedostoa luotiin

## Tulostiedostojen nimeäminen

PDF-jakaja nimeää tulostiedostot automaattisesti alkuperäisen tiedoston nimen perusteella:

- **Kiinteät alueet**: [alkuperäinen_nimi]_sivut_[alku]-[loppu].pdf
  Esim. "raportti_sivut_1-2.pdf", "raportti_sivut_3-4.pdf"

- **Omat alueet**: [alkuperäinen_nimi]_alue_[numero]_sivut_[alku]-[loppu].pdf
  Esim. "raportti_alue_1_sivut_1-3.pdf", "raportti_alue_2_sivut_5-7.pdf"

## Virheilmoitukset

Jos sovelluksen käytössä ilmenee ongelmia, tilakenttään tulee virheilmoitus.

- **Tiedostoa ei voitu avata**: Tarkista, että tiedosto on PDF-muodossa ja että sinulla on lukuoikeudet tiedostoon.
- **Tallennushakemistoa ei valittu**: Valitse hakemisto, johon sinulla on kirjoitusoikeudet.
- **Virheellinen sivualue**: Tarkista, että sivunumerot ovat oikein ja sivualueet ovat mahdollisia.