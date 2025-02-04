import requests
import pandas as pd
import streamlit as st
from textblob import TextBlob

# Function to get Saudi-specific news from StockData.org API
def get_saudi_news_from_api():
    api_token = "QKU9spqJtgUYIuzjolTQecfytOIfVGd006xICQ7u"
    url = f"https://api.stockdata.org/v1/news/all?countries=sa&filter_entities=true&limit=10&published_after=2025-02-03T20:18&api_token={api_token}"
    
    # Send GET request to the API
    response = requests.get(url)
    news_data = response.json()

    if "data" in news_data:
        articles = []
        for article in news_data["data"]:
            title = article["title"]
            description = article.get("summary", "")
            source = article["source"]["name"] if article.get("source") else "Unknown"
            url = article["url"]
            
            # Sentiment analysis using TextBlob
            sentiment_score = TextBlob(title + " " + description).sentiment.polarity
            sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
            
            # Only keep positive sentiment news
            if sentiment_label == "Positive":
                articles.append((title, description, source, sentiment_label, sentiment_score, url))
        
        df = pd.DataFrame(articles, columns=["Title", "Description", "Source", "Sentiment Label", "Sentiment Score", "URL"])
        return df
    else:
        st.write("No news found!")
        return pd.DataFrame()

# Streamlit App
st.title("TASI Positive News Sentiment Analysis")

# Fetch and display positive sentiment news
st.write("Fetching and analyzing the latest positive news from Saudi Arabia...")
sentiment_df = get_saudi_news_from_api()
if not sentiment_df.empty:
    st.dataframe(sentiment_df)
    st.bar_chart(sentiment_df["Sentiment Label"].value_counts())
else:
    st.write("No positive news found.")
