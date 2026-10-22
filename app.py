
import streamlit as st
import pandas as pd

from profile_fetcher import fetch_leetcode_profile

from database import (
    initialize_database,
    save_student_profile,
    get_latest_student_profile,
    save_topic_progress,
    get_latest_topic_progress,
    get_previous_topic_progress,
    save_source_evidence,
    get_source_evidence,
    save_fetched_profile,
    get_latest_fetched_profile,
    get_previous_fetched_profile,
    save_approved_weekly_plan,
    get_approved_weekly_plans,
    save_solved_problems,
    get_unique_solved_problems
)

from analyzer import (
    analyze_coding_progress,
    generate_weekly_plan,
    get_recommended_problems,
    generate_weekly_progress_summary,
    compare_fetched_profiles,
    generate_voice_briefing
)

initialize_database()
# Page configuration
st.set_page_config(
    page_title="Coding Practice Progress Coach",
    page_icon="🎯",
    layout="wide"
)

# Application title
st.title("🎯 Coding Practice Progress Coach")

st.write(
    "Your personal AI coach for coding practice, "
    "weak-topic identification, and weekly learning plans."
)

st.divider()

# Student information
st.header("👤 Student Profile")

with st.form("student_profile"):
    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    leetcode_profile = st.text_input(
        "Public LeetCode Profile URL",
        placeholder="https://leetcode.com/u/yourusername/"
    )

    other_profiles = st.text_input(
        "Other Coding Profile URLs (optional)",
        placeholder="Enter other public profile URLs"
    )

    target_companies = st.multiselect(
        "Target Companies",
        [
            "Google",
            "Microsoft",
            "Amazon",
            "Meta",
            "Apple",
            "Other"
        ]
    )

    weekly_hours = st.number_input(
        "Available Practice Hours Per Week",
        min_value=1,
        max_value=80,
        value=10,
        step=1
    )

    submitted = st.form_submit_button(
        "Save Profile"
    )

if submitted:
    if not student_name.strip():
        st.error("Please enter your name.")

    elif not leetcode_profile.strip() and not other_profiles.strip():
        st.error(
            "Please provide at least one coding profile URL."
        )

    else:
        profile = {
            "name": student_name.strip(),
            "leetcode_profile": leetcode_profile.strip(),
            "other_profiles": other_profiles.strip(),
            "target_companies": target_companies,
            "weekly_hours": weekly_hours
        }

        save_student_profile(profile)

        st.session_state["saved_student_profile"] = profile

        st.success(
            "Profile saved successfully to the database!"
        )

# Display saved profile
if "saved_student_profile" not in st.session_state:
    saved_profile = get_latest_student_profile()

    if saved_profile is not None:
        st.session_state["saved_student_profile"] = saved_profile

if "saved_student_profile" in st.session_state:
    profile = st.session_state["saved_student_profile"]
    

    st.divider()
    st.header("📋 Your Saved Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Weekly Practice Hours", profile["weekly_hours"])

    with col2:
        st.metric(
            "Target Companies",
            len(profile["target_companies"])
        )

    with col3:
        st.metric(
            "Profile URLs Provided",
            int(bool(profile["leetcode_profile"]))
            + int(bool(profile["other_profiles"]))
        )

    st.write("**Student:**", profile["name"])

    st.write(
        "**Target companies:**",
        ", ".join(profile["target_companies"])
        if profile["target_companies"]
        else "None selected"
    )

    st.success(
         "Your profile is saved in the database and "
         "will remain available after restarting the application."
    )

st.divider()

st.caption(
    "Project1 | Agentic AI Hackathon 2026 | "
    "Education & Career AI"
)

# ==========================================
# CODING PRACTICE ANALYSIS
# ==========================================

st.divider()

st.header("📊 Coding Practice Analysis")

st.write(
    "Analyze coding practice progress and identify "
    "topics that need more attention."
)

# Load the latest saved coding progress
saved_profile = (
    st.session_state.get("saved_student_profile")
    or get_latest_student_profile()
)

saved_progress = None

if saved_profile is not None:
    saved_progress = get_latest_topic_progress(saved_profile["name"])

if saved_progress is not None:
    default_progress = saved_progress["topics"]
else:
    default_progress = {
        "Arrays": 25,
        "Strings": 18,
        "Trees": 8,
        "Graphs": 0,
        "Dynamic Programming": 3
    }

# Student coding practice data

st.subheader("📝 Enter Your Coding Practice Progress")

