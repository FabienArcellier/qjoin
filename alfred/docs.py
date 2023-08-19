import os

import alfred
import click


@alfred.command('docs:html', help="build documentation in html format")
def docs_html():
    make = alfred.sh('make')
    directory = alfred.project_directory()
    os.chdir(os.path.join(directory, 'docs'))
    alfred.run(make, 'html')


@alfred.command('docs:display', help="open documentation in the browser")
def docs_display():
    open_browser = alfred.sh(["open", "xdg-open"])
    directory = alfred.project_directory()

    documentation_directory = os.path.join(directory, 'docs', '_build', 'html')
    if os.path.isdir(documentation_directory) == False:
        alfred.invoke_command('docs:html')

    os.chdir(os.path.join(directory, 'docs', '_build', 'html'))
    click.echo(f"opening {documentation_directory}/index.html")
    alfred.run(open_browser, 'index.html')
