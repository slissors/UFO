import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.signal import correlate

def standardise(moviecsv):
    # Read the data
    movie = pd.read_csv(moviecsv)
    nuforc = pd.read_csv("../../../nuforc_reports.csv")

    # Convert dates to datetime objects
    movie['date'] = pd.to_datetime(movie['date'])
    nuforc['date'] = pd.to_datetime(nuforc['date'])


    # Filter nuforc data to match the specified range
    nuforc_range_start = movie['date'].min() - pd.DateOffset(months=3)
    nuforc_range_end = movie['date'].max() + pd.DateOffset(months=3)
    nuforc_filtered = nuforc[(nuforc['date'] >= nuforc_range_start) & (nuforc['date'] <= nuforc_range_end)]
    nuforc_filtered = nuforc_filtered['date']


    # Group the data by 'date' and count sightings for each date
    sightings_counts = nuforc_filtered.groupby('date').size().reset_index(name='sightings')
    # Merge the counts back into the original DataFrame based on the 'date' column
    nuforc_filtered = nuforc_filtered.merge(sightings_counts, on='date', how='left')

    
    # Standardize the data and create a new column in both DataFrames
    movie['standardized_gross'] = (movie['gross'] - movie['gross'].mean()) / movie['gross'].std()
    nuforc_filtered['standardized_sightings'] = (nuforc_filtered['sightings'] - nuforc_filtered['sightings'].mean()) / nuforc_filtered['sightings'].std()

    # Save the updated DataFrames to new CSV files (if needed)
    movie.to_csv(moviecsv, index=False)
    nuforc_filtered.to_csv('standardised_movie.csv', index=False)


  

