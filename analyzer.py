
def analyze_coding_progress(topic_progress):
    """
    Analyze coding practice progress and identify weak topics.

    Args:
        topic_progress: A dictionary containing topic names
        and the number of problems solved in each topic.

    Returns:
        A dictionary containing the analysis results.
    """

    weak_topics = []
    strong_topics = []

    for topic, solved_count in topic_progress.items():

        if solved_count == 0:
            weak_topics.append({
                "topic": topic,
                "solved": solved_count,
                "priority": "High",
                "reason": "No problems solved in this topic."
            })

        elif solved_count < 5:
            weak_topics.append({
                "topic": topic,
                "solved": solved_count,
                "priority": "High",
                "reason": "Very little practice completed."
            })

        elif solved_count < 10:
            weak_topics.append({
                "topic": topic,
                "solved": solved_count,
                "priority": "Medium",
                "reason": "More practice is recommended."
            })

        else:
            strong_topics.append({
                "topic": topic,
                "solved": solved_count
            })

    # Sort weak topics by solved count.
    # Topics with fewer solved problems appear first.
    weak_topics.sort(key=lambda item: item["solved"])

    return {
        "weak_topics": weak_topics,
        "strong_topics": strong_topics,
        "total_topics": len(topic_progress),
        "total_problems_solved": sum(topic_progress.values())
    }

if __name__ == "__main__":

    # Sample coding practice data
    topic_progress = {
        "Arrays": 25,
        "Strings": 18,
        "Trees": 8,
        "Graphs": 0,
        "Dynamic Programming": 3
    }

    # Analyze the coding practice data
    result = analyze_coding_progress(topic_progress)

    print("\n===== CODING PRACTICE ANALYSIS =====")

    print("\nTotal topics:", result["total_topics"])
    print("Total problems solved:", result["total_problems_solved"])

    print("\n--- Weak Topics ---")

    for topic in result["weak_topics"]:
        print(
            f'{topic["topic"]}: '
            f'{topic["solved"]} problems solved | '
            f'Priority: {topic["priority"]} | '
            f'{topic["reason"]}'
        )

    print("\n--- Strong Topics ---")

    for topic in result["strong_topics"]:
        print(
            f'{topic["topic"]}: '
            f'{topic["solved"]} problems solved'
        )

def generate_weekly_plan(topic_progress, weekly_hours):
    """
    Generate a personalized weekly coding practice plan.
    """

    analysis = analyze_coding_progress(topic_progress)

    weak_topics = analysis["weak_topics"]

    if not weak_topics:
        return [
            {
                "day": "Monday",
                "topic": "Mixed Practice",
                "hours": weekly_hours,
                "task": "Solve problems from different topics and review mistakes."
            }
        ]

    # Prioritize topics with fewer solved problems.
    daily_plan = []

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    base_hours = round(weekly_hours / len(days), 2)

    
    for index, day in enumerate(days):
         # Give the weakest topics more practice sessions.
        if index < 4:
            topic_info = weak_topics[0]
        else:
            topic_info = weak_topics[index % len(weak_topics)]



        if index == len(days) - 1:
            hours = round(
                weekly_hours - base_hours * (len(days) - 1),
                2   
        )
        else:
            hours = base_hours

        daily_plan.append({
                "day": day,
                "topic": topic_info["topic"],
                "hours": hours,
                "task": (
                f"Practice {topic_info['topic']} problems, "
                "review solutions, and record mistakes."
        )
    })

    return daily_plan

if __name__ == "__main__":
    topic_progress = {
        "Arrays": 25,
        "Strings": 18,
        "Trees": 8,
        "Graphs": 0,
        "Dynamic Programming": 3
    }

    plan = generate_weekly_plan(topic_progress, 10)

    print("\n===== WEEKLY CODING PRACTICE PLAN =====\n")

    for item in plan:
        print("Day:", item["day"])
        print("Topic:", item["topic"])
        print("Hours:", item["hours"])
        print("Task:", item["task"])
        print("-" * 40)


