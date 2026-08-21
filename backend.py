import os
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import telegram_bot


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health", "/healthz"):
            body = b'{"status":"ok","service":"telegram-game-info-bot"}'

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404)

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.environ.get("PORT", "8080"))

    server = ThreadingHTTPServer(
        ("0.0.0.0", port),
        HealthHandler,
    )

    print(
        f"🌐 Health server listening on port {port}",
        flush=True,
    )

    server.serve_forever()


def run_bot_forever():
    restart_delay = 5

    while True:
        try:
            print(
                "🚀 Starting Telegram bot...",
                flush=True,
            )

            telegram_bot.main()

            print(
                f"⚠️ Bot stopped normally. "
                f"Restarting in {restart_delay} seconds...",
                flush=True,
            )

        except Exception as error:
            print(
                f"❌ Bot stopped unexpectedly "
                f"({type(error).__name__}): {error}",
                flush=True,
            )

            traceback.print_exc()

        time.sleep(restart_delay)


def main():
    print(
        "🚀 Starting backend...",
        flush=True,
    )

    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True,
    )

    health_thread.start()

    print(
        "✅ Health server thread started.",
        flush=True,
    )

    run_bot_forever()


if __name__ == "__main__":
    main()