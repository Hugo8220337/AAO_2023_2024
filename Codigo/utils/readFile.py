import numpy as np

def read_data(file_path):
    with open(file_path, 'r') as file:
        # Ler o número de armazéns e clientes
        m, n = map(int, file.readline().split())

        # Inicializar a lista para os custos fixos
        fixed_costs = []

        # Ler os custos fixos dos armazéns
        for _ in range(m):
            line = file.readline().split()
            fixed_cost = float(line[1])  # Guardar apenas o segundo valor
            fixed_costs.append(fixed_cost)

        # Inicializar a matriz para os custos de alocação
        allocation_costs = []

        # Ignorar a linha com o demand
        file.readline()

        lineReaded = 0
        costs = []
        # Ler os custos de alocação
        percurredClients = 0
        while percurredClients != n:
            line = file.readline().split()

            costs += [float(cost) for cost in line[:n]]

            lineReaded += len(line)
            if(lineReaded == m):
                lineReaded = 0
                percurredClients += 1
                allocation_costs.append(costs)
                costs = []

                # ignorar demand
                line = file.readline().split()

                # se por acaso a linha ignorada for um enter, ignora tb a próxima linha
                if not line:
                    file.readline()

            
    # Converter allocation_costs e fixed_costs para um array NumPy
    allocation_costs = np.array(allocation_costs)
    fixed_costs = np.array(fixed_costs)

    file.close()

    return m, n, fixed_costs, allocation_costs