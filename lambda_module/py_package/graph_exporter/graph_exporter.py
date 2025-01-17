from abc import ABC, abstractmethod


class GraphExporter(ABC):
    @abstractmethod
    def export_graph(self, graph, path):
        pass

    @abstractmethod
    def import_graph(self, graph):
        pass
