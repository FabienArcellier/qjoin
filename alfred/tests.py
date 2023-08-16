import alfred


@alfred.command("tests", help="workflow to execute all automatic tests")
def tests():
    """
    execute tests with unittests

    >>> $ alfred tests
    """
    pytest = alfred.sh("pytest")
    alfred.run(pytest, ['tests/units'])




