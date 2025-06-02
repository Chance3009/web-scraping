import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
import time
import random
from fake_useragent import UserAgent
import re


class IMDbScraper:
    def __init__(self, base_url="https://www.imdb.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.ua = UserAgent()
        self.data = []

    def _get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def fetch_page(self, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(2, 5))
                response = self.session.get(
                    url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(
                    f"Error fetching page (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep((2 ** attempt) + random.uniform(1, 3))

    def parse_movies(self, html):
        if not html:
            return

        soup = BeautifulSoup(html, 'lxml')
        movie_items = soup.find_all(
            'li', class_='ipc-metadata-list-summary-item')

        for movie in movie_items:
            try:
                # Title
                title_tag = movie.find('h3', class_='ipc-title__text')
                title = title_tag.text.strip() if title_tag else ''

                # Metadata (year, duration, content rating)
                metadata_spans = movie.find_all(
                    'span', class_='cli-title-metadata-item')
                year = ''
                duration = ''
                content_rating = ''
                for span in metadata_spans:
                    text = span.text.strip()
                    if re.match(r'^\d{4}$', text):
                        year = text
                    elif re.match(r'^\d+h( \d+m)?$', text):
                        duration = text
                    elif len(text) <= 5:
                        content_rating = text

                # IMDb rating
                rating_elem = movie.find(
                    'span', class_='ipc-rating-star--rating')
                rating = rating_elem.text.strip() if rating_elem else ''

                # Number of votes
                votes_elem = movie.find(
                    'span', class_='ipc-rating-star--voteCount')
                votes = votes_elem.text.replace(
                    '(', '').replace(')', '').strip() if votes_elem else ''

                # Movie URL
                link_tag = movie.find(
                    'a', class_='ipc-title-link-wrapper', href=True)
                url = f"{self.base_url}{link_tag['href']}" if link_tag else ''

                # Poster image URL
                poster_img = movie.find('img', class_='ipc-image')
                poster_url = poster_img['src'] if poster_img and poster_img.has_attr(
                    'src') else ''

                self.data.append({
                    'title': title,
                    'year': year,
                    'duration': duration,
                    'content_rating': content_rating,
                    'rating': rating,
                    'votes': votes,
                    'url': url,
                    'poster_url': poster_url,
                    'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f"Scraped: {title}")

            except Exception as e:
                print(f"Error parsing movie: {e}")

    def scrape_popular_movies(self):
        print("Starting to scrape IMDb popular movies...")
        url = f"{self.base_url}/chart/moviemeter/"
        html = self.fetch_page(url)

        if html:
            self.parse_movies(html)
        else:
            print("Failed to fetch IMDb popular movies page")

    def save_data(self):
        if not self.data:
            print("No data to save!")
            return

        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(
            'data', f'imdb_popular_movies_{timestamp}.csv')

        df = pd.DataFrame(self.data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Data saved to {output_path}")


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
