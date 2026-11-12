 
"""AI Learning Roadmap Generator — Streamlit + Groq."""
import os
import re
from datetime import datetime

import streamlit as st
from groq import (
    Groq,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APIStatusError,
    BadRequestError,
)

MODEL_ID = "openai/gpt-oss-120b"

DURATIONS = {
    "1 month": 4,
    "2 months": 8,
    "3 months": 12,
    "6 months": 26,
    "1 year": 52,
}


def get_api_key():
    """Read API key from Streamlit Secrets or environment."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GROQ_API_KEY", "")


def create_prompt(domain, level, duration, hours_per_week, learning_goal):
    weeks = DURATIONS[duration]

    goal = learning_goal.strip() or (
        "No extra goal supplied. Create a balanced learning path."
    )

    return f"""
Create a personalized and realistic learning roadmap.

LEARNER PROFILE
- Domain: {domain}
- Current level: {level}
- Available duration: {duration} (approximately {weeks} weeks)
- Study time: {hours_per_week} hours per week
- Learning goal: {goal}

REQUIREMENTS

1. Return properly formatted Markdown.
2. Start with an overview and expected outcomes.
3. Divide the roadmap into weekly phases for 1–3 months
   and monthly phases for 6 months or 1 year.
4. Include learning objectives and specific topics in every phase.
5. Include practical exercises and mini-projects.
6. Recommend official documentation, tutorials, courses,
   books, and YouTube channels.
7. Do not invent resource URLs.
8. Identify important skills, tools, and technologies.
9. Provide a daily and weekly study routine.
10. Include measurable milestones and progress tracking.
11. Suggest a final capstone project with evaluation criteria.
12. Recommend possible career opportunities.
13. Adjust the difficulty to the selected skill level.
14. Keep the workload realistic for the available hours.
15. End with advice for maintaining consistency.

Use clear headings, bullet points, and tables.
Make the roadmap specific and actionable.
"""


def generate_roadmap(
    domain,
    level,
    duration,
    hours_per_week,
    learning_goal,
):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "Groq API key is missing. Configure GROQ_API_KEY "
            "in environment variables or Streamlit Secrets."
        )

    client = Groq(
        api_key=api_key,
        timeout=90.0,
        max_retries=2,
    )

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert learning designer. "
                    "Create realistic learning roadmaps and "
                    "never fabricate resource URLs."
                ),
            },
            {
                "role": "user",
                "content": create_prompt(
                    domain,
                    level,
                    duration,
                    hours_per_week,
                    learning_goal,
                ),
            },
        ],
        temperature=0.55,
        max_tokens=6000,
    )

    answer = response.choices[0].message.content

    if not answer or not answer.strip():
        raise RuntimeError(
            "The AI returned an empty response. Please try again."
        )

    return answer.strip()


def make_markdown(roadmap, details):
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    goal = details["learning_goal"].strip() or "Not specified"

    header = f"""# Learning Roadmap: {details["domain"]}

- **Current level:** {details["level"]}
- **Duration:** {details["duration"]}
- **Study time:** {details["hours_per_week"]} hours/week
- **Learning goal:** {goal}
- **Generated:** {generated}

---

