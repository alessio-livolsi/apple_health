# PyPI
import pandas as pd
import matplotlib.pyplot as plt


def load_data(file_path):
    """
    Load the running data CSV file.
    """
    try:
        # attempt to read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # handle the case where the file path is incorrect or the file is missing
        print(f"File not found: {file_path}")
        return None


def preprocess_data(df):
    """
    Preprocess the data to filter for 2024 runs and convert distances to numeric values.
    """
    # convert 'start_date' column to datetime format to make filtering by year easier
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    # filter the data to only include runs from the year 2024
    df_2024 = df[df["start_date"].dt.year == 2024]

    # convert 'distance' from string format (e.g., "5.00km") to a numeric float value
    # this will make it easier to perform calculations later
    df_2024["distance_km"] = (
        df_2024["distance"].str.replace("km", "", regex=False).astype(float)
    )

    return df_2024


def calculate_average_distance(df):
    """
    Calculate the average distance of all runs in 2024.
    """
    # calculate the mean (average) of the 'distance_km' column
    return df["distance_km"].mean()


def visualise_average_distance(average_distance):
    """
    Visualize the average distance using a bar chart and display the value on the bar.
    """
    plt.figure(figsize=(6, 4))

    # plot a bar chart with the average distance
    bar = plt.bar(["Average Distance"], [average_distance], color="#1f77b4")

    # add the exact value on top of the bar for clarity
    plt.text(
        0,
        average_distance + 0.2,
        f"{average_distance:.2f} km",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="white",
        bbox=dict(facecolor="black", alpha=0.7, boxstyle="round,pad=0.3"),
    )

    plt.ylabel("Distance (km)")
    plt.title("Average Distance per Run in 2024")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.ylim(0, average_distance + 1)
    plt.show()


def visualise_monthly_distances(df):
    """
    Visualize the total running distance for each month in 2024.
    """
    # extract the month from the 'start_date' and create a new column
    df['month'] = df['start_date'].dt.month

    # group by month and sum the distances
    monthly_distances = df.groupby('month')['distance_km'].sum()

    plt.figure(figsize=(10, 6))
    monthly_distances.plot(kind='bar', color='#76c7c0')

    # add labels and title
    plt.xlabel('Month')
    plt.ylabel('Total Distance (km)')
    plt.title('Total Running Distance per Month in 2024')

    # set custom month labels
    plt.xticks(ticks=range(12), labels=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def main():
    # specify the path to the CSV file
    file_path = "data/apple_health_workout_running_data.csv"

    # load the CSV data into a DataFrame
    df = load_data(file_path)
    if df is None:
        return

    # preprocess the data to filter for 2024 and convert distances
    df_2024 = preprocess_data(df)
    if df_2024.empty:
        print("No running data available for 2024.")
        return

    # calculate the average distance per run for 2024
    average_distance = calculate_average_distance(df_2024)
    print(f"Average Distance per Run in 2024: {average_distance:.2f} km")

    # visualise the average distance using a bar chart
    visualise_average_distance(average_distance)

    # visualise the total running distance for each month in 2024
    visualise_monthly_distances(df_2024)


if __name__ == "__main__":
    main()
