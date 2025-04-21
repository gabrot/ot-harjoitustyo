# tasks.py
"""Invoke-tehtävät sovelluksen kehitystä varten.

Tämä moduuli sisältää invoke-kirjaston mukaiset tehtävämäärittelyt, joiden avulla
voidaan helposti suorittaa sovelluksen kehitykseen liittyviä toimintoja, kuten
sovelluksen käynnistäminen, testien ajaminen ja koodin laadun tarkistaminen.
"""

from invoke import task


@task
def start(ctx):
    """Käynnistää sovelluksen paikallisesti.

    Suorittaa pääsovellustiedoston Python 3 -tulkilla.

    Args:
        ctx: Invoke-kontekstiobjekti.
    """
    ctx.run("python3 src/main.py", pty=True)


@task
def test(ctx):
    """Suorittaa sovelluksen yksikkötestit pytestillä.

    Args:
        ctx: Invoke-kontekstiobjekti.
    """
    ctx.run("pytest src", pty=True)


@task
def coverage(ctx):
    """Kerää testikattavuustiedot pytestin ja coveragen avulla.

    Suorittaa testit ja tallentaa kattavuusdatan myöhempää raportointia varten.

    Args:
        ctx: Invoke-kontekstiobjekti.
    """
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    """Luo HTML-muotoisen testikattavuusraportin.

    Tämä tehtävä vaatii, että 'coverage'-tehtävä on ajettu ensin.

    Args:
        ctx: Invoke-kontekstiobjekti.
    """
    ctx.run("coverage html", pty=True)


@task
def lint(ctx):
    """Suorittaa koodin staattisen analyysin pylintillä.

    Tarkistaa koodin laadun ja mahdolliset virheet src-hakemistossa.

    Args:
        ctx: Invoke-kontekstiobjekti.
    """
    ctx.run("pylint src", pty=True)
