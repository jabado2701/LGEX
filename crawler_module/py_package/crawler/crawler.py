# crawler_base.py
from abc import ABC, abstractmethod
import os


class Crawler(ABC):

    @abstractmethod
    def download_content(self):
        pass
