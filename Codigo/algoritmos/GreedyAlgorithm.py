import numpy as np
from numba import njit


"""
https://www.geeksforgeeks.org/greedy-algorithms/
    Este algoritmo baseia-se na informação disponível no momento, não levando em consideração as consequências
    futuras, ele procura a melhor localização em cada passo. Pode levar em soluções distantes das ótimas, mas 
    que já são boas o bastante para muitos problemas
"""

@njit
def greedy_uflp(cost_matrix, facility_costs):
    """
    Heurístico construtivo de greedy

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.

    Returns:
    tuple: Array booleano indicando quais instalações estão abertas e o custo total da solução.
    """

    num_clients, num_facilities = cost_matrix.shape
    facilities_open = np.zeros(num_facilities, dtype=np.bool_)
    total_cost = 0.0
    
    for client in range(num_clients):
        min_cost = np.inf
        best_facility = -1
        
        # Itera sobre cada instalação para encontrar a melhor instalação para o cliente atual
        for facility in range(num_facilities):
            # Calcula o custo para atender este cliente em cada instalação
            if facilities_open[facility]:
                # Se a instalação já está aberta, apenas o custo de transporte é considerado
                cost_val = cost_matrix[client][facility]
            else:
                # Se a instalação não está aberta, o custo de transporte mais o custo de abertura é considerado
                cost_val = cost_matrix[client][facility] + facility_costs[facility]
            
            # Atualiza o custo mínimo e a melhor instalação se o custo calculado for menor
            if cost_val < min_cost:
                min_cost = cost_val
                best_facility = facility
        
        # Abrir instalação se já não estiver aberta
        if not facilities_open[best_facility]:
            facilities_open[best_facility] = True
            total_cost += facility_costs[best_facility]
        
        # Somar o custo de transporte do cliente à melhor instalação encontrada
        total_cost += cost_matrix[client][best_facility]
    
    return facilities_open, total_cost


"""
const_Matrix[m][n] -> m são os clientes e n são as facilities
"""