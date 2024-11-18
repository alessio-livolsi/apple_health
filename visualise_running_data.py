# python
import os

# PyPI
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def load_running_data(file_path):
    """
    Load the running data CSV file.
    """
    try:
        # attempt to read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def preprocess_running_data(df):
    """
    Preprocess the data to filter for 2024 runs and convert distances to numeric values.
    """
    # convert 'start_date' column to datetime format to handle dates
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    # filter the DataFrame to include only rows where the year is 2024
    df_2024 = df[df["start_date"].dt.year == 2024]

    # convert 'distance' column from string (e.g., '5.00km') to a numeric value (float)
    df_2024["distance_km"] = (
        df_2024["distance"].str.replace("km", "", regex=False).astype(float)
    )

    return df_2024


def calculate_average_run_distance(df):
    """
    Calculate the average distance of all runs in 2024.
    """
    # calculate the mean of the 'distance_km' column and return it
    return df["distance_km"].mean()


def save_plot(fig, filename):
    """
    Save the current plot as a PNG file in the 'data_visualisations' directory.
    """
    # create the directory if it doesn't exist
    os.makedirs("data_visualisations", exist_ok=True)

    # save the figure with the specified filename
    file_path = os.path.join("data_visualisations", filename)
    fig.savefig(file_path)
    print(f"Saved plot as: {file_path}")


def visualise_average_run_distance(average_distance):
    """
    Visualise the average distance using a bar chart.
    """
    # create a new figure for the bar chart
    fig = plt.figure(figsize=(6, 4))

    # plot a single bar showing the average distance
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

    # set labels and title for the chart
    plt.ylabel("Distance (km)")
    plt.title("Average Distance per Run in 2024")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.ylim(0, average_distance + 1)

    # save the plot as a PNG file
    save_plot(fig, "average_run_distance_2024.png")
    plt.show()


def visualise_monthly_total_distances(df):
    """
    Visualise the total running distance for each month in 2024.
    """
    # extract month from 'start_date' and create a new column
    df["month"] = df["start_date"].dt.month

    # group data by month and sum the distances
    monthly_distances = df.groupby("month")["distance_km"].sum()

    # create a new figure for the bar chart
    fig = plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_distances.index, monthly_distances.values, color="#76c7c0")

    # add labels and title for the chart
    plt.xlabel("Month")
    plt.ylabel("Total Distance (km)")
    plt.title("Total Running Distance per Month in 2024")
    plt.xticks(
        range(1, 13),
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        rotation=45,
    )
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # add the exact value on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height:.2f} km",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="white",
            bbox=dict(facecolor="black", alpha=0.7, boxstyle="round,pad=0.3"),
        )

    # save the plot as a PNG file
    save_plot(fig, "monthly_total_distances_2024.png")
    plt.show()


def visualise_monthly_total_runs(df):
    """
    Visualise the total number of runs for each month in 2024.
    """
    # extract month from 'start_date' and create a new column
    df["month"] = df["start_date"].dt.month

    # group data by month and count the number of runs
    monthly_run_counts = df.groupby("month").size()

    # create a new figure for the bar chart
    fig = plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly_run_counts.index, monthly_run_counts.values, color="#ff7f0e")

    # add labels and title for the chart
    plt.xlabel("Month")
    plt.ylabel("Number of Runs")
    plt.title("Total Number of Runs per Month in 2024")
    plt.xticks(
        range(1, 13),
        [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        rotation=45,
    )
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # add the exact value on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{int(height)} runs",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="white",
            bbox=dict(facecolor="black", alpha=0.7, boxstyle="round,pad=0.3"),
        )

    # save the plot as a PNG file
    save_plot(fig, "monthly_total_runs_2024.png")
    plt.show()


def visualise_weekly_total_distances_bar(df):
    """
    Visualise the total running distance for each week in 2024 using a horizontal bar chart.
    """
    # extract the week number from 'start_date' and create a new column
    df["week"] = df["start_date"].dt.isocalendar().week

    # group data by week and sum the distances
    weekly_distances = df.groupby("week")["distance_km"].sum()

    # create a new figure for the horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 10))

    # reduce bar height for more spacing
    bar_height = 0.5

    # plot the bars with reduced height to increase spacing
    bars = ax.barh(
        weekly_distances.index,
        weekly_distances.values,
        height=bar_height,
        color="#1f77b4",
        edgecolor="black",
    )

    # add labels and title
    ax.set_xlabel("Total Distance (km)")
    ax.set_ylabel("Week Number")
    ax.set_title("Total Running Distance per Week in 2024")
    ax.set_yticks(weekly_distances.index)
    ax.set_yticklabels([f"Week {int(week)}" for week in weekly_distances.index])
    ax.grid(axis="x", linestyle="--", alpha=0.7)

    # annotate each bar with the exact value, using a smaller font and boxed labels
    for bar, distance in zip(bars, weekly_distances.values):
        ax.text(
            # positioning the text slightly outside the bar
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{distance:.2f} km",
            va="center",
            fontsize=8,
            fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
        )

    # save the plot as a PNG file
    save_plot(fig, "weekly_total_distances_spaced_bar_2024.png")
    plt.show()


def visualise_weekly_total_runs(df):
    """
    Visualise the total number of runs for each week in 2024.
    """
    # extract the week number from 'start_date' and create a new column
    df["week"] = df["start_date"].dt.isocalendar().week

    # group data by week and count the number of runs
    weekly_run_counts = df.groupby("week").size()

    # create a new figure for the line chart
    fig = plt.figure(figsize=(12, 6))
    plt.plot(
        weekly_run_counts.index,
        weekly_run_counts.values,
        marker="o",
        linestyle="-",
        color="#2ca02c",
    )

    # add labels and title for the chart
    plt.xlabel("Week Number")
    plt.ylabel("Number of Runs")
    plt.title("Total Number of Runs per Week in 2024")
    plt.xticks(weekly_run_counts.index, rotation=45)
    plt.grid(axis="both", linestyle="--", alpha=0.7)

    # save the plot as a PNG file
    save_plot(fig, "weekly_total_runs_2024.png")
    plt.show()


def main():
    file_path = "data/apple_health_workout_running_data.csv"

    # load the CSV data into a DataFrame
    df = load_running_data(file_path)
    if df is None:
        return

    # preprocess the data to filter for 2024 and convert distances
    df_2024 = preprocess_running_data(df)
    if df_2024.empty:
        print("No running data available for 2024.")
        return

    # calculate the average distance per run for 2024
    average_distance = calculate_average_run_distance(df_2024)
    print(f"Average Distance per Run in 2024: {average_distance:.2f} km")

    # visualise the charts and save them as images
    visualise_average_run_distance(average_distance)
    visualise_monthly_total_distances(df_2024)
    visualise_monthly_total_runs(df_2024)
    visualise_weekly_total_runs(df_2024)
    visualise_weekly_total_distances_bar(df_2024)


if __name__ == "__main__":
    main()
