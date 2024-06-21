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
            # Se a instalação estiver aberta
            if solution[facility]:
                cost_val = cost_matrix[client, facility]
                if cost_val < min_cost:
                    min_cost = cost_val
        cost += min_cost

    # Adiciona o custo de abertura das instalações
    cost += np.sum(solution * facility_costs)
    return cost

@njit
def swap_heuristic_local_search(cost_matrix, facility_costs, initial_solution):
    """
    Local Search Swap.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    initial_solution (np.array): Solução inicial fornecida pelo greedy algorithm.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """

    num_clients, num_facilities = cost_matrix.shape
    current_solution = initial_solution.copy()
    current_cost = calculate_cost(current_solution, cost_matrix, facility_costs) # Calcula o custo inicial
    improved = True

    while improved:
        improved = False
        best_neighbor = current_solution.copy() # Inicializa o melhor vizinho como a solução atual
        best_cost = current_cost

        # Tenta trocar o estado de cada par de instalações
        for facility1 in range(num_facilities):
            for facility2 in range(facility1 + 1, num_facilities):
                neighbor = current_solution.copy()
                neighbor[facility1] = not neighbor[facility1]  # Mudar o estado da instalação 1
                neighbor[facility2] = not neighbor[facility2]  # Mudar o estado da instalação 2
                neighbor_cost = calculate_cost(neighbor, cost_matrix, facility_costs)  # Calcula o custo do vizinho

                # Verifica se a nova solução é melhor
                if neighbor_cost < best_cost:
                    best_cost = neighbor_cost
                    best_neighbor = neighbor.copy()
                    improved = True
        
        if improved:
            current_solution = best_neighbor.copy() # Atualiza a solução atual para a melhor solução encontrada
            current_cost = best_cost

    return current_solution, current_cost

def swap_heuristic_uflp(cost_matrix, facility_costs):
    # converter facility_costs para um array em numpy
    facility_costs = np.array(facility_costs, dtype=np.float64)
    
    # Comçar com uma solução inicial do algoritmo de greedy
    facilities_open, initial_cost = greedy_uflp(cost_matrix, facility_costs)
    initial_solution = np.array(facilities_open, dtype=np.bool_)

    # Começar o Swap local Search
    best_solution, best_cost = swap_heuristic_local_search(cost_matrix, facility_costs, initial_solution)

    return best_solution, best_cost