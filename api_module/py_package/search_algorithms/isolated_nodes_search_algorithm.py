from .search_algorithm import SearchAlgorithm
import networkx as nx


class IsolatedNodesSearchAlgorithm(SearchAlgorithm):
    def search(self, _, __, graph):

        try:
            isolated_nodes = [node for node in graph.nodes if graph.degree(node) == 0]
            if not isolated_nodes:
                print("No isolated nodes found in the graph.")
                return []
            return isolated_nodes
        except Exception as e:
            print(f"Error while finding isolated nodes: {e}")
            return None
