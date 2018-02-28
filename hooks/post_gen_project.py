"""
NOTE:
    the below code is to be maintained Python 2.x-compatible
    as the whole Cookiecutter Django project initialization
    can potentially be run in Python 2.x environment
    (at least so we presume in `pre_gen_project.py`).

TODO: ? restrict Cookiecutter Django project initialization to Python 3.x environments only
"""

import os
import random
import shutil
import string
import sys

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

PROJECT_DIR_PATH = os.path.realpath(os.path.curdir)


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def append_to_project_gitignore(path):
    gitignore_file_path = os.path.join(PROJECT_DIR_PATH, '.gitignore')
    with open(gitignore_file_path, 'a') as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(length,
                           using_digits=False,
                           using_ascii_letters=False,
                           using_punctuation=False):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        symbols += string.punctuation \
            .replace('"', '') \
            .replace("'", '') \
            .replace('\\', '')
    return ''.join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path,
             flag,
             value=None,
             *args,
             **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            import sys
            sys.stdout.write(
                "We couldn't find a secure pseudo-random number generator on your system. "
                "Please, make sure to manually {} later.".format(flag)
            )
            random_string = flag
        value = random_string

    with open(file_path, 'r+') as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    django_secret_key = set_flag(
        file_path,
        '!!!SET DJANGO_SECRET_KEY!!!',
        length=50,
        using_digits=True,
        using_ascii_letters=True
    )
    return django_secret_key


def set_postgres_user(file_path,
                      value=None):
    postgres_user = set_flag(
        file_path,
        '!!!SET POSTGRES_USER!!!',
        value=value,
        length=8,
        using_ascii_letters=True
    )
    return postgres_user


def set_postgres_password(file_path):
    postgres_password = set_flag(
        file_path,
        '!!!SET POSTGRES_PASSWORD!!!',
        length=42,
        using_digits=True,
        using_ascii_letters=True
    )
    return postgres_password


def initialize_dotenv(postgres_user):
    # Initializing `env.example` first.
    envexample_file_path = os.path.join(PROJECT_DIR_PATH, 'env.example')
    set_django_secret_key(envexample_file_path)
    set_postgres_user(envexample_file_path, value=postgres_user)
    set_postgres_password(envexample_file_path)
    # Renaming `env.example` to `.env`.
    dotenv_file_path = os.path.join(PROJECT_DIR_PATH, '.env')
    shutil.move(envexample_file_path, dotenv_file_path)


def initialize_localyml(postgres_user):
    set_postgres_user(os.path.join(PROJECT_DIR_PATH, 'local.yml'), value=postgres_user)


def initialize_local_settings():
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'local.py'))


def initialize_test_settings():
    set_django_secret_key(os.path.join(PROJECT_DIR_PATH, 'config', 'settings', 'test.py'))


def main():
    postgres_user = generate_random_string(length=16, using_ascii_letters=True)
    initialize_dotenv(postgres_user)
    initialize_localyml(postgres_user)
    initialize_local_settings()
    initialize_test_settings()

if __name__ == '__main__':
    main()
