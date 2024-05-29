import os

import nox

nox.options.default_venv_backend = "uv|virtualenv"
nox.options.sessions = []


IS_CI = bool(os.getenv("CI"))


@nox.session
def build(session: nox.Session):
    session.env["GITHUB_PAGES_URL"] = ""
    if not IS_CI:
        session.env.setdefault("HATCH_GRADLE_DIR", "versions/1.20.1")
        session.env.setdefault("HEXDOC_PROPS", "versions/1.20.1/hexdoc.toml")

    session.install("-e", ".", "hatch", "--find-links", "./libs")

    hexdoc_minecraft(session, "fetch")
    hexdoc_minecraft(session, "unzip")
    hexdoc_minecraft(session, "entity-models")
    hexdoc(session, "build", "--no-clean-exports")

    if not IS_CI:
        session.run("hatch", "build")


def hexdoc(session: nox.Session, *args: str):
    if IS_CI:
        session.run("hexdoc", "ci", *args)
    else:
        session.run("hexdoc", *args)


def hexdoc_minecraft(session: nox.Session, *args: str):
    if IS_CI:
        session.run("hexdoc-minecraft", *args, "--ci")
    else:
        session.run("hexdoc-minecraft", *args)
