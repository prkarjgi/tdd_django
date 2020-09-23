import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/prkarjgi/tdd_django.git"

env.user = "ubuntu"
env.hosts = ["ec2-13-233-116-180.ap-south-1.compute.amazonaws.com"]
env.key_filename = ["/Users/pranavkarajgikar/Downloads/tdd-django.pem"]


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {site_folder}")
    with cd(site_folder):
        _get_latest_source()
        _install_python()
        _update_venv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _install_python():
    # updating system packages
    run("sudo apt update")
    run("sudo apt upgrade")
    run("sudo apt install software-properties-common")

    # install python 3.8.5
    run("sudo add-apt-repository ppa:deadsnakes/ppa")
    run("sudo apt install python3.8")
    print(local("python3.8 --version"))


def _update_venv():
    if not exists("venv/bin/pip3"):
        run("python3.8 -m venv venv")
    run("./venv/bin/pip3 install -r requirements.txt")


def _create_or_update_dotenv():
    run("rm .env")
    append(".env", f"export SITENAME={env.host}")
    current_contents = run("cat .env")
    if "DJANGO_SECRET_KEY" not in current_contents:
        new_secret_key = ''.join(
            random.SystemRandom().choices(
                "abcdefghijklmnopqrstuvwxyz0123456789", k=50
            )
        )
        append(".env", f"export DJANGO_SECRET_KEY={new_secret_key}")
    # run("source .env")
    # run("echo $SITENAME")
    # run("echo $DJANGO_SECRET_KEY")


def _update_static_files():
    run("source .env && ./venv/bin/python3.8 manage.py collectstatic --noinput")


def _update_database():
    run("source .env && ./venv/bin/python3.8 manage.py migrate --noinput")
