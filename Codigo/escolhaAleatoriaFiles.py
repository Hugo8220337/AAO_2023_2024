import time
import csv
import os
import math
from utils.getFiles import getTxtFilesFromFolder
from utils.readFile import read_data
from algoritmos.EscolhaAleatoria import openRandomFacility

# Receber todos os ficheiros txt de uma pasta
directory = r'C:\Users\User\OneDrive - Instituto Politécnico do Porto\Documentos\Obsidian Vault\AAO - Trabalho Pratico\Algoritmos\FicheirosTeste'
file_paths = getTxtFilesFromFolder(directory)

# Ficheiro CSV que vai ser criado
output_csv = './ResultadosCsv/RandomFacilityResults.csv'

# Abre o ficheiro csv para escrita
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ficheiro', 'Num. Instalacoes', 'Num. Clientes', 'S.Otima', 'S.Obtida', '%', 'TC'])

    # Itera sobre cada ficheiro
    for file_path in file_paths:
        start_time = time.time()

        num_facilities, num_clients, fixed_costs, allocation_costs = read_data(file_path)

        """ 
            Regra de 3 simples com base no estudo realizado para o pprimeiro ficheiro (8 foi o melhor número para o primeiro ficheiro)
            Se para 100 instalações abriu-se 8, então para len(fixed_costs) abre-se num_of_open_facilities
        """
        num_of_open_facilities = math.floor((len(fixed_costs) * 8) / 100)

        facilities_open, total_cost = openRandomFacility(allocation_costs, fixed_costs, num_of_open_facilities)

        # calcula o tempo de execução
        end_time = time.time()
        execution_time = end_time - start_time

        # Mostrar os resultados
        print(f"File: {file_path}")
        # print(f"Facilities open: {facilities_open}")
        print(f"Total cost: {total_cost}")
        print(f"Execution time: {execution_time:.3f}s")

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