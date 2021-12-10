from invoke import run, task
import getpass
import re
import os
import subprocess
import shutil

@task
def test(docs=False):
    print('test')


@task
def mwInstall(docs=False):
    """
    Install mediawiki
    @see (https://gerrit.wikimedia.org/g/mediawiki/core/+/HEAD/DEVELOPERS.md)
    """
    # Create .env configuration file
    ENV_FILE = 'mediawiki/.env'
    password = getpass.getpass(
        "Please enter the desired password for user 'Admin': ")
    env = """
    MW_SCRIPT_PATH=/w
    MW_SERVER=http://localhost:8080
    MW_DOCKER_PORT=8080
    MEDIAWIKI_USER=Admin
    MEDIAWIKI_PASSWORD={}
    XDEBUG_CONFIG=
    XDEBUG_ENABLE=true
    XHPROF_ENABLE=true
    MW_DOCKER_UID={}
    MW_DOCKER_GID={}
    """.format(
        password,     # Admin password, entered above
        os.getuid(),  # UID of current user, for Docker
        os.getgid()   # GID of current user, for Docker
    )
    env = re.sub(r'\s+', '\n', env)  # drop spaces
    with open(ENV_FILE, 'w') as handler:
        handler.write(env)
    print('Created {}'.format(ENV_FILE))
    # Overwrite docker-compose.yml to set database to MariaDB
    shutil.copyfile('docker-compose.tpl', 'mediawiki/docker-compose.yml')
    # Run the mediawiki containers
    subprocess.run(
        ["docker-compose", "-f", "mediawiki/docker-compose.yml", "up", "-d"])


@task
def mwPostInstall(docs=False):
    """
    Install mediawiki database, skin, and required extensions
    """
    subprocess.run([
        "docker-compose", "exec", " mediawiki",
        'php maintenance/install.php  --server=http://localhost:8080 --scriptpath="/w" --dbuser=root --dbserver=database --lang en --pass dockerpass mediawiki admin'])
    subprocess.run(
        ["docker-compose", "exec", "mediawiki", "composer", "update"], cwd="./mediawiki")
    subprocess.run(
        ["docker-compose", "exec", "mediawiki", "/bin/bash", "/docker/install.sh"], cwd="./mediawiki")
    # skin
    if not os.path.isdir('./mediawiki/skins/Vector'):
        subprocess.run([
            "git", "clone", "https://gerrit.wikimedia.org/r/mediawiki/skins/Vector"], cwd="./mediawiki/skins")
    with open("./mediawiki/LocalSettings.php", "a") as handler:
        handler.write("wfLoadSkin( 'Vector' );")
        
