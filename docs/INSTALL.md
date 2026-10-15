# 安裝

語言：[繁體中文](INSTALL.md) · [English (UK)](INSTALL.en-GB.md)

回到：[README](../README.md) · [文件索引](README.md)

需要 **Python 3.12+**。正式環境建議 Docker Compose（PostgreSQL 16 + Nginx）。

## 本機開發（SQLite）

```bash
git clone https://github.com/naritaroad/umamusume-information-platform.git
cd umamusume-information-platform

python -m venv venv
```

Windows：

```bat
venv\Scripts\activate
```

macOS / Linux：

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

瀏覽 [http://127.0.0.1:8000](http://127.0.0.1:8000)。

可選：

```bash
python manage.py collectstatic --noinput
python manage.py run_discord_bot
python manage.py createsuperuser
```

## 環境變數

複製根目錄 [`.env.example`](../.env.example) 為 `.env`，**不要提交**。`website_configs/settings.py` 只讀專案根目錄的 `.env`。

| 變數 | 必要 | 說明 |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | 建議 | 隨機長字串。可用 `python -c "import secrets; print(secrets.token_hex(50))"` |
| `DJANGO_DEBUG` | 否 | 本機 `True`；對外務必 `False` |
| `DJANGO_ALLOWED_HOSTS` | 否 | 逗號分隔。預設 `*` |
| `GEMINI_API_KEY` | 報告／Agent／RAG | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `ANTHROPIC_API_KEY` | 雙模型報告 | [Anthropic Console](https://console.anthropic.com/) |
| `YOUTUBE_API_KEY` | YouTube 頁 | Cloud Console，啟用 YouTube Data API v3 |
| `DISCORD_BOT_TOKEN` | Bot | [Discord Developer Portal](https://discord.com/developers/applications) |
| `DISCORD_CLIENT_ID` / `DISCORD_CLIENT_SECRET` | Portal OAuth | UMA Info 登入 |
| `DJANGO_DB_ENGINE` | Docker | 設 `postgres` 才用 PostgreSQL，否則 SQLite |
| `POSTGRES_*` | Docker | 與 `docker-compose.yml` 對齊 |

沒有 YouTube／Discord 金鑰時，對應頁面與 Bot 不會啟動，網站其餘功能仍可跑。沒有 Gemini 時，AI 報告、情感標記與 RAG 會失敗或略過。

## Docker

```bash
docker compose up -d --build
docker compose logs -f web-poa
docker compose down
```

Compose 會起：

| 服務 | 容器名 | 角色 |
| --- | --- | --- |
| `db` | `postgres-poa` | PostgreSQL 16 Alpine |
| `web-poa` | `web-poa` | Django + Gunicorn（entrypoint 會 migrate、collectstatic，必要時建 RAG 索引） |
| `nginx` | `nginx-poa` | `:80` 反向代理與靜態檔 |
| `discord-bot` | （同映像） | `python manage.py run_discord_bot` |

本機已有 SQLite 要搬進 Docker 資料庫，可用 `scripts/migrate_dev_to_docker.ps1`（見 CHANGELOG 0.6.55-alpha）。

## 常見問題

| 現象 | 處理 |
| --- | --- |
| `Couldn't import Django` | 虛擬環境未啟動，或 Python 不是 3.12+ |
| RAG 查詢失敗 | 確認 `app/agent/app_rag_uma/index/uma_knowledge.faiss`；可執行 `python app/agent/app_rag_uma/build_index.py` |
| YouTube 配額用盡 | 控制台 `/crawler-admin/youtube/` 看當日用量（預設 10,000 units／日） |
| Bot 不起來 | Token、Intent、頻道 ID；本機另開一個終端跑 `run_discord_bot` |
| 靜態檔 404 | `python manage.py collectstatic`；Docker 由 Nginx 掛 `staticfiles` volume |

架構說明：[ARCHITECTURE.md](ARCHITECTURE.md)。
