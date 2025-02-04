import streamlit as st
import requests
import pandas as pd
from textblob import TextBlob

# NewsAPI function
def get_news_from_api(company_name):
    api_key = "9b508ce5380844f3a69110ba56b375fd"
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={api_key}&language=en&sortBy=publishedAt"
    response = requests.get(url)
    news_data = response.json()

    if "articles" in news_data:
        articles = []
        for article in news_data["articles"]:
            title = article["title"]
            description = article.get("description", "")
            source = article["source"]["name"]
            url = article["url"]
            
            # Sentiment Analysis using TextBlob
            blob = TextBlob(title + " " + description)
            sentiment_score = blob.sentiment.polarity
            sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

            articles.append((title, description, source, sentiment_label, sentiment_score, url))
        
        df = pd.DataFrame(articles, columns=["Title", "Description", "Source", "Sentiment Label", "Sentiment Score", "URL"])
        return df
    else:
        st.write("No news found!")
        return pd.DataFrame()

# Streamlit App
st.title("TASI News Sentiment Analysis")

company_name = st.text_input("Enter the company name for sentiment analysis:")
if company_name:
    st.write("Fetching and analyzing news...")
    sentiment_df = get_news_from_api(company_name)
    if not sentiment_df.empty:
        st.dataframe(sentiment_df)
        st.bar_chart(sentiment_df["Sentiment Score"])
