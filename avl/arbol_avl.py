from avl.nodo import Nodo

class ArbolAVL:
    def __init__(self):
        self.raiz : Nodo = None
        
    def insertar(self, nuevo_nodo: Nodo):
        nodo = self.buscarNodo(nuevo_nodo)
        if(nodo is not None):
            print(f"El valor ya existe en el árbol, en la posición ({nuevo_nodo.valor_x}, {nuevo_nodo.valor_y})")
        else:
            if not self.raiz:
                self.raiz = nuevo_nodo
            else:
                self._insertar_recursivo(self.raiz, nuevo_nodo)
    
    def _insertar_recursivo(self, nodo_actual: Nodo, nuevo_nodo: Nodo):
        #Nuevo nodo Izquierdo por X
        if nuevo_nodo.valor_x < nodo_actual.valor_x:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = nuevo_nodo
                nuevo_nodo.padre = nodo_actual
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, nuevo_nodo)
                self._balancear(nodo_actual)
        #Nuevo nodo Derecho por x
        elif nuevo_nodo.valor_x > nodo_actual.valor_x:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = nuevo_nodo
                nuevo_nodo.padre = nodo_actual
            else:
                self._insertar_recursivo(nodo_actual.derecho, nuevo_nodo)
                self._balancear(nodo_actual)
        #Empate de x comparacion a través de Y
        else: 
            if nuevo_nodo.valor_y < nodo_actual.valor_y:
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
                
    
    def _balancear(self, nodo: Nodo):
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
    
    def _actualizar_factor_balanceo(self, nodo: Nodo):
        nodo.factor_balanceo = self._altura(nodo.izquierdo) - self._altura(nodo.derecho)
        
    def _altura(self, nodo: Nodo):
        if nodo is None:
            return 0
        return 1 + max(self._altura(nodo.izquierdo), self._altura(nodo.derecho))
    
    def _rotacion_derecha(self, nodo: Nodo):
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
        
    def _rotacion_izquierda(self, nodo: Nodo):
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
    
    def buscarNodo(self, nodo_buscado):
        if self.raiz is None:
            print("El árbol está vacío.")
            return None
        else:
            return self._buscar_recursivo(self.raiz, nodo_buscado)
    
    def _buscar_recursivo(self, nodo_raiz: Nodo, nodo_buscado: Nodo):
        if nodo_raiz is None:
            return None
        if nodo_buscado.valor_x == nodo_raiz.valor_x and nodo_buscado.valor_y == nodo_raiz.valor_y:
            return nodo_raiz
        elif nodo_buscado.valor_x < nodo_raiz.valor_x:
            return self._buscar_recursivo(nodo_raiz.izquierdo, nodo_buscado)
        else:
            return self._buscar_recursivo(nodo_raiz.derecho, nodo_buscado)
        
    def preorden(self, nodo: Nodo = None):
        if nodo is None:
            nodo = self.raiz
        if nodo:
            print(f"({nodo.valor_x}, {nodo.valor_y})", end=" -> ")
            self.preorden(nodo.izquierdo)
            self.preorden(nodo.derecho)

    def inorden(self, nodo: Nodo = None, resultado=None):
        if resultado is None:
            resultado = []
            
        if nodo is None:
            nodo = self.raiz

        if nodo is None:
            return resultado

        if nodo.izquierdo:
            self.inorden(nodo.izquierdo, resultado)

        resultado.append(nodo)

        if nodo.derecho:
            self.inorden(nodo.derecho, resultado)

        return resultado


    def postorden(self, nodo: Nodo = None):
        if nodo is None:
            nodo = self.raiz
        if nodo:
            self.postorden(nodo.izquierdo)
            self.postorden(nodo.derecho)
            print(f"({nodo.valor_x}, {nodo.valor_y})", end=" -> ")
    
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