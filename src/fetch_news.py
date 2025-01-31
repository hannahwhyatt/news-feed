import feedparser
import json
import requests
import datetime
import pprint
RSS_FEEDS = [
    "https://www.deepmind.com/blog/feed/basic",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed"
]

def clean_date(date_str):
    # Parse the date string and format it without timezone and seconds
    try:
        date = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return date.strftime("%a, %d %b %Y %H:%M")
    except ValueError:
        return date_str  # Return original if parsing fails

def fetch_deep_mind_news():
    articles = []
    feed = feedparser.parse("https://www.deepmind.com/blog/feed/basic")
    for entry in feed.entries:
        # pprint.pprint(entry)
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": clean_date(entry.published),
            "summary": entry.summary,
            "source": "DeepMind",
        })
    return articles

def fetch_technology_review_news():
    articles = []
    feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed")
    for entry in feed.entries:
        # pprint.pprint(entry)
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": clean_date(entry.published),
            "summary": entry.summary,
            "source": "Technology Review",
        })
    return articles



def fetch_all_news():
    deep_mind_news = fetch_deep_mind_news()
    technology_review_news = fetch_technology_review_news()
    return deep_mind_news + technology_review_news

if __name__ == "__main__":
    news = fetch_all_news()
    print(len(news))
    # Save to JSON file
    with open("data/news.json", "w") as f:
        json.dump(news, f, indent=4)
