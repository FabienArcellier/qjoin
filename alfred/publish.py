import io
import os
import sys
from typing import Optional

import alfred
import click
import toml
from click import UsageError, Choice
from plumbum.commands.processes import ProcessExecutionError

@alfred.command("publish", help="tag a new release through github action that trigger pypi publication")
def publish():
    """
    tag a release through github actions

    >>> $ alfred publish
    """
    git = alfred.sh("git", "git should be present")

    # update the existing tags
    alfred.run(git, ["fetch"])

    current_version: Optional[str] = None
    try:
        current_version = git["describe", "--tags", "--abbrev=0"]().strip()
    except ProcessExecutionError as exception:
        # happens when no tag exists yet
        if "fatal: No names found, cannot describe anything." in exception.stderr:
            current_version = None
        else:
            raise
    git_status: str = git["status"]()

    on_master = "On branch master" in git_status
    if not on_master:
        click.echo(click.style("Branch should be on master, use git checkout master", fg="red"))
        click.echo(git_status.strip()[0])
        sys.exit(1)

    up_to_date = "Your branch is up to date with 'origin/master'" in git_status
    if not up_to_date:
        click.echo(click.style("Branch should be up to date with origin/master, push your change to repository", fg="red"))
        sys.exit(1)

    non_commited_changes = "Changes not staged for commit" in git_status or "Changes to be committed" in git_status
    if non_commited_changes:
        click.echo(click.style("Changes in progress, can't release a new version", fg="red"))
        sys.exit(1)

    version = __version()
    if current_version == __version():
        click.echo(click.style(f"Version {version} already exists, update version in pyproject.toml", fg='red'))
        sys.exit(1)

    click.echo("")
    click.echo(f"Next release {version} (current: {current_version})")
    click.echo("")
    value = click.prompt("Confirm", type=Choice(['y', 'n']), show_choices=True, default='n')

    if value == 'y':
        alfred.run(git, ['tag', version])
        alfred.run(git, ['push', 'origin', version])


@alfred.command("publish:pypi", help="workflow to release fixtup to pypi")
def publish__pypi():
    """
    workflow to release fixtup current version to pypi

    >>> $ alfred publish:pypi
    """
    alfred.invoke_command('dist')
    alfred.invoke_command('publish:twine')


@alfred.command("publish:twine", help="push fixtup to pypi")
def publish__twine():
    """
    push fixtup to pypi

    This operation requires you set a pypi publication token as env var

    * TWINE_USERNAME
    * TWINE_PASSWORD

    >>> $ alfred publish:twine
    """
    username = os.getenv('TWINE_USERNAME', None)
    password = os.getenv('TWINE_PASSWORD', None)
    if username is None:
        os.environ['TWINE_USERNAME'] = '__token__'

    if password is None:
        raise UsageError('TWINE_PASSWORD should contains your pypi token to publish this library : https://pypi.org/help/#apitoken')

    twine = alfred.sh("twine")
    alfred.run(twine, ['upload', '--non-interactive', 'dist/*'])


def __version() -> str:
    pyproject_path = os.path.realpath('pyproject.toml')
    try:
        with io.open(pyproject_path) as filep:
            pyproject_content = toml.load(filep)
            poetry = pyproject_content.get('tool').get('poetry')
            version = poetry.get('version')
            return version
    except BaseException as exception:
        raise UsageError(f"Can't read pyproject.toml : {exception}")
