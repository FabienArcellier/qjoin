import alfred

@alfred.command("dist", help="build distribution packages")
def dist():
    """
    build distribution packages

    >>> $ alfred dist
    """
    poetry = alfred.sh("poetry", "poetry should be present")
    alfred.run(poetry, ['build'])

