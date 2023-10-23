from abc import ABC, abstractmethod


class ListADT(ABC):

    @abstractmethod
    def insert(self, indice, elemento):
        """Insere na posição <indice> o valor <elemento>.
        Como se trata de uma lista, deve ser graratido que
        se houver valor em <indice> que ele não seja apagado"""
        ...

    @abstractmethod
    def remove(self, elemento):
        """Remove primeira ocorrência de <elemento>"""
        ...

    @abstractmethod
    def count(self, elemento):
        """Conta a quantidade de <elemento> na lista"""
        ...

    @abstractmethod
    def clear(self):
        """Apaga a lista"""
        ...

    @abstractmethod
    def index(self, elemento):
        """Retorna o primeiro índice de <elemento>"""
        ...

    @abstractmethod
    def length(self):
        """Retorna o tamanho da lista"""
        ...


class Node:

    def __init__(self, element=None, next=None):
        self.__element = element
        self.__next = next

    def get_next(self):
        return self.__next

    def set_next(self, next):
        self.__next = next

    def get_element(self):
        return self.__element

    def __str__(self):
        return '|' + self.__element.__str__() + '|'


class LinkedList(ListADT):

    def __init__(self, elem=None):
        if elem:
            self._head = Node(elem)  # Atenção ao manipular esta referência
            self._tail = self._head  # Facilita a inserção no fim da lista
            self._length = 1
        else:
            self._head = None  # Atenção ao manipular esta referência
            self._tail = None  # Facilita a inserção no fim da lista
            self._length = 0

    def insert(self, index, elem):
        # a inserção pode acontecer em três locais: início, meio e fim da lista
        # separei em métodos diferentes (privados) para facilitar o entendimento
        if index == 0:  # primeiro local de inserção é no começo da lista
            self.__insert_at_beginning(elem)
        elif index > self._length:  # segundo local de inserção é no fim da lista
            self.__insert_at_end(elem)  # se o índice passado foi maior que o tamanho da lista, insero no fim
        else:  # por fim, a inserção no meio da lista
            self.__insert_in_between(index, elem)

        self._length += 1  # após inserido, o tamanho da lista é modificado

    def __insert_at_beginning(self, elem):
        n = Node(elem)  # primeiro criamos o nó com o elemento a ser inserido
        if self.empty():  # caso particular da lista vazia
            self.__empty_list_insertion(n)
        else:  # se houver elemento na lista
            n.set_next(self._head)  # o head atual passa a ser o segundo elemento
            self._head = n  # e o novo nó criado passa a ser o novo head

    def __insert_at_end(self, elem):
        n = Node(elem)  # primeiro criamos o nó com o elemento a ser inserido
        if self.empty():  # caso particular da lista vazia
            self.__empty_list_insertion(n)
        else:
            self._tail.set_next(n)  # o último elemento da lista aponta para o nó criado
            self._tail = n  # o nó criado ...a a ser o último elemento

    def __empty_list_insertion(self, node):
        # na inserçõa na lista vazia, head e tail apontam para o nó
        self._head = node
        self._tail = node

    def __insert_in_between(self, index, elem):  # 3
        n = Node(elem)  # primeiro criamos o nó com o elemento a ser inserido
        pos = 0  # a partir daqui vamos localizar a posição de inserção
        aux = self._head  # variável auxiliar para nos ajudar na configuração da posição do novo nó
        while pos < index - 1:  # precorre a lista até a posição imediatamente anterior
            aux = aux.get_next()  # à posição onde o elemento será inserido
            pos += 1
        n.set_next(aux.get_next())  # quando a posição correta tiver sido alcançada, insere o nó
        aux.set_next(n)

    def remove(self, elem):
        if not self.empty():  # Só pode remover se a lista não estiver vazia, não é?!
            aux = self._head
            removed = False  # Flag que marca quando a remoção foi feita
            if aux.get_element() == elem:  # Caso especial: elemento a ser removido está no head
                self._head = aux.get_next()  # head passa a ser o segundo elemento da lista
            else:
                while aux.get_next() and not removed:  # verifico se estamos no fim da lista e não foi removido elemento
                    prev = aux
                    aux = aux.get_next()  # passoo para o próximo elemento
                    if aux.get_element() == elem:  # se for o elemento desejado, removo da lista
                        prev.set_next(aux.get_next())
                        removed = True  # marco que foi removido

            if removed:
                self._length -= 1

    def count(self, elem):
        counter = 0
        if not self.empty():  # Verifica se a lista não está vazia (só faz sentido contar em linear não vazias!)
            aux = self._head  # Se a lista não estiver vazia, percorre a lista contando as ocorrências
            if aux.get_element() is elem:
                counter += 1
            while aux.get_next():  # precorrendo a lista....
                aux = aux.get_next()
                if aux.get_element() is elem:
                    counter += 1
        return counter

    def clear(self):
        self._head = None  # todos os nós que compunham a lista serão removidos da memória pelo coletor de lixo
        self._tail = None
        self._length = 0

    def index(self, elem):
        result = None
        pos = 0
        aux = self._head
        # Vamos percorrer a lista em busca de elem
        while not result and pos < self._length:  # lembrando que not None é o mesmo que True
            if aux.get_element() is elem:
                result = pos
            aux = aux.get_next()
            pos += 1
        return result  # se o elemento não estiver na lista, retorna None

    def length(self):
        return self._length

    def empty(self):
        result = False
        if not self._head:
            result = True
        return result

    def __str__(self):
        if not self.empty():
            result = ''
            aux = self._head
            result += aux.__str__()
            while aux.get_next():
                aux = aux.get_next()
                result += aux.__str__()
            return result
        else:
            return '||'