"""

    return header + roadmap + "\n"


# -------------------- STREAMLIT CONFIGURATION --------------------

st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            135deg,
            #f7f9ff 0%,
            #eef4ff 100%
        );
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem;
        border-radius: 20px;
        color: white;
        background: linear-gradient(
            115deg,
            #243b80,
            #4267c7 60%,
            #6288e8
        );
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white;
        margin-bottom: .4rem;
    }

    .hero p {
        color: #edf2ff;
        margin-bottom: 0;
    }

    div[data-testid="stForm"] {
        background: white;
        padding: 1.2rem;
        border: 1px solid #e6eaf2;
        border-radius: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🧭 AI Learning Roadmap Generator</h1>
        <p>
        Build a practical learning plan tailored to your
        goals, level, and schedule.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.header("About this app")

    st.write(f"**Groq model:** `{MODEL_ID}`")

    st.write(
        "Your learning preferences are sent to Groq "
        "to generate your personalized roadmap."
    )

    st.divider()

    st.caption(
        "Configure GROQ_API_KEY in your environment "
        "or Streamlit Community Cloud Secrets."
    )


# -------------------- USER INPUT FORM --------------------

st.subheader("Your Learning Preferences")

st.write(
    "Fields marked * are required. "
    "The learning goal is optional."
)

with st.form("roadmap_input_form"):

    domain = st.text_input(
        "Learning Domain *",
        placeholder="e.g. Python, Data Science, AI",
        max_chars=100,
    )

    left, right = st.columns(2)

    with left:

        level = st.selectbox(
            "Current Skill Level *",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )

        duration = st.selectbox(
            "Available Learning Time *",
            list(DURATIONS.keys()),
            index=2,
        )

    with right:

        hours_per_week = st.number_input(
            "Study Hours Per Week *",
            min_value=1,
            max_value=80,
            value=8,
            step=1,
        )

        learning_goal = st.text_input(
            "Learning Goal (Optional)",
            placeholder="e.g. Build a portfolio project",
            max_chars=250,
        )

    submitted = st.form_submit_button(
        "✨ Generate My Learning Roadmap",
        type="primary",
        use_container_width=True,
    )


# -------------------- GENERATE ROADMAP --------------------

if submitted:

    clean_domain = domain.strip()

    if len(clean_domain) < 2:

        st.error(
            "Please enter a learning domain "
            "with at least 2 characters."
        )

    elif re.search(r"[\x00-\x1f]", clean_domain):

        st.error(
            "The learning domain contains unsupported characters."
        )

    else:

        with st.spinner(
            "Creating your personalized learning roadmap..."
        ):

            try:

                result = generate_roadmap(
                    clean_domain,
                    level,
                    duration,
                    int(hours_per_week),
                    learning_goal,
                )

                st.session_state["roadmap"] = result

                st.session_state["roadmap_details"] = {
                    "domain": clean_domain,
                    "level": level,
                    "duration": duration,
                    "hours_per_week": int(hours_per_week),
                    "learning_goal": learning_goal,
                }

                st.success(
                    "Your roadmap has been generated!"
                )

            except ValueError as exc:

                st.error(str(exc))

            except AuthenticationError:

                st.error(
                    "Groq rejected the API key. "
                    "Check that your API key is correct and active."
                )

            except RateLimitError:

                st.warning(
                    "Groq rate limit or quota reached. "
                    "Wait and try again."
                )

            except APIConnectionError:

                st.error(
                    "Could not connect to Groq. "
                    "Check your internet connection."
                )

            except BadRequestError as exc:

                st.error(
                    "Groq rejected the request. "
                    f"Check model availability. Details: {exc}"
                )

            except APIStatusError as exc:

                st.error(
                    f"Groq returned HTTP {exc.status_code}. "
                    "Please try again later."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# -------------------- DISPLAY ROADMAP --------------------

if st.session_state.get("roadmap"):

    details = st.session_state["roadmap_details"]

    st.divider()

    st.subheader("📚 Your Personalized Learning Roadmap")

    st.caption(
        f'{details["domain"]} · '
        f'{details["level"]} · '
        f'{details["duration"]} · '
        f'{details["hours_per_week"]} hours/week'
    )

    st.markdown(
        st.session_state["roadmap"]
    )

    markdown_file = make_markdown(
        st.session_state["roadmap"],
        details,
    )

    safe_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        details["domain"],
    ).strip("_")

    st.download_button(
        "⬇️ Download Roadmap (Markdown)",
        data=markdown_file,
        file_name=f"{safe_name or 'learning'}_roadmap.md",
        mime="text/markdown",
        use_container_width=True,
    )

else:

    st.info(
        "Complete the form above to generate your "
        "personalized learning roadmap."
    )


# -------------------- FOOTER --------------------

st.divider()

st.caption(
    "AI-generated recommendations may need verification. "
    "Check resource links and adapt the suggested workload "
    "to your circumstances."
)