def get_recommended_problems(topic):
    """Return coding problems with difficulty and recommendation priority."""

    problems = {
        "Graphs": [
            {
                "name": "Number of Islands",
                "url": "https://leetcode.com/problems/number-of-islands/",
                "difficulty": "Medium",
                "priority": "High"
            },
            {
                "name": "Clone Graph",
                "url": "https://leetcode.com/problems/clone-graph/",
                "difficulty": "Medium",
                "priority": "Medium"
            },
            {
                "name": "Course Schedule",
                "url": "https://leetcode.com/problems/course-schedule/",
                "difficulty": "Medium",
                "priority": "Medium"
            }
        ],
        "Dynamic Programming": [
            {
                "name": "Climbing Stairs",
                "url": "https://leetcode.com/problems/climbing-stairs/",
                "difficulty": "Easy",
                "priority": "High"
            },
            {
                "name": "House Robber",
                "url": "https://leetcode.com/problems/house-robber/",
                "difficulty": "Medium",
                "priority": "Medium"
            },
            {
                "name": "Coin Change",
                "url": "https://leetcode.com/problems/coin-change/",
                "difficulty": "Medium",
                "priority": "Medium"
            }
        ],
        "Trees": [
            {
                "name": "Maximum Depth of Binary Tree",
                "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
                "difficulty": "Easy",
                "priority": "High"
            },
            {
                "name": "Invert Binary Tree",
                "url": "https://leetcode.com/problems/invert-binary-tree/",
                "difficulty": "Easy",
                "priority": "Medium"
            },
            {
                "name": "Binary Tree Level Order Traversal",
                "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
                "difficulty": "Medium",
                "priority": "Medium"
            }
        ],
        "Arrays": [
            {
                "name": "Two Sum",
                "url": "https://leetcode.com/problems/two-sum/",
                "difficulty": "Easy",
                "priority": "High"
            },
            {
                "name": "Best Time to Buy and Sell Stock",
                "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
                "difficulty": "Easy",
                "priority": "Medium"
            },
            {
                "name": "Product of Array Except Self",
                "url": "https://leetcode.com/problems/product-of-array-except-self/",
                "difficulty": "Medium",
                "priority": "Medium"
            }
        ],
        "Strings": [
            {
                "name": "Valid Anagram",
                "url": "https://leetcode.com/problems/valid-anagram/",
                "difficulty": "Easy",
                "priority": "High"
            },
            {
                "name": "Longest Substring Without Repeating Characters",
                "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
                "difficulty": "Medium",
                "priority": "Medium"
            },
            {
                "name": "Longest Palindromic Substring",
                "url": "https://leetcode.com/problems/longest-palindromic-substring/",
                "difficulty": "Medium",
                "priority": "Medium"
            }
        ]
    }

    return problems.get(topic, [])


def count_unique_solved_problems(solved_problems):
    """
    Count unique solved problems across multiple platforms.

    Each problem should be a dictionary containing at least:
    - name: problem name
    - platform: platform name

    If a problem has a URL, the URL is used to identify it
    when possible. Otherwise, its normalized name is used.
    """

    unique_problems = {}

    for problem in solved_problems:
        name = problem.get("name", "").strip()
        url = problem.get("url", "").strip()

        if url:
            # Normalize URLs so trailing slashes do not create duplicates.
            problem_id = url.rstrip("/").lower()
        else:
            # Use the normalized problem name if no URL is available.
            problem_id = name.lower()

        if not problem_id:
            continue

        if problem_id not in unique_problems:
            unique_problems[problem_id] = problem

    return {
        "unique_count": len(unique_problems),
        "duplicate_count": len(solved_problems) - len(unique_problems),
        "unique_problems": list(unique_problems.values())
    }




def generate_weekly_progress_summary(previous_progress, current_progress):
    """Generate an accurate summary by comparing two progress snapshots."""

    if previous_progress is None:
        return {
            "status": "No previous data",
            "message": (
                "This is your first recorded progress snapshot. "
                "Save another snapshot later to compare your progress."
            ),
            "total_problems_solved": sum(current_progress.values()),
            "increased_topics": [],
            "unchanged_topics": [],
            "decreased_topics": []
        }

    all_topics = sorted(set(previous_progress) | set(current_progress))

    increased_topics = []
    unchanged_topics = []
    decreased_topics = []

    for topic in all_topics:
        previous_count = previous_progress.get(topic, 0)
        current_count = current_progress.get(topic, 0)
        change = current_count - previous_count

        topic_result = {
            "topic": topic,
            "previous": previous_count,
            "current": current_count,
            "change": change
        }

        if change > 0:
            increased_topics.append(topic_result)
        elif change < 0:
            decreased_topics.append(topic_result)
        else:
            unchanged_topics.append(topic_result)

    if increased_topics and not decreased_topics:
        status = "Progress increased"
        message = (
            "Your recorded solved-problem counts increased in "
            f"{len(increased_topics)} topic(s). Keep up the practice!"
        )
    elif decreased_topics and not increased_topics:
        status = "Progress decreased"
        message = (
            "Some recorded counts decreased. Check your profile data "
            "and source information before drawing conclusions."
        )
    elif increased_topics and decreased_topics:
        status = "Mixed progress"
        message = (
            "Some topic counts increased while others decreased. "
            "Review the topic-by-topic changes below."
        )
    else:
        status = "No change"
        message = (
            "No change detected since the previous snapshot. "
            "Your recorded solved-problem counts have not increased "
            "or decreased."
        )

    return {
        "status": status,
        "message": message,
        "total_problems_solved": sum(current_progress.values()),
        "increased_topics": increased_topics,
        "unchanged_topics": unchanged_topics,
        "decreased_topics": decreased_topics
    }


