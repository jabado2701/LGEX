from .graph_builder import GraphBuilder
import networkx as nx


class WeightGraphBuilder(GraphBuilder):

    def build_graph(self, word_count):
        graph = nx.Graph()

        for word, count in word_count.items():
            graph.add_node(word, count=count)

        words = list(word_count.keys())
        n = len(words)
        for i in range(n):
            for j in range(i + 1, n):
                word1 = words[i]
                word2 = words[j]
                if self._differ_by_one(word1, word2):
                    count1 = word_count[word1]
                    count2 = word_count[word2]
                    weight = (count1 + count2) / 2
                    graph.add_edge(word1, word2, weight=weight)

        return graph

    def _differ_by_one(self, w1, w2):
        len_diff = abs(len(w1) - len(w2))
        if len_diff > 1:
            return False
        if len_diff == 0:
            return sum(c1 != c2 for c1, c2 in zip(w1, w2)) == 1
        if len_diff == 1:
            if len(w1) > len(w2):
                w1, w2 = w2, w1
            for i in range(len(w1) + 1):
                if w1[:i] + w2[i] + w1[i:] == w2:
                    return True
        return False
