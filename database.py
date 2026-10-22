import sqlite3
import json
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

DATABASE_NAME = "coding_coach.db"


def initialize_database():
    """Create the database and student profiles table."""
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS student_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                leetcode_profile TEXT,
                other_profiles TEXT,
                target_companies TEXT,
                weekly_hours INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS approved_weekly_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                plan_hash TEXT NOT NULL,
                plan_data TEXT NOT NULL,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_name, plan_hash)
            )
        
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS solved_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                problem_name TEXT NOT NULL,
                problem_url TEXT NOT NULL,
                platform TEXT NOT NULL,
                solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_student_profile(profile):
    """Save a student profile permanently in SQLite."""
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            INSERT INTO student_profiles (
                student_name,
                leetcode_profile,
                other_profiles,
                target_companies,
                weekly_hours
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            profile["name"],
            profile["leetcode_profile"],
            profile["other_profiles"],
            json.dumps(profile["target_companies"]),
            profile["weekly_hours"]
        ))


def get_latest_student_profile():
    """Retrieve the most recently saved student profile."""
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute("""
            SELECT *
            FROM student_profiles
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

        if row is None:
            return None

        return {
            "id": row["id"],
            "name": row["student_name"],
            "leetcode_profile": row["leetcode_profile"],
            "other_profiles": row["other_profiles"],
            "target_companies": json.loads(row["target_companies"]),
            "weekly_hours": row["weekly_hours"],
            "created_at": row["created_at"]
        }


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")

def save_topic_progress(student_name, topic_progress):
    """Save a snapshot of a student's coding practice progress."""

    with sqlite3.connect(DATABASE_NAME) as connection:

        # Create tables if they do not already exist.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS progress_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS topic_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,
                topic TEXT NOT NULL,
                solved_count INTEGER NOT NULL,
                FOREIGN KEY (snapshot_id)
                    REFERENCES progress_snapshots(id)
            )
        """)

        # Create a new progress snapshot.
        cursor = connection.execute("""
            INSERT INTO progress_snapshots (student_name)
            VALUES (?)
        """, (student_name,))

        snapshot_id = cursor.lastrowid

        # Save each topic's problem count.
        for topic, solved_count in topic_progress.items():

            connection.execute("""
                INSERT INTO topic_progress (
                    snapshot_id,
                    topic,
                    solved_count
                )
                VALUES (?, ?, ?)
            """, (snapshot_id, topic, solved_count))

    return snapshot_id


def get_latest_topic_progress(student_name):
    """Retrieve the most recently saved progress snapshot."""

    with sqlite3.connect(DATABASE_NAME) as connection:

        connection.row_factory = sqlite3.Row

        snapshot = connection.execute("""
            SELECT id, recorded_at
            FROM progress_snapshots
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 1
        """, (student_name,)).fetchone()

        if snapshot is None:
            return None

        rows = connection.execute("""
            SELECT topic, solved_count
            FROM topic_progress
            WHERE snapshot_id = ?
        """, (snapshot["id"],)).fetchall()

        return {
            "recorded_at": snapshot["recorded_at"],
            "topics": {
                row["topic"]: row["solved_count"]
                for row in rows
            }
        }

def get_previous_topic_progress(student_name):
    """Retrieve the second-most-recent progress snapshot."""

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        snapshot = connection.execute("""
            SELECT id, recorded_at
            FROM progress_snapshots
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 1 OFFSET 1
        """, (student_name,)).fetchone()

        if snapshot is None:
            return None

        rows = connection.execute("""
            SELECT topic, solved_count
            FROM topic_progress
            WHERE snapshot_id = ?
        """, (snapshot["id"],)).fetchall()

        return {
            "recorded_at": snapshot["recorded_at"],
            "topics": {
                row["topic"]: row["solved_count"]
                for row in rows
            }
        }


def save_source_evidence(
    student_name,
    source_type,
    source_url,
    notes=""
):
    """Save evidence about the source of coding progress data."""

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS source_evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        """)

        connection.execute("""
            INSERT INTO source_evidence (
                student_name,
                source_type,
                source_url,
                notes
            )
            VALUES (?, ?, ?, ?)
        """, (
            student_name,
            source_type,
            source_url,
            notes
        ))

    return True


def get_source_evidence(student_name):
    """Retrieve saved source evidence for a student."""

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        connection.execute("""
            CREATE TABLE IF NOT EXISTS source_evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_url TEXT NOT NULL,
                retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        """)

        rows = connection.execute("""
            SELECT
                id,
                student_name,
                source_type,
                source_url,
                retrieved_at,
                notes
            FROM source_evidence
            WHERE student_name = ?
            ORDER BY id DESC
        """, (student_name,)).fetchall()

        return [dict(row) for row in rows]




