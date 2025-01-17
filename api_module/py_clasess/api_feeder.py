from api_module.py_clasess.aws_handler import AWSHandler
from api_module.py_package.graph_exporter import PickleGraphExporter
import threading
import time


class ApiFeeder:
    def __init__(self):
        self.graph = None
        self.graph_loader = PickleGraphExporter()
        self.last_loaded = 0
        self.cache_expiration = 600
        self.is_loading = False

    def _reload_graph_in_background(self):
        if not self.is_loading:
            self.is_loading = True
            aws_handler = AWSHandler("lgex-app-bucket")
            try:
                print("Reloading graph from S3 in background...")
                s3_graph_data = aws_handler.get_object_content_from_s3("lgex_graph.pkl")
                new_graph = self.graph_loader.import_graph(s3_graph_data)
                self.graph = new_graph
                self.last_loaded = time.time()
                print("Graph reloaded successfully.")
            except Exception as e:
                print(f"Failed to reload graph in background: {e}")
            finally:
                self.is_loading = False

    def ensure_graph_loaded(self):
        current_time = time.time()
        if self.graph is None or (current_time - self.last_loaded > self.cache_expiration):
            print("Cache expired or graph not loaded. Triggering background reload.")
            threading.Thread(target=self._reload_graph_in_background, daemon=True).start()
