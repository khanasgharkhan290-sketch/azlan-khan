# AI Learning Roadmap Generator

A Streamlit application that uses the Groq API and an LLM to create a personalized, actionable learning plan. Enter a learning domain, choose your current level and available duration, set weekly study hours, and optionally add a learning goal.

## Features

- Learning domain input (Python, Data Science, AI, Web Development, and more)
- Beginner, Intermediate, and Advanced levels
- Duration options: 1, 2, 3, or 6 months, or 1 year
- Configurable study hours per week
- Optional learning goal (not required)
- Weekly or monthly phases with topics, objectives, exercises, and milestones
- Resource recommendations, including documentation, tutorials, courses, books, and YouTube channels
- Skills, tools, and technology checklist
- Daily and weekly study routine
- Capstone project and possible career directions
- Download the generated plan as a Markdown (`.md`) file
- API-key handling through environment variables or Streamlit Secrets
- Validation and user-friendly handling for missing keys, authentication failures, rate limits, connection errors, and API errors

## Project structure

Keep these **exactly three files** in the root of your GitHub repository:

```text
ai-learning-roadmap-generator/
├── app.py
├── requirements.txt
└── README.md
```

No additional application files are required.

## Technology stack

- Python 3.10+
- Streamlit — user interface
- Groq Python SDK — API client
- Groq model: `openai/gpt-oss-120b`

