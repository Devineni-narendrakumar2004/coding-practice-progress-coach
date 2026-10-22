# Coding Practice Progress Coach

An AI-assisted coding practice coach that helps students analyze their problem-solving progress, identify weak data structures and algorithms topics, and prepare a focused weekly practice plan.

## 🎯 Project Overview

The Coding Practice Progress Coach is a Python-based web application built with Streamlit. It helps students organize their coding practice, monitor progress over time, and focus on topics that need improvement.

The application combines progress analysis, problem recommendations, weekly planning, persistent storage, and voice briefings in one interface.

## ✨ Features

* **Student Profile Management:** Save student details, weekly practice hours, target companies, and coding profile URLs.
* **Coding Progress Analysis:** Review solved-problem counts across Arrays, Strings, Trees, Graphs, and Dynamic Programming.
* **Weak Topic Identification:** Highlight topics that need more practice.
* **Problem Recommendations:** Recommend specific coding problems based on weak topics.
* **Progress Comparison:** Compare saved progress snapshots and identify increases, decreases, or unchanged counts.
* **Weekly Practice Planning:** Generate a seven-day plan based on topic priorities and available practice hours.
* **Human Approval:** Allow students to review and approve a weekly plan before saving it.
* **Duplicate Approval Prevention:** Prevent an identical weekly plan from being saved repeatedly.
* **Solved Problem Tracking:** Store solved problems and identify duplicates across coding platforms.
* **Profile Retrieval:** Attempt to retrieve publicly accessible LeetCode profile information, with safe handling of inaccessible profiles.
* **Source Evidence:** Store source URLs and retrieval timestamps for traceability.
* **Voice Briefing:** Generate a written progress briefing, play its audio, and download the audio file.
* **SQLite Persistence:** Store student profiles, progress history, approved plans, source evidence, and solved problems in a local database.

## 🛠️ Technology Stack

* Python 3.11
* Streamlit
* SQLite
* Pandas
* Requests
* Python text-to-speech/audio functionality

## 📁 Project Structure

```text
project1/
├── app.py
├── analyzer.py
├── database.py
├── profile_fetcher.py
├── main.py
├── coding_coach.db
├── README.md
└── .venv/
```

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.11 or a compatible Python version
* Visual Studio Code (recommended)

### 1. Open the project folder

Open the `project1` folder in Visual Studio Code.

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the project dependencies have not already been installed, run:

```powershell
python -m pip install streamlit pandas requests pyttsx3
```

### 4. Run the application

From the project directory, run:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## 🚀 How to Use

1. Create or load a student profile.
2. Enter or review the solved-problem counts for the supported topics.
3. Analyze coding progress and identify weak topics.
4. Review recommended coding problems and their links.
5. Compare current progress with previous snapshots.
6. Review the generated seven-day practice plan.
7. Approve the plan to save it.
8. Generate and listen to the voice briefing.
9. Track solved problems and review source evidence.

## 🧪 Testing and Verification

The following behaviors have been tested during development:

| Test                                 | Expected behavior                                                      | Observed result                         |
| ------------------------------------ | ---------------------------------------------------------------------- | --------------------------------------- |
| Weak-topic identification            | Topics with very low solved counts receive high priority.              | Verified                                |
| Problem recommendations              | Relevant coding problems are displayed with working links.             | Verified                                |
| Unchanged progress                   | Unchanged counts are not reported as improvement.                      | Verified                                |
| Weekly plan approval                 | An approved plan is saved and can be displayed later.                  | Verified                                |
| Duplicate approval prevention        | An identical plan is not saved repeatedly.                             | Verified                                |
| Cross-platform problem deduplication | Matching problem names are counted once in the unique-problem summary. | Verified                                |
| Voice briefing                       | Written briefing and audio playback/download work.                     | Verified                                |
| Python syntax                        | Project Python files compile without syntax errors.                    | Verified                                |
| Inaccessible profile handling        | Unverified profile data is not guessed.                                | Verified using an inaccessible test URL |

## ⚠️ Current Limitations

* Topic-progress values may be manually entered or sample data; they should not be represented as verified live profile statistics unless independently retrieved and confirmed.
* Public profile retrieval currently supports limited LeetCode profile statistics.
* Individual solved-problem retrieval from LeetCode is not fully implemented.
* Private profiles and inaccessible pages may require a user-provided export.
* Problem recommendations are based on curated lists and topic priorities.
* The application currently uses a local SQLite database.

## 🔐 Privacy and Responsible Use

* Use publicly accessible profile information only.
* Do not attempt to bypass login protections, OTP verification, CAPTCHA, or access controls.
* Ask users to provide an export when a profile cannot be accessed.
* Require human approval before saving a weekly practice plan.
* Clearly distinguish sample data from verified profile data.

## 🔮 Future Improvements

* Integrate additional public coding platforms.
* Improve automatic retrieval of individual solved problems.
* Add more comprehensive topic mapping.
* Introduce configurable target-company topic distributions.
* Improve recommendation personalization.
* Add downloadable weekly plan reports.
* Enhance voice briefing quality and accessibility.
* Deploy the application to a hosted environment.

## 🏁 Conclusion

The Coding Practice Progress Coach provides a structured way for students to understand their coding practice, identify areas for improvement, and follow a focused weekly plan. It combines progress tracking, personalized recommendations, persistent storage, human approval, and voice briefings in a single application.
