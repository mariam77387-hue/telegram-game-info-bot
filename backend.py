import time
import telegram_bot


def main():
    restart_delay = 5

    while True:
        try:
            print("🚀 Starting Telegram bot...", flush=True)

            telegram_bot.main()

            print(
                f"⚠️ Bot stopped normally. "
                f"Restarting in {restart_delay} seconds...",
                flush=True,
            )

        except Exception as error:
            print(
                f"❌ Bot stopped with "
                f"{type(error).__name__}: {error}",
                flush=True,
            )

            print(
                f"🔄 Restarting in {restart_delay} seconds...",
                flush=True,
            )

        time.sleep(restart_delay)


if __name__ == "__main__":
    main()