class DoublyLinkedList(ListADT):
    class _DoublyNode:

        def __init__(self, elem, prev, next):
            self._elem = elem
            self._prev = prev
            self._next = next

        def __str__(self):
            if self._elem is not None:
                return str(self._elem) + ' '
            else:
                return '|'

    def __init__(self):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._length = 0

    def insert(self, index, elem):
        if index >= self._length:  # se o indice se inserção passado for maior que a lista
            index = self._length  # atualiza para o último indice
        if self.empty():  # Caso da lista vazia
            new_node = self._DoublyNode(elem, self._header, self._trailer)
            self._header._next = new_node
            self._trailer._prev = new_node
        elif index == 0:  # caso da inserção na primeira posição da lista
            new_node = self._DoublyNode(elem, self._header, self._header._next)
            self._header._next._prev = new_node
            self._header._next = new_node
        else:  # outros casos de inserção
            this = self._header._next
            successor = this._next
            pos = 0
            while pos < index - 1:
                this = successor
                successor = this._next
                pos += 1
            new_node = self._DoublyNode(elem, this, successor)
            this._next = new_node
            successor._prev = new_node

        self._length += 1

    def remove(self, elemento):
        if not self.empty():
            node = self._header._next
            pos = 0
            found = False
            while not found and pos < self._length:
                if node._elem == elemento:
                    found = True
                else:
                    node = node._next
                    pos += 1
            if found:
                node._prev._next = node._next
                node._next._prev = node._prev
                self._length -= 1

    def count(self, elem):
        result = 0
        this = self._header._next
        if self._length > 0:
            while this._next is not None:  # aqui a lista é percorrida
                if this._elem == elem:
                    result += 1
                this = this._next
        return result

    def clear(self):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._length = 0

    def index(self, elem):
        result = None  # armazena a primeira posição do elemento
        pos = 0
        aux = self._header._next
        # Vamos percorrer a lista em busca de elem
        while not result and pos < self._length:  # lembrando que not None é o mesmo que True
            if aux._elem is elem:
                result = pos
            aux = aux._next
            pos += 1
        return result  # se o elemento não estiver na lista, retorna None

    def length(self):
        return self._length

    def empty(self):
        return self._length == 0

    def __str__(self):
        if not self.empty():
            result = ''
            aux = self._header
            result += aux.__str__()
            while aux._next:
                aux = aux._next
                result += aux.__str__()
            return result
        else:
            return '||'


if __name__ == '__main__':
    print('Linked List')
    lista = LinkedList()
    print(lista)

    print('inserção')
    lista.insert(0, 'teste')
    print(lista)

    lista.insert(20, 20)
    print(lista)

    lista.insert(0, 3.14)
    print(lista)

    lista.insert(1, 'no meio')
    print(lista)

    lista.insert(3, 'no meio')
    print(lista)

    lista.insert(10000, 'loooonge')
    print(lista)

    print('contagem')
    print(lista.count('no meio'))
    print(lista.count('oi'))
    print(lista.count(20))

    print('indices')
    print(lista.index('no meio'))
    print(lista.index('loooonge'))
    print(lista.index('bla'))
    print('remoção')

    print('lista inicial')
    print(lista)

    print('vamos remover...')
    lista.remove('no meio')
    print(lista)

    lista.remove('teste')
    print(lista)

    lista.remove(3.14)
    print(lista)
    print('-----------------------------')
    print()
    print('-----------------------------')
    print('Doubly Linked List')
    lista = DoublyLinkedList()
    lista.insert(0, 0)
    print(lista)
    lista.insert(1, 1)
    print(lista)
    lista.insert(2, 2)
    print(lista)
    lista.insert(0, 3)
    print(lista)
    lista.insert(1000, 4)
    print(lista)
    lista.insert(3, 5)
    print(lista)
    print(lista.index(1))
    print(lista.count(1))
    lista.insert(0, 1)
    print(lista.count(1))
    lista.remove(5)
    print(lista)
