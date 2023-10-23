""" Escreva um programa em Python que simula um ecosistema.
Este ecosistema consiste de um rio, modelado como uma lista,
que contém dois tipos de animais: ursos e peixes.

No ecosistema, cada elemento da lista deve ser um objeto do
tipo Urso, Peixe ou None (que indica que a posição do rio
está vazia).

A cada rodada do jogo, baseada em um processo aleatório, cada
animal tenta se mover para uma posição da lista adjacente (a
esquerda ou direita) ou permanece na sua mesma posição.

Se dois animais do mesmo tipo colidirem (urso com urso ou peixe com peixe),
eles permanecem em suas posições originais, mas uma nova instância do
animal deve ser posicionada em um local vazio, aleatoriamente determinado.

Se um Urso e um peixe colidirem, entretanto, o peixe morre."""

from abc import ABC, abstractmethod
from enum import IntEnum, unique
import random


@unique
class Direcao(IntEnum):
    ESQUERDA = -1
    PARADO = 0
    DIREITA = 1


identifier: int = 0  # apenas debug


class Rio:

    def __init__(self, tamanho_rio: int):
        self.__controle_terra = [False] * tamanho_rio
        self.__rio = [Planta()] * tamanho_rio
        self.__popular_rio()

    def __popular_rio(self):
        """ No ecosistema, cada elemento da lista deve ser um objeto do
        tipo Urso, Peixe, Planta (que indica que a posição do rio está
        vazia) ou None (que indica que posição do rio é 'terra arrasada')."""
        qtd_ursos = int(0.2 * len(self.__rio))
        qtd_peixes = int(0.4 * len(self.__rio))
        qtd_tocas = int(0.1 * len(self.__rio))
        self.__gerar(qtd_ursos, Urso)
        self.__gerar(qtd_peixes, Peixe)
        self.__gerar(qtd_tocas, Toca)

    def __gerar(self, qtd_animal, elemento):
        if Terra() in self.__rio or Planta() in self.__rio:
            bicho = 0
            while bicho < qtd_animal:
                posicao = random.randint(0, len(self.__rio) - 1)
                if self.__rio[posicao] == Planta() or self.__rio[posicao] == Terra():
                    self.__rio[posicao] = elemento()
                    bicho += 1

    def fluir(self):
        for i in range(len(self.__rio)):
            if isinstance(self.__rio[i], Animal):  # apenas animais se movem
                animal = self.__rio[i]
                direcao = animal.obter_direcao()
                nova = i + direcao
                if i != nova and not nova < 0 and not nova >= len(self.__rio):
                    self.__colidir(i, nova)
            elif isinstance(self.__rio[i], Toca) and not self.__rio[i].vazia():
                animal = self.__rio[i].sair()
                direcao = animal.obter_direcao()
                nova = i + direcao
                if i != nova and not nova < 0 and not nova >= len(self.__rio):
                    self.__colidir(i, nova)
                else:
                    self.__rio[i].entrar(animal)
        print(self)

    def __colidir(self, atual, nova):
        if isinstance(self.__rio[atual], Urso):
            self.__colisao_urso(atual, nova)
        elif isinstance(self.__rio[atual], Peixe):
            self.__colisao_peixe(atual, nova)
        elif isinstance(self.__rio[atual], Toca):
            if not self.__rio[atual].vazia():
                self.__colisao_peixe_na_toca(atual, nova)

    def __colisao_peixe_na_toca(self, atual, nova):
        peixe = self.__rio[atual].sair()
        if peixe.reproduzir(self.__rio[nova]):
            self.__gerar(1, Peixe)
            self.__rio[atual].entrar(peixe)
        elif isinstance(self.__rio[nova], Toca):
            if self.__rio[nova].vazia():
                self.__rio[nova].entrar(peixe)
            else:
                self.__rio[atual].entrar(peixe)
        elif isinstance(self.__rio[nova], Planta) or isinstance(self.__rio[nova], Terra):  # planta ou terra
            self.__rio[nova] = peixe

    def __colisao_urso(self, atual, nova):
        urso = self.__rio[atual]
        self.__controle_terra[atual] = True
        if urso.reproduzir(self.__rio[nova]):
            self.__gerar(1, Urso)
        elif isinstance(self.__rio[nova], Peixe):
            direcao = nova - atual
            toca = nova + direcao
            if toca in range(len(self.__rio)) and isinstance(self.__rio[toca], Toca):
                if self.__rio[toca].vazia():
                    self.__rio[toca].entrar(self.__rio[nova])
            self.__arrasar(atual, nova, urso)
        elif not isinstance(self.__rio[nova], Toca):  # se for planta ou terra
            self.__arrasar(atual, nova, urso)

    def __arrasar(self, atual, nova, urso):
        self.__rio[atual] = Terra()
        self.__rio[nova] = urso
        self.__controle_terra[nova] = True

    def __colisao_peixe(self, atual, nova):
        peixe = self.__rio[atual]
        if peixe.reproduzir(self.__rio[nova]):
            self.__gerar(1, Peixe)
        elif isinstance(self.__rio[nova], Urso):
            self.__controle_terra_arrasada(atual)
        elif isinstance(self.__rio[nova], Toca) and self.__rio[nova].vazia():
            self.__rio[nova].entrar(peixe)
            self.__controle_terra_arrasada(atual)
        else:  # planta ou terra
            self.__rio[nova] = peixe
            self.__controle_terra_arrasada(atual)

    def __controle_terra_arrasada(self, posicao):
        if not self.__controle_terra[posicao]:
            self.__rio[posicao] = Planta()
        else:
            self.__rio[posicao] = Terra()

        """if self.__rio[nova] and isinstance(self.__rio[nova], Peixe):  # peixe
            if isinstance(self.__rio[atual], Urso):  # and self.__rio[atual].comer(self.__rio[nova]):  # urso x peixe
                self.__substituir_animal(nova, atual)

            elif self.__rio[atual].reproduzir(self.__rio[nova]):  # peixe x peixe
                self.__gerar(1, Peixe)

        elif self.__rio[nova] and isinstance(self.__rio[nova], Urso):  # Urso
            if self.__rio[atual].reproduzir(self.__rio[nova]):  # urso X urso
                
            else:
                self.__substituir_animal(atual, nova)
        else:
            self.__substituir_animal(nova, atual)
            # urso x nada
            # peixe x nada
            # peixe x urso
"""

    def __str__(self):
        result = '|'
        for i in range(len(self.__rio)):
            result = result + self.__rio[i].__str__() + '|'
        return result


