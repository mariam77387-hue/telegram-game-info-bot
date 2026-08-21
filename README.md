# Telegram Game Info Bot

An always-on Telegram bot that provides game information in Arabic and English.

## Included games

- Minecraft
- Roblox
- Fortnite
- Valorant
- Rocket League
- Brawl Stars

## Run locally

1. Install Python 3.11 or newer.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set the `BOT_TOKEN` environment variable to your Telegram bot token.
4. Start the service:

   ```bash
   python backend.py
   ```

The bot uses Telegram polling. The backend also exposes `/healthz` on port 8080.

## Deploy on Render

This repository includes `render.yaml` for a Render Background Worker.

1. Create a new Render service from this repository.
2. Use the `BOT_TOKEN` environment variable field to add the token securely.
3. Deploy the worker.

Never commit the bot token to GitHub.