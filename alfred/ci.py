import alfred

@alfred.command("ci", help="workflow to execute the continuous integration process")
def ci():
    """
    workflow to execute the continuous integration process

    * run the linter
    * run the automated tests beginning with units tests
    * build docker image

    >>> $ alfred ci
    """
    alfred.invoke_command('lint')
    alfred.invoke_command('tests')
    alfred.invoke_command('docker:build')