st.write(
    "Enter the number of problems you have solved "
    "in each topic."
)

topic_names = [
    "Arrays",
    "Strings",
    "Trees",
    "Graphs",
    "Dynamic Programming"
]

topic_progress = {}

col1, col2 = st.columns(2)

for index, topic in enumerate(topic_names):

    with col1 if index % 2 == 0 else col2:

        topic_progress[topic] = st.number_input(
            f"{topic} problems solved",
            min_value=0,
            max_value=10000,
            value=default_progress.get(topic, 0),
            step=1,
            key=f"progress_{topic}"
        )
# Save coding progress to the database
saved_profile = (
    st.session_state.get("saved_student_profile")
    or get_latest_student_profile()
)

if saved_profile is None:
    st.warning("Please save a student profile before saving coding progress.")
else:
    if st.button("💾 Save Coding Progress to Database"):
        snapshot_id = save_topic_progress(
            saved_profile["name"],
            topic_progress
        )

        st.success(
            f"Coding progress saved successfully! Record ID: {snapshot_id}"
        )
# Analyze coding progress
analysis = analyze_coding_progress(topic_progress)
st.subheader("📊 Problems Solved by Topic")

chart_data = pd.DataFrame({
    "Topic": list(topic_progress.keys()),
    "Problems Solved": list(topic_progress.values())
})

st.bar_chart(
    chart_data,
    x="Topic",
    y="Problems Solved",
    use_container_width=True
)
st.subheader("📈 Progress Comparison")

if saved_profile is None:
    st.info("Save a student profile to compare your progress.")

else:
    current_progress = get_latest_topic_progress(
        saved_profile["name"]
    )

    previous_progress = get_previous_topic_progress(
        saved_profile["name"]
    )

    if current_progress is None:
        st.info(
            "Save your coding progress to start tracking changes."
        )

    elif previous_progress is None:
        st.info(
            "Your first progress snapshot is saved. "
            "Save another snapshot later to compare progress."
        )

    else:
        previous_topics = previous_progress["topics"]
        current_topics = current_progress["topics"]

        comparison_data = []

        all_topics = sorted(
            set(previous_topics) | set(current_topics)
        )

        for topic in all_topics:
            previous_count = previous_topics.get(topic, 0)
            current_count = current_topics.get(topic, 0)
            change = current_count - previous_count

            if change > 0:
                status = f"+{change} 🟢"
            elif change < 0:
                status = f"{change} 🔴"
            else:
                status = "0 ⚪"

            comparison_data.append({
                "Topic": topic,
                "Previous Problems": previous_count,
                "Current Problems": current_count,
                "Change": status
            })

        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )

        if all(
            current_topics.get(topic, 0)
            == previous_topics.get(topic, 0)
            for topic in all_topics
        ):
            st.info(
                "No change detected since the previous snapshot. "
                "Your progress has not increased or decreased."
            )
        else:
            st.success(
                "Progress comparison completed successfully!"
            )

        st.caption(
            f"Previous snapshot: {previous_progress['recorded_at']} | "
            f"Current snapshot: {current_progress['recorded_at']}"
        )

# ==========================================
# WEEKLY PROGRESS INSIGHTS
# ==========================================

st.divider()
st.subheader("📊 Weekly Progress Insights")

if saved_profile is None:
    st.info("Save a student profile to view weekly insights.")

else:
    latest_snapshot = get_latest_topic_progress(
        saved_profile["name"]
    )

    previous_snapshot = get_previous_topic_progress(
        saved_profile["name"]
    )

    if latest_snapshot is None:
        st.info(
            "Save your coding progress to start generating insights."
        )

    else:
        current_counts = latest_snapshot["topics"]

        previous_counts = (
            previous_snapshot["topics"]
            if previous_snapshot is not None
            else None
        )

        weekly_summary = generate_weekly_progress_summary(
            previous_counts,
            current_counts
        )

        st.metric(
            "Total Problems in Latest Snapshot",
            weekly_summary["total_problems_solved"]
        )

        if weekly_summary["status"] == "Progress increased":
            st.success(weekly_summary["message"])

        elif weekly_summary["status"] == "No change":
            st.info(weekly_summary["message"])

        elif weekly_summary["status"] == "Mixed progress":
            st.warning(weekly_summary["message"])

        elif weekly_summary["status"] == "Progress decreased":
            st.warning(weekly_summary["message"])

        else:
            st.info(weekly_summary["message"])

        if weekly_summary["increased_topics"]:
            st.write("**📈 Topics with increased counts**")

            for item in weekly_summary["increased_topics"]:
                st.write(
                    f"- {item['topic']}: "
                    f"{item['previous']} → {item['current']} "
                    f"(+{item['change']})"
                )

        if weekly_summary["unchanged_topics"]:
            st.write("**➡️ Topics with unchanged counts**")

            unchanged_lines = [
                f"- {item['topic']}: "
                f"{item['previous']} → {item['current']}"
                for item in weekly_summary["unchanged_topics"]
            ]
            st.markdown("\n".join(unchanged_lines))
            

    if weekly_summary["decreased_topics"]:
            st.write("**📉 Topics with decreased counts**")

            for item in weekly_summary["decreased_topics"]:
                st.write(
                    f"- {item['topic']}: "
                    f"{item['previous']} → {item['current']} "
                    f"({item['change']})"
                )

