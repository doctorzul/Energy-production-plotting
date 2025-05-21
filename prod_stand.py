import pandas as pd
import os
import matplotlib.pyplot as plt

def load_and_standardize_production(producao_path, plot_debug=False):
    if not os.path.isfile(producao_path):
        print(f"Arquivo '{producao_path}' não encontrado.")
        return {}

    # Read data starting from row 14 (skiprows=13)
    df = pd.read_excel(producao_path, engine="openpyxl", header=None, skiprows=13, usecols="A,B,E")
    df.columns = ['Data', 'Hora', 'Producao_kW']

    # Combine date + time into single datetime
    df['Timestamp'] = pd.to_datetime(df['Data'].astype(str) + ' ' + df['Hora'].astype(str), errors='coerce')
    nat_count = df['Timestamp'].isna().sum()
    if nat_count > 0:
        # print(f"Warning: Found {nat_count} invalid Timestamp entries (NaT), these rows will be dropped.")
        pass
    df = df.dropna(subset=['Timestamp'])

    # Set Timestamp as index for resampling
    df.set_index('Timestamp', inplace=True)

    # Resample to 15-minute intervals taking mean production values
    df_15min = df['Producao_kW'].resample('15min').mean()

    # Interpolate missing values (smoothing spikes)
    df_15min = df_15min.interpolate(method='time')

    # Fill any remaining NaNs (e.g. start/end) with 0
    df_15min = df_15min.fillna(0)

    # Debug prints
    # nan_count = df_15min.isna().sum()
    # print(f"After resampling + interpolation, production data has {nan_count} NaN values.")

    if plot_debug:
        # plt.figure(figsize=(12,4))
        # df_15min.plot(title="Resampled + Interpolated Production Data (15-min intervals)")
        # plt.xlabel("Timestamp")
        # plt.ylabel("Production kW")
        # plt.show()
        pass

    # Add columns for month and time_of_day
    df_15min = df_15min.to_frame()
    df_15min['Mes'] = df_15min.index.month
    df_15min['Time_of_day'] = df_15min.index.time

    ##################################################
    # Portuguese month names mapping                 #
    ##################################################
    # If the name of the files are not month names,  #
    # the standardized production will not associate # 
    # it with the correct motnh, and thus the        #
    # production graph will not show correctly.      #
    ##################################################

    month_names = {
        1: 'janeiro', 2: 'fevereiro', 3: 'marco', 4: 'abril',
        5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
        9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
    }

    monthly_production = {}
    full_time_index = pd.date_range("00:00", "23:45", freq="15min").time

    for month_num, group in df_15min.groupby('Mes'):
        avg_by_time = group.groupby('Time_of_day')['Producao_kW'].mean()
        avg_by_time = avg_by_time.reindex(full_time_index, fill_value=0)

        # print(f"Month {month_names.get(month_num, month_num)}: {len(avg_by_time)} entries, NaNs: {avg_by_time.isna().sum()}")

        month_name = month_names.get(month_num)
        if month_name:
            monthly_production[month_name] = avg_by_time.dropna()

    return monthly_production
