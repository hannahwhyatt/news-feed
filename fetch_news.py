import feedparser
import json
import requests
import datetime

# RSS Feeds to fetch news from
RSS_FEEDS = [
    "https://www.deepmind.com/blog/feed/basic",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed"
]

# Your LLM API endpoint for summarization
LLM_API_URL = "YOUR_LLM_API_ENDPOINT"

def fetch_rss_news():
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Get latest 5 articles per feed
            # summary = summarize_article(entry.summary)
            articles.append({
                "title": entry.title,
                "link": entry.link,
                # "summary": summary
            })
    return articles

# def summarize_article(text):
#     response = requests.post(LLM_API_URL, json={"text": text, "summary_length": 2})
#     return response.json().get("summary", text)  # Use original text if API fails

if __name__ == "__main__":
    news = fetch_rss_news()
    
    # Save to JSON file
    # with open(f"news_data/news_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w") as f:
    with open("news.json", "w") as f:
        json.dump(news, f, indent=4)
