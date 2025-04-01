# Ohjelmistotekniikka – Harjoitustyö

Tämä projekti on osa Helsingin yliopiston ohjelmistotekniikan kurssia. Projektissa toteutetaan harjoitustyö, jonka aikana kehitetään dokumentoitu, testattu ja ylläpidettävä ohjelmisto.

## Viikkoharjoitukset

**[Laskarit-kansio](./laskarit/)** sisältää viikkokohtaiset harjoitukset ja materiaalit:

- [Viikko 1](./laskarit/viikko1/viikko1.md)
- [Viikko 2](./laskarit/viikko2/)
- [Viikko 3](./laskarit/viikko3/viikko3.md)

## 📚 Dokumentaatio

Kaikki projektin dokumentit löytyvät kansiosta [dokumentaatio](./scanflow/dokumentaatio/):

- 📄 [Vaatimusmäärittely](./scanflow/dokumentaatio/vaatimusmaarittely.md)
- 🏗️ [Arkkitehtuuri](./scanflow/dokumentaatio/arkkitehtuuri.md)
- 👨‍🏫 [Käyttöohje](./scanflow/dokumentaatio/kayttoohje.md)
- 📝 [Changelog](./scanflow/dokumentaatio/changelog.md)
- ⏱️ [Tuntikirjanpito](./scanflow/dokumentaatio/tuntikirjanpito.md)

## 🚀 Asennus ja käyttö

1. Siirry projektihakemistoon:
   ```bash
   cd scanflow
   ```

2. Asenna riippuvuudet:
   ```bash
   poetry install
   ```

3. Käynnistä sovellus:
   ```bash
   poetry run invoke start
   ```

## Komentorivityökalut

### ▶️ Sovelluksen käynnistys

```bash
poetry run invoke start
```

### 🕵️ Testien suoritus

```bash
poetry run invoke test
```

### 📊 Testikattavuusraportti

Generoi kattavuusraportti komennolla:

```bash
poetry run invoke coverage-report
```

Raportti löytyy `htmlcov/`-hakemistosta.

### 🧹 Koodin laadun tarkistus

Suorita `pylint`-tarkistukset:

```bash
poetry run invoke lint
```