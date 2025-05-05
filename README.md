# Scanflow - PDF-jakaja
Scanflow tarjoaa käyttäjäystävällisen ratkaisun PDF-tiedostojen jakamiseen. Käyttäjä voi jakaa kokonaiset PDF-tiedostot pienempiin osiin, kuten yksittäisiksi sivuiksi tai määriteltyjen sivujoukkojen perusteella.

![Scanflow käyttöliittymä](./scanflow/dokumentaatio/kuvat/sovelluksen_paaikkuna.png)

## 📚 Dokumentaatio

Kaikki projektin dokumentit löytyvät kansiosta [dokumentaatio](./scanflow/dokumentaatio/):

- 📄 [Vaatimusmäärittely](./scanflow/dokumentaatio/vaatimusmaarittely.md)
- 🏗️ [Arkkitehtuuri](./scanflow/dokumentaatio/arkkitehtuuri.md)
- 👨‍🏫 [Käyttöohje](./scanflow/dokumentaatio/kayttoohje.md)
- 🧪 [Testausdokumentti](./scanflow/dokumentaatio/testausdokumentti.md)
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
   > 💡 Käytä komentoa `poetry install --only main` mikäli haluat asentaa ohjelman ilman dev-riippuvuuksia

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

- [Viikko 5 release](https://github.com/gabrot/ot-harjoitustyo/releases/tag/viikko5)
- [Viikko 6 release](https://github.com/gabrot/ot-harjoitustyo/releases/tag/viikko6)
- [Final release](https://github.com/gabrot/ot-harjoitustyo/releases/latest)

## 🏗️ Build

### Yleistä

Sovelluksen voi kääntää suoritettaviksi tiedostoiksi käyttäen [PyInstalleria](https://pyinstaller.org/). Build-työkalut on määritelty `dev`-riippuvuudeksi.

### Riippuvuuksien asennus

```bash
poetry install --with dev
```
### Buildausohjeet
#### Windows

```bash
poetry run invoke build-windows
```

#### macOS

```bash
poetry run invoke build-macos
```

#### Linux

```bash
poetry run invoke build-linux
```

### Huomioitavaa

- Kuvakkeet tulee lisätä paikallisesti `src/assets/`-kansioon. Kuvakkeita ei ole versioitu.
- Buildauksen jälkeen julkaistavat ohjelmat löytyvät `dist/`-kansiosta

## Lisenssi

Tämä projekti on lisensoitu MIT-lisenssillä. Katso lisätiedot [`LICENSE`](LICENSE).
