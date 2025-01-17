from flask import Flask, request, jsonify
from api_module.py_package.graph_exporter import PickleGraphExporter
from api_module.py_package.search_algorithms import AstarSearchAlgorithm, DijkstraSearchAlgorithm, IsolatedNodesSearchAlgorithm
from api_module.py_clasess.api_feeder import ApiFeeder


class SearchApi:
    def __init__(self):
        self.dijkstra_search_algorithm = DijkstraSearchAlgorithm()
        self.astar_search_algorithm = AstarSearchAlgorithm()
        self.isolated_nodes_search_algorithm = IsolatedNodesSearchAlgorithm()
        self.api_feeder = None
        self.app = None

    def _register_routes(self):
        @self.app.route('/search/astar/', methods=['GET'])
        def search_astar():
            start = request.args.get('start')
            goal = request.args.get('goal')

            if not start or not goal:
                return jsonify({"error": "Missing 'start' or 'goal' parameter."}), 400

            try:
                self.api_feeder.ensure_graph_loaded()
                result = self.astar_search_algorithm.search(start, goal, self.api_feeder.graph)
                if result is None:
                    return jsonify({"error": f"No path found between '{start}' and '{goal}'."}), 404
                return jsonify({"algorithm": "A*", "start": start, "goal": goal, "path": result})
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except RuntimeError as e:
                return jsonify({"error": str(e)}), 500
            except Exception as e:
                return jsonify({"error": f"Error performing A* search: {str(e)}"}), 500

        @self.app.route('/search/dijkstra/', methods=['GET'])
        def search_dijkstra():
            start = request.args.get('start')
            goal = request.args.get('goal')

            if not start or not goal:
                return jsonify({"error": "Missing 'start' or 'goal' parameter."}), 400

            try:
                self.api_feeder.ensure_graph_loaded()
                result = self.dijkstra_search_algorithm.search(start, goal, self.api_feeder.graph)
                if result is None:
                    return jsonify({"error": f"No path found between '{start}' and '{goal}'."}), 404
                return jsonify({"algorithm": "Dijkstra", "start": start, "goal": goal, "path": result})
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except RuntimeError as e:
                return jsonify({"error": str(e)}), 500
            except Exception as e:
                return jsonify({"error": f"Error performing Dijkstra search: {str(e)}"}), 500

        @self.app.route('/search/isolated_nodes/', methods=['GET'])
        def search_isolated_nodes():
            try:
                self.api_feeder.ensure_graph_loaded()
                result = self.isolated_nodes_search_algorithm.search(None, None, self.api_feeder.graph)
                if result is None:
                    return jsonify({"error": "No isolated nodes found in the graph."}), 404
                return jsonify({"algorithm": "Isolated Nodes", "isolated_nodes": result})
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except RuntimeError as e:
                return jsonify({"error": str(e)}), 500
            except Exception as e:
                return jsonify({"error": f"Error performing Isolated Nodes search: {str(e)}"}), 500

    def run(self):
        self.api_feeder = ApiFeeder()
        self.app = Flask(__name__)
        self._register_routes()
        self.app.run(host="0.0.0.0", port=8080, debug=False)
