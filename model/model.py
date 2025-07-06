import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getAllStore(self):
        return DAO.getAllStore()

    def buildGraph(self, store_id, k):
        self._graph.clear()
        nodes = DAO.getAllNodes(store_id)
        for n in nodes:
            self._idMap[n.order_id] = n
        self._graph.add_nodes_from(nodes)

        archi = DAO.getAllEdges(store_id, k, self._idMap)
        for a in archi:
            if a.o1 in self._graph and a.o2 in self._graph:
                self._graph.add_edge(a.o1, a.o2, weight=a.peso)

    def graphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getNodes(self, store_id):
        return DAO.getAllNodes(store_id)

    def camminoPiuLungo(self, idNodo):
        oggettoO = self._idMap[int(idNodo)] #dato l'id dell'ordine (nodo) selezionato nel dd prendo tutto l'oggetto ordine
        cammino = list((nx.dfs_preorder_nodes(self._graph, oggettoO))) #ordina i nodi per dare il cammino più lungo, dato il grafo e il nodo di partenza

        #cammino più corto: cammino = nx.shortest_path_length(self._graph, oggettoO)
        return cammino