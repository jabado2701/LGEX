from .search_algorithm import SearchAlgorithm
import networkx as nx


class DijkstraSearchAlgorithm(SearchAlgorithm):
    def search(self, start, goal, graph):
        if start not in graph.nodes:
            print(f"Error: The start word '{start}' is not in the graph_builder.")
            return None
        if goal not in graph.nodes:
            print(f"Error: The goal word '{goal}' is not in the graph_builder.")
            return None

        try:

            path = nx.dijkstra_path(graph, start, goal, weight='weight')

            return path
        except nx.NetworkXNoPath:
            print(f"No path exists between '{start}' and '{goal}'.")
            return None
        except Exception as e:
            print(f"Error while calculating the path: {e}")
            return None
