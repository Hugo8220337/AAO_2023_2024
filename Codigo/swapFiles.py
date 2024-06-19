import time
import csv
import os
from utils.getFiles import getTxtFilesFromFolder
from utils.readFile import read_data
from algoritmos.SwapLocalSeach import swap_heuristic_uflp

# Receber todos os ficheiros txt de uma pasta
directory = r'C:\Users\User\OneDrive - Instituto Politécnico do Porto\Documentos\Obsidian Vault\AAO - Trabalho Pratico\Algoritmos\FicheirosTeste'
file_paths = getTxtFilesFromFolder(directory)

# Ficheiro CSV que vai ser criado
output_csv = './ResultadosCsv/SwapResults.csv'


# Abre o ficheiro csv para escrita
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ficheiro', 'Num. Instalacoes', 'Num. Clientes', 'S.Otima', 'S.Obtida', '%', 'TC'])

    # Itera sobre cada ficheiro
    for file_path in file_paths:
        start_time = time.time()

        num_facilities, num_clients, fixed_costs, allocation_costs = read_data(file_path)

        # Solução inicial para a pesquisa de troca (switch)
        facilities_open, total_cost = swap_heuristic_uflp(allocation_costs, fixed_costs)

        # calcula o tempo de execução
        end_time = time.time()
        execution_time = end_time - start_time

        # Mostrar os resultados
        print(f"File: {file_path}")
        print(f"Total cost: {total_cost:.3f}")
        print(f"Execution time: {execution_time:.3f}s")
        # print(f"Facilities open: {facilities_open}")

        # Escreve os resultados no ficheiro csv
        writer.writerow([
            os.path.basename(file_path),
            num_facilities,
            num_clients,
            '',
            round(total_cost, 3),
            '',
            round(execution_time, 3)
        ])
