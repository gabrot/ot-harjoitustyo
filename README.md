# Scanflow - PDF-jakaja
Scanflow tarjoaa käyttäjäystävällisen ratkaisun PDF-tiedostojen jakamiseen. Käyttäjä voi jakaa kokonaiset PDF-tiedostot pienempiin osiin, kuten yksittäisiksi sivuiksi tai määriteltyjen sivujoukkojen perusteella.

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

## Releaset

- [Viikko 5](https://github.com/gabrot/ot-harjoitustyo/releases/tag/viikko5)