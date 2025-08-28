import streamlit as st
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt

# Download NLTK data
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)

# Load API credentials from Streamlit's secrets
try:
    reddit = praw.Reddit(
        client_id=st.secrets["reddit"]["client_id"],
        client_secret=st.secrets["reddit"]["client_secret"],
        user_agent=st.secrets["reddit"]["user_agent"]
    )
except KeyError as e:
    st.error(f"Missing Streamlit secret: {e}. Please add your Reddit API credentials to secrets.toml.")
    st.stop()

analyzer = SentimentIntensityAnalyzer()

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

# Inject custom CSS for a cleaner look
st.markdown("""
<style>
.st-emotion-cache-183q1h0{
    background-color: #f0f2f6;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.st-emotion-cache-121p2k {
    background-color: #f0f2f6;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.st-emotion-cache-13m0o0p h1 {
    font-size: 2.5rem;
}
</style>
""", unsafe_allow_html=True)


# Main Streamlit app logic
st.set_page_config(page_title="Reddit Sentiment Analyzer", layout="wide")
st.title("Reddit Sentiment Analysis 🗣️")
st.markdown("Analyze real-time sentiment for any keyword on Reddit. This app fetches top posts and comments to understand public opinion.")

# Use columns for a better layout
col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("User Inputs")
    query = st.text_input("Enter a keyword or phrase", "AI")
    limit = st.slider("Number of Posts/Comments to Scrape", 10, 200, 50)
    search_type = st.selectbox("Search Type", ["Subreddit", "All of Reddit"])
    subreddit_name = st.text_input("Subreddit (e.g., technology)", "technology")
    
    if st.button("Analyze Sentiment"):
        with st.spinner("Scraping Reddit... this may take a moment."):
            data = []
            if search_type == "Subreddit":
                try:
                    subreddit = reddit.subreddit(subreddit_name)
                    for submission in subreddit.search(query, limit=limit):
                        submission.comments.replace_more(limit=0)
                        for comment in submission.comments:
                            data.append({'text': comment.body, 'score': comment.score})
                        data.append({'text': submission.title + " " + submission.selftext, 'score': submission.score})
                except Exception as e:
                    st.error(f"Error accessing subreddit: {e}. Please check the subreddit name.")
                    st.stop()
            else: # All of Reddit
                for submission in reddit.subreddit('all').search(query, limit=limit):
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments:
                        data.append({'text': comment.body, 'score': comment.score})
                    data.append({'text': submission.title + " " + submission.selftext, 'score': submission.score})

with col_main:
    if 'data' in locals() and data:
        st.header(f"Sentiment Analysis for: '{query}'")
        
        df = pd.DataFrame(data)
        df.dropna(inplace=True)
        df['preprocessed_text'] = df['text'].apply(preprocess_text)
        
        # Sentiment Analysis
        df['compound'] = df['preprocessed_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
        df['sentiment'] = df['compound'].apply(lambda x: 'Positive' if x >= 0.05 else ('Negative' if x <= -0.05 else 'Neutral'))
        
        # Display key metrics and distribution
        total_analyzed = len(df)
        pos_count = len(df[df['sentiment'] == 'Positive'])
        neg_count = len(df[df['sentiment'] == 'Negative'])
        neu_count = len(df[df['sentiment'] == 'Neutral'])
        
        st.subheader("Sentiment Distribution")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("Positive 😃", pos_count)
        metrics_col2.metric("Negative 😠", neg_count)
        metrics_col3.metric("Neutral 😐", neu_count)

        sentiment_counts = df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
        
        # Use an expander to show raw data, keeping the main page clean
        with st.expander("View Raw Data and Sentiment Scores"):
            st.subheader("Raw Data and Sentiment Scores")
            st.dataframe(df[['text', 'compound', 'sentiment']])
    elif 'data' in locals() and not data:
        st.warning("No posts or comments found for this query. Try a different keyword.")
    else:
        st.info("Enter your search query and click 'Analyze Sentiment' to begin.")