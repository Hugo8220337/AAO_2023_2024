import random
import numpy as np
from random import seed
import time

def openRandomFacility(cost_matrix, facility_costs, number_of_open_facilities):
    """
    Abre um número aleatório de instalações.

    Parameters:
    cost_matrix (np.array): Matriz de custos de transporte entre clientes e instalações.
    facility_costs (np.array): Array de custos de abertura das instalações.
    number_of_open_facilities (int): Número de instalações a serem abertas.

    Returns:
    tuple: Array booleano indicando quais instalações estão abertas e o custo total de abertura.
    """
    # Define a seed aleatória com base no tempo atual e no número de instalações abertas
    random.seed(time.time() + number_of_open_facilities)

    
    num_clients, num_facilities = cost_matrix.shape

    # Cria um array booleano para marcar quais instalações estão abertas (começam todas a 0 - fechadas)
    facilities_open = np.zeros(num_facilities, dtype=bool)

    total_cost = 0

    i = 0
    while i < number_of_open_facilities:
        # Seleciona aleatoriamente uma instalação
        random_facility = random.randint(0, num_facilities - 1)

        # Verifica se a instalação está fechada, se está fechada então vai abri-la
        if not facilities_open[random_facility]:
            facilities_open[random_facility] = True
            total_cost += facility_costs[random_facility]
            i += 1

    return facilities_open, total_cost