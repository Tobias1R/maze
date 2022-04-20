"""Labirinto
    [Sobre o app]
    O aplicativo visa aprensentar solução gráfica para um problema do 
    tipo labirinto. 

    [Conceito de labirinto]
        1."vasta construção onde uma rede de salas e galerias se 
        entrecruzam de tal maneira que fica difícil encontrar a saída."
        2.emaranhado de caminhos
    Com o conceito em mente espera-se então uma matriz que defina paredes
    com um valor, o piso em outro, representando-os visualmente sob uma 
    perspectiva perpendicular ao plano de desenho.

    [Idéia da solução]
    O algoritmo de Dijskstra visa solucionar o problema do caminho mais 
    curto em um gráfico direcional. A matriz a ser analisada pode ser 
    interpretada como gráfico direcional, se considerarmos cada nodo
    como um vértice e associar arestas, com valores definidos pelas dife-
    renças de valores entre os nodos vizinhos. Partindo do ponto de origem
    definido como entrada, o algoritmo vai seguir nodo a nodo da matriz
    computando o tamanho das arestas e armazenando a distância do vértice
    até a origem, assim como o nodo(parente) utilizado como base para o 
    cálculo dessa distância. Ao final do processo, todos os nodos, 
    conterão informações da distância até o nodo origem e o seu parente.
    Um desses nodos é nosso nodo de interesse na reconstrução do trajeto,
    o nodo de destino, identificado como saida, tem agora informação
    sobre quem é o seu parente, o trajeto já ordenado pela menor distância.
    Então para reconstruir o trajeto basta seguir os parentes do parente
    do nodo de destino.
    Para isso é necessário computador todos os trajetos definidos pela
    grandeza de entradas*saidas. O menor caminho é aquele que passou pelo
    menor número de nodos da matriz.

    [Sobre o código]
    A matriz é lida de um arquivo texto e transformada em numpy array
    para iniciar o 
    
    Com a matriz populada, o algoritmo instancia os vértices e os empilha
    na lista de prioridades(min-heap) para manter registro dos nodos não 
    processados. 
    Todos os vértices são iniciados com a distância até a origem como 
    infinito.
    O nodo de origem recebe valor zero de distância e passa ser o 
    primeiro nodo de interesse.
    Partindo dele é necessário reindexar a pilha de prioridades para 
    levar o ponto de origem para o início da pilha.
        
    Agora que o primeiro nodo foi estabelecido, inicia-se o processo
    de relaxamento das arestas com seus respectivos vizinhos.
    A aresta é mensurada definindo valores de distância 0.1 para valores
    na matriz que representem o piso(0) e valor 1000 para nodos que 
    representem parede(1). 
        
    Para cada vizinho que tiver a distância até o ponto de origem maior
    que a (distancia do seu vizinho até a origem mais a distância entre 
    eles), precisa ser reindexado(heapsort). Após esse processo cada 
    vértice na matriz conterá a menor distância entre ele a origem e a 
    posição do nodo parente.
    
    O caminho pode então ser definido reversamente seguindo os nodos
    parente a partir do ponto de destino, uma vez que eles ja foram
    ordenados pela menor distância até a origem.

    [Interface]
    A interface foi construída em QT6, contém 1 widget para apresentação
    da interface como janela, um widget para servir de paint device
    onde a imagem representativa da matriz será exibida, 1 botão para 
    selecionar novo arquivo com matriz, 1 botão para executar solução do
    labirinto 4 labels para informações.


"""

import sys
import traceback

from PySide6.QtCore import (
    QEvent, QObject,  QRect, QThreadPool,
    Signal, Slot, QRunnable
)
from PySide6.QtGui import (
    QBrush, QColor,  QPaintDevice, QPainter, QPen,
    Qt
)
from PySide6.QtWidgets import (
    QApplication, QFileDialog,  QWidget
)

import itertools
from datetime import datetime
import labirinto_matriz
import interfaceui_matriz


def trata_ponto_tupla(p):
    # p = (y,x)
    # retorna (x,y)
    ponto = (p[1], p[0])
    return str(ponto)


