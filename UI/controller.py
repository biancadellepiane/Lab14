import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDD(self):
        store = self._model.getAllStore()
        for s in store:
            self._view._ddStore.options.append(ft.dropdown.Option(str(s)))
        self._view.update_page()



    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value
        if store is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessuno store inserito", color="red"))
            self._view.update_page()
            return
        k = self._view._txtIntK.value
        if k is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessun k inserito", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero intero", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(store, kInt)

        numNodi, numArchi = self._model.graphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {numNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {numArchi}"))

        self._view._ddNode.options.clear()
        self.fillDDNode()

        self._view.update_page()

    def fillDDNode(self):
        self._view._ddNode.options.clear()
        store = self._view._ddStore.value
        nodes = self._model.getNodes(store)
        for n in nodes:
            #sono classi intere quindi text è il riempimento del dd e data è l'ordine
            self._view._ddNode.options.append(ft.dropdown.Option(text= n.order_id, data=n))
        self._view.update_page()

    def handleCerca(self, e):
        nodoP = self._view._ddNode.value
        if nodoP is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Nessun nodo inserito", color="red"))
            self._view.update_page()
            return

        cammino = self._model.camminoPiuLungo(nodoP)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {nodoP}"))
        for n in cammino[1:]:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass
