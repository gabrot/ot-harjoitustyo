from invoke import task
import platform

@task
def start(ctx):
    ctx.run("python3 -m src.main", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def test(ctx):
    ctx.run("pytest src/tests", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src/tests", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)

@task
def build_windows(ctx):
    if platform.system() != "Windows":
        print("⛔ This build command must be run on Windows.")
        return
    ctx.run(
        "set PYTHONPATH=src && pyinstaller src/main.py --name scanflow --onefile --windowed --noconfirm --clean --icon=src/assets/icon.ico",
        pty=False
    )

@task
def build_macos(ctx):
    ctx.run(
        "PYTHONPATH=src pyinstaller src/main.py --name scanflow --onedir --windowed --noconfirm --clean --icon=src/assets/icon.icns",
        pty=True
    )

@task
def build_linux(ctx):
    ctx.run(
        "PYTHONPATH=src pyinstaller src/main.py --name scanflow --onefile --noconfirm --clean --icon=src/assets/icon.png",
        pty=True
    )
