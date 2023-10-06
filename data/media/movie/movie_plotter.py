import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
  

def graph_plotter(moviecsv):
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
        # Assign a unique label to each movie (e.g., 'Movie 1', 'Movie 2', etc.)
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
    # Read the data
    movie = pd.read_csv(moviecsv)
    nuforc = pd.read_csv("../../../nuforc_reports.csv")

    # Convert dates to datetime objects
    movie['date'] = pd.to_datetime(movie['date'])
    nuforc['date'] = pd.to_datetime(nuforc['date'])

    # Calculate the time range around movie's release date
    nuforc_range_start = movie['date'].min()
    nuforc_range_end = movie['date'].max() 
    nuforc_filtered = nuforc[(nuforc['date'] >= nuforc_range_start) & (nuforc['date'] <= nuforc_range_end)]

    # Group and aggregate UFO sightings data by date
    nuforc_grouped = nuforc_filtered.groupby('date').size().reset_index(name='sightings_count')

    # Merge movie data and UFO sightings data on the date
    merged_data = pd.merge(movie, nuforc_grouped, on='date', how='inner')

    n = len(merged_data)
    alpha = 0.05

    # Calculate correlation coefficient
    r = np.corrcoef(merged_data['gross'], merged_data['sightings_count'])[0, 1]

    # Print the correlation coefficient
    print(f"Correlation Coefficient for {moviecsv}: {r}")

    # Calculate degrees of freedom
    df = n - 2

    # Calculate critical t-value
    t_crit_right = stats.t.ppf(1 - alpha/2, df)
    t_crit_left = -abs(t_crit_right)

    # Calculate t-value
    t_val = r / (np.sqrt((1-r**2)/(n-2)))

    print(f"For {moviecsv} Critical region is p > {t_crit_right} or p < {t_crit_left} and T value is {t_val}")
    if t_val > t_crit_right:
        print("Reject null hypothesis, more") 
    elif t_val < t_crit_left:
        print("Reject null hypothesis, less") 
    else:
        print("Accept hypothesis")

    return merged_data










