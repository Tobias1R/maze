import numpy as np


class Vertice:
    """Classe para representar os vértices
    """
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        self.d=float('inf') 
        self.parente_x=None
        self.parente_y=None
        self.processado=False
        self.indice_na_pilha=None

def nodos_vizinhos(matriz,linha,coluna):
    """ Retorna lista com os nodos vizinhos existentes

    Args:
        matriz (nparray): matriz numpy 
        linha (int): indice linha
        coluna (int): indice coluna

    Returns:
        [list]: Lista com vizinhos acima, abaixo, direita e esquerda
    """
    
    shape=matriz.shape
    vizinhos=[]
    # Em todos, garantir que estão dentro do limite da matriz e ainda não
    # foram processados
    if linha > 0 and not matriz[linha-1][coluna].processado:
         vizinhos.append(matriz[linha-1][coluna])

    if linha < shape[0] - 1 and not matriz[linha+1][coluna].processado:
        vizinhos.append(matriz[linha+1][coluna])

    if coluna > 0 and not matriz[linha][coluna-1].processado:
        vizinhos.append(matriz[linha][coluna-1])

    if coluna < shape[1] - 1 and not matriz[linha][coluna+1].processado:
        vizinhos.append(matriz[linha][coluna+1])
        
    return vizinhos

def r_indexa_acima(pilha, index):
    """Heapsort parte superior da pilha


    Args:
        pilha (list): Pilha de prioridades
        index (int): índice do nodo de interesse

    Returns:
        [list]: Pilha de prioridades com novos índices
    """
    # retorna o proprio pilha quando o indice for menor igual zero
    if index <= 0:
        return pilha
    # index na metade da porção superior a esse index na pilha
    p_index=(index-1)//2
    # se a distância ao source do indice atual for menor que a distancia
    # do item na pilha no index p_index
    # caso positivo, invertem-se os valores na pilha  localizados por 
    # index e p_index e chama recursivamente essa função com o p_index
    # que agora contem o nodo de interesse
    if pilha[index].d < pilha[p_index].d:
            pilha[index], pilha[p_index]=pilha[p_index], pilha[index]
            pilha[index].indice_na_pilha=index
            pilha[p_index].indice_na_pilha=p_index
            _ = r_indexa_acima(pilha, p_index)
    return pilha
    
def r_indexa_abaixo(pilha, index):
    """Heapsort
        Ordena recursivamente os items na parte inferior da pilha
        a partir do índice do nodo de interesse(pilha[index]).

    Args:
        pilha (list): Pilha de prioridades
        index (int): índice do nodo de interesse

    Returns:
        [list]: Pilha de prioridades com novos índices
    """
    # o tamanho da pilha
    length=len(pilha)    
    indice_e=2*index+1
    indice_d=indice_e+1
    if indice_e >= length:
        return pilha
    if indice_e < length and indice_d >= length: 
        if pilha[index].d > pilha[indice_e].d:
            pilha[index], pilha[indice_e]=pilha[indice_e], pilha[index]
            pilha[index].indice_na_pilha=index
            pilha[indice_e].indice_na_pilha=indice_e
            pilha = r_indexa_abaixo(pilha, indice_e)
    else:
        small = indice_e
        if pilha[indice_e].d > pilha[indice_d].d:
            small = indice_d
        if pilha[small].d < pilha[index].d:
            pilha[index],pilha[small]=pilha[small],pilha[index]
            pilha[index].indice_na_pilha=index
            pilha[small].indice_na_pilha=small
            pilha = r_indexa_abaixo(pilha, small)
    return pilha

def calcula_distancia(matriz,u,v):
    """ Calcula a distância entre dois nodos
           

    Args:
        matriz (list): matriz com valores
        u (tuple(x,y)): nodo de interesse
        v (type(x,y)): vizinho

    Returns:
        float: distância entre dois nodos
    """
    #if not cor_igual(img,u,v,matriz):
    #    if vertice_em_separador(img,matriz,v):
    #        return 0.1
    
    d = 0.1
    nodo1_x = u[1]
    nodo1_y = u[0]

    nodo2_x = v[1]
    nodo2_y = v[0]
    
    valor1 = matriz[nodo1_y][nodo1_x]
    valor2 = matriz[nodo2_y][nodo2_x]

    if valor1 == -1:
        return 1

    if valor2 == 1:        
        d = 1000
    else:
        d = 1

    return d

