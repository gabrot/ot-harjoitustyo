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

## PDF-tiedoston valitseminen

Sovelluksen päänäkymässä voit valita PDF-tiedoston klikkaamalla "Valitse PDF" -painiketta ja valitsemalla tiedoston tiedostoselaimesta.

## PDF-tiedoston jakaminen

Kun olet valinnut PDF-tiedoston, sovellus näyttää PDF-käsittelynäkymän:

### Jakaminen tasaisiin osiin

1. Valitse "Jaa tasaisiin osiin" -vaihtoehto
2. Määritä osien määrä kenttään (oletusarvo on 2)
3. Klikkaa "Jaa PDF" -painiketta
4. Valitse hakemisto, johon haluat tallentaa jaetut PDF-tiedostot
5. Sovellus jakaa PDF-tiedoston tasaisiin osiin ja tallentaa ne valittuun hakemistoon

### Jakaminen mukautettujen sivualueiden mukaan

1. Valitse "Jaa mukautettujen sivualueiden mukaan" -vaihtoehto
2. Määritä sivualueet kenttään muodossa "1-5, 8, 11-13"
   - Sivunumerot alkavat 1:stä
   - Voit määritellä yksittäisiä sivuja (esim. "8") tai sivualueita (esim. "1-5")
   - Voit määritellä useita sivualueita erottamalla ne pilkulla
3. Klikkaa "Jaa PDF" -painiketta
4. Valitse hakemisto, johon haluat tallentaa jaetut PDF-tiedostot
5. Sovellus jakaa PDF-tiedoston määriteltyjen sivualueiden mukaan ja tallentaa ne valittuun hakemistoon

## Sivuvalikko

Sovelluksen sivuvalikkoon pääset klikkaamalla vasemmassa yläkulmassa olevaa hampurilaisvalikkopainiketta (☰). Sivuvalikosta löydät seuraavat toiminnot:

- Etusivu (palaa päänäkymään)
- PDF-työkalut (lisää PDF-työkaluja, ei vielä käytettävissä)
- Asetukset (sovelluksen asetukset, ei vielä käytettävissä)
- Tietoja (tietoja sovelluksesta, ei vielä käytettävissä)