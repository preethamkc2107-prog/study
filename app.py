import os
from contextlib import closing
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from backend.database import get_connection, get_database_path, init_db, seed_sample_data
from backend.review_service import get_topic_material


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.environ.get("STUDYSYNC_DB", "studysync.db"),
    )

    if test_config:
        app.config.update(test_config)

    db_path = get_database_path(app.config)
    init_db(db_path)
    if os.environ.get("STUDYSYNC_SEED_DATA") == "1":
        seed_sample_data(db_path)

    @app.errorhandler(400)
    def handle_bad_request(error):
        response = {"error": "The request could not be processed."}
        if hasattr(error, "description"):
            response["error"] = error.description
        return jsonify(response), 400

    @app.errorhandler(500)
    def handle_server_error(error):
        return jsonify({"error": "Something went wrong while finding study material. Please try again."}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"})

    @app.route("/api/study-plan", methods=["POST"])
    def save_study_plan():
        payload = request.get_json(silent=True) or {}
        subject = str(payload.get("subject", "")).strip()
        topics = payload.get("topics", [])

        if not subject or not isinstance(topics, list) or not topics:
            return jsonify({"error": "subject and topics are required."}), 400

        normalized_topics = [str(topic).strip() for topic in topics]
        if not all(normalized_topics):
            return jsonify({"error": "Topics must be valid names."}), 400

        with get_connection(db_path) as connection:
            connection.executemany(
                "INSERT OR IGNORE INTO study_plans (subject, topic) VALUES (?, ?)",
                [(subject, topic) for topic in normalized_topics],
            )
            connection.commit()

        return jsonify({"subject": subject, "topics": normalized_topics}), 201

    @app.route("/api/review-topics", methods=["POST"])
    def review_topics():
        payload = request.get_json(silent=True) or {}
        subject = str(payload.get("subject", "")).strip()
        topics = payload.get("topics", [])

        if not subject or not isinstance(topics, list) or not topics:
            return jsonify({"error": "subject and topics are required."}), 400

        normalized_topics = [str(topic).strip() for topic in topics]
        if not all(normalized_topics):
            return jsonify({"error": "Topics must be valid names."}), 400

        with closing(get_connection(db_path)) as connection:
            placeholders = ", ".join("?" for _ in normalized_topics)
            rows = connection.execute(
                "SELECT topic FROM study_plans WHERE subject = ? AND topic IN (" + placeholders + ")",
                [subject, *normalized_topics],
            ).fetchall()

        saved_topics = {row["topic"] for row in rows}
        missing_topics = [topic for topic in normalized_topics if topic not in saved_topics]
        if missing_topics:
            return jsonify({"error": "One or more topics are not in the study plan."}), 400

        try:
            review_material = get_topic_material(subject, normalized_topics)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        with closing(get_connection(db_path)) as connection:
            connection.executemany(
                "INSERT OR IGNORE INTO completion_records (subject, topic, completed_at) VALUES (?, ?, ?)",
                [(subject, topic, datetime.now(timezone.utc).isoformat(timespec="seconds")) for topic in normalized_topics],
            )
            connection.commit()

        return jsonify(review_material)

    return app
