# Cooliente scraper

This repo provides a CLI tool to scrape data from betting sites like Caliente.mx
and Bet365, and stores them in a PostgreSQL database. The target is to be able
to update the odds of all Liga MX matches once every 60 seconds.

## Running the scraper

### Pre-requirements

The project is still a PoC, so all things run locally. The requirements for
running this project are:

- Docker (Docker Desktop).
- Nix (with flakes enabled).

### Steps

1. **Start the Docker container**:

First, we need to start the container. For this, there is `docker-compose.yaml`
in this repo which is going to bring up a PostgreSQL and Adminer container.

There is a provided `.env.dev` with the required environmental variables. For
testing purposes, we can do:

```bash
cp .env.dev .env
```

After this, we can run the following to set up the containers:

```bash
docker-compose up -d
```

2. **Enable the CLI tool**:

Initial instructions are going to be using Nix. The project has a uv workspaces
which can be used independently, but instructions are not provided.

First, we need to enter the devshell where the CLI is available. This command is
going to download and build all related dependencies for the project, so it
might take a while:

```bash
nix develop
```

After the setup finished, we can check the CLI is available with the following
command:

```bash
cooliente --help
```

Lastly, we need to install the required web driver:

```bash
patchright install chrome
```

2. **Running the CLI**:

> [!NOTE] 
> This currently scrapes Bet365 from Argentina, as it blocks VPNs. If you are 
> trying to test this from another country, you'll need to navigate the the 
> Liga MX website for your bet365, copy the link to 
> `packages/cooliente/src/cooliente/scrapers/__init__.py`. This might be moved
> to a configuration file later.

Running the CLI is simple. We only need to specify a comma-separated list of
betting sites:

```bash
cooliente "caliente,bet365"
```

We can verify that it runs correctly going to `localhost:8080` to reach Adminer,
logging in, and going to the `cooliente.public.matches` table.
