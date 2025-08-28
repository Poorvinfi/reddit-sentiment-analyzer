Reddit Sentiment Analysis Dashboard
Project Overview
This project is a real-time sentiment analysis dashboard for Reddit. It allows users to scrape posts and comments for a given keyword and visualize the overall public sentiment. The application demonstrates skills in data engineering, web scraping, and natural language processing (NLP).

Features
Real-time Scraping: Fetches data from Reddit's API based on a user-defined keyword, subreddit, and post limit.

Sentiment Analysis: Uses the VADER (Valence Aware Dictionary and sEntiment Reasoner) model for fast and effective sentiment scoring.

Interactive Dashboard: Provides a clean and interactive Streamlit front-end with visualizations (bar charts) and key metrics for positive, negative, and neutral sentiment.

Secure Deployment: The application is built for deployment on Streamlit Cloud, with sensitive API credentials securely managed using Streamlit's secrets management.

Business Insights & Findings
This dashboard can be used to monitor brand reputation, track public opinion on a new product, or analyze trending topics. For example, a company can:

Track a product launch by analyzing real-time sentiment in a relevant subreddit.

Identify pain points by searching for a competitor's name and finding negative sentiment.

Measure public reception to a political or social issue.

Technologies Used
Python: The core programming language.

Streamlit: For building the interactive web application.

PRAW (Python Reddit API Wrapper): For scraping data from the Reddit API.

VADER Sentiment: A lexicon- and rule-based sentiment analysis model for scoring text.

NLTK (Natural Language Toolkit): For basic text preprocessing.

Pandas: For data manipulation and analysis.

How to Run the Project Locally
Clone the repository:

Bash

git clone https://github.com/Poorvinfi/reddit-sentiment-analyzer.git
cd reddit-sentiment-analyzer
Create and activate a virtual environment:

Bash

python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
Set up Reddit API credentials:

Go to https://www.reddit.com/prefs/apps to create a new script app.

Create a folder named .streamlit in your project's root directory.

Inside that folder, create a file named secrets.toml and add your credentials:

Ini, TOML

[reddit]
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
user_agent = "YOUR_USER_AGENT"
Run the Streamlit app:

Bash

streamlit run app.py
Live Demo
You can interact with the live application deployed on Streamlit Cloud here:

https://reddit-sentiment-analyzer-13.streamlit.app/
