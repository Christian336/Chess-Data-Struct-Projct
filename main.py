from flask import Flask
from flask import render_template, request
import chess
from chess import Board
import networkx
from networkx import DiGraph
from stockfish import Stockfish
import matplotlib.pyplot as plt
from collections import deque


app=Flask(__name__)

lances_feitos = []


@app.route('/')
def home():

    #Configurando a Engine
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    stockfish.set_depth(10)
    stockfish.set_skill_level(20)

    # Função para calcular a sequência de melhores lances

    def monta_grafo(grafo, profundidade, lances, hash, seq, exe):
        if profundidade == 0:
            return 0
        else:
            tabuleiro = Board()
            for l in lances:
                tabuleiro.push_san(l)
            stockfish.set_fen_position(tabuleiro.fen())
            best = stockfish.get_best_move()
            if best == None:
                return 0
            grafo.add_node(best)
            grafo.add_edge(lances[-1], best)
            if best in hash.keys():
                hash[best][seq] = exe
            else:
                hash[best] = []
                for i in hash[lances[-1]]:
                    hash[best].append(0)
                hash[best][seq] = exe

            monta_grafo(grafo, profundidade - 1, lances + [best], hash, seq, exe + 1)

    # Função para fazer com que mais de uma sequência seja calculada
    def melhores_sequencias_lances(grafo, profundidade, lances, quantidade):
        tabuleiro = Board()
        hash = {}
        for l in lances:
            tabuleiro.push_san(l)
        stockfish.set_fen_position(tabuleiro.fen())
        l = stockfish.get_top_moves(quantidade)
        best_moves = []
        for d in l:
            best_moves.append(d['Move'])
            grafo.add_node(d['Move'])
            hash[d['Move']] = []
            for i in l:
                hash[d['Move']].append(0)
        seq = 0
        for m in best_moves:
            hash[m][best_moves.index(m)] = 1
            monta_grafo(grafo, profundidade - 1, lances + [m], hash, seq, 2)
            seq += 1
        return hash

    # Função que retorna os vértices apontados
    def vertices(grafo, lance):
        l = []
        for t in grafo.edges():
            if t[0] == lance:
                l.append(t[1])
        return l

    # Função Busca em Largura
    def busca_largura(grafo, origem, hash, seq, saida):
        p = 0
        visitados = set()
        fila = deque()

        visitados.add(origem)
        fila.append(origem)

        while fila:
            vertice = fila.popleft()
            if p == 1:
                saida += " ,"
            saida += vertice
            p = 1

            for vizinho in grafo.neighbors(vertice):
                if vizinho not in visitados and hash[vizinho][seq] != 0:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return saida

    # Função para printar todas as sequências a partir do grafo:
    def print_seq(grafo, hash, seq, saida):
        for s in range(seq):
            saida += str(s+1)+'.'
            saida += busca_largura(grafo, list(grafo.nodes())[s], hash, s, " ")
            saida += ";\n"
        return saida

    board = chess.Board()
    grafo = DiGraph()
    profundidade = 5
    sequencias = 5


    count = 0
    cor = 'Brancas'


    #print(board)
    possibilidades = []
    for l in board.legal_moves:
        possibilidades.append(str(l))
    # print(possibilidades)
    val = int(stockfish.get_evaluation()['value']) * 0.01
    # print(val) #Valores Incorretos
    hash = melhores_sequencias_lances(grafo, profundidade, lances_feitos, sequencias)
    #print(hash)
    # Plotar o grafo
    plt.figure(figsize=(10, 10))
    pos = networkx.spring_layout(grafo)
    networkx.draw_networkx(grafo, pos, with_labels=True, node_size=1000, node_color='lightgreen',
                           edge_color='black', linewidths=1.5)

    plt.title('Grafo de melhores lances')
    plt.axis('off')
    #plt.show()
    plt.savefig("static/grafo.jpg")

    #print('Nós: ', grafo.nodes)
    #print('Número de nós = ', grafo.number_of_nodes())

    #print('Arestas: ', grafo.edges)
    #print('Número de arestas = ', grafo.number_of_edges())

    saida=""

    saida = print_seq(grafo, hash, sequencias, saida)

    return render_template('page.html', saida = saida, lances_feitos = "")