def compare_fetched_profiles(previous_profile, current_profile):
    """Compare two successful LeetCode profile retrievals."""

    if not current_profile or not current_profile.get("success"):
        return {
            "available": False,
            "message": "The latest profile retrieval was unsuccessful."
        }

    if not previous_profile:
        return {
            "available": False,
            "message": "No previous profile retrieval is available for comparison."
        }

    if (
            previous_profile.get("username", "").lower()
            != current_profile.get("username", "").lower()
        ):
        return {
            "available": False,
            "message": (
                "The previous and current profiles belong to different "
                "usernames. Progress comparison is not available."
            )
        }

    if not previous_profile.get("success"):
        return {
            "available": False,
            "message": "The previous profile retrieval was unsuccessful."
        }

    previous_counts = previous_profile.get("solved_by_difficulty") or {}
    current_counts = current_profile.get("solved_by_difficulty") or {}

    if "All" not in previous_counts or "All" not in current_counts:
        return {
            "available": False,
            "message": "Total solved counts are missing, so progress cannot be verified."
        }


    metrics = ["All", "Easy", "Medium", "Hard"]
    changes = {}

    for metric in metrics:
        previous_value = previous_counts.get(metric)
        current_value = current_counts.get(metric)

        if (
            not isinstance(previous_value, int)
            or isinstance(previous_value, bool)
            or not isinstance(current_value, int)
            or isinstance(current_value, bool)
            or previous_value < 0
            or current_value < 0
        ):
            return {
                "available": False,
                "message": (
                    f"Invalid or missing {metric} solved count. "
                    "Progress cannot be verified."
                )
            }



    for metric in metrics:
        previous_value = previous_counts.get(metric)
        current_value = current_counts.get(metric)

        if previous_value is None or current_value is None:
            changes[metric] = None
        else:
            changes[metric] = current_value - previous_value

    total_change = changes["All"]

    if total_change is None:
        message = "Total solved counts are unavailable."
    elif total_change > 0:
        message = (
            f"Total solved count increased by {total_change} "
            "since the previous retrieval."
        )
    elif total_change < 0:
        message = (
            f"Total solved count decreased by {abs(total_change)} "
            "since the previous retrieval."
        )
    else:
        message = "No change detected in the total solved count."

    return {
        "available": True,
        "previous_retrieved_at": previous_profile.get("retrieved_at"),
        "current_retrieved_at": current_profile.get("retrieved_at"),
        "changes": changes,
        "message": message
    }


def generate_voice_briefing(
    student_name,
    topic_progress,
    weekly_hours
):
    """
    Generate a written script for the weekly coding progress briefing.
    The script can later be converted into audio.
    """

    

    analysis = analyze_coding_progress(topic_progress)

    weak_topics = analysis.get("weak_topics", [])
    strong_topics = analysis.get("strong_topics", [])

    total_solved = sum(topic_progress.values())

    briefing = f"Hello {student_name}! Welcome to your weekly coding practice briefing. "

    briefing += (
        f"You have solved {total_solved} coding problems across "
        f"{len(topic_progress)} topics. "
    )

    briefing += (
        f"You have {weekly_hours} hours available for coding practice "
        "next week. "
    )

    if weak_topics:
        briefing += "Your priority topics for next week are: "
        weak_topic_names = [
            topic["topic"] if isinstance(topic, dict) else topic
            for topic in weak_topics
        ]

        briefing += ", ".join(weak_topic_names) + ". "
        briefing += (
            "Spend more time strengthening these topics "
            "before moving to more advanced problems. "
        )
    else:
        briefing += (
            "No weak topics were identified from the supplied progress data. "
        )

    if strong_topics:
        briefing += "Your stronger topics are: "
        strong_topic_names = [
            topic["topic"] if isinstance(topic, dict) else topic
            for topic in strong_topics
        ]

        briefing += ", ".join(strong_topic_names) + ". "

    briefing += (
        "Follow your weekly practice plan, review mistakes after each problem, "
        "and track your progress consistently. "
        "Good luck with your coding preparation!"
    )

    return briefing



