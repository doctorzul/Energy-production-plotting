import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import math
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def colours():
    # Hex colors
    background = "#FFFFFF"
    gridlines = "#8A8A8A"
    plotline_one = "#ff0000"

    # Set white background and grid/text colors
    plt.rcParams['figure.facecolor'] = background
    plt.rcParams['axes.facecolor'] = background
    plt.rcParams['axes.edgecolor'] = gridlines
    plt.rcParams['axes.labelcolor'] = gridlines
    plt.rcParams['xtick.color'] = gridlines
    plt.rcParams['ytick.color'] = gridlines
    plt.rcParams['grid.color'] = gridlines
    plt.rcParams['text.color'] = gridlines

    # Grid style
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 1

    return plotline_one

def process_file(filepath):
    # Load Excel workbook to get title from B7
    wb = load_workbook(filepath, data_only=True)
    sheet = wb.active
    graph_title = sheet["B7"].value

    # Load column names from 10th row (row index 9)
    column_names = pd.read_excel(filepath, engine="openpyxl", header=None,
                                 skiprows=9, nrows=1, usecols="A:C").values[0]

    # Load data starting from row 11 (skiprows=10)
    df = pd.read_excel(filepath, engine="openpyxl", header=None, skiprows=10, usecols="A:C")
    df.columns = column_names

    # Compute average power consumption grouped by time increments
    avg_by_time = df.groupby(column_names[1])[column_names[2]].mean()

    # Create full 15-minute time index from 00:00 to 23:45
    full_time_index = pd.date_range("00:00", "23:45", freq="15min").time

    # Convert avg_by_time index to datetime.time for reindexing
    avg_by_time.index = pd.to_datetime(avg_by_time.index, format='%H:%M').time

    # Reindex to fill missing times with 0
    avg_by_time = avg_by_time.reindex(full_time_index, fill_value=0)

    return avg_by_time, graph_title, column_names[2]

def plot_monthly_graphs(filepaths, line_color, producao_data=None):
    num_files = len(filepaths)
    cols = 3
    rows = math.ceil(num_files / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 6, rows * 4), constrained_layout=True)

    if isinstance(axes, plt.Axes):
        axes = [axes]
    else:
        axes = axes.flatten()

    production_color = "#0022FF"

    for i, filepath in enumerate(filepaths):
        avg_by_time, title, power_label = process_file(filepath)
        ax = axes[i]

        times_formatted = [t.strftime('%H:%M') for t in avg_by_time.index]
        ax.plot(times_formatted, avg_by_time, color=line_color, label="Consumo")
        # ax.plot(times_formatted, [0.5]*len(times_formatted), color=production_color, label="prod_test")

        month_key = os.path.splitext(os.path.basename(filepath))[0].lower()

        ymax = avg_by_time.max()

        if producao_data and month_key in producao_data:
            production_series = producao_data[month_key]
            # print(f"Month: {month_key} — Production series length: {len(production_series)}")
            # print(production_series.head())
            prod_times = [t.strftime('%H:%M') for t in production_series.index]
            ax.plot(prod_times, production_series, color=production_color, label="Produção")
            ymax = max(ymax, production_series.max())

        ax.set_title(title)
        ax.set_xlabel("") # Hora do dia
        ax.set_ylabel(f"kW") # kilowatts
        ax.grid(True)

        # Mark every hour on x-axis
        hour_ticks = [t.strftime('%H:%M') for t in avg_by_time.index if t.minute == 0]
        hour_positions = [idx for idx, t in enumerate(avg_by_time.index) if t.minute == 0]
        ax.set_xticks(hour_positions)
        ax.set_xticklabels(hour_ticks, rotation=45, fontsize=8)

        ax.set_ylim(0, max(ymax * 1.1, 1))

        # Show legend if production is included
        if producao_data and month_key in producao_data:
            ax.legend(loc='upper right', fontsize=8)

    for j in range(num_files, len(axes)):
        fig.delaxes(axes[j])

    plt.savefig("consumo_anual.png", dpi=150)
    plt.close(fig)
    print("Gráfico guardado como consumo_anual.png")
