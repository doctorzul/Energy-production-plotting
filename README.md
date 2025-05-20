# Monthly Energy Consumption & Production Visualizer

This Python tool helps you visualize monthly energy consumption data and optionally overlay production data (e.g., solar energy generation) for a given year.

## Features

- Reads monthly consumption Excel files (`janeiro.xlsx`, `fevereiro.xlsx`, etc.) from a year folder.
- Optionally loads `producao.xlsx` to include energy production data, standardized and averaged on 15-minute intervals.
- Generates clear, easy-to-interpret plots for each month showing consumption and production side-by-side.
- Handles missing or incomplete data gracefully by interpolation and filling gaps.
- Outputs intuitive graphs that help analyze patterns and compare consumption vs. production.

## How to Use

1. Organize your data in folders named by year (e.g., `2024/`).
2. Inside each year folder, place monthly Excel files named by month in Portuguese (`janeiro.xlsx`, `fevereiro.xlsx`, etc.).
3. Optionally add a `producao.xlsx` file with detailed production data in 10-minute intervals.
4. Run the script and input the year you want to visualize.
5. View the generated monthly graphs showing your consumption and production data.

## Technical Details

- Uses `pandas` to read and process Excel files and timestamps.
- Standardizes production data by resampling into 15-minute intervals and averaging over days in the month.
- Interpolates missing values to smooth production data and avoid spikes.
- Modular design separating data loading (`prod_standardization.py`) and plotting (`plot_utils.py`).

## Requirements

- Python 3.x
- `pandas`
- `matplotlib`
- `openpyxl` (for Excel reading)
