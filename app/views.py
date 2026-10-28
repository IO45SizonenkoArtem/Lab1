import os
from datetime import UTC, datetime

from flask import Flask, jsonify

app = Flask(__name__)


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


@app.route("/healthz/live", methods=["GET"])
def liveness_check():
    """Перевірка життєздатності процесу застосунку (Liveness)."""
    return jsonify({"status": "alive", "timestamp": utc_now()}), 200


@app.route("/healthz/ready", methods=["GET"])
def readiness_check():
    """Перевірка готовності застосунку до обробки трафіку (Readiness)."""
    # На етапі Лабораторної №1 підключення до БД відсутнє
    return jsonify(
        {
            "status": "ready",
            "database": "not_connected_yet",
            "timestamp": utc_now(),
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))