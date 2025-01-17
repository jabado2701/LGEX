from .graph_exporter import GraphExporter
import pickle


class PickleGraphExporter(GraphExporter):
    def import_graph(self, graph):
        return pickle.loads(graph)

    def export_graph(self, graph, path):
        with open(path, 'wb') as f:
            pickle.dump(graph, f)
