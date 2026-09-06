# Become Butter Bot 🧈✨

> **"Better is Good, but Butter is Best."**

**Become Butter** is a self-improvement Telegram bot based on a 28-day transformation cycle. We don’t just become better; we change our entire structure: from "liquid cream" to "pure gold" (Solid Gold Butter).

No motivational fluff — only scientifically backed micro-tasks grounded in neurobiology and psychology.

## 🎯 Project Philosophy
Everything in life should run **smooth like butter**. But to achieve that smoothness, you must first "churn" your character, remove the excess noise, and set into the shape of your best self.

### The 28-Day Program:
1.  **Week 1: Churning the Cream** — Clearing mental clutter and establishing health basics.
2.  **Week 2: Smooth Texture** — Productivity and focus training.
3.  **Week 3: Rich Flavor** — Intellect, mindfulness, and neuroplasticity.
4.  **Week 4: Solid Gold** — Discipline and character tempering.

## 🛠 Tech Stack
- **Python 3.11**
- **Aiogram 3.x** (Asynchronous framework for the bot)
- **SQLAlchemy 2 (async) / aiosqlite** (Database)
- **APScheduler** (Automated daily task distribution)
- **python-dotenv** (Configuration management)

## 📁 Project Structure
The project is built on a modular architecture for easy scaling:
- `bot/` — Settings and configuration.
- `data/` — Task content and bot text strings.
- `database/` — Data models and CRUD queries.
- `handlers/` — Logic for handling commands and tasks.
- `services/` — Broadcast scheduler and external services.

## 💎 Gamification
Complete daily tasks to earn **Butter Drops** 💧 (+10 per task). Your status upgrades automatically as you progress:
- **🥛 Raw Cream** — day 0
- **🥣 Whipped Butter** — day 7
- **🧈 Smooth Texture** — day 14
- **🧈✨ Premium Block** — day 21
- **🏆 Solid Gold** — day 28

## ⚙️ Local Setup
```bash
git clone https://github.com/keshtoim/become_butter_bot.git
cd become_butter_bot

python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env      # then put your BOT_TOKEN from @BotFather into .env
python main.py
```
The SQLite database (`database.db`) is created automatically on first run.

## 🚀 Deployment
The bot is a long-running **worker** (polling, no web server / no exposed port).

**Docker**
```bash
docker build -t become-butter-bot .
docker run -d --name butter-bot --restart unless-stopped \
  -e BOT_TOKEN=123456:ABC... \
  -e DB_URL=sqlite+aiosqlite:///data/database.db \
  -v butter-bot-data:/app/data \
  become-butter-bot
```

**PaaS (Railway / Render / Fly / Heroku-like)**
- Start command: `python main.py` (a `Procfile` with a `worker` process is included).
- Set `BOT_TOKEN` (and optionally `DB_URL`) as environment variables — do **not** commit `.env`.
- SQLite lives on the container filesystem: attach a **persistent volume** and point `DB_URL` at it, or switch to Postgres (`postgresql+asyncpg://…`, add `asyncpg` to `requirements.txt`).

**VPS (systemd)**
```ini
# /etc/systemd/system/butter-bot.service
[Service]
WorkingDirectory=/opt/become_butter_bot
ExecStart=/opt/become_butter_bot/.venv/bin/python main.py
EnvironmentFile=/opt/become_butter_bot/.env
Restart=always
[Install]
WantedBy=multi-user.target
```

> **Schema changes:** startup only runs `create_all` (creates missing tables, never alters existing ones). After changing `database/models.py`, migrate manually or recreate the database.
