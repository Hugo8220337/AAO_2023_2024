import numpy as np
from numba import njit
from algoritmos.GreedyAlgorithm import greedy_uflp

@njit
def calculate_cost(solution, cost_matrix, facility_costs):
    """
    Calcula o custo total da solução atual.

    Parameters:
    solution (np.array): Array booleano que indica se a instalação está aberta.
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.

    Returns:
    float: Custo total da solução.
    """
    num_clients, num_facilities = cost_matrix.shape
    cost = 0.0
    # Calcula o custo de transporte
    for client in range(num_clients):
        min_cost = np.inf
        for facility in range(num_facilities):
            if solution[facility]:  # Verifica se a instalação está aberta
                cost_val = cost_matrix[client, facility]
                if cost_val < min_cost:
                    min_cost = cost_val
        cost += min_cost

    # Adiciona o custo de abertura das instalações
    cost += np.sum(solution * facility_costs)
    return cost

@njit
def is_solution_in_tabu_list(solution, tabu_list):
    """
    Verifica se a solução atual está na lista tabu.

    Parameters:
    solution (np.array): Solução atual.
    tabu_list (np.array): Lista tabu que contém as soluções proibidas.

    Returns:
    bool: True se a solução está na lista tabu, False caso contrário.
    """
    for tabu_solution in tabu_list:
        if np.array_equal(solution, tabu_solution):
            return True
    return False

@njit(parallel=True)
def tabu_search_core(cost_matrix, facility_costs, initial_solution, max_iterations=100, tabu_tenure=5):
    """
    Núcleo da pesquisa tabu para refinar a solução inicial.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    initial_solution (np.array): Solução inicial fornecida pelo algoritmo de greedy.
    max_iterations (int): Número máximo de iterações para a pesquisa.
    tabu_tenure (int): Número de soluções a serem mantidas na lista tabu.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """
    num_clients, num_facilities = cost_matrix.shape
    current_solution = initial_solution.copy()
    current_cost = calculate_cost(current_solution, cost_matrix, facility_costs)
    best_solution = current_solution.copy()
    best_cost = current_cost
    tabu_list = np.zeros((tabu_tenure, num_facilities), dtype=np.bool_)
    tabu_list_ptr = 0 # pointer para a posição atual na tabu list

    for iteration in range(max_iterations):
        neighborhood = []

        # Gera vizinhos alterando o estado de cada instalação
        for facility in range(num_facilities):
            neighbor = current_solution.copy()
            neighbor[facility] = not neighbor[facility]
            if not is_solution_in_tabu_list(neighbor, tabu_list):
                neighbor_cost = calculate_cost(neighbor, cost_matrix, facility_costs)
                neighborhood.append((neighbor, neighbor_cost))

        # Seleciona o melhor movimento não-tabu
        if neighborhood:
            neighborhood.sort(key=lambda x: x[1])  # Ordena os vizinhos pelo custo
            for neighbor, neighbor_cost in neighborhood:
                if neighbor_cost < best_cost:
                    best_solution = neighbor.copy()
                    best_cost = neighbor_cost
                    break

            # Atualiza a solução atual e o custo
            current_solution = best_solution.copy()
            current_cost = best_cost

            # Atualiza a lista tabu
            tabu_list[tabu_list_ptr % tabu_tenure] = current_solution.copy() 
            tabu_list_ptr += 1
            # tabu_list_ptr % tabu_tenure é  Calcula o índice na tabu_list onde a solução atual será armazenada. Isso garante que o índice esteja sempre dentro dos limites da tabu_list.

    return best_solution, best_cost

def tabu_search_uflp(cost_matrix, facility_costs, max_iterations=100, tabu_tenure=5):
    """
    Aplica a pesquisa tabu para resolver o problema de localização de instalações sem capacidade.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    max_iterations (int): Número máximo de iterações para a pesquisa.
    tabu_tenure (int): Número de soluções a serem mantidas na lista tabu.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """
    # Converte facility_costs para um array do numpy
    facility_costs = np.array(facility_costs, dtype=np.float64)
    
    # Inicia o algoritmo com uma solução inicial do algoritmo de greedy
    facilities_open, initial_cost = greedy_uflp(cost_matrix, facility_costs)
    initial_solution = np.array(facilities_open, dtype=np.bool_)

    # Chama o núcleo da pesquisa tabu otimizado
    best_solution, best_cost = tabu_search_core(cost_matrix, facility_costs, initial_solution, max_iterations, tabu_tenure)

    return best_solution, best_cost