from serpapi import GoogleSearch
import mysql.connector
from datetime import datetime, timedelta

# Initialize API parameters
params = {
    "api_key": "d4e2320f7928a2440257e8bb149a8988f2e8381573d6641a52d58da5f7807113",
    "engine": "google_news",
    "q": "India",
    "hl": "en",
    "gl": "in",
    "sort_by": "date",
    "tbs": "qdr:w"  # Fetch news from the last 7 days
}

# Fetch news data using SerpAPI
search = GoogleSearch(params)
results = search.get_dict()

# Extract articles from the response
articles = []
for news in results.get("news_results", []):
    article = {
        "title": news.get("title"),
        "source": news.get("source", {}).get("name", ""),  # Extract 'name' from 'source' dictionary
        "link": news.get("link"),
        "published_date": news.get("date"),
        "snippet": news.get("snippet"),
        "image": news.get("thumbnail") 
    }
    articles.append(article)

print(f"Fetched {len(articles)} articles related to India.")

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_root_password",
    database="news_db"
)
cursor = db.cursor()

# Create table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS india_news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    source VARCHAR(100),
    link TEXT,
    published_date VARCHAR(100),
    snippet TEXT
);
"""
cursor.execute(create_table_query)

# Insert data into the table
insert_query = """
INSERT INTO india_news (title, source, link, published_date, snippet)
VALUES (%s, %s, %s, %s, %s)
"""

for article in articles:
    try:
        cursor.execute(insert_query, (
            article['title'],
            article['source'],  # Source is now just a string (name of the source)
            article['link'],
            article['published_date'],
            article['snippet']
            
        ))
    except Exception as e:
        print(f"Error inserting article: {e}")

# Commit changes and close connection
db.commit()
print("Data inserted into MySQL successfully.")

cursor.close()
db.close()
