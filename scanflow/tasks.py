from invoke import task

@task
def start(ctx):
    """Käynnistää sovelluksen"""
    ctx.run("python3 src/main.py", pty=True)

@task
def test(ctx):
    """Suorittaa testit"""
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    """Kerää testikattavuuden"""
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    """Luo testikattavuusraportin"""
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    """Suorittaa pylint-tarkistukset"""
    ctx.run("pylint src", pty=True)