# Display summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Topics Tracked",
        analysis["total_topics"]
    )

with col2:
    st.metric(
        "Problems Solved",
        analysis["total_problems_solved"]
    )

with col3:
    st.metric(
        "Topics Needing Practice",
        len(analysis["weak_topics"])
    )

# Display weak topics
st.subheader("🎯 Topics to Improve")

if analysis["weak_topics"]:

    for topic in analysis["weak_topics"]:

        st.warning(
            f'**{topic["topic"]}** — '
            f'{topic["solved"]} problems solved | '
            f'Priority: {topic["priority"]}\n\n'
            f'{topic["reason"]}'
        )

else:
    st.success(
        "No weak topics identified in the current analysis."
    )

# Display strong topics
st.subheader("💪 Strong Topics")

if analysis["strong_topics"]:

    for topic in analysis["strong_topics"]:

        st.success(
            f'**{topic["topic"]}** — '
            f'{topic["solved"]} problems solved'
        )

else:
    st.info(
        "More practice data is needed to identify strong topics."
    )

# Weekly practice recommendations
st.subheader("📅 Recommended Focus for Next Week")

if analysis["weak_topics"]:

    for topic in analysis["weak_topics"][:3]:

        st.write(
            f'- Practise **{topic["topic"]}** '
            f'({topic["priority"]} priority).'
        )

else:
    st.write(
        "Continue practising a balanced mix of coding topics."
    )

# ==========================================

# WEEKLY CODING PRACTICE PLAN

# ==========================================

st.divider()
st.header("🗓️ Your Weekly Coding Practice Plan")

st.write(
"A personalized seven-day plan based on your coding progress "
"and available weekly practice hours."
)


# Get the saved student profile
saved_profile = (
    st.session_state.get("saved_student_profile")
    or get_latest_student_profile()
)

if saved_profile is None:
    st.warning("Please save a student profile first.")

else:
    weekly_hours = saved_profile["weekly_hours"]

    # Generate the weekly plan
    weekly_plan = generate_weekly_plan(
        topic_progress,
        weekly_hours
    )

    st.subheader(
        f"🎯 Your plan for {weekly_hours} hours per week"
    )

    
    st.info(
        "Review your weekly practice plan below. "
        "You can approve and save it after reviewing the recommendations."
    )

    if st.button("✅ Approve & Save Weekly Plan"):
        approval_result = save_approved_weekly_plan(
            saved_profile["name"],
            weekly_plan
        )

        if approval_result["success"]:
            st.success(approval_result["message"])
        else:
            st.warning(approval_result["message"])



    # Display the weekly plan with recommended problems
    for item in weekly_plan:
        with st.expander(
            f"📅 {item['day']} — {item['topic']}"
        ):
            st.write(f"**Topic:** {item['topic']}")
            st.write(f"**Practice time:** {item['hours']} hours")
            st.write(f"**Recommended task:** {item['task']}")

            problems = get_recommended_problems(item["topic"])

            st.write("**Recommended coding problems:**")

            if problems:
                for problem in problems:
                    st.markdown(
                        f"- [{problem['name']}]({problem['url']})"
                        f" — **Difficulty:** {problem['difficulty']}"
                        f" | **Priority:** {problem['priority']}"
                    )
            else:
                st.info(
                    "No recommended problems available for this topic yet."
                )

    # Download the weekly plan
    st.divider()
    st.subheader("📥 Download Your Weekly Plan")

    download_data = []

    for item in weekly_plan:
        problems = get_recommended_problems(item["topic"])

        problem_names = ", ".join(
            problem["name"] for problem in problems
        )

        problem_links = ", ".join(
            problem["url"] for problem in problems
        )

        download_data.append({
            "Day": item["day"],
            "Topic": item["topic"],
            "Practice Hours": item["hours"],
            "Recommended Task": item["task"],
            "Recommended Problems": problem_names,
            "Problem Links": problem_links,
            "Problem Difficulties": ", ".join(
                problem["difficulty"] for problem in problems
            ),
            "Problem Priorities": ", ".join(
                problem["priority"] for problem in problems
            )
        })

    weekly_plan_df = pd.DataFrame(download_data)

    csv_data = weekly_plan_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Weekly Plan (CSV)",
        data=csv_data,
        file_name="weekly_coding_practice_plan.csv",
        mime="text/csv"
    )