@app.route('/home', methods=['POST'])
def home2():

    #Configurando a Engine
    stockfish = Stockfish("stockfish-windows-2022-x86-64-avx2.exe")
    stockfish.set_depth(10)
    stockfish.set_skill_level(20)

    # Função para calcular a sequência de melhores lances

    def monta_grafo(grafo, profundidade, lances, hash, seq, exe):
        if profundidade == 0:
            return 0
        else:
            tabuleiro = Board()
            for l in lances:
                tabuleiro.push_san(l)
            stockfish.set_fen_position(tabuleiro.fen())
            best = stockfish.get_best_move()
            if best == None:
                return 0
            grafo.add_node(best)
            grafo.add_edge(lances[-1], best)
            if best in hash.keys():
                hash[best][seq] = exe
            else:
                hash[best] = []
                for i in hash[lances[-1]]:
                    hash[best].append(0)
                hash[best][seq] = exe

            monta_grafo(grafo, profundidade - 1, lances + [best], hash, seq, exe + 1)

    # Função para fazer com que mais de uma sequência seja calculada
    def melhores_sequencias_lances(grafo, profundidade, lances, quantidade):
        tabuleiro = Board()
        hash = {}
        for l in lances:
            tabuleiro.push_san(l)
        stockfish.set_fen_position(tabuleiro.fen())
        l = stockfish.get_top_moves(quantidade)
        best_moves = []
        for d in l:
            best_moves.append(d['Move'])
            grafo.add_node(d['Move'])
            hash[d['Move']] = []
            for i in l:
                hash[d['Move']].append(0)
        seq = 0
        for m in best_moves:
            hash[m][best_moves.index(m)] = 1
            monta_grafo(grafo, profundidade - 1, lances + [m], hash, seq, 2)
            seq += 1
        return hash

    # Função que retorna os vértices apontados
    def vertices(grafo, lance):
        l = []
        for t in grafo.edges():
            if t[0] == lance:
                l.append(t[1])
        return l

    # Função Busca em Largura
    def busca_largura(grafo, origem, hash, seq, saida):
        p = 0
        visitados = set()
        fila = deque()

        visitados.add(origem)
        fila.append(origem)

        while fila:
            vertice = fila.popleft()
            if p == 1:
                saida += " ,"
            saida += vertice
            p = 1

            for vizinho in grafo.neighbors(vertice):
                if vizinho not in visitados and hash[vizinho][seq] != 0:
                    visitados.add(vizinho)
                    fila.append(vizinho)
        return saida

    # Função para printar todas as sequências a partir do grafo:
    def print_seq(grafo, hash, seq, saida):
        for s in range(seq):
            saida += str(s+1)+'.'
            saida += busca_largura(grafo, list(grafo.nodes())[s], hash, s, " ")
            saida += ";\n"
        return saida

    board = chess.Board()
    grafo = DiGraph()
    profundidade = 5
    sequencias = 5

    count = 0
    cor = 'Brancas'


    lance = request.form.get('lance')
    lances_feitos.append(lance)
    print(lance)
    print(lances_feitos)

    #print(board)
    possibilidades = []
    for l in board.legal_moves:
        possibilidades.append(str(l))
    # print(possibilidades)
    val = int(stockfish.get_evaluation()['value']) * 0.01
    # print(val) #Valores Incorretos
    hash = melhores_sequencias_lances(grafo, profundidade, lances_feitos, sequencias)
    #print(hash)
    # Plotar o grafo
    plt.figure(figsize=(10, 10))
    pos = networkx.spring_layout(grafo)
    networkx.draw_networkx(grafo, pos, with_labels=True, node_size=1000, node_color='lightgreen',
                           edge_color='black', linewidths=1.5)

    plt.title('Grafo de melhores lances')
    plt.axis('off')
    #plt.show()
    plt.savefig("static/grafo.jpg")

    #print('Nós: ', grafo.nodes)
    #print('Número de nós = ', grafo.number_of_nodes())

    #print('Arestas: ', grafo.edges)
    #print('Número de arestas = ', grafo.number_of_edges())

    saida=""

    saida = print_seq(grafo, hash, sequencias, saida)

    return render_template('page.html', saida = saida, lances_feitos = lances_feitos)

if __name__ == "__main__":
    app.run()