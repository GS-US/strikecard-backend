# Installation and Local Setup Instructions

We use `pip` and `venv` to manage the development environment when installed
locally. To set up the development environment and get working, please follow
these instructions.

1. (One-time setup) [Install and Configure the Development Environment](#install-and-configure-the-development-environment).
1. Each time you start a new terminal or IDE session, be sure to [Activate the Virtual Environment](#activate-the-virtual-environment).
1. When ready to run the server, [Start the Local Server](#start-the-local-server).

## Working With the Operation Starfish Project

### Install and Configure the Development Environment

This is a one-time setup and must be run before subsequent steps.

- Run `pushd starfish/` to enter the subdirectory where the installers are.
- Run `./install.sh` to set up the local development environment.
- Edit `.env` to configure the local deployment environment.
    - Set a value for `DJANGO_SECRET_KEY`.
    - Set a value for `DJANGO_CONTACT_HASH_SALT`.
    - See [Generating Secret Keys for
      Development](#generating-secret-keys-for-development) below for how to
      securely generate these values.

#### Generating Secret Keys for Development

Run the following in a terminal with the `venv` activated to output values
appropriate for both `DJANGO_SECRET_KEY` and `DJANGO_CONTACT_HASH_SALT`. You
will need to run this twice, once for each value. Copy the returned values into
the `.env` file.

```shell
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Activate the Virtual Environment

- Ensure you are in the `starfish/` directory.
- Run `source ./venv/bin/activate` to activate the virtual environment.

### Start the Local Server

- Ensure you are in the `starfish/` directory.
- Run `./dev.sh` to start the server.
- Visit `localhost:8000` in your favorite browser to view the site.

#### For Other Networking Configurations

If any of the following apply, then add the following line to your `.env` file,
making appropriate substitutions for bracketed `<values>`.

- Running on a host other than `localhost`.
- Changed the name of `localhost` on your system.
- Have multiple hostnames you need to allow in Django.

```shell
export DJANGO_ALLOWED_HOSTS='<yourhostname>,<yourotherhostname>,localhost,<ifyouuseit>'
```

## Working With the Docs

### Installing the Docs

- Ensure you are in the repo root directory.
- Perform at least the first two steps in [Install and Configure the Development
  Environment](#install-and-configure-the-development-environment). If you are
  only working with the docs, there is no need to perform additional steps.

### Building the Docs

To check for errors, use the following command.

```shell
mkdocs build --strict
```

To engage with a local dynamic server, use the following command.

```shell
mkdocs serve
```
