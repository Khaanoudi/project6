import requests
import pandas as pd
import streamlit as st

# Function to get Saudi-specific news from StockData.org API
def get_saudi_news_from_api(company_name):
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
            source = article["source"]["name"]
            url = article["url"]
            
            # Sentiment analysis (you can modify this part based on your own sentiment model)
            sentiment_label = "Positive" if "positive" in title.lower() else "Negative"
            
            articles.append((title, description, source, sentiment_label, url))
        
        df = pd.DataFrame(articles, columns=["Title", "Description", "Source", "Sentiment Label", "URL"])
        return df
    else:
        st.write("No news found!")
        return pd.DataFrame()

# Streamlit App
st.title("TASI News Sentiment Analysis")

company_name = st.text_input("Enter the company name for sentiment analysis:")
if company_name:
    st.write("Fetching and analyzing news...")
    sentiment_df = get_saudi_news_from_api(company_name)
    if not sentiment_df.empty:
        st.dataframe(sentiment_df)
        st.bar_chart(sentiment_df["Sentiment Label"].value_counts())
