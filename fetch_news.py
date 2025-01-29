import feedparser
import json
import requests
import datetime
import pprint
# RSS Feeds to fetch news from
RSS_FEEDS = [
    "https://www.deepmind.com/blog/feed/basic",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed"
]

# Your LLM API endpoint for summarization
LLM_API_URL = "YOUR_LLM_API_ENDPOINT"

def fetch_deep_mind_news():
    articles = []
    feed = feedparser.parse("https://www.deepmind.com/blog/feed/basic")
    for entry in feed.entries:
        pprint.pprint(entry)
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary,
        })
    return articles

results = fetch_deep_mind_news()
pprint.pprint(results)

# def fetch_rss_news():
#     articles = []
#     for url in RSS_FEEDS:
#         feed = feedparser.parse(url)
#         for entry in feed.entries[:5]:  # Get latest 5 articles per feed
#             # summary = summarize_article(entry.summary)
#             articles.append({
#                 "title": entry.title,
#                 "link": entry.link,
#                 # "summary": summary
#             })
#     return articles

# # def summarize_article(text):
# #     response = requests.post(LLM_API_URL, json={"text": text, "summary_length": 2})
# #     return response.json().get("summary", text)  # Use original text if API fails

if __name__ == "__main__":
    # news = fetch_rss_news()
    news = fetch_deep_mind_news()

    # Sort news by published date
    news = sorted(news, key=lambda x: datetime.datetime.strptime(x["published"], "%a, %d %b %Y %H:%M:%S %z"), reverse=True)
    news = news[:5]
    # Save to JSON file
    # with open(f"news_data/news_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w") as f:
    with open("news.json", "w") as f:
        json.dump(news, f, indent=4)
