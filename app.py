import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd

# Define a function to scrape and analyze sentiment
def get_tasi_news_sentiment(keyword):
    search_url = f"https://www.google.com/search?q={keyword}+site:argaam.com"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [title.get_text() for title in soup.find_all('h3')]

    if not headlines:
        st.write(f"No news found for {keyword}")
        return pd.DataFrame()

    sentiment_data = []
    for headline in headlines:
        blob = TextBlob(headline)
        sentiment_score = blob.sentiment.polarity
        sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        sentiment_data.append((headline, sentiment_score, sentiment_label))

    df = pd.DataFrame(sentiment_data, columns=["Headline", "Sentiment Score", "Sentiment Label"])
    return df

# Streamlit App
st.title("TASI News Sentiment Analysis")

company_name = st.text_input("Enter the company name for sentiment analysis:")
if company_name:
    st.write("Fetching and analyzing news...")
    sentiment_df = get_tasi_news_sentiment(company_name)
    if not sentiment_df.empty:
        st.dataframe(sentiment_df)
        st.bar_chart(sentiment_df["Sentiment Score"])
