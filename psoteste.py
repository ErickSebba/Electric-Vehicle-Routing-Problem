import tkinter as tk
from tkinter import scrolledtext
from tkinter import END
import random
import numpy as np

# Função para inicializar partículas binárias
def inicializar_particulas(num_particulas, num_cidades):
    return [[random.randint(0, 1) for _ in range(num_cidades)] for _ in range(num_particulas)]

# Função de fitness com verificação de cobertura e autonomia
def fitness(particula, distancias, X, penalidade=1000):
    num_postos = sum(particula)
    penalidade_total = 0
    
    for cidade in range(len(particula)):
        if particula[cidade] == 1:
            continue  # Cidade já tem posto
        
        coberto = False
        for vizinha in range(len(particula)):
            if vizinha != cidade and particula[vizinha] == 1 and distancias[cidade][vizinha] <= X:
                coberto = True
                break
        
        if not coberto:
            penalidade_total += penalidade  # Penalidade por cidade não coberta
    
    return num_postos + penalidade_total

# PSO binário adaptado para otimização de postos
def pso(num_particulas, num_geracoes, num_cidades, distancias, X, w=0.5, c1=1.49445, c2=1.49445):
    particulas = inicializar_particulas(num_particulas, num_cidades)
    melhores_locais = [p.copy() for p in particulas]
    fitness_melhores = [fitness(p, distancias, X) for p in particulas]
    melhor_global = particulas[np.argmin(fitness_melhores)].copy()
    fitness_global = min(fitness_melhores)
    
    for _ in range(num_geracoes):
        for i in range(num_particulas):
            velocidade = [random.uniform(-3, 3) for _ in range(num_cidades)]
            
            # Atualiza velocidade
            for j in range(num_cidades):
                r1 = random.random()
                r2 = random.random()
                velocidade[j] = (w * velocidade[j] + 
                                c1 * r1 * (melhores_locais[i][j] - particulas[i][j]) + 
                                c2 * r2 * (melhor_global[j] - particulas[i][j]))
            
            # Atualiza posição usando sigmoide
            for j in range(num_cidades):
                prob = 1 / (1 + np.exp(-velocidade[j]))
                particulas[i][j] = 1 if random.random() < prob else 0
            
            # Atualiza melhores locais e global
            fit_atual = fitness(particulas[i], distancias, X)
            if fit_atual < fitness_melhores[i]:
                melhores_locais[i] = particulas[i].copy()
                fitness_melhores[i] = fit_atual
                
                if fit_atual < fitness_global:
                    melhor_global = particulas[i].copy()
                    fitness_global = fit_atual
    
    return melhor_global

# Lista para histórico de soluções
historico_solucoes = []

def executar_pso():
    num_particulas = 30
    num_geracoes = 200
    num_cidades = 10
    X = 50  # Autonomia máxima
    
    # Matriz de distâncias com cidades isoladas (999 = sem conexão direta)
    distancias = [
        [0, 30, 45, 999, 999, 60, 999, 999, 999, 999],  # Cidade 0
        [30, 0, 20, 55, 999, 999, 999, 999, 999, 999],  # Cidade 1
        [45, 20, 0, 999, 999, 999, 999, 999, 999, 999], # Cidade 2
        [999, 55, 999, 0, 40, 999, 999, 999, 999, 999], # Cidade 3
        [999, 999, 999, 40, 0, 35, 999, 999, 999, 999], # Cidade 4
        [60, 999, 999, 999, 35, 0, 999, 999, 999, 999],# Cidade 5 (isolada)
        [999, 999, 999, 999, 999, 999, 0, 60, 999, 999],# Cidade 6 (isolada)
        [999, 999, 999, 999, 999, 999, 60, 0, 50, 999], # Cidade 7
        [999, 999, 999, 999, 999, 999, 999, 50, 0, 30],  # Cidade 8
        [999, 999, 999, 999, 999, 999, 999, 999, 30, 0], # Cidade 9
    ]
    
    melhor = pso(num_particulas, num_geracoes, num_cidades, distancias, X)
    
    # Cálculo de métricas
    postos = sum(melhor)
    cidades_nao_cobertas = 0
    total_km = 0
    
    for cidade in range(num_cidades):
        if melhor[cidade] == 1:
            continue  # Cidade é um posto
        
        min_dist = X + 1  # Inicializa com valor maior que a autonomia
        for vizinha in range(num_cidades):
            if melhor[vizinha] == 1 and distancias[cidade][vizinha] <= X:
                if distancias[cidade][vizinha] < min_dist:
                    min_dist = distancias[cidade][vizinha]
        
        if min_dist <= X:
            total_km += min_dist
        else:
            cidades_nao_cobertas += 1
    
    historico_solucoes.append((melhor, postos, cidades_nao_cobertas, total_km))

    # Exibição dos resultados
    texto_resultado.delete(1.0, END)
    texto_resultado.insert(tk.INSERT, "Melhor distribuição de postos:\n")
    texto_resultado.insert(tk.INSERT, f"Postos instalados: {melhor}\n")
    texto_resultado.insert(tk.INSERT, f"Total de postos: {postos}\n")
    texto_resultado.insert(tk.INSERT, f"Cidades não cobertas: {cidades_nao_cobertas}\n")
    texto_resultado.insert(tk.INSERT, f"Quilômetros totais percorridos: {total_km} km\n\nHistórico:\n")
    
    for idx, (sol, p, nc, km) in enumerate(historico_solucoes):
        texto_resultado.insert(tk.INSERT, f"Execução {idx+1}: Postos={p}, Não cobertas={nc}, KM={km}\n")

# Interface gráfica
janela = tk.Tk()
janela.title("Otimização de Postos de Recarga")
janela.geometry("600x400")

botao_executar = tk.Button(janela, text="Executar PSO", command=executar_pso)
botao_executar.pack(pady=10)

texto_resultado = scrolledtext.ScrolledText(janela, width=70, height=20, wrap=tk.WORD)
texto_resultado.pack(padx=10, pady=10)

janela.mainloop()