
import requests
from datetime import datetime, timezone
from urllib.parse import urlparse


def get_leetcode_username(profile_url):
    """Extract the username from a standard LeetCode profile URL."""

    parsed_url = urlparse(profile_url.strip())
    hostname = (parsed_url.hostname or "").lower()

    if hostname not in {"leetcode.com", "www.leetcode.com"}:
        return None

    parts = parsed_url.path.strip("/").split("/")

    if len(parts) != 2 or parts[0] != "u" or not parts[1]:
        return None

    return parts[1]


def fetch_leetcode_profile(profile_url):
    """
    Retrieve publicly accessible LeetCode profile information.

    This function reports retrieval failures instead of guessing data.
    """

    username = get_leetcode_username(profile_url)

    if username is None:
        return {
            "success": False,
            "message": (
                "Please provide a standard LeetCode profile URL, "
                "such as https://leetcode.com/u/username/."
            ),
            "source_url": profile_url,
            "retrieved_at": None,
            "data": None
        }

    endpoint = "https://leetcode.com/graphql"

    query = """
    query userPublicProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile {
                realName
                ranking
            }
            submitStats {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    try:
        response = requests.post(
            endpoint,
            json={
                "query": query,
                "variables": {"username": username}
            },
            headers={
                "Content-Type": "application/json",
                "Referer": f"https://leetcode.com/u/{username}/"
            },
            timeout=15
        )

        retrieved_at = datetime.now(timezone.utc).isoformat()
        response.raise_for_status()

        result = response.json()

        if result.get("errors"):
            return {
                "success": False,
                "message": (
                    "LeetCode could not verify the profile information. "
                    "Please check the profile URL and try again later. "
                    "If the profile is private or remains inaccessible, "
                    "please provide a profile export so your progress "
                    "can be analyzed without guessing."
                ),
                "source_url": profile_url,
                "retrieved_at": retrieved_at,
                "data": None
            }

        user = result.get("data", {}).get("matchedUser")

        if not user:
            return {
                "success": False,
                "message": (
                    "The profile could not be found or its information "
                    "is not publicly available. Please check the profile URL. "
                    "If the profile is private or inaccessible, please provide "
                    "a profile export so your progress can be analyzed "
                    "without guessing."
                ),
                "source_url": profile_url,
                "retrieved_at": retrieved_at,
                "data": None
            }

        submissions = user.get("submitStats", {}).get(
            "acSubmissionNum", []
        )

        solved_counts = {
            item["difficulty"]: item["count"]
            for item in submissions
        }

        return {
            "success": True,
            "message": "Public profile information retrieved.",
            "source_url": profile_url,
            "retrieved_at": retrieved_at,
            "data": {
                "username": user.get("username"),
                "real_name": user.get("profile", {}).get("realName"),
                "ranking": user.get("profile", {}).get("ranking"),
                "solved_by_difficulty": solved_counts
            }
        }

    except requests.RequestException:
        return {
            "success": False,
            "message": (
                "Could not retrieve the profile. Check your internet "
                "connection and try again later."
            ),
            "source_url": profile_url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "data": None
        }

    except (ValueError, TypeError, KeyError):
        return {
            "success": False,
            "message": (
                "The profile response could not be interpreted safely."
            ),
            "source_url": profile_url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "data": None
        }


def fetch_leetcode_solved_problems(profile_url):
    """
    Retrieve publicly accessible solved problem names and URLs
    for a LeetCode user.

    Returns an explicit failure if the profile cannot be verified.
    """
    username = get_leetcode_username(profile_url)

    if username is None:
        return {
            "success": False,
            "message": "Please provide a valid LeetCode profile URL.",
            "source_url": profile_url,
            "retrieved_at": None,
            "problems": []
        }

    endpoint = "https://leetcode.com/graphql"

    query = """
    query userProblemsSolved($username: String!) {
        matchedUser(username: $username) {
            username
            problemsSolvedBeatsStats {
                difficulty
                percentage
            }
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """

    try:
        response = requests.post(
            endpoint,
            json={
                "query": query,
                "variables": {"username": username}
            },
            headers={
                "Content-Type": "application/json",
                "Referer": f"https://leetcode.com/u/{username}/"
            },
            timeout=15
        )

        retrieved_at = datetime.now(timezone.utc).isoformat()
        response.raise_for_status()

        result = response.json()

        if result.get("errors"):
            return {
                "success": False,
                "message": "LeetCode could not verify the requested data.",
                "source_url": profile_url,
                "retrieved_at": retrieved_at,
                "problems": []
            }

        user = result.get("data", {}).get("matchedUser")

        if not user:
            return {
                "success": False,
                "message": (
                    "The profile was not found or its information "
                    "is not publicly available."
                ),
                "source_url": profile_url,
                "retrieved_at": retrieved_at,
                "problems": []
            }

        return {
            "success": True,
            "message": (
                "Profile statistics retrieved, but individual solved "
                "problem names and URLs are not provided by this query."
            ),
            "source_url": profile_url,
            "retrieved_at": retrieved_at,
            "username": user.get("username"),
            "problems": []
        }

    except (requests.RequestException, ValueError, TypeError):
        return {
            "success": False,
            "message": "Could not retrieve or interpret the LeetCode response.",
            "source_url": profile_url,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "problems": []
        }

