from arbol.arbol_avl import ArbolAVL

if __name__ == "__main__":
    arbol = ArbolAVL()
    valores = [20,15,10,25,30,35,23,18,28,32]
    
    for valor in valores:
        arbol.insertar(valor)
    
    print("Árbol AVL después de las inserciones:")
    arbol.imprimirArbol(arbol.raiz)  
    # Debería mostrar los valores en orden
    # Aquí podrías agregar más operaciones para probar el árbol AVL
    # como eliminar nodos, buscar nodos, etc.