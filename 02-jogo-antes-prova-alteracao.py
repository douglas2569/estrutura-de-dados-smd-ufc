from abc import ABC, abstractmethod
from enum import IntEnum, unique
import random

@unique
class Sexo(IntEnum):
    F = 0
    M = 1

@unique
class Direcao(IntEnum):
    ESQUERDA = -1
    PARADO = 0
    DIREITA = 1

class Rio:
    def __init__(self, tamanho_rio: int):
        self.__controle_terra = [False] * tamanho_rio
        self.__rio = [Planta()] * tamanho_rio
        self.__popular_rio()

    def __popular_rio(self):        
        qtd_ursos = int(0.2 * len(self.__rio))
        qtd_peixes = int(0.4 * len(self.__rio))
        qtd_tocas = int(0.1 * len(self.__rio))
        self.__gerar(qtd_ursos, Urso)
        self.__gerar(qtd_peixes, Peixe)
        self.__gerar(qtd_tocas, Toca)

    def __gerar(self, qtd_elemento, elemento):
        if Terra() in self.__rio or Planta() in self.__rio:
            contador = 0
            while contador < qtd_elemento:
                posicao = random.randint(0, len(self.__rio) - 1)
                if self.__rio[posicao] == Planta() or self.__rio[posicao] == Terra(): 
                    if isinstance(elemento(), Peixe):
                        self.__rio[posicao] = elemento(random.randint(2,5))
                    elif isinstance(elemento(), Urso):
                        self.__rio[posicao] = elemento(random.randint(20,30))
                    else:
                        self.__rio[posicao] = elemento()
                                                               
                    contador += 1

    def fluir(self):
        for i in range(len(self.__rio)):
            if isinstance(self.__rio[i], Animal):  
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
        elif isinstance(self.__rio[nova], Planta) or isinstance(self.__rio[nova], Terra):  
            self.__rio[nova] = peixe

    def __colisao_urso(self, atual, nova):
        urso = self.__rio[atual]
        self.__controle_terra[atual] = True
        if urso.atacar(self.__rio[nova]):
            if urso.forca > self.__rio[nova].forca :
               self.__arrasar(atual, nova, urso) 
            elif urso.forca < self.__rio[nova].forca:
               self.__arrasar(nova, atual, self.__rio[nova]) 

        elif urso.reproduzir(self.__rio[nova]):
            self.__gerar(1, Urso)

        elif isinstance(self.__rio[nova], Peixe):
            direcao = nova - atual
            toca = nova + direcao
            if toca in range(len(self.__rio)) and isinstance(self.__rio[toca], Toca):
                if self.__rio[toca].vazia():
                    self.__rio[toca].entrar(self.__rio[nova])
            self.__arrasar(atual, nova, urso)
        elif not isinstance(self.__rio[nova], Toca):  
            self.__arrasar(atual, nova, urso)

    def __arrasar(self, atual, nova, urso):
        self.__rio[atual] = Terra()
        self.__rio[nova] = urso
        self.__controle_terra[nova] = True

    def __colisao_peixe(self, atual, nova):
        peixe = self.__rio[atual]
        if peixe.atacar(self.__rio[nova]):
            if peixe.forca > self.__rio[nova].forca:
               self.__arrasar(atual, nova, peixe) 
            elif peixe.forca < self.__rio[nova].forca :
               self.__arrasar(nova, atual, self.__rio[nova])                
        elif peixe.reproduzir(self.__rio[nova]):
            self.__gerar(1, Peixe)
        elif isinstance(self.__rio[nova], Urso):
            self.__controle_terra_arrasada(atual)
        elif isinstance(self.__rio[nova], Toca) and self.__rio[nova].vazia():
            self.__rio[nova].entrar(peixe)
            self.__controle_terra_arrasada(atual)
        else:  
            self.__rio[nova] = peixe
            self.__controle_terra_arrasada(atual)

    def __controle_terra_arrasada(self, posicao):
        if not self.__controle_terra[posicao]:
            self.__rio[posicao] = Planta()
        else:
            self.__rio[posicao] = Terra()

    def briga_territorio(self, atual, nova):
        ...

    def __str__(self):
        result = '|'
        for i in range(len(self.__rio)):
            result = result + self.__rio[i].__str__() + '|'
        return result


class Animal(ABC):
    def __init__(self, forca):        
        self.sexo = random.randint(0, 1) 
        self.forca = forca     

    
    def obter_direcao(self):
        return random.randint(Direcao.ESQUERDA, Direcao.DIREITA)

    
    def reproduzir(self, other):        
        result = False
        if self.__class__ == other.__class__ and self.sexo != other.sexo:
            result = True

        return result
    
    
    def atacar(self, other):        
        result = False
        if self.__class__ == other.__class__ and self.sexo == Sexo.M and other.sexo == Sexo.M:            
            result = True

        return result


class Urso(Animal):

    def comer(self, other):
        result = False
        if isinstance(other, Peixe):
            result = True
        return result    

    def __str__(self):
        if self.sexo == Sexo.F:
            return ' 🐻 ♀️ ' 
        else:
            return ' 🐻 ♂️' 


class Peixe(Animal):

    def __str__(self):
        if self.sexo == Sexo.F:
            return ' 🐟 ♀️' 
        else:
            return ' 🐟 ♂️'


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
        return ' 🟤 '

    def __eq__(self, other):
        result = False
        if isinstance(other, Terra):
            result = True
        return result


if __name__ == '__main__':  
    r = Rio(20)
    print(r)
    turnos = int(input("Insira a quantidade de turnos: "))
    turno = 0
    while turno < turnos:
        r.fluir()
        turno += 1