class Worker(QRunnable):
    '''
    Worker thread

    Herda de QRunnable para a configuração do thread.

    :param callback: O callback de função a ser executado 
                    neste thread de trabalho. Args fornecidos e
                    kwargs serão passados para o runner.

    :param args: Argumentos para passar a função callback
    :param kwargs: Keywords para passar a função callback

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # iniciais
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # adiciona callback aos kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Inicializa o runner e passa os argumentos
        '''
        # Obtem e passa os argumentos para a função
        try:
            result = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit(
                (exctype, value, traceback.format_exc()))
        else:
            # retorna
            self.signals.result.emit(result)
        finally:
            # fim do thread
            self.signals.finished.emit()


class WorkerSignals(QObject):
    '''
    Signals utilizados pelo runner

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(str)


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


class Janela(QWidget):
    """ Janela principal do app.

    Implementa:
        QWidget : Qt6.
    """

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)

        # caminho do arquivo de imagem do labirinto
        self.arquivo_matriz = False
        # matriz do labirinto
        self.matriz_labirinto = []
        # caminhos encontrados
        self.caminhos = []
        # variavel para medir tempo de execução
        self.t1 = None
        # thread pool
        self.thread_pool = QThreadPool(self)
        # total de threads
        self.total_threads = 3
        # o caminho a ser desenhado
        # iniciado como False
        self.draw_path = False
        # carrega interface criada com QtCreator
        self.form = interfaceui_matriz.Ui_Form()
        self.form.setupUi(self)
        # conecta evento "clicked" do botão de executar 
        # com função local
        self.form.controle_executa.clicked.connect(
                self.resolve_labirinto)
        # inicia como desabilitado
        self.form.controle_executa.setDisabled(True)
        # carrega matriz
        self.carrega_matriz()
        # instala filtro de evento para o widget container da pixmap
        self.form.widgetImagem.installEventFilter(self)
        # conecta botao abrir nova imagem
        self.form.toolButton.clicked.connect(self.seleciona_nova_matriz)


    def seleciona_nova_matriz(self):
        """ Mostra QDialog para selecionar novo arquivo
        """
        qf = QFileDialog(self)
        qf.setFileMode(QFileDialog.FileMode.ExistingFiles)
        qf.setNameFilters(['*.txt'])
        if qf.exec():
            arquivo = qf.selectedFiles()
            if arquivo:
                self.form.controle_executa.setEnabled(True)
                self.arquivo_matriz = arquivo[0]
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
        ao carregar a matriz ela será automaticamente pintada no widget.

        Aqui espera-se uma matriz como a seguir:
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
            self.form.widgetImagem.update()
            self.form.controle_executa.setEnabled(True)

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
        self.form.lb_info_entradas.setText(info)
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
        self.form.lb_info_saidas.setText(info)
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

    def solucao_result(self, r):
        """Callback para o retorno do thread

        Args:
            r (list|bool): path ou False
        """
        if r:
            # pinta o menor caminho
            self.caminhos.append(r)
            if len(self.caminhos) == (
                    len(self.entradas)*len(self.saidas)):
                menor = self.menor_caminho()
                # só setar o caminho a ser desenhado. Ele vai ser 
                # pintado do EventFilter do widget
                self.draw_path = menor
                # a lista de path é formada de modo reverso
                # a entrada é o ultimo da lista, a saida o primeiro
                origem = str(menor[-1:][0])
                destino = str(menor[0])
                info = 'Menor trajeto: Origem:'
                info += origem + ' ->  Destino: ' + destino
                self.form.lb_resultado.setText(info)                
                t2 = datetime.now()
                self.form.log.appendPlainText(
                    'Tempo de execução: '+str(t2-self.t1))
                self.form.widgetImagem.update()
        else:
            self.form.log.appendPlainText('Não encontrou o caminho')

    def solucao_thread_finished(self,):
        """Callback do fim do thread
        """
        print('thread finished')

    def solucao_progress(self, s):
        """ Callback do progress do worker que está resolvendo o 
        labirinto

        Args:
            s (str): Informação a ser mostrada no log
        """
        self.form.log.appendPlainText(str(s))

    def resolve_labirinto(self):
        """ Handler do click no botão executa.
            Inicia o pool e o worker que vai resolver o labirinto
        """
        self.t1 = datetime.now()
        pool = self.thread_pool
        pool.setMaxThreadCount(self.total_threads)
        caminhos = list(
            itertools.product(
                self.entradas,
                self.saidas
            ))
        self.form.log.appendPlainText(
            'Caminhos possíveis: '+str(len(caminhos)))

        for caminho in caminhos:
            # para cada caminho inicia um thread.
            # QThreadPool vai empilhar eles e resolver conforme a variável
            # self.total_threads
            worker = Worker(self.resolve_multithread)
            worker.signals.result.connect(self.solucao_result)
            worker.signals.finished.connect(self.solucao_thread_finished)
            worker.signals.progress.connect(self.solucao_progress)
            worker.kwargs['caminho'] = caminho
            pool.start(worker)

    def resolve_multithread(self, progress_callback=None, caminho=None):
        """ Essa função executa em um thread separado da interface
        para encontrar os caminhos na imagem.

        Args:
            progress_callback (Signal): Sinal para informar progresso.
            caminho (tuple): tupla de tuplas com ((origem),(destino))

        Returns:
            list/bool: lista caso tenha encontrado o caminho, False se não
            encontrou
        """

        matriz = self.matriz_labirinto
        shape = self.formato_matriz()
        path = False
        if caminho:
            origem = caminho[0]
            destino = caminho[1]
            path = labirinto_matriz.encontra_menor_caminho(
                matriz, origem, destino, shape
            )
            if path:
                progress_callback.emit(
                    trata_caminho(caminho)+' Distância: '+str(len(path)))
            else:
                progress_callback.emit(
                    'Caminho não encontrado '+trata_caminho(caminho))

        return path

    def desenha_matriz(self, device: QPaintDevice):
        """Desenha a matriz no widget

        Args:
            device (QPaintDevice): objeto que será pintado

        """

        painter = QPainter(device)

        # cores
        cor_piso = QColor(0, 255, 255)
        cor_outro = QColor(100, 20, 254)
        cor_parede = QColor(0, 0, 0)
        cor_path = QColor(139, 236, 80)

        shape = self.formato_matriz()

        linhas = shape[0]
        colunas = shape[1]

        matriz = self.matriz_labirinto
        # tamanho do container onde a imagem vai ser pintada
        width = device.width()
        # 20 de margem
        tamanho_nodo = (width - 20) // colunas

        # brushs
        brush_piso = QBrush()
        brush_piso.setColor(cor_piso)
        brush_piso.setStyle(Qt.SolidPattern)
        pen = QPen()

        brush_parede = QBrush()
        brush_parede.setColor(cor_parede)
        brush_parede.setStyle(Qt.SolidPattern)

        brush_path = QBrush()
        brush_path.setColor(cor_path)
        brush_path.setStyle(Qt.SolidPattern)

        brush_outro = QBrush()
        brush_outro.setColor(cor_outro)
        brush_outro.setStyle(Qt.SolidPattern)


        for l in range(linhas):
            for c in range(colunas):
                valor = matriz[l][c]
                if valor == -1:
                    valor = 0
                if int(valor) == 1:
                    brush = brush_parede
                elif int(valor) == 0:
                    brush = brush_piso
                else:
                    brush = brush_outro

                # se tiver caminho a ser pintado
                if self.draw_path:
                    # o draw_path é uma lista de tuplas
                    # contendo os nodos que fazem parte do trajeto.
                    t = (c, l)
                    if t in self.draw_path:
                        # se a coordenada esta no trajeto
                        # usa a o brush com a cor do trajeto.
                        brush = brush_path

                # calcula o tamanho do nodos a serem pintados
                left = l * tamanho_nodo
                top = c * tamanho_nodo
                width = tamanho_nodo
                height = tamanho_nodo
                # figura geometrica a ser pintada
                rect = QRect(top, left, width, height)

                # seta pen e brush no painter
                pen.setWidth(0)
                painter.setBrush(brush)
                painter.setPen(pen)

                # pinta o quadrado
                painter.fillRect(rect, brush)
                painter.drawRect(rect)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """ Event Filter do widget
            Filtro de evento para manter pintado no widget a imagem
            e o caminho traçado.
        Args:
            watched (QObject): objeto Qt que gerou o evento
            event (QEvent): Evento emitido

        Returns:
            bool: retorna essa função da super class
        """
        if (watched == self.form.widgetImagem
                and event.type() == QEvent.Paint):
            if self.matriz_labirinto:
                self.desenha_matriz(watched)
        return super().eventFilter(watched, event)


if __name__ == '__main__':
    # inicia aplicativo Qt
    app = QApplication(sys.argv)
    # instancia e mostra widget da janela.
    janela = Janela(None)
    janela.show()
    # executa applicativo 
    sys.exit(app.exec())
