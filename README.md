 
# AI Learning Roadmap Generator

An AI-powered learning roadmap application built using Python, Streamlit, and Groq API.

## Features

- Enter any learning domain.
- Select Beginner, Intermediate, or Advanced.
- Choose learning duration.
- Specify weekly study hours.
- Optional learning goal.
- Generate personalized learning roadmaps.
- Weekly and monthly learning phases.
- Learning topics and practical projects.
- Recommended learning resources.
- Skills and technologies checklist.
- Daily and weekly study schedules.
- Learning milestones.
- Final capstone project.
- Career opportunities.
- Download roadmap as Markdown.

## Project Structure

ai-learning-roadmap-generator/

    app.py
    requirements.txt
    README.md

## Requirements

- Python 3.10 or newer
- Groq API key
- Internet connection

## 1. Obtain Groq API Key

1. Visit https://console.groq.com/
2. Create an account or sign in.
3. Navigate to API Keys.
4. Generate a new API key.
5. Copy and securely store the key.

Never upload your API key to GitHub.

## 2. Install Dependencies

Open your terminal in the project folder.

Run:

    pip install -r requirements.txt

## 3. Configure API Key

For Windows PowerShell:

    $env:GROQ_API_KEY="your_actual_api_key"

For macOS/Linux:

    export GROQ_API_KEY="your_actual_api_key"

## 4. Run the Application

Execute:

    streamlit run app.py

Open:

    http://localhost:8501

## 5. Google Colab Development

1. Open https://colab.research.google.com/
2. Create a new notebook.
3. Upload app.py, requirements.txt, and README.md.
4. Install dependencies:

    !pip install -r requirements.txt

5. Configure the API key:

    import os
    from getpass import getpass

    os.environ["GROQ_API_KEY"] = getpass("Enter Groq API Key: ")

6. Install ngrok:

    !pip install pyngrok

7. Start Streamlit:

    !streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > /content/streamlit.log 2>&1 &

8. Create a temporary tunnel:

    from pyngrok import ngrok

    url = ngrok.connect(8501, "http")
    print(url)

Follow ngrok's current instructions if authentication is required.

## 6. Upload to GitHub

1. Open https://github.com/
2. Create a new repository.
3. Name it ai-learning-roadmap-generator.
4. Upload the three project files.

Alternatively, use Git:

    git init
    git add app.py requirements.txt README.md
    git commit -m "Initial project upload"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/ai-learning-roadmap-generator.git
    git push -u origin main

Replace YOUR_USERNAME with your GitHub username.

## 7. Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Sign in with GitHub.
3. Click Create App.
4. Select your repository.
5. Select main as the branch.
6. Set the main file path to app.py.
7. Open Advanced Settings.
8. Add your Groq API key under Secrets.

Use this format:

    GROQ_API_KEY = "your_actual_groq_api_key"

9. Click Deploy.

Your application will receive a public Streamlit URL.

## 8. Troubleshooting

### Missing API Key

Check that GROQ_API_KEY is configured correctly.

### Invalid API Key

Generate a new key from Groq Console.

### Rate Limit Error

Wait and retry or check your Groq account usage.

### Connection Error

Check your internet connection.

### Model Error

Check current supported models:

https://console.groq.com/docs/models

## 9. Security

- Never upload API keys to GitHub.
- Use Streamlit Secrets for deployment.
- Do not share private credentials.
- Verify AI-generated learning resources.

## Technologies

- Python
- Streamlit
- Groq API
- Google Colab
- GitHub
- Streamlit Community Cloud

## Author

AI Learning Roadmap Generator Project
