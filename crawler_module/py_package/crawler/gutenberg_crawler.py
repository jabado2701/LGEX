import requests
import random
from bs4 import BeautifulSoup
from .crawler import Crawler
import os


class GutenbergCrawler(Crawler):
    BASE_URL = "https://www.gutenberg.org/cache/epub/"
    METADATA_URL = "https://www.gutenberg.org/ebooks/"
    BOOK_ID_RANGE = (1, 75000)

    def __init__(self, book_count=20, download_dir="./downloads"):
        self.download_dir = download_dir
        self.create_download_dir()
        self.book_count = book_count

    def create_download_dir(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def generate_random_book_id(self):
        return random.randint(self.BOOK_ID_RANGE[0], self.BOOK_ID_RANGE[1])

    def is_english(self, book_id):
        metadata_url = f"{self.METADATA_URL}{book_id}"
        try:
            response = requests.get(metadata_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            language_row = soup.find(lambda tag: tag.name == "th" and "Language" in tag.text)
            if language_row:
                language = language_row.find_next("td").text.strip()
                return "English" in language

            print(f"Book ID {book_id} is not in English.")
        except Exception as e:
            print(f"Error checking language for book {book_id}: {e}")
        return False

    def download_content(self):
        downloaded_books = 0
        attempted_books = set()
        downloaded_files = []

        while downloaded_books < self.book_count:
            book_id = self.generate_random_book_id()

            if book_id in attempted_books:
                continue

            attempted_books.add(book_id)

            file_path = self._download_books(book_id)
            if file_path:
                downloaded_books += 1
                downloaded_files.append(file_path)

        return downloaded_files

    def _download_books(self, book_id):
        download_url = f"{self.BASE_URL}{book_id}/pg{book_id}.txt"
        file_path = os.path.join(self.download_dir, f"pg{book_id}.txt")

        if self.is_english(book_id):
            try:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return os.path.abspath(file_path)
            except Exception as e:
                print(f"Error downloading book ID {book_id}: {e}")
        return None
