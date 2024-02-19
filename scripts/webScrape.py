import sqlite3
from bs4 import BeautifulSoup
import requests
import dotenv
import os

#import dotenv 
dotenv.load_dotenv()
OPEN_AI_KEY = os.getenv('OPEN-AI-KEY')
# SQLite setup
def setup_database():
    conn = sqlite3.connect('movies.db')
    # if movie_text exists, delete it

    cur = conn.cursor()
    cur.execute('''DROP TABLE IF EXISTS movie_text''')
    cur.execute('''CREATE TABLE IF NOT EXISTS movie_text
                   (chunk_text TEXT, embedding BLOB)''')
    
    
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_into_db(text_chunk):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO movie_text(chunk_text,embedding) VALUES (?,?)", (text_chunk, None))
    conn.commit()
    conn.close()

# Modified scraping function
def scrape_movie_text(movie_name):
    url = f"https://themoviespoiler.com/movies/{movie_name}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find('div', class_='entry-content')
    paragraphs = main_content.find_all('p')

    for paragraph in paragraphs:
        text = paragraph.get_text(strip=True)
        print(text)
        print(movie_name)
        text = movie_name.replace('-',' ') + " " + text
        if text:
            insert_into_db(text)

# Setup database
setup_database()

# List of movies to scrape
movies = ['anatomy-of-a-fall', 'maestro', 'american-fiction',
          'barbie', 'oppenheimer', 'the-zone-of-interest', 'the-holdovers',
          'poor-things','past-lives','killers-of-the-flower-moon']

# Iterate over movies and scrape content
for movie in movies:
    scrape_movie_text(movie)

# print out the data
conn = sqlite3.connect('movies.db')
cur = conn.cursor()
cur.execute("SELECT * FROM movie_text")
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()