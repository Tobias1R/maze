import itertools
from datetime import datetime
import labirinto_matriz
import sys

import os
# define o caminho BASE DIR
BASE_DIR = os.path.normpath(repr(os.getcwd()).replace('\'','')) 
sys.path.insert(0,BASE_DIR)

def trata_ponto_tupla(p):
    # p = (y,x)
    # retorna (x,y)
    ponto = (p[1], p[0])
    return str(ponto)

def trata_caminho(c):
    """ Retorna uma string de informação no formato
    "Origem: (x,y) Destino: (x,y)"

    Args:
        c (tuple): tupla de tuplas

    Returns:
        [type]: string
    """

    origem = c[0]
    destino = c[1]
    info = 'Origem: ('+str(origem[1])+', '+str(origem[0])+')'
    info += ' '
    info += 'Destino: ('+str(destino[1])+', '+str(destino[0])+')'
    return info

class Aplicativo:
    def __init__(self, arquivo) -> None:
        self.arquivo_matriz = arquivo
        # matriz do labirinto
        self.matriz_labirinto = []
        # caminhos encontrados
        self.caminhos = []
        # variavel para medir tempo de execução
        self.t1 = None
        
        # entradas encontradas
        self.entradas = []
        # saidas encontradas
        self.saidas = []
        # carrega matriz
        self.carrega_matriz()
    
    def formato_matriz(self):
        """Retorna o formato da matriz

        Returns:
            tuple: (linhas,colunas)
        """
        colunas = 0
        linhas = len(self.matriz_labirinto)
        if linhas > 0:
            linha0 = self.matriz_labirinto[0]
            colunas = len(linha0)

        return (linhas, colunas)
    
    def carrega_matriz(self):
        """Carrega a matriz
        
        Aqui espera-se uma matriz como a do gabarito enviado para o 
        exercício nos quesitos:
            \n separando linhas
            \t separando valores
            -1 entradas se a direita
            -1 saidas se a esquerda
             1 paredes
             0 piso
        """
        self.draw_path = False
        self.matriz_labirinto = []
        self.caminhos = []
        
        # arquivo matriz inicia como False
        if self.arquivo_matriz:
            # ja foi informado o arquivo.
            with open(self.arquivo_matriz, 'r') as arquivo:
                matriz_lida = arquivo.read()
            matriz = []

            linhas = matriz_lida.split('\n')

            for l in range(len(linhas)):
                linha = list(map(int, linhas[l].split('\t')))
                matriz.append(linha)

            self.matriz_labirinto = matriz
            self.entradas = self.identifica_entradas()
            self.saidas = self.identifica_saidas()
    
    def identifica_entradas(self,):
        """Identifica as entradas no labirinto

        Returns:
            list: Uma lista de Tuplas ou vazia
        """
        entradas = []

        linhas, colunas = self.formato_matriz()
        for i in range(linhas):
            linha = self.matriz_labirinto[i]
            valor = linha[colunas-1]

            if valor == -1:
                entradas.append((i, len(linha)-1))
        total = len(entradas)
        if total > 0:
            info = str(total) + ' entradas encontradas.'
        else:
            info = 'Nenhuma entrada encontrada.'
        print(info)
        return entradas
    
    def identifica_saidas(self):
        """Identifica as saídas do labirinto

        Returns:
            list: Uma lista de Tuplas ou vazia
        """
        saidas = []
        linhas, colunas = self.formato_matriz()
        for i in range(linhas):
            linha = self.matriz_labirinto[i]
            valor = linha[0]
            if valor == -1:
                saidas.append((i, 0))
        total = len(saidas)
        if total > 0:
            info = str(total) + ' saidas encontradas.'
        else:
            info = 'Nenhuma saída encontrada.'
        print(info)
        return saidas

    def menor_caminho(self):
        """ Os paths foram analisados pelos threads e se encontram
        na lista self.caminhos. 
        O menor caminho é o caminho que tem o menor numero de nodos.        

        Returns:
            list: Lista de pontos a serem desenhados.
        """
        menor = float("inf")
        menor_caminho = False
        for caminho in self.caminhos:
            if len(caminho) < menor:
                menor = len(caminho)
                menor_caminho = caminho
        return menor_caminho

    def resolve_labirinto(self):
        self.t1 = datetime.now()
        
        matriz = self.matriz_labirinto
        shape = self.formato_matriz()
        caminhos = list(
            itertools.product(
                self.entradas,
                self.saidas
            ))
        print('Resolvendo labirinto')
        for caminho in caminhos:
            path = False
            if caminho:
                origem = caminho[0]
                destino = caminho[1]
                path = labirinto_matriz.encontra_menor_caminho(
                    matriz, origem, destino, shape
                )
                if path:
                    print(
                    trata_caminho(caminho)+' Distância: '+str(len(path)))
                    self.caminhos.append(path)
                else:
                    print(
                        'Caminho não encontrado '+trata_caminho(caminho))
        print('CAMINHOS',len(caminhos))
        menor = self.menor_caminho()
        
        # a lista de path é formada de modo reverso
        # a entrada é o ultimo da lista, a saida o primeiro
        origem = str(menor[-1:][0])
        destino = str(menor[0])
        info = 'Menor trajeto: Origem:'
        info += origem + ' ->  Destino: ' + destino
        print(info)                
        t2 = datetime.now()
        print(
            'Tempo de execução: '+str(t2-self.t1))


    def print_log(self):
        pass


if __name__ == '__main__':
    args = sys.argv
    arquivo = args[1]
    arquivo_existe = False
    if '\\' in arquivo or '/' in arquivo:
        pass
    else:
        # tentar abrir o arquivo no diretorio de execução
        arquivo = os.path.join(BASE_DIR,arquivo)
        print('Tentando abrir:',arquivo)        
    if os.path.isfile(arquivo):
        app = Aplicativo(arquivo)
        app.resolve_labirinto()
    else:
        print('Favor informar um arquivo válido.')

    