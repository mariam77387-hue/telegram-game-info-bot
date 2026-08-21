import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import telegram_bot


PORT = int(os.getenv("PORT", "10000"))


class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"OK")

    def log_message(self, format, *args):
        return


def start_health_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)

    print(
        f"🌐 Health server listening on port {PORT}",
        flush=True,
    )

    server.serve_forever()


def main():

    print("🚀 Starting backend...", flush=True)

    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True,
    )

    health_thread.start()

    print(
        "✅ Health server thread started.",
        flush=True,
    )

    print(
        "🚀 Starting Telegram bot...",
        flush=True,
    )

    # نشغل البوت مرة واحدة فقط.
    # لا يوجد restart loop حتى نعرف مصدر الـ Conflict.
    telegram_bot.main()


if __name__ == "__main__":
    main()