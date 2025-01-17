import os
import re
from collections import Counter

DEFAULT_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by',
    'for', 'from', 'has', 'he', 'in', 'is', 'it',
    'its', 'of', 'on', 'that', 'the', 'to', 'was',
    'were', 'will', 'with', 'this', 'what', 'who',
    'when', 'which', 'why', 'how', 'or', 'if', 'else'
}


class TextAnalyzer:
    def __init__(self):

        self.stop_words = DEFAULT_STOPWORDS

    def _load_text_file(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(filename, 'r', encoding='latin-1') as file:
                return file.read()

    def _clean_text(self, text):
        return re.sub(r'[^a-zA-Z\s]', ' ', text.lower())

    def _basic_word_tokenize(self, text):

        return re.findall(r'[a-zA-Z]+', text)

    def _is_valid_word(self, word):
        return (
                word not in self.stop_words
                and len(set(word)) > 1
                and not all(char == word[0] for char in word)
        )

    def _extract_words_by_length_from_file(self, filename, lengths, remove_stopwords=True):
        raw_text = self._load_text_file(filename)
        cleaned_text = self._clean_text(raw_text)
        tokens = self._basic_word_tokenize(cleaned_text)

        valid_words = []
        for w in tokens:
            if len(w) in lengths:
                if remove_stopwords:
                    if self._is_valid_word(w):
                        valid_words.append(w)
                else:
                    if len(set(w)) > 1:
                        valid_words.append(w)

        return Counter(valid_words)

    def extract_words_by_length_from(self, filenames, lengths, remove_stopwords=True):
        combined_counter = Counter()

        for filename in filenames:
            try:
                file_counter = self._extract_words_by_length_from_file(filename, lengths, remove_stopwords)
                combined_counter.update(file_counter)
            except FileNotFoundError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing '{filename}': {e}")

        return combined_counter

    def extract_words_from_directory(self, directory, lengths, remove_stopwords=True):
        txt_files = [
            os.path.join(directory, f) for f in os.listdir(directory)
            if f.endswith('.txt')
        ]
        return self.extract_words_by_length_from(txt_files, lengths, remove_stopwords)
