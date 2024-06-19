import numpy as np
from numba import njit, prange
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

@njit(parallel=True)
def local_search(cost_matrix, facility_costs, initial_solution):
    """
    Realiza a pesquisa local a partir de um swap

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    initial_solution (np.array): Solução inicial fornecida pelo algoritmo de greedy.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """
    num_clients, num_facilities = cost_matrix.shape
    current_solution = initial_solution.copy()  # Copia a solução inicial
    current_cost = calculate_cost(current_solution, cost_matrix, facility_costs)  # Calcula o custo inicial
    improved = True

    while improved:
        improved = False
        best_neighbor = current_solution.copy()  # Inicializa o melhor vizinho como a solução atual
        best_cost = current_cost

        # Tenta trocar o estado de cada par de instalações
        for facility1 in prange(num_facilities):  # Utiliza paralelismo para acelerar a execução
            for facility2 in range(facility1 + 1, num_facilities):
                neighbor = current_solution.copy()
                neighbor[facility1] = not neighbor[facility1]  # Troca o estado da instalação 1
                neighbor[facility2] = not neighbor[facility2]  # Troca o estado da instalação 2
                neighbor_cost = calculate_cost(neighbor, cost_matrix, facility_costs)  # Calcula o custo do vizinho

                # Verifica se a nova solução é melhor
                if neighbor_cost < best_cost:
                    best_cost = neighbor_cost
                    best_neighbor = neighbor.copy()
                    improved = True
        
        if improved:
            current_solution = best_neighbor.copy()  # Atualiza a solução atual para a melhor solução encontrada
            current_cost = best_cost

    return current_solution, current_cost

@njit
def generate_candidate_solution(current_solution):
    """
    Gera uma nova solução candidata a partir da solução atual, fazendo alterações substanciais.

    Parameters:
    current_solution (np.array): Solução atual.

    Returns:
    np.array: Nova solução candidata.
    """
    num_facilities = len(current_solution)
    candidate_solution = current_solution.copy()
    for _ in range(num_facilities // 5):  # Faz alterações substanciais trocando 20% das instalações
        facility = np.random.randint(num_facilities)
        candidate_solution[facility] = not candidate_solution[facility]
    return candidate_solution

def filter_and_fan(cost_matrix, facility_costs, initial_solution, max_iterations=50, num_candidates=5):
    """
    Aplica o algoritmo Filter and Fan para refinar a solução inicial.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    initial_solution (np.array): Solução inicial fornecida pelo algoritmo de greedy.
    max_iterations (int): Número máximo de iterações para a pesquisa.
    num_candidates (int): Número de candidatos a serem gerados em cada iteração.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """
    current_solution, current_cost = local_search(cost_matrix, facility_costs, initial_solution)
    
    for iteration in range(max_iterations):
        candidates = []
        for _ in range(num_candidates):
            candidate_solution = generate_candidate_solution(current_solution)
            candidate_solution, candidate_cost = local_search(cost_matrix, facility_costs, candidate_solution)
            candidates.append((candidate_solution, candidate_cost))
        
        # Seleciona a melhor solução candidata
        best_candidate_solution, best_candidate_cost = min(candidates, key=lambda x: x[1])
        
        if best_candidate_cost < current_cost:
            current_solution, current_cost = best_candidate_solution, best_candidate_cost
        else:
            break
    
    return current_solution, current_cost

def filter_and_fan_uflp(cost_matrix, facility_costs):
    """
    Aplica o algoritmo Filter and Fan para resolver o UFLP.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.

    Returns:
    tuple: Melhor solução encontrada e o custo associado.
    """
    facility_costs = np.array(facility_costs, dtype=np.float64)
    
    # Obtém uma solução inicial usando o algoritmo de greedy
    facilities_open, initial_cost = greedy_uflp(cost_matrix, facility_costs)
    initial_solution = np.array(facilities_open, dtype=np.bool_)

    # Aplica o algoritmo Filter and Fan
    best_solution, best_cost = filter_and_fan(cost_matrix, facility_costs, initial_solution)

    return best_solution, best_cost