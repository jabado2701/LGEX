import time
from multiprocessing import Event
from crawler_module.py_package.crawler import GutenbergCrawler
from crawler_module.py_classes.aws_handler import AWSHandler
import os


class CrawlerController:

    def __init__(self):
        self.crawler = GutenbergCrawler(book_count=3, download_dir="../data")
        self.check_interval = 60
        self.books_downloaded_event = Event()

    def execute(self):
        aws_handler = AWSHandler("lgex-download-bucket")
        while True:
            try:
                print("Downloading content...")
                content = self.crawler.download_content()
                for file_path in content:
                    aws_handler.upload_file_to_s3(file_path, os.path.basename(file_path))
                    print("Content downloaded successfully.")

                if not self.books_downloaded_event.is_set():
                    self.books_downloaded_event.set()
                    print("Books downloaded for the first time. Notifying other processes.")
            except Exception as e:
                print(f"Error during content download: {e}")
            time.sleep(self.check_interval)