def graph_plotter(moviecsv):
    nuforc_filtered, movie= read(moviecsv)

    # Create the figure and axes
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # Plot movie data on the first y-axis
    ax1.plot(movie['date'], movie['gross'], marker='o', label='movie', color='tab:blue')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Gross Revenue", color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a secondary y-axis for nuforc frequency
    ax2 = ax1.twinx()
    ax2.hist(nuforc_filtered['date'], bins=50, edgecolor='white', label='NUFORC', color='tab:orange', alpha=0.5)
    ax2.set_ylabel("Frequency", color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')


    # Customize the plot
    moviecsv = moviecsv.split(".")[0]
    plt.title(f"{moviecsv} Release Date vs. Domestic Gross Revenue Over Time and UFO Sightings Reports per Population")
    fig.tight_layout()

    # Show the combined plot
    plt.show()




    
def full_graph(movie_csv_list):
    # Create an empty list to store movie dataframes
    movie_dfs = []

    # Read and process each movie CSV file, numbering them sequentially
    for i, movie_csv in enumerate(movie_csv_list, start=1):
        movie = pd.read_csv(movie_csv)
        movie['date'] = pd.to_datetime(movie['date'])
        # Assign a unique label to each movie
        movie['movie'] = f'{movie_csv}'  
        movie_dfs.append(movie)

    # Combine the movie dataframes into one dataframe
    combined_movie_df = pd.concat(movie_dfs)

    # Read the UFO data
    nuforc = pd.read_csv("../../../nuforc_reports.csv")
    nuforc['date'] = pd.to_datetime(nuforc['date'])

    # Filter UFO data to match the specified range
    nuforc_range_start = combined_movie_df['date'].min() - pd.DateOffset(months=3)
    nuforc_range_end = combined_movie_df['date'].max() + pd.DateOffset(months=3)
    nuforc_filtered = nuforc[(nuforc['date'] >= nuforc_range_start) & (nuforc['date'] <= nuforc_range_end)]

    # Create the figure and axes
    fig, ax1 = plt.subplots(figsize=(24, 8))

    # Plot gross revenue of each movie on the first y-axis
    for movie_df in movie_dfs:
        ax1.plot(movie_df['date'], movie_df['gross'], marker='.', label=movie_df['movie'].iloc[0])

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Gross Revenue")
    ax1.legend(loc="upper left")

    # Create a secondary y-axis for UFO sightings frequency
    ax2 = ax1.twinx()
    ax2.hist(nuforc_filtered['date'], bins=50, edgecolor='white', label='NUFORC', color='tab:orange', alpha=0.5)
    ax2.set_ylabel("Frequency")
    ax2.legend(loc="upper right")

    # Customize the plot
    plt.title("Gross Revenue Over Time and UFO Sightings Reports per Population")
    fig.tight_layout()

    # Show the combined plot
    plt.show()




def t_test(moviecsv):

    nuforc_filtered, movie= read(moviecsv)

    # Group and aggregate UFO sightings data by date
    nuforc_grouped = nuforc_filtered.groupby('date').size().reset_index(name='sightings_count')

    # Merge movie data and UFO sightings data on the date
    merged_data = pd.merge(movie, nuforc_grouped, on='date', how='inner')

    n = len(merged_data)
    alpha = 0.05

    # Calculate correlation coefficient
    r = np.corrcoef(merged_data['gross'], merged_data['sightings_count'])[0, 1]


    # Calculate degrees of freedom
    df = n - 2

    # Calculate critical t-value
    t_crit_right = stats.t.ppf(1 - alpha, df)

    # Calculate t-value
    t_val = r / (np.sqrt((1-r**2)/(n-2)))


    # Prints Hypothesis Test results for Movie
    print(moviecsv)
    print(f"Correlation Coefficient: {r}")

    print(f"Critical region is t0 > {t_crit_right} and T value is {t_val}")
    if t_val > t_crit_right:
        print("Reject null hypothesis, more") 
    else:
        print("Accept hypothesis")
    print()

    return merged_data




def spearman(moviecsv):

    nuforc_filtered, movie= read(moviecsv)

    # Group and aggregate UFO sightings data by date
    nuforc_grouped = nuforc_filtered.groupby('date').size().reset_index(name='sightings_count')

    # Merge movie data and UFO sightings data on the date
    merged_data = pd.merge(movie, nuforc_grouped, on='date', how='inner')

    # Calculate Spearman's Rank Correlation coefficient
    rho, _ = stats.spearmanr(merged_data['gross'], merged_data['sightings_count'])

    # Prints Hypothesis Test results for Movie
    print(moviecsv)
    print(f"Spearman's Rank Correlation Coefficient: {rho}")

    # Perform a significance test, you can use a critical value based on your alpha level
    if abs(rho) > 0.5:  # You can adjust this threshold based on your significance level
        print("Reject null hypothesis, there is a significant correlation")
    else:
        print("Accept null hypothesis, there is no significant correlation")
    print()






def time_series(moviecsv):
    nuforc_filtered, movie= read(moviecsv)

    # Group and aggregate UFO sightings data by date
    nuforc_grouped = nuforc_filtered.groupby('date').size().reset_index(name='sightings_count')

    # Merge movie data and UFO sightings data on the date
    merged_data = pd.merge(movie, nuforc_grouped, on='date', how='inner')

    # Extract the relevant time series data
    movie_gross = merged_data['gross']
    ufo_sightings = merged_data['sightings_count']

        # Calculate cross-correlation
    cross_corr = correlate(ufo_sightings, movie_gross, mode='same')

    # Determine the time lag associated with the maximum correlation
    time_lag = np.arange(-len(ufo_sightings) // 2, len(ufo_sightings) // 2 + 1)  # Adjust time_lag calculation

    # Calculate the maximum correlation coefficient
    max_corr_coeff = cross_corr.max()

    # Print results
    print(moviecsv)
    print(f"Maximum Cross-Correlation Coefficient: {max_corr_coeff}")
    print(f"Time Lags (in days): {time_lag}")

    # Create a cross-correlation plot
    plt.figure(figsize=(10, 6))
    plt.plot(time_lag, cross_corr, marker='o', linestyle='-')

    # Add labels and a title
    plt.xlabel('Time Lag (in days)')
    plt.ylabel('Cross-Correlation Coefficient')
    plt.title('Cross-Correlation Plot')

    # Add grid lines
    plt.grid(True)

    # Display the plot
    plt.show()





