The model ID is configured near the top of `app.py`. Check the [Groq supported models page](https://console.groq.com/docs/models) before changing it, because model availability and IDs can change.

## 1. Get a Groq API key

1. Open [Groq Console](https://console.groq.com/).
2. Sign in or create an account.
3. Open the API keys section and create a new key.
4. Copy the key and store it securely. Do not paste it into `app.py`, commit it to GitHub, or share it publicly.

Groq usage limits and pricing depend on your account and model. Review the current information in the Groq Console.

## 2. Run locally

### Prerequisites

Install Python 3.10 or newer. Confirm your installation:

```bash
python --version
```

### Create and activate a virtual environment (recommended)

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

Place `app.py`, `requirements.txt`, and `README.md` in the same folder, then run:

```bash
pip install -r requirements.txt
```

### Configure the API key

macOS/Linux:

```bash
export GROQ_API_KEY="your_real_groq_api_key"
```

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_real_groq_api_key"
```

Replace the example value in your terminal command with your actual key. Do not add the key to source code.

### Start the application

```bash
streamlit run app.py
```

Streamlit will print a local URL, normally `http://localhost:8501`. Open it in your browser.

## 3. Develop in Google Colab

Colab is a notebook environment rather than a permanent web-hosting service. Use it to edit and test the three project files; deploy the finished app to Streamlit Community Cloud for a persistent public URL.

### Step 1 — Create a notebook

1. Visit [Google Colab](https://colab.research.google.com/).
2. Create a new notebook.
3. In the left Files panel, create a folder named `ai-learning-roadmap-generator`, or use `/content` as your working folder.

### Step 2 — Create the three project files

In a Colab cell, create the files by uploading them from your computer or by using the notebook's file-writing interface. The easiest approach is:

1. Download `app.py`, `requirements.txt`, and `README.md` from your project.
2. In Colab, open the Files panel.
3. Upload all three files into the same folder.
4. Change into that folder:

```python
%cd /content/ai-learning-roadmap-generator
```

If you uploaded the files directly to `/content`, use `%cd /content` instead.

### Step 3 — Install dependencies

```python
!pip install -r requirements.txt
!pip install pyngrok
```

`pyngrok` is only used to expose the Colab test server through a temporary tunnel; it is not an application dependency and does not need to be added to `requirements.txt`.

### Step 4 — Set the API key safely in the notebook session

For a quick test, enter the key using a hidden prompt:

```python
import os
from getpass import getpass

os.environ["GROQ_API_KEY"] = getpass("Enter your Groq API key: ")
```

Do not put the real key in a notebook code cell as a literal string, and do not share a notebook containing secrets.

### Step 5 — Start Streamlit and open a tunnel

Run the Streamlit server in the background:

```python
!streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > /content/streamlit.log 2>&1 &
```

Then create a temporary public tunnel:

```python
from pyngrok import ngrok

# If ngrok asks for an account, create one at https://ngrok.com/
# and configure your auth token in this private Colab session:
# ngrok.set_auth_token(getpass("Enter your ngrok auth token: "))

public_url = ngrok.connect(8501, "http")
print("Open your app here:", public_url)
```

If the tunnel service requires an account or token, follow its current setup instructions. The tunnel URL is temporary and should not be treated as production hosting. Stop the tunnel when finished:

```python
ngrok.kill()
```

### Step 6 — Test the app

- Try a domain such as `Python` or `Data Science`.
- Test each skill level and duration.
- Enter different weekly study-hour values.
- Leave the optional learning goal blank and confirm generation still works.
- Enter a goal and confirm it is reflected in the plan.
- Download the Markdown file and open it to verify its content.
- Check the Colab output log if the app does not start:

```python
!tail -n 80 /content/streamlit.log
```

## 4. Upload the project to GitHub

### Create a repository

1. Sign in at [GitHub](https://github.com/).
2. Click **New repository**.
3. Choose a repository name, for example `ai-learning-roadmap-generator`.
4. Choose Public or Private.
5. Do not initialize it with another README if you already have this project's `README.md`.
6. Create the repository.

### Push the three files

Open a terminal in the project folder (or use a Colab cell after uploading the files) and run:

```bash
git init
git add app.py requirements.txt README.md
git commit -m "Add AI learning roadmap generator"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ai-learning-roadmap-generator.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username and adjust the repository name if you chose a different one. GitHub may ask you to authenticate using a browser flow or personal access token; never use your Groq key as a GitHub credential.

If the remote is already configured, do not run `git remote add origin` again. Check it with:

```bash
git remote -v
```

For later changes:

```bash
git add app.py requirements.txt README.md
git commit -m "Improve roadmap generator"
git push
```

## 5. Deploy on Streamlit Community Cloud

1. Push the three files to GitHub.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
3. Select **Create app**.
4. Choose the GitHub repository, branch (`main`), and app entrypoint file (`app.py`).
5. Open **Advanced settings** before deploying.
6. In the **Secrets** field, add:

```toml
GROQ_API_KEY = "your_real_groq_api_key"
```

7. Select a supported Python version (Python 3.11 or 3.12 is a sensible choice).
8. Save and deploy.
9. Wait for the build to finish, then open the generated `*.streamlit.app` URL.

The app reads the key from `st.secrets` on Community Cloud and falls back to the `GROQ_API_KEY` environment variable for local development.

### Update the deployed application

Commit and push code changes to the connected GitHub branch. Community Cloud detects repository updates and redeploys the app. If you change dependencies, update `requirements.txt` and push that change too.

## 6. Troubleshooting

| Message / symptom | What to check |
|---|---|
| Missing Groq API key | Set `GROQ_API_KEY` in your terminal environment or Streamlit Secrets. Restart the app after changing local environment variables. |
| Groq rejected the API key | Confirm the key is active, copied completely, and belongs to your Groq account. |
| Rate limit or quota reached | Wait and retry; check your Groq account usage and limits. |
| Connection error | Check your internet connection, tunnel, firewall, and Groq service status. |
| Model unavailable / bad request | Check the current supported model IDs in Groq documentation and update `MODEL_ID` in `app.py` if needed. |
| Community Cloud build fails | Review app logs and confirm `requirements.txt` is in the repository root alongside `app.py`. |
| App works locally but not in deployment | Confirm the deployed app's Secrets contain the exact `GROQ_API_KEY` key and a valid quoted value. |

## 7. Security and responsible use

- Never commit API keys, passwords, or private credentials.
- Do not place API keys in notebook cells that you intend to share.
- Rotate your Groq key immediately if it is accidentally exposed.
- The app sends the domain, level, duration, weekly hours, and optional goal to Groq. Do not enter confidential or sensitive personal information.
- AI-generated resources, URLs, timelines, and career suggestions may be incomplete or inaccurate. Verify important details and adapt the plan to your needs.
- The application does not guarantee employment or professional certification.

## Useful links

- [Groq Console](https://console.groq.com/)
- [Groq models](https://console.groq.com/docs/models)
- [Groq Python SDK](https://github.com/groq/groq-python)
- [Streamlit documentation](https://docs.streamlit.io/)
- [Streamlit Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Streamlit Community Cloud secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Google Colab](https://colab.research.google.com/)
