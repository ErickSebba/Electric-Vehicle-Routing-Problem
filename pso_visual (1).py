
import tkinter as tk
from tkinter import Text, END
import random
import matplotlib.pyplot as plt

def gerar_posicoes_clientes(num_clientes):
    return {i: (random.randint(0, 100), random.randint(0, 100)) for i in range(num_clientes)}

def fitness(solucao, distancias):
    veiculos = {}
    for i, veiculo in enumerate(solucao):
        if veiculo not in veiculos:
            veiculos[veiculo] = []
        veiculos[veiculo].append(i)
    custo_total = 0
    for rota in veiculos.values():
        for i in range(len(rota) - 1):
            custo_total += distancias[rota[i]][rota[i+1]]
    return custo_total

def inicializar_particulas(num_particulas, num_clientes, num_veiculos):
    return [[random.randint(1, num_veiculos) for _ in range(num_clientes)] for _ in range(num_particulas)]

def pso(num_particulas, num_geracoes, num_clientes, num_veiculos, distancias, w, c1, c2):
    particulas = inicializar_particulas(num_particulas, num_clientes, num_veiculos)
    melhores_locais = particulas.copy()
    fitness_melhores_locais = [fitness(p, distancias) for p in melhores_locais]
    melhor_global = melhores_locais[fitness_melhores_locais.index(min(fitness_melhores_locais))]
    fitness_melhor_global = min(fitness_melhores_locais)
    
    historico_fitness = [fitness_melhor_global]

    for _ in range(num_geracoes):
        for i, particula in enumerate(particulas):
            velocidade = [random.uniform(-1, 1) * w for _ in range(num_clientes)]
            for j in range(len(particula)):
                r1 = random.random()
                r2 = random.random()
                if r1 < c1:
                    particula[j] = melhores_locais[i][j]
                elif r2 < c2:
                    particula[j] = melhor_global[j]
            for j in range(len(particula)):
                velocidade[j] = w * velocidade[j] + c1 * random.uniform(0, 1) * (melhores_locais[i][j] - particula[j]) + c2 * random.uniform(0, 1) * (melhor_global[j] - particula[j])
                particula[j] += int(velocidade[j])
                particula[j] = max(1, min(particula[j], num_veiculos))
            if fitness(particula, distancias) < fitness_melhores_locais[i]:
                melhores_locais[i] = particula.copy()
                fitness_melhores_locais[i] = fitness(particula, distancias)
            if fitness_melhores_locais[i] < fitness_melhor_global:
                melhor_global = particula.copy()
                fitness_melhor_global = fitness_melhores_locais[i]
        historico_fitness.append(fitness_melhor_global)

    return melhor_global, historico_fitness

def exibir_resultado_visual(melhor_rota, posicoes, num_veiculos):
    cores = ['red', 'blue', 'green', 'orange', 'purple']
    for veiculo in range(1, num_veiculos + 1):
        clientes = [i for i, v in enumerate(melhor_rota) if v == veiculo]
        coords = [posicoes[c] for c in clientes]
        if coords:
            xs, ys = zip(*coords)
            plt.plot(xs, ys, marker='o', label=f'Veículo {veiculo}', color=cores[veiculo % len(cores)])
    for i, (x, y) in posicoes.items():
        plt.text(x+1, y+1, str(i), fontsize=8)
    plt.title("Rota final por veículo")
    plt.legend()
    plt.grid(True)
    plt.show()

def exibir_evolucao_fitness(historico):
    plt.plot(historico)
    plt.title("Evolução do custo (fitness) ao longo das gerações")
    plt.xlabel("Geração")
    plt.ylabel("Custo")
    plt.grid(True)
    plt.show()

def executar_pso():
    num_particulas = 20
    num_geracoes = 100
    num_clientes = 20
    num_veiculos = 2
    w = 0.5
    c1 = 1
    c2 = 1
    distancias = [[random.randint(1, 100) if i != j else 0 for j in range(num_clientes)] for i in range(num_clientes)]
    posicoes = gerar_posicoes_clientes(num_clientes)

    melhor_rota, historico = pso(num_particulas, num_geracoes, num_clientes, num_veiculos, distancias, w, c1, c2)
    custo_total = fitness(melhor_rota, distancias)
    rotas_encontradas.append((melhor_rota, custo_total))
    texto_resultado.delete(1.0, END)
    texto_resultado.insert(tk.INSERT, "Rotas encontradas:\n")
    for i, (rota, custo) in enumerate(rotas_encontradas):
        texto_resultado.insert(tk.INSERT, f"Rota {i+1}: {rota} - Custo: {custo}\n")

    exibir_evolucao_fitness(historico)
    exibir_resultado_visual(melhor_rota, posicoes, num_veiculos)

janela = tk.Tk()
janela.title("PSO para Roteamento de Veículos")
texto_resultado = Text(janela, height=20, width=80)
texto_resultado.pack()
rotas_encontradas = []
botao_executar = tk.Button(janela, text="Executar PSO", command=executar_pso)
botao_executar.pack()
janela.mainloop()
