import random
import matplotlib.pyplot as plt
import networkx as nx
import math

# Gerar posições aleatórias para cidades e postos
def gerar_posicoes(num_cidades, num_postos):
    total = num_cidades + num_postos
    posicoes = {i: (random.randint(0, 100), random.randint(0, 100)) for i in range(total)}
    postos = set(random.sample(range(total), num_postos))
    return posicoes, postos

# Calcular distância euclidiana entre as posições
def calcular_distancias(posicoes):
    total = len(posicoes)
    distancias = [[0] * total for _ in range(total)]
    for i in range(total):
        for j in range(total):
            if i != j:
                xi, yi = posicoes[i]
                xj, yj = posicoes[j]
                distancias[i][j] = math.hypot(xj - xi, yj - yi)
    return distancias

# Função de avaliação (fitness)
def fitness(rotação, distancias, postos, autonomia_maxima):
    autonomia = autonomia_maxima
    custo_total = 0
    num_postos_usados = 0
    penalidade = 1000

    for i in range(len(rotação) - 1):
        atual = rotação[i]
        proximo = rotação[i + 1]
        distancia = distancias[atual][proximo]

        if distancia > autonomia:
            custo_total += penalidade
        else:
            autonomia -= distancia
            custo_total += distancia
            if proximo in postos:
                autonomia = autonomia_maxima
                num_postos_usados += 1

    return custo_total + num_postos_usados * 10

# Inicialização da população
def inicializar_populacao(num_particulas, num_cidades):
    return [random.sample(range(num_cidades), num_cidades) for _ in range(num_particulas)]

# PSO adaptado
def pso(num_particulas, num_geracoes, num_cidades, distancias, postos, autonomia_maxima):
    populacao = inicializar_populacao(num_particulas, num_cidades)
    melhor_global = min(populacao, key=lambda p: fitness(p, distancias, postos, autonomia_maxima))
    historico = [fitness(melhor_global, distancias, postos, autonomia_maxima)]

    for _ in range(num_geracoes):
        for i in range(num_particulas):
            nova_particula = populacao[i][:]
            idx1, idx2 = random.sample(range(num_cidades), 2)
            nova_particula[idx1], nova_particula[idx2] = nova_particula[idx2], nova_particula[idx1]

            if fitness(nova_particula, distancias, postos, autonomia_maxima) < fitness(populacao[i], distancias, postos, autonomia_maxima):
                populacao[i] = nova_particula

        candidato = min(populacao, key=lambda p: fitness(p, distancias, postos, autonomia_maxima))
        if fitness(candidato, distancias, postos, autonomia_maxima) < fitness(melhor_global, distancias, postos, autonomia_maxima):
            melhor_global = candidato

        historico.append(fitness(melhor_global, distancias, postos, autonomia_maxima))

    return melhor_global, historico

# Mostrar todos os gráficos lado a lado
def exibir_tres_graficos(posicoes, distancias, postos, autonomia_maxima, historico, rota):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # Gráfico 1: Grafo de ligações
    G = nx.Graph()
    for i, (x, y) in posicoes.items():
        tipo = 'posto' if i in postos else 'cidade'
        G.add_node(i, pos=(x, y), tipo=tipo)

    for i in range(len(posicoes)):
        for j in range(i + 1, len(posicoes)):
            if distancias[i][j] <= autonomia_maxima:
                G.add_edge(i, j, weight=round(distancias[i][j], 1))

    pos = {i: (x, y) for i, (x, y) in posicoes.items()}
    tipos = nx.get_node_attributes(G, 'tipo')
    for tipo, forma in {'posto': 's', 'cidade': 'o'}.items():
        nos = [n for n in G.nodes() if tipos[n] == tipo]
        nx.draw_networkx_nodes(G, pos, nodelist=nos,
                               node_color=['red' if tipo == 'posto' else 'skyblue'],
                               node_shape=forma, ax=axs[0], label=tipo)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=axs[0])
    nx.draw_networkx_labels(G, pos, font_size=8, ax=axs[0])
    axs[0].set_title("Grafo de Conexões")
    axs[0].axis('off')

    # Gráfico 2: Evolução do Fitness
    axs[1].plot(historico)
    axs[1].set_title("Evolução do Fitness")
    axs[1].set_xlabel("Geração")
    axs[1].set_ylabel("Fitness")
    axs[1].grid(True)

    # Gráfico 3: Rota Final
    xs, ys = zip(*[posicoes[i] for i in rota])
    axs[2].plot(xs, ys, marker='o', linestyle='-', color='blue')
    for i, (x, y) in posicoes.items():
        cor = 'red' if i in postos else 'black'
        axs[2].text(x + 1, y + 1, str(i), fontsize=8, color=cor)
    axs[2].set_title("Rota Final do Veículo")
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

# Execução principal
def executar():
    num_cidades = 40
    num_postos = 15
    num_particulas = 30
    num_geracoes = 100
    autonomia_maxima = 70

    posicoes, postos = gerar_posicoes(num_cidades, num_postos)
    distancias = calcular_distancias(posicoes)
    melhor_rota, historico = pso(num_particulas, num_geracoes, num_cidades, distancias, postos, autonomia_maxima)

    exibir_tres_graficos(posicoes, distancias, postos, autonomia_maxima, historico, melhor_rota)
    return melhor_rota

rota_final = executar()
rota_final