class Animal(ABC):

    def obter_direcao(self):
        return random.randint(Direcao.ESQUERDA, Direcao.DIREITA)

    @abstractmethod
    def reproduzir(self, other):
        # TODO TESTAR
        result = False
        if self.__class__ == other.__class__:
            result = True

        return result


class Urso(Animal):

    def __init__(self):
        global identifier
        self.__id = identifier
        identifier += 1

    def comer(self, other):
        result = False
        if isinstance(other, Peixe):
            result = True

        return result

    def reproduzir(self, other):
        result = False
        if isinstance(other, Urso):
            result = True

        return result

    def __str__(self):
        return ' 🐻 '  # +str(self.__id)


class Peixe(Animal):

    def __init__(self):
        global identifier
        self.__id = identifier
        identifier += 1

    def reproduzir(self, other):
        result = False
        if isinstance(other, Peixe):
            result = True

        return result

    def __str__(self):
        return ' 🐟 '  # +str(self.__id)


class Planta:

    def __str__(self):
        return ' 🌿 '

    def __eq__(self, other):
        result = False
        if isinstance(other, Planta):
            result = True
        return result


class Toca:

    def __init__(self):
        self.__vazia = True
        self.__peixe = None

    def vazia(self):
        return self.__vazia

    def entrar(self, obj):
        if isinstance(obj, Peixe) and self.__vazia:
            self.__vazia = False
            self.__peixe = obj

    def sair(self):
        if not self.__vazia:
            self.__vazia = True
            return self.__peixe

    def __str__(self):
        return ' 🍙 '


class Terra:

    def __str__(self):
        return ' T '

    def __eq__(self, other):
        result = False
        if isinstance(other, Terra):
            result = True
        return result


if __name__ == '__main__':  # programa
    r = Rio(20)
    print(r)
    turnos = int(input("Insira a quantidade de turnos: "))
    turno = 0
    while turno < turnos:
        r.fluir()
        turno += 1
