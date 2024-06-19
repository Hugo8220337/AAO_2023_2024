import csv
import os
import statistics
from utils.readFile import read_data
from algoritmos.EscolhaAleatoria import openRandomFacility

file_path = r'C:\Users\User\OneDrive - Instituto Politécnico do Porto\Documentos\Obsidian Vault\AAO - Trabalho Pratico\Algoritmos\FicheirosTeste\M\Kcapmo1.txt'


# Ficheiro CSV que vai ser criado
output_csv = './Results/Media.csv'

# Abre o ficheiro csv para escrita
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ficheiro', 'Num. Instalacoes Abertas', 'Media'])



    fixed_costs, allocation_costs = read_data(file_path)
    print(f"Li agora coisas do: {file_path}")
    print(len(fixed_costs))

    i = 0
    j = 0
    max_facilities = len(fixed_costs)
    iterations_per_facility = 200
    solutions = []
    for i in range(max_facilities):
        solutions = []
        for j in range(iterations_per_facility):

            facilities_open, total_cost = openRandomFacility(allocation_costs, fixed_costs, i + 1)
            solutions.append(total_cost)

            # Print results
            # print(f"Facilities open: {facilities_open}")
            # print(f"Total cost: {total_cost}")

        # Calculate the mean of the solutions
        if solutions:
            mean_solution = statistics.mean(solutions)
        else:
            mean_solution = 0

        # Escreve os resultados no ficheiro csv
        writer.writerow([os.path.basename(file_path), i + 1, round(mean_solution, 3)])
        print(f"{i+1}: {round(mean_solution, 3)}")