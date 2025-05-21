import os
import pandas as pd
from plot_utils import colours, plot_monthly_graphs
from prod_stand import load_and_standardize_production

def list_month_files(year_folder):
    month_names = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho',
                   'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    available_files = []
    for month in month_names:
        filename = os.path.join(year_folder, f"{month}.xlsx")
        if os.path.isfile(filename):
            available_files.append(filename)
    return available_files

def main():
    line_color = colours()
    year = input("Diretório: ").strip()
    year_folder = os.path.join('.', year)

    if not os.path.isdir(year_folder):
        print(f"Diretório '{year_folder}' não existe.")
        return

    month_files = list_month_files(year_folder)

    if not month_files:
        print(f"Nenhum ficheiro Excel válido encontrado em '{year_folder}'. Esperados ficheiros como janeiro.xlsx, etc.")
        return

    producao_path = os.path.join(year_folder, "producao.xlsx")
    producao_data = None
    if os.path.isfile(producao_path):
        print("Ficheiro producao.xlsx encontrado. A carregar dados de produção...")
        producao_data = load_and_standardize_production(producao_path)
    else:
        print("Ficheiro producao.xlsx não encontrado. Apenas o consumo será desenhado...")

    plot_monthly_graphs(month_files, line_color, producao_data)
    # plot_monthly_graphs(month_files, line_color)

if __name__ == "__main__":
    main()