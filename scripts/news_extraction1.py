from serpapi import GoogleSearch
import mysql.connector
from datetime import datetime

# Initialize API parameters
params = {
    "api_key": "d4e2320f7928a2440257e8bb149a8988f2e8381573d6641a52d58da5f7807113",
    "engine": "google_news",
    "q": "India",  # Query to fetch India-related news
    "hl": "en",
    "gl": "in",
    "sort_by": "date",
    "tbs": "qdr:w",  # Fetch news from the last 7 days
}

# Fetch news data using SerpAPI
search = GoogleSearch(params)
results = search.get_dict()

# Connect to MySQL with updated credentials
db = mysql.connector.connect(
    host="localhost",        # Hostname
    user="root",             # MySQL username
    password="your_root_password",  # Your MySQL password
    database="news_db"       # Database name
)

cursor = db.cursor()

# Extract articles and insert them into the database
for news in results.get("news_results", []):
    title = news.get("title")
    source = news.get("source")
    link = news.get("link")
    published_date = news.get("date")
    snippet = news.get("snippet")

    # Prepare and execute the insert query
    try:
        cursor.execute("""
            INSERT INTO news_articles (title, source, link, published_date, snippet)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, source, link, published_date, snippet))
        db.commit()  # Commit the transaction
        print(f"Inserted article: {title}")
    except mysql.connector.Error as err:
        print(f"Error inserting article: {err}")

# Close the cursor and database connection
cursor.close()
db.close()
