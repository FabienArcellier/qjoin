import alfred

@alfred.command("lint", help="check type consistency on source code")
def lint():
    """
    check the type consistency with mypy

    >>> $ alfred lint
    """
    mypy = alfred.sh("mypy", "mypy should be present")
    alfred.run(mypy, ['src'])

