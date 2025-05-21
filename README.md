# Monthly Energy Consumption & Production Visualizer

A Python script to visualize monthly energy consumption from Excel files and overlay standardized production data (like solar generation) for comparison. Created at the request of my dad. Monetarily unpaid word, but compensated in the form of daily feedings, which we common folk usually call “meals” (his words, not mine).

## Features

- Reads monthly consumption Excel files (`janeiro.xlsx`, `fevereiro.xlsx`, etc.) from a year folder.
- Optionally loads `producao.xlsx` to include energy production data, standardized and averaged on 15-minute intervals.
- Generates clear, easy-to-interpret plots for each month showing consumption and production side-by-side.
- Handles missing or incomplete data gracefully by interpolation and filling gaps.
- Outputs intuitive graphs that help analyze patterns and compare consumption vs. production.

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
