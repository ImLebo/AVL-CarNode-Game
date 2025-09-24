from arbol.nodo import Nodo

class ArbolAVL:
    def __init__(self):
        self.raiz : Nodo = None
        
    def insertar(self, valor):
        nodo = self.buscarNodo(valor)
        if(nodo is not None):
            print("El valor ya existe en el árbol.")
        else:
            nuevo_nodo = Nodo(valor)
            if not self.raiz:
                self.raiz = nuevo_nodo
            else:
                self._insertar_recursivo(self.raiz, nuevo_nodo)
    
    def _insertar_recursivo(self, nodo_actual, nuevo_nodo):
        if nuevo_nodo.valor < nodo_actual.valor:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = nuevo_nodo
                nuevo_nodo.padre = nodo_actual
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, nuevo_nodo)
                self._balancear(nodo_actual)
        else:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = nuevo_nodo
                nuevo_nodo.padre = nodo_actual
            else:
                self._insertar_recursivo(nodo_actual.derecho, nuevo_nodo)
                self._balancear(nodo_actual)
    
    def _balancear(self, nodo):
        if nodo is None:
            return
        
        self._actualizar_factor_balanceo(nodo)
        
        if nodo.factor_balanceo > 1:
            if nodo.izquierdo and nodo.izquierdo.factor_balanceo < 0:
                self._rotacion_izquierda(nodo.izquierdo)
            self._rotacion_derecha(nodo)
        elif nodo.factor_balanceo < -1:
            if nodo.derecho and nodo.derecho.factor_balanceo > 0:
                self._rotacion_derecha(nodo.derecho)
            self._rotacion_izquierda(nodo)
        
        self._balancear(nodo.padre)
    
    def _actualizar_factor_balanceo(self, nodo):
        nodo.factor_balanceo = self._altura(nodo.izquierdo) - self._altura(nodo.derecho)
        
    def _altura(self, nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def _rotacion_derecha(self, nodo):
        nuevo_padre = nodo.izquierdo
        nodo.izquierdo = nuevo_padre.derecho
        if nuevo_padre.derecho:
            nuevo_padre.derecho.padre = nodo
        nuevo_padre.padre = nodo.padre
        if nodo.padre is None:
            self.raiz = nuevo_padre
        elif nodo == nodo.padre.derecho:
            nodo.padre.derecho = nuevo_padre
        else:
            nodo.padre.izquierdo = nuevo_padre
        nuevo_padre.derecho = nodo
        nodo.padre = nuevo_padre
        
        self._actualizar_factor_balanceo(nodo)
        self._actualizar_factor_balanceo(nuevo_padre)
        
    def _rotacion_izquierda(self, nodo):
        nuevo_padre = nodo.derecho
        nodo.derecho = nuevo_padre.izquierdo
        if nuevo_padre.izquierdo:
            nuevo_padre.izquierdo.padre = nodo
        nuevo_padre.padre = nodo.padre
        if nodo.padre is None:
            self.raiz = nuevo_padre
        elif nodo == nodo.padre.izquierdo:
            nodo.padre.izquierdo = nuevo_padre
        else:
            nodo.padre.derecho = nuevo_padre
        nuevo_padre.izquierdo = nodo
        nodo.padre = nuevo_padre
        
        self._actualizar_factor_balanceo(nodo)
        self._actualizar_factor_balanceo(nuevo_padre)
        
    def eliminar(self, valor):
        nodo = self.buscarNodo(valor)
        if nodo is None:
            print("El valor no existe en el árbol.")
            return
        self._eliminar_nodo(nodo)
        self._balancear(nodo.padre)
        
    def _eliminar_nodo(self, nodo):
        if nodo.izquierdo is None and nodo.derecho is None:
            if nodo.padre is None:
                self.raiz = None
            elif nodo == nodo.padre.izquierdo:
                nodo.padre.izquierdo = None
            else:
                nodo.padre.derecho = None
        elif nodo.izquierdo is None:
            if nodo.padre is None:
                self.raiz = nodo.derecho
                self.raiz.padre = None
            elif nodo == nodo.padre.izquierdo:
                nodo.padre.izquierdo = nodo.derecho
                nodo.derecho.padre = nodo.padre
            else:
                nodo.padre.derecho = nodo.derecho
                nodo.derecho.padre = nodo.padre
        elif nodo.derecho is None:
            if nodo.padre is None:
                self.raiz = nodo.izquierdo
                self.raiz.padre = None
            elif nodo == nodo.padre.izquierdo:
                nodo.padre.izquierdo = nodo.izquierdo
                nodo.izquierdo.padre = nodo.padre
            else:
                nodo.padre.derecho = nodo.izquierdo
                nodo.izquierdo.padre = nodo.padre
        else:
            sucesor = self._minimo(nodo.derecho)
            nodo.valor = sucesor.valor
            self._eliminar_nodo(sucesor)
            
    def _minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    def inorder(self, nodo=None):
        if nodo is None:
            nodo = self.raiz
        if nodo.izquierdo:
            self.inorder(nodo.izquierdo)
        print(nodo.value, end=" ")
        if nodo.derecho:
            self.inorder(nodo.derecho)
    
    def buscarNodo(self, valor):
        if self.raiz is None:
            print("El árbol está vacío.")
            return None
        else:
            return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return None
        if valor == nodo.valor:
            return nodo
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)
    
    def imprimirArbol(self, nodo: Nodo =None, prefijo="", es_izquierdo=True):
        if nodo is not None:
            # Print right subtree
            if nodo.derecho:
                new_prefijo = prefijo + ("│   " if es_izquierdo else "    ")
                self.imprimirArbol(nodo.derecho, new_prefijo, False)

            # Print current nodo
            connector = "└── " if es_izquierdo else "┌── "
            print(prefijo + connector + str(nodo.valor))

            # Print left subtree
            if nodo.izquierdo:
                new_prefijo = prefijo + ("    " if es_izquierdo else "│   ")
                self.imprimirArbol(nodo.izquierdo, new_prefijo, True)