st.divider()

st.header("🔎 Source Evidence")

if saved_profile is not None:
    student_name = saved_profile["name"]

    st.write(
        "Record and review the sources used for coding progress "
        "and recommended problems."
    )

    with st.form("source_evidence_form"):
        source_type = st.selectbox(
            "Source Type",
            [
                "Public Coding Profile",
                "Problem List",
                "Other"
            ]
        )

        source_url = st.text_input(
            "Source URL",
            placeholder="https://example.com/profile"
        )

        notes = st.text_area(
            "Notes",
            placeholder="Describe what this source is intended to support."
        )

        evidence_submitted = st.form_submit_button(
            "Save Source Evidence"
        )

    if evidence_submitted:
        if source_url.strip().startswith(("https://", "http://")):
            save_source_evidence(
                student_name,
                source_type,
                source_url.strip(),
                notes.strip()
            )
            st.success("Source evidence record saved successfully!")
        else:
            st.error("Please enter a valid HTTP or HTTPS URL.")

    evidence_records = get_source_evidence(student_name)

    if evidence_records:
        st.subheader("Saved Evidence Records")

        evidence_df = pd.DataFrame(evidence_records)

        st.dataframe(
            evidence_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No source evidence has been recorded yet.")

else:
    st.info("Save a student profile before adding source evidence.")


st.divider()

st.header("🌐 Public LeetCode Profile")

if saved_profile is not None:
    saved_fetched_profile = get_latest_fetched_profile(
        saved_profile["name"]
    )

    previous_fetched_profile = get_previous_fetched_profile(
        saved_profile["name"]
    )
else:
    saved_fetched_profile = None
    previous_fetched_profile = None

if saved_fetched_profile is not None:
    st.subheader("📁 Latest Saved LeetCode Profile")

    if saved_fetched_profile["success"]:
        st.success("Previously fetched profile loaded from the database.")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Saved Username",
                saved_fetched_profile["username"] or "Unavailable"
            )

        with col2:
            ranking = saved_fetched_profile["ranking"]
            st.metric(
                "Saved Ranking",
                ranking if ranking is not None else "Unavailable"
            )

        st.write("**Source URL:**", saved_fetched_profile["source_url"])
        st.write(
            "**Retrieved at (UTC):**",
            saved_fetched_profile["retrieved_at"] or "Unavailable"
        )

        st.write("**Problems Solved by Difficulty**")

        saved_counts = saved_fetched_profile["solved_by_difficulty"]

        if saved_counts:
            saved_df = pd.DataFrame(
                list(saved_counts.items()),
                columns=["Difficulty", "Solved Problems"]
            )
            st.dataframe(
                saved_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No solved-problem counts were saved.")
    else:
        st.warning(
            "The latest saved retrieval was unsuccessful: "
            + saved_fetched_profile["message"]
        )
else:
    st.info("No previously fetched LeetCode profile is saved for this student.")


st.write(
    "Retrieve publicly accessible profile information from LeetCode. "
    "This first version retrieves overall solved counts by difficulty, "
    "not topic-specific counts."
)

profile_url = st.text_input(
    "Enter a LeetCode Profile URL",
    placeholder="https://leetcode.com/u/username/",
    key="profile_fetch_url"
)


if st.button("🔍 Fetch Profile", key="fetch_leetcode_profile"):
    if not profile_url.strip():
        st.warning("Please enter a LeetCode profile URL.")
    else:
        with st.spinner("Retrieving public profile information..."):
            result = fetch_leetcode_profile(profile_url.strip())
            
        st.session_state["last_fetched_profile"] = result

        save_fetched_profile(
            saved_profile["name"] if saved_profile else "Unknown",
            result
        )


        save_source_evidence(
            saved_profile["name"] if saved_profile else "Unknown",
            "Public Coding Profile",
            result.get("source_url") or profile_url.strip(),
            (
                f"Success: {result['success']}. "
                f"{result['message']}. "
                f"Retrieved at: {result.get('retrieved_at')}"
            )
        )

        if result["success"]:
            st.success(result["message"])


            st.write("**Source URL:**", result["source_url"])
            st.write("**Retrieved at (UTC):**", result["retrieved_at"])

            profile_data = result["data"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Username",
                    profile_data.get("username") or "Unavailable"
                )

            with col2:
                st.metric(
                    "Ranking",
                    profile_data.get("ranking")
                    if profile_data.get("ranking") is not None
                    else "Unavailable"
                )

            st.subheader("Problems Solved by Difficulty")

            solved_counts = profile_data.get(
                "solved_by_difficulty", {}
            )

            if solved_counts:
                difficulty_df = pd.DataFrame(
                    list(solved_counts.items()),
                    columns=["Difficulty", "Solved Problems"]
                )

                st.dataframe(
                    difficulty_df,
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info("No solved-problem counts were returned.")

            st.info(
                "These are overall difficulty counts. They are not "
                "topic-specific progress data and will not automatically "
                "change your existing topic analysis."
            )

        else:
            st.error(result["message"])


st.divider()
st.subheader("📈 LeetCode Profile Progress Comparison")

if saved_fetched_profile is None:
    st.info("Fetch a LeetCode profile to begin tracking changes.")

elif previous_fetched_profile is None:
    st.info(
        "Only one profile retrieval is saved. "
        "Fetch the same profile again to compare your results."
    )

else:
    comparison = compare_fetched_profiles(
        previous_fetched_profile,
        saved_fetched_profile
    )

    if comparison["available"]:
        st.write(comparison["message"])

        st.caption(
            f"Previous retrieval: "
            f"{comparison.get('previous_retrieved_at') or 'Unavailable'}"
        )
        st.caption(
            f"Latest retrieval: "
            f"{comparison.get('current_retrieved_at') or 'Unavailable'}"
        )

        previous_counts = previous_fetched_profile["solved_by_difficulty"]
        current_counts = saved_fetched_profile["solved_by_difficulty"]

        st.subheader("📊 Solved Problems Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Previous Total Solved",
                previous_counts.get("All", "Unavailable")
            )

        with col2:
            st.metric(
                "Latest Total Solved",
                current_counts.get("All", "Unavailable")
            )

        with col3:
            total_change = comparison["changes"].get("All")
            
            st.metric(
                "Problems Gained/Lost",
                f"{total_change:+d}" if total_change is not None else "Unavailable"
            )

        changes = comparison["changes"]
        columns = st.columns(4)

        for column, metric_name in zip(
            columns, ["All", "Easy", "Medium", "Hard"]
        ):
            change = changes.get(metric_name)

            with column:
                if change is None:
                    st.metric(metric_name, "Unavailable")
                else:
                    st.metric(
                        label=metric_name,
                        value=f"{change:+d}" if change != 0 else "0"
                    )
    else:
        st.warning(comparison["message"])


st.header("✅ Solved Problems Summary")

with st.form("add_solved_problem_form"):
    st.subheader("Add a Solved Problem")

    problem_name = st.text_input("Problem Name")

    platform = st.selectbox(
        "Platform",
        ["LeetCode", "GeeksforGeeks", "HackerRank", "Codeforces", "Other"]
    )

    problem_url = st.text_input("Problem URL")

    submitted = st.form_submit_button("Save Solved Problem")

    if submitted:
        if not saved_profile:
            st.error("Please save a student profile first.")
        elif not problem_name.strip():
            st.error("Please enter a problem name.")
        elif not problem_url.strip():
            st.error("Please enter the problem URL.")
        else:
            save_solved_problems(
                saved_profile["name"],
                [{
                    "name": problem_name.strip(),
                    "platform": platform,
                    "url": problem_url.strip()
                }]
            )

            st.success("Solved problem saved successfully!")
            st.rerun()



if saved_profile:
    student_name = saved_profile["name"]

    solved_summary = get_unique_solved_problems(student_name)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Unique Problems Solved",
            solved_summary["unique_count"]
        )

    with col2:
        st.metric(
            "Duplicate Records",
            solved_summary["duplicate_count"]
        )

    if solved_summary["unique_problems"]:
        solved_df = pd.DataFrame(
            solved_summary["unique_problems"]
        )

        st.dataframe(
            solved_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "No solved problems have been recorded yet. "
            "Solved-problem import will be added in a later step."
        )
else:
    st.info("Save a student profile to view the solved-problems summary.")



st.header("📚 Previously Approved Weekly Plans")

if saved_profile:
    approved_plans = get_approved_weekly_plans(
        saved_profile["name"]
    )

    if approved_plans:
        for plan_record in approved_plans:
            with st.expander(
                f"Approved Plan #{plan_record['id']} — "
                f"{plan_record['approved_at']}"
            ):
                st.write(
                    f"Student: {plan_record['student_name']}"
                )

                st.json(plan_record["plan_data"])
    else:
        st.info("No approved weekly plans found for this student.")
else:
    st.info("Please save a student profile to view approved plans.")



# ==============================
# 🎙️ VOICE BRIEFING
# ==============================

st.header("🎙️ Weekly Voice Briefing")

if saved_profile:
    student_name = saved_profile["name"]

    
    current_progress = get_latest_topic_progress(student_name)

  

    
    if current_progress and current_progress.get("topics"):
        topic_progress = current_progress["topics"]

        weekly_hours = saved_profile["weekly_hours"]

        if st.button("📝 Generate Voice Briefing"):
            briefing = generate_voice_briefing(
                student_name,
                topic_progress,
                weekly_hours
            )

            st.session_state["voice_briefing"] = briefing

        if "voice_briefing" in st.session_state:
            st.subheader("Your Weekly Briefing")
            st.write(st.session_state["voice_briefing"])

        
        
        import os
        import tempfile
        import pyttsx3

        if st.button("🔊 Read Briefing Aloud"):
            audio_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False
                ) as audio_file:
                    audio_path = audio_file.name

                engine = pyttsx3.init()
                engine.save_to_file(
                    st.session_state["voice_briefing"],
                    audio_path
                )
                engine.runAndWait()
                engine.stop()

                with open(audio_path, "rb") as file:
                    audio_bytes = file.read()

                st.audio(audio_bytes, format="audio/wav")
                st.success("Voice briefing is ready to play!")

            except Exception as error:
                st.error(f"Voice playback failed: {error}")

            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)

        if st.button("🎧 Generate Downloadable Audio"):
            audio_path = None
            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False
                ) as audio_file:
                    audio_path = audio_file.name

                engine = pyttsx3.init()
                engine.save_to_file(
                    st.session_state["voice_briefing"],
                    audio_path
                )
                engine.runAndWait()
                engine.stop()

                with open(audio_path, "rb") as file:
                    audio_bytes = file.read()

                st.audio(audio_bytes, format="audio/wav")

                st.download_button(
                    "⬇️ Download Voice Briefing",
                    data=audio_bytes,
                    file_name="weekly_coding_briefing.wav",
                    mime="audio/wav"
                )

                st.success("Audio generated successfully!")

            except Exception as error:
                st.error(f"Audio generation failed: {error}")

            finally:
                if audio_path and os.path.exists(audio_path):
                    os.remove(audio_path)




            
    else:
        st.info("Please save your coding topic progress first to generate a voice briefing.")





        weekly_hours = saved_profile["weekly_hours"]

        if st.button("📝 Generate Voice Briefing"):
            briefing = generate_voice_briefing(
                student_name,
                topic_progress,
                weekly_hours
            )

            st.session_state["voice_briefing"] = briefing

        if "voice_briefing" in st.session_state:
            st.subheader("Your Weekly Briefing")
            st.write(st.session_state["voice_briefing"])

            if st.button("🔊 Read Briefing Aloud"):
                try:
                    import pyttsx3

                    engine = pyttsx3.init()
                    engine.say(st.session_state["voice_briefing"])
                    engine.runAndWait()
                    engine.stop()

                    st.success(
                        "Voice briefing completed! "
                        "Check your computer's speakers."
                    )

                except Exception as error:
                    st.error(
                        f"Could not play the voice briefing: {error}"
                    )

        else:
            st.info(
                "Please save your coding topic progress first "
                "to generate a voice briefing."
            )

else:
    st.info(
        "Please save a student profile first "
        "to generate a voice briefing."
    )

