import random
import json
import numpy as np
from sklearn.decomposition import PCA
from django.shortcuts import render

# Dados do problema (fixos conforme sua tabela)
num_itens = 10
capacity = 10
weights  = [4, 1, 3, 2, 1, 0.5, 1, 0.3, 2, 1]
benefits = [3, 1.5, 2, 1, 0.8, 0.2, 0.5, 0.3, 0.4, 1]

# --- Função de avaliação ---
def evaluate_individual(individual):
    total_weight = sum(individual[i] * weights[i] for i in range(num_itens))
    total_benefit = sum(individual[i] * benefits[i] for i in range(num_itens))
    if total_weight > capacity:
        fitness = 0
    else:
        fitness = total_benefit
    return fitness, total_weight, total_benefit

# --- Funções do Algoritmo Evolutivo ---
def generate_individual():
    return [random.choice([0, 1]) for _ in range(num_itens)]

def generate_population(pop_size):
    return [generate_individual() for _ in range(pop_size)]

def roulette_selection(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0:
        return random.choice(population)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fit in zip(population, fitnesses):
        current += fit
        if current >= pick:
            return individual

def crossover(parent1, parent2, crossover_rate=0.9):
    if random.random() < crossover_rate:
        point = random.randint(1, num_itens - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    else:
        child1, child2 = parent1[:], parent2[:]
    return child1, child2

def mutate(individual, mutation_rate=0.1):
    return [1 - bit if random.random() < mutation_rate else bit for bit in individual]

def repair_individual(individual):
    fitness_value, total_weight, total_benefit = evaluate_individual(individual)
    while total_weight > capacity:
        worst_ratio = float('inf')
        index_to_remove = None
        for i in range(num_itens):
            if individual[i] == 1:
                ratio = benefits[i] / weights[i]
                if ratio < worst_ratio:
                    worst_ratio = ratio
                    index_to_remove = i
        if index_to_remove is None:
            break
        individual[index_to_remove] = 0
        fitness_value, total_weight, total_benefit = evaluate_individual(individual)
    return individual

def create_new_population(population, crossover_rate=0.9, mutation_rate=0.1):
    new_population = []
    fitnesses = [evaluate_individual(ind)[0] for ind in population]
    while len(new_population) < len(population):
        parent1 = roulette_selection(population, fitnesses)
        parent2 = roulette_selection(population, fitnesses)
        child1, child2 = crossover(parent1, parent2, crossover_rate)
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        child1 = repair_individual(child1)
        child2 = repair_individual(child2)
        new_population.append(child1)
        if len(new_population) < len(population):
            new_population.append(child2)
    return new_population

# Função para executar o algoritmo evolutivo completo
def run_evolution(pop_size=50, max_generations=100):
    population = generate_population(pop_size)
    best_fitness_evolution = []
    populations_by_generation = {}  # Armazena a população de cada geração
    
    for generation in range(max_generations):
        # Armazena cópia da população atual para projeção
        populations_by_generation[generation+1] = [ind[:] for ind in population]
        fitnesses = [evaluate_individual(ind)[0] for ind in population]
        best_fitness = max(fitnesses)
        best_fitness_evolution.append(best_fitness)
        population = create_new_population(population)
    
    # Seleciona o melhor indivíduo da população final
    fitnesses = [evaluate_individual(ind)[0] for ind in population]
    best_index = fitnesses.index(max(fitnesses))
    best_individual = population[best_index]
    final_fitness, final_weight, final_benefit = evaluate_individual(best_individual)
    
    # Calcula a projeção PCA de forma consistente para todas as gerações
    all_individuals = []
    for gen in range(1, max_generations+1):
        all_individuals.extend(populations_by_generation[gen])
    all_individuals_np = np.array(all_individuals)
    pca = PCA(n_components=2)
    pca.fit(all_individuals_np)
    
    # Para cada geração, projeta os indivíduos para 2D
    projection_data = {}
    best_points = {}
    for gen in range(1, max_generations+1):
        pop = np.array(populations_by_generation[gen])
        projected = pca.transform(pop)
        points = [{"x": float(pt[0]), "y": float(pt[1])} for pt in projected]
        projection_data[gen] = points
        # Identifica o melhor indivíduo dessa geração
        fitnesses_gen = [evaluate_individual(ind)[0] for ind in populations_by_generation[gen]]
        max_fit = max(fitnesses_gen)
        best_idx = fitnesses_gen.index(max_fit)
        best_points[gen] = points[best_idx]
    
    evolution_data = {
        "generations": list(range(1, max_generations+1)),
        "best_fitness": best_fitness_evolution,
    }
    result = {
        "best_individual": best_individual,
        "final_fitness": final_fitness,
        "final_weight": final_weight,
        "final_benefit": final_benefit,
    }
    projection = {
        "points": projection_data,
        "best": best_points,
    }
    return evolution_data, projection, result

# --- View Principal ---
def index(request):
    context = {}
    max_generations = 100
    if request.method == "POST":
        evolution_data, projection, result = run_evolution(pop_size=50, max_generations=max_generations)
        context["evolution_data_json"] = json.dumps(evolution_data)
        context["projection_data_json"] = json.dumps(projection)
        context["result"] = result
        context["max_generations"] = max_generations
        context["executed"] = True
    else:
        context["executed"] = False
    return render(request, "evolution/index.html", context)
