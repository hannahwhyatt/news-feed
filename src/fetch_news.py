import feedparser
import json
import requests
import datetime
import pprint

RSS_FEEDS = {
    "DeepMind": "https://www.deepmind.com/blog/feed/basic",
    "Technology Review": "https://www.technologyreview.com/topic/artificial-intelligence/feed"
    # "Berkeley AI Research": "https://bair.berkeley.edu/blog/feed",
    # "MIT News": "http://news.mit.edu/rss/topic/artificial-intelligence2",
}

request_urls = {
    "Ahead of AI": "https://magazine.sebastianraschka.com/api/v1/archive?sort=new&search=&limit=12",
    "Interconnects": "https://www.interconnects.ai/api/v1/archive?sort=new&search=&limit=12",
    "Hyperdimensional": "https://www.hyperdimensional.co/api/v1/archive?sort=new&search=&limit=12",
    "The AI Frontier": "https://frontierai.substack.com/api/v1/archive?sort=new&search=&limit=12"
}



def clean_date(date_str):
    # Parse the date string and format it without timezone and seconds
    try:
        date = datetime.datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return date.strftime("%a, %d %b %Y %H:%M")
    except ValueError:
        return date_str  # Return original if parsing fails

def fetch_news(feed_url, name, max_articles=5):
    articles = []
    feed = feedparser.parse(feed_url)
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=1)
    
    for entry in feed.entries:
        try:
            # Parse the entry's publication date and ensure it's UTC
            pub_date = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
            pub_date = pub_date.astimezone(datetime.timezone.utc)
            
            # Only include articles from the last 7 days
            if pub_date >= start_date or name in ["Ahead of AI"]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": clean_date(entry.published),
                    "numerical_date": pub_date.isoformat(),  # Store as ISO format string
                    "summary": entry.summary,
                    "source": name,
                })
        except (ValueError, AttributeError):
            continue

    number_of_articles = len(articles)

    print(f"Found {number_of_articles} articles from {name}. Saving {max_articles if number_of_articles > max_articles else number_of_articles} articles.")
    return articles[:max_articles if number_of_articles > max_articles else number_of_articles]

def fetch_request_url(url, name, max_articles=5):
    articles = []
    start_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=1)
    print(start_date)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for entry in data:
            # Convert the post_date to UTC datetime
            post_date = datetime.datetime.fromisoformat(entry['post_date'].replace('Z', '+00:00'))
            post_date = post_date.astimezone(datetime.timezone.utc)
            if post_date >= start_date:
                formatted_date = post_date.strftime("%a, %d %b %Y %H:%M")
                
                articles.append({
                    "title": entry['title'],
                    "link": entry['canonical_url'],
                    "published": formatted_date,
                    "numerical_date": post_date.isoformat(),  # Store as ISO format string
                    "summary": entry.get('subtitle', ''),
                    "source": name,
                    })
    
    number_of_articles = len(articles)
    print(f"Found {number_of_articles} articles from {name}. Saving {max_articles if number_of_articles > max_articles else number_of_articles} articles.")
    return articles[:max_articles if number_of_articles > max_articles else number_of_articles]

def fetch_all_news():
    all_news = []
    # Fetch RSS feeds
    for name, feed_url in RSS_FEEDS.items():
        news = fetch_news(feed_url, name)
        all_news.extend(news)
    
    # Fetch API-based feeds
    for name, request_url in request_urls.items():
        news = fetch_request_url(request_url, name)
        all_news.extend(news)
    return all_news

if __name__ == "__main__":
    news = fetch_all_news()

    # Sort news by date (parse ISO strings for comparison)
    news.sort(key=lambda x: datetime.datetime.fromisoformat(x['numerical_date']), reverse=True)
    
    # Remove numerical_date
    for article in news:
        article.pop('numerical_date')

    # Save to JSON file
    with open("data/news.json", "w") as f:
        json.dump(news, f, indent=4)