def save_fetched_profile(student_name, profile_result):
    """Save retrieved LeetCode profile information in SQLite."""
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS fetched_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                username TEXT,
                source_url TEXT NOT NULL,
                ranking INTEGER,
                solved_by_difficulty TEXT,
                success INTEGER NOT NULL,
                message TEXT,
                retrieved_at TEXT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        profile_data = profile_result.get("data") or {}

        connection.execute("""
            INSERT INTO fetched_profiles (
                student_name, username, source_url, ranking,
                solved_by_difficulty, success, message, retrieved_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            student_name,
            profile_data.get("username"),
            profile_result.get("source_url") or "",
            profile_data.get("ranking"),
            json.dumps(profile_data.get("solved_by_difficulty", {})),
            int(profile_result.get("success", False)),
            profile_result.get("message", ""),
            profile_result.get("retrieved_at")
        ))


def get_latest_fetched_profile(student_name):
    """Retrieve the most recently saved LeetCode profile."""
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute("""
            SELECT *
            FROM fetched_profiles
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 1
        """, (student_name,)).fetchone()

        if row is None:
            return None

        result = dict(row)
        result["solved_by_difficulty"] = json.loads(
            result["solved_by_difficulty"] or "{}"
        )
        result["success"] = bool(result["success"])

        return result

def get_previous_fetched_profile(student_name):
    """Retrieve the second-most-recent fetched profile for a student."""
    import json

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute("""
            SELECT *
            FROM fetched_profiles
            WHERE student_name = ?
            ORDER BY id DESC
            LIMIT 1 OFFSET 1
        """, (student_name,)).fetchone()

        if row is None:
            return None

        result = dict(row)

        result["solved_by_difficulty"] = json.loads(
            result["solved_by_difficulty"] or "{}"
        )
        result["success"] = bool(result["success"])

        return result

    




def save_approved_weekly_plan(student_name, plan_data):
    """
    Save an approved weekly plan.
    Prevent duplicate approvals of identical plans for the same student.
    """

    plan_json = json.dumps(
        plan_data,
        sort_keys=True,
        ensure_ascii=False
    )

    plan_hash = hashlib.sha256(
        plan_json.encode("utf-8")
    ).hexdigest()

    with sqlite3.connect(DATABASE_NAME) as connection:
        ist_timestamp = datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).strftime("%Y-%m-%d %H:%M:%S")

        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO approved_weekly_plans (
                student_name,
                plan_hash,
                plan_data,
                approved_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (student_name, plan_hash, plan_json, ist_timestamp)
        )

        if cursor.rowcount == 0:
            return {
                "success": False,
                "message": "This identical plan has already been approved and saved."
            }

    return {
        "success": True,
        "message": "Approved weekly plan saved successfully."
    }


def get_approved_weekly_plans(student_name):
    """Retrieve previously approved weekly plans for a student."""

    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT id, student_name, plan_data, approved_at
            FROM approved_weekly_plans
            WHERE student_name = ?
            ORDER BY approved_at DESC, id DESC
            """,
            (student_name,)
        ).fetchall()

    approved_plans = []

    for row in rows:
        approved_plans.append({
            "id": row["id"],
            "student_name": row["student_name"],
            "plan_data": json.loads(row["plan_data"]),
            "approved_at": row["approved_at"]
        })

    return approved_plans



def save_solved_problems(student_name, solved_problems):
    """
    Save solved problems without inserting duplicate records
    for the same student, problem URL, and platform.
    """
    with sqlite3.connect(DATABASE_NAME) as connection:
        for problem in solved_problems:
            name = problem.get("name", "").strip()
            platform = problem.get("platform", "").strip()
            url = problem.get("url", "").strip().rstrip("/").lower()

            if not name or not platform:
                continue

            # Check whether this record already exists.
            existing = connection.execute(
                """
                SELECT id
                FROM solved_problems
                WHERE student_name = ?
                  AND platform = ?
                  AND (
                      LOWER(RTRIM(problem_url, '/')) = ?
                      OR (
                          problem_url = ''
                          AND LOWER(problem_name) = LOWER(?)
                      )
                  )
                LIMIT 1
                """,
                (student_name, platform, url, name)
            ).fetchone()

            if existing:
                continue

            connection.execute(
                """
                INSERT INTO solved_problems
                (student_name, problem_name, problem_url, platform)
                VALUES (?, ?, ?, ?)
                """,
                (student_name, name, url, platform)
            )




def get_unique_solved_problems(student_name):
    """
    Retrieve solved problems and count the same problem only once
    across platforms when their normalized problem names match.
    """
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT problem_name, problem_url, platform
            FROM solved_problems
            WHERE student_name = ?
            ORDER BY id ASC
            """,
            (student_name,)
        ).fetchall()

    unique_problems = {}
    duplicate_count = 0

    for row in rows:
        name = row["problem_name"].strip()
        url = row["problem_url"].strip().rstrip("/").lower()
        platform = row["platform"].strip()

        # Normalize the problem name for cross-platform comparison.
        normalized_name = " ".join(name.lower().split())

        # Prefer the normalized name so matching problem names
        # across platforms can be counted only once.
        key = normalized_name

        if key in unique_problems:
            duplicate_count += 1
        else:
            unique_problems[key] = {
                "name": name,
                "url": url,
                "platform": platform
            }

    return {
        "unique_count": len(unique_problems),
        "duplicate_count": duplicate_count,
        "unique_problems": list(unique_problems.values())
    }


