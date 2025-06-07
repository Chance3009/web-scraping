import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re


class IMDbScraper:
    def __init__(self):
        self.data = []

    def fetch_page(self, url):
        try:
            time.sleep(random.uniform(2, 4)) 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None

    def parse_movies(self, html):
        if not html:
            return

        soup = BeautifulSoup(html, 'lxml')
        # Parse movie container
        movie_items = soup.find_all('li', class_='ipc-metadata-list-summary-item')
        print(f"Total <li> items found: {len(movie_items)}")

        for movie in movie_items:
            try:
                # Title
                title_tag = movie.find('h3', class_='ipc-title__text')
                title = title_tag.text.strip() if title_tag else 'N/A'
                
                # Metadata (year, duration, content rating)
                metadata_spans = movie.find_all('span', class_='cli-title-metadata-item')
                year = 'N/A'
                duration = 'N/A'
                content_rating = 'N/A'
                for span in metadata_spans:
                    text = span.text.strip()
                    if re.match(r'^\d{4}$', text):
                        year = text
                    elif re.match(r'^\d+h( \d+m)?$', text):
                        duration = text
                    elif len(text) <= 5:
                        content_rating = text
                
                # IMDb rating
                rating_elem = movie.find('span', class_='ipc-rating-star--rating')
                rating = rating_elem.text.strip() if rating_elem else 'N/A'
                
                # Number of votes
                votes_elem = movie.find('span', class_='ipc-rating-star--voteCount')
                votes = votes_elem.text.replace('(', '').replace(')', '').strip() if votes_elem else 'N/A'
                
                # Movie URL
                link_tag = movie.find('a', class_='ipc-title-link-wrapper', href=True)
                url = f"https://www.imdb.com{link_tag['href']}" if link_tag else 'N/A'
                
                # Poster image URL
                poster_img = movie.find('img', class_='ipc-image')
                poster_url = poster_img['src'] if poster_img and poster_img.has_attr('src') else 'N/A'

                self.data.append({
                    'title': title,
                    'year': year,
                    'duration': duration,
                    'content_rating': content_rating,
                    'rating': rating,
                    'votes': votes,
                    'url': url,
                    'poster_url': poster_url,
                })
                print(f"Scraped: {title}")

            except Exception as e:
                print(f"Error parsing movie: {e}")

    def scrape_popular_movies(self):
        print("Starting to scrape IMDb popular movies...")
        url = "https://www.imdb.com/chart/moviemeter/"
        html = self.fetch_page(url)

        if html:
            self.parse_movies(html)
        else:
            print("Failed to fetch IMDb popular movies page")

    def save_data(self):
        if not self.data:
            print("No data to save!")
            return

        df = pd.DataFrame(self.data)
        df.to_csv("imdb_popular_movies.csv", index=False)
        print("Data saved to imdb_popular_movies.csv")


def main():
    scraper = IMDbScraper()
    try:
        scraper.scrape_popular_movies()
        scraper.save_data()
        print("Scraping completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
