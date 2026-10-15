# Installation

Languages: [繁體中文](INSTALL.md) · [English (UK)](INSTALL.en-GB.md)

Back to: [README (zh)](../README.md) · [README (en-GB)](README.en-GB.md) · [docs index](README.md)

**Python 3.12+** is required. For a full stack, use Docker Compose (PostgreSQL 16 + Nginx).

## Local development (SQLite)

```bash
git clone https://github.com/naritaroad/umamusume-information-platform.git
cd umamusume-information-platform

python -m venv venv
```

Windows:

```bat
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Optional:

```bash
python manage.py collectstatic --noinput
python manage.py run_discord_bot
python manage.py createsuperuser
```

## Environment variables

Copy [`.env.example`](../.env.example) at the repository root to `.env`. **Do not commit it.** `website_configs/settings.py` loads only that root file.

| Variable | Required | Notes |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | recommended | Long random string: `python -c "import secrets; print(secrets.token_hex(50))"` |
| `DJANGO_DEBUG` | no | `True` on a laptop; `False` when exposed |
| `DJANGO_ALLOWED_HOSTS` | no | Comma-separated. Default `*` |
| `GEMINI_API_KEY` | reports / agents / RAG | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `ANTHROPIC_API_KEY` | dual-model reports | [Anthropic Console](https://console.anthropic.com/) |
| `YOUTUBE_API_KEY` | YouTube page | Cloud Console, YouTube Data API v3 enabled |
| `DISCORD_BOT_TOKEN` | bot | [Discord Developer Portal](https://discord.com/developers/applications) |
| `DISCORD_CLIENT_ID` / `DISCORD_CLIENT_SECRET` | Portal OAuth | UMA Info sign-in |
| `DJANGO_DB_ENGINE` | Docker | Set `postgres` to use PostgreSQL; otherwise SQLite |
| `POSTGRES_*` | Docker | Must match `docker-compose.yml` |

Without YouTube or Discord keys, those pages and the bot stay off; the rest of the site still runs. Without Gemini, reports, sentiment labelling, and RAG will fail or skip.

## Docker

```bash
docker compose up -d --build
docker compose logs -f web-poa
docker compose down
```

Compose starts:

| Service | Container | Role |
| --- | --- | --- |
| `db` | `postgres-poa` | PostgreSQL 16 Alpine |
| `web-poa` | `web-poa` | Django + Gunicorn (entrypoint migrates, collects static files, builds the RAG index if needed) |
| `nginx` | `nginx-poa` | port 80 reverse proxy and static files |
| `discord-bot` | (same image) | `python manage.py run_discord_bot` |

To move an existing SQLite database into Docker Postgres, use `scripts/migrate_dev_to_docker.ps1` (see CHANGELOG 0.6.55-alpha).

## Common problems

| Symptom | What to try |
| --- | --- |
| `Couldn't import Django` | Activate the virtual environment; use Python 3.12+ |
| RAG query fails | Check `app/agent/app_rag_uma/index/uma_knowledge.faiss`, or run `python app/agent/app_rag_uma/build_index.py` |
| YouTube quota exhausted | `/crawler-admin/youtube/` shows today's usage (default 10,000 units/day) |
| Bot does not start | Token, intents, channel IDs; run `run_discord_bot` in a second terminal locally |
| Static files 404 | `python manage.py collectstatic`; Docker serves them from the Nginx `staticfiles` volume |

Architecture: [ARCHITECTURE.en-GB.md](ARCHITECTURE.en-GB.md).
