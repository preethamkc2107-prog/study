from __future__ import annotations

from typing import Iterable


TOPIC_LIBRARY = {
    "DBMS": {
        "Topic 1": {
            "summary": "Database Management Systems organize and manage data so it can be stored, retrieved, and updated safely.",
            "keyPoints": [
                "A database stores related data in an organized way.",
                "A DBMS provides an interface between users and the database.",
                "Data integrity and consistency are important database goals."
            ],
            "importantTerms": ["Database", "DBMS", "Data Integrity"],
            "quickQuestions": [
                "What is the difference between data and information?",
                "Why is a DBMS useful for managing large amounts of data?",
                "How does a DBMS help protect data integrity?"
            ]
        },
        "Topic 2": {
            "summary": "A relational database stores data in tables, with relationships defined through keys and associations.",
            "keyPoints": [
                "A table contains rows and columns.",
                "A primary key uniquely identifies each row.",
                "A foreign key connects data between related tables."
            ],
            "importantTerms": ["Table", "Primary Key", "Foreign Key"],
            "quickQuestions": [
                "What is the purpose of a primary key?",
                "How does a foreign key create a relationship?",
                "Why are keys important in relational databases?"
            ]
        }
    },
    "Biology": {
        "Cells": {
            "summary": "Cells are the basic structural and functional units of living organisms.",
            "keyPoints": [
                "The cell membrane controls movement into and out of the cell.",
                "The nucleus contains most of the cell's genetic material.",
                "Organelles perform specialized functions inside the cell."
            ],
            "importantTerms": ["Cell", "Nucleus", "Organelle"],
            "quickQuestions": [
                "What is the basic unit of life?",
                "What does the cell membrane do?",
                "Why do cells contain specialized organelles?"
            ]
        },
        "Photosynthesis": {
            "summary": "Photosynthesis allows plants to use light energy to produce glucose from carbon dioxide and water.",
            "keyPoints": [
                "Plants absorb carbon dioxide from the air.",
                "Chlorophyll captures light energy.",
                "Glucose stores chemical energy for the plant."
            ],
            "importantTerms": ["Photosynthesis", "Chlorophyll", "Glucose"],
            "quickQuestions": [
                "What is the main purpose of photosynthesis?",
                "Which gas do plants take in during photosynthesis?",
                "Why is chlorophyll important?"
            ]
        }
    }
}


def get_topic_material(subject: str, topics: Iterable[str]):
    """Return study material for each requested topic using the local topic library."""
    normalized_subject = (subject or "").strip()
    normalized_topics = [topic.strip() for topic in topics if isinstance(topic, str) and topic.strip()]

    if not normalized_subject:
        raise ValueError("Subject is required.")

    subject_library = TOPIC_LIBRARY.get(normalized_subject)
    if not subject_library:
        raise ValueError(f"No study material is available for {normalized_subject}.")

    material = []
    for topic_name in normalized_topics:
        topic_info = subject_library.get(topic_name)
        if not topic_info:
            raise ValueError(f"No study material is available for topic: {topic_name}.")

        material.append({
            "name": topic_name,
            "summary": topic_info["summary"],
            "keyPoints": topic_info["keyPoints"],
            "importantTerms": topic_info["importantTerms"],
            "quickQuestions": topic_info["quickQuestions"],
        })

    return {"subject": normalized_subject, "topics": material}