def encontra_menor_caminho(img,src,dst,shape):
    """Encontra o menor caminho entre a origem e o destino
        * Estabelece pilha de prioridades
        * Define os pontos de origem e saida como x,y na matriz
        * Popula a matriz com objetos Vertice para representar
            os pixels [Dijkstra passos 1 e 2]
        [Dijkstra passo 3]
        * Ordena a pilha

    Args:
        img (list): Matriz com os valores, lista de lista
        src (tuple): Origem
        dst (tuple): Destino

    Returns:
        [list|False]: Lista com os nodos(y,x) do trajeto. Ou False
        se não encontrar
    """
    

    # pilha de prioridades
    prioridades=[] 
    # ponto de partida x, y
    origem_x=int(src[1])
    origem_y=int(src[0])
    # ponto de saida x, y
    saida_x=int(dst[1])
    saida_y=int(dst[0])
    
    
    linhas,colunas=shape
    # seta valores na matriz com os vertices referentes aos nodos
    
    matriz = np.full((linhas, colunas), None)    
    for r in range(linhas):
        for c in range(colunas):
            # seta novo vertice na matriz e adiciona sua posição na pilha
            # de prioridades
            matriz[r][c]=Vertice(c,r)
            matriz[r][c].indice_na_pilha=len(prioridades)
            prioridades.append(matriz[r][c])
    
    # seta a distância da origem para zero no nodo de origem
    # Sobre: ao iniciar o vértice aqui o nodo(matriz[src.x][src.y])
    # recebe o valor de inf (infinito), como ele é a origem ele vai ser 
    # o primeiro a ser processado. então sua distância para a origem é 
    # zero.
    
    matriz[origem_y][origem_x].d=0
    # r_indexa_acima com nodo de interesse = posição de partida
    # isso vai trazer o nodo de origem para o inicio da pilha 
    prioridades=r_indexa_acima(prioridades, 
        matriz[origem_y][origem_x].indice_na_pilha)    
    counter = 0
    while len(prioridades) > 0:
        counter += 1
        # processa os nodos da pilha
        # o nodo de interesse é sempre o primeiro da fila
        u=prioridades[0]
        # marca como processado
        u.processado=True
        # coloca o ultimo item da lista na primeira posição
        # (nodo de interesse)
        prioridades[0]=prioridades[-1]
        # marca novo index para nodo a ser analisado
        prioridades[0].indice_na_pilha=0
        # remove o nodo do fim da pilha 
        # (ele acabou de ser copiado para o inicio)
        prioridades.pop()
        # r_indexa_abaixo com nodo de interesse
        prioridades=r_indexa_abaixo(prioridades,0)
        # vizinhos do nodo de interesse na matriz
        vizinhos = nodos_vizinhos(matriz,u.y,u.x)        
        for v in vizinhos:
            # a distância entre os nodos
            dist=calcula_distancia(img,(u.y,u.x),(v.y,v.x))            
            if (u.d + dist < v.d):
                # os vértices são iniciados com d = infinito
                # a distância correta do vizinho é 
                # a distância entre o nodo atual e a origem + 
                # a distância entre o vizinho e o nodo atual
                v.d = u.d+dist
                # nodo parente para reconstruir o caminho
                v.parente_x=u.x
                v.parente_y=u.y                                
                # indice atual do vizinho
                idx=v.indice_na_pilha
                # re-orderna abaixo o vizinho na pilha
                prioridades=r_indexa_abaixo(prioridades,idx)
                # re-orderna acima o vizinho na pilha
                prioridades=r_indexa_acima(prioridades,idx)
    
    # lista com pontos a serem pintados                      
    path=[]
    # iterador vertical na matriz
    iter_v=matriz[saida_y][saida_x]  
    # o path é montado de modo reverso, então o primeiro ponto
    # é o ponto de saída do labirinto
    path.append((saida_x,saida_y))    
    while(iter_v.y!=origem_y or iter_v.x!=origem_x):
        # enquanto a coordenada do iterador vertical for diferente
        # da posição de inicio, adiciona a coordenada a ser pintada
        # e seta o próximo nodo do iterador vertical como o parent
        # do nodo atual.
        path.append((iter_v.x,iter_v.y))
        iter_v=matriz[iter_v.parente_y][iter_v.parente_x]
        if isinstance(iter_v,np.ndarray):
            # nao foi possivel encontrar o caminho            
            return False

    # o último ponto a ser pintado é o ponto de origem.
    path.append((origem_x,origem_y))
    return path