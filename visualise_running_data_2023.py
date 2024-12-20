# python
import os

# PyPI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    Preprocess the data to filter for 2023 runs and convert distances to numeric values.
    """
    # convert 'start_date' column to datetime format to handle dates
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")

    # filter the DataFrame to include only rows where the year is 2023
    df_2023 = df[df["start_date"].dt.year == 2023].copy()

    # convert 'distance' column from string (e.g., '5.00km') to a numeric value (float)
    df_2023["distance_km"] = (
        df_2023["distance"].str.replace("km", "", regex=False).astype(float)
    )
    return df_2023


def calculate_average_run_distance(df):
    """
    Calculate the average distance of all runs in 2023.
    """
    # calculate the mean of the 'distance_km' column and return it
    return df["distance_km"].mean()


def save_plot(fig, filename):
    """
    Save the current plot as a PNG file in the 'data_visualisations/running/2023' directory.
    """
    # create the directory if it doesn't exist
    os.makedirs("data_visualisations/running/2023", exist_ok=True)

    # save the figure with the specified filename
    file_path = os.path.join("data_visualisations/running/2023", filename)
    fig.savefig(file_path)
    print(f"Saved plot as: {file_path}")


def visualise_average_run_distance(average_distance):
    """
    Visualise the average distance using a bar chart.
    """
    # create a new figure for the bar chart
    fig = plt.figure(figsize=(6, 4))

    # plot a single bar showing the average distance
    plt.bar(["Average Distance"], [average_distance], color="#1f77b4")

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
    plt.title("Average Distance per Run in 2023")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.ylim(0, average_distance + 1)

    # save the plot as a PNG file
    save_plot(fig, "average_run_distance_2023.png")
    plt.show()


def visualise_monthly_total_distances(df):
    """
    Visualise the total running distance for each month in 2023.
    """

    df = df.copy()

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
    plt.title("Total Running Distance per Month in 2023")
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
    save_plot(fig, "monthly_total_distances_2023.png")
    plt.show()


def visualise_monthly_total_runs(df):
    """
    Visualise the total number of runs for each month in 2023.
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
    plt.title("Total Number of Runs per Month in 2023")
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
            height + 0.2,
            f"{int(height)} runs",
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
            color="white",
            bbox=dict(facecolor="black", alpha=0.7, boxstyle="round,pad=0.3"),
        )

    # save the plot as a PNG file
    save_plot(fig, "monthly_total_runs_2023.png")
    plt.show()


def visualise_weekly_total_distances_bar(df):
    """
    Visualise the total running distance for each week in 2023 using a horizontal bar chart.
    """

    df = df.copy()

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
    ax.set_title("Total Running Distance per Week in 2023")
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
    save_plot(fig, "weekly_total_distances_spaced_bar_2023.png")
    plt.show()


def visualise_weekly_total_runs(df):
    """
    Visualise the total number of runs for each week in 2023.
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
    plt.title("Total Number of Runs per Week in 2023")
    plt.xticks(weekly_run_counts.index, rotation=45)
    plt.grid(axis="both", linestyle="--", alpha=0.7)

    # save the plot as a PNG file
    save_plot(fig, "weekly_total_runs_2023.png")
    plt.show()


def find_longest_run(df):
    """
    Identify the longest run based on distance.
    """
    return df.loc[df["distance_km"].idxmax()]


def visualise_longest_run(longest_run):
    """
    Visualise the longest run as a bar chart.
    """
    # prepare data for visualization
    distance = longest_run["distance_km"]
    label = f"Longest Run ({longest_run['start_date'].strftime('%Y-%m-%d')})"

    # create the bar chart
    fig = plt.figure(figsize=(8, 5))
    bar = plt.bar([label], [distance], color="#4caf50")

    # annotate the bar with the exact distance
    plt.text(
        bar[0].get_x() + bar[0].get_width() / 2,
        bar[0].get_height() + 0.2,
        f"{distance:.2f} km",
        ha="center",
        va="top",
        fontsize=12,
        fontweight="bold",
        color="white",
        bbox=dict(facecolor="black", alpha=0.7, boxstyle="round,pad=0.3"),
    )

    # add labels and title
    plt.ylabel("Distance (km)")
    plt.title("Longest Run in 2023")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # save the plot as a PNG file
    save_plot(fig, "longest_run_2023.png")
    plt.show()


def visualise_run_frequency_heatmap(df):
    """
    Create a heatmap of run frequency by day of the week and hour of the day.
    """
    # extract day of the week and hour of the day
    df["day_of_week"] = df["start_date"].dt.day_name()
    df["hour_of_day"] = df["start_date"].dt.hour

    # create a pivot table for the heatmap
    heatmap_data = (
        df.groupby(["day_of_week", "hour_of_day"]).size().unstack(fill_value=0)
    )

    # reorder the days of the week for better visualization
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    heatmap_data = heatmap_data.reindex(days_order)

    # create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        heatmap_data,
        cmap="Blues",
        annot=True,
        fmt="d",
        linewidths=0.5,
        cbar_kws={"label": "Number of Runs"},
    )

    # add labels and title
    plt.title("Run Frequency by Day of Week and Hour of Day in 2023")
    plt.xlabel("Hour of Day")
    plt.ylabel("Day of Week")

    # save the heatmap as a PNG file
    save_plot(plt.gcf(), "run_frequency_heatmap_2023.png")
    plt.show()


def calculate_speed_and_filter(df):
    """
    Preprocess the data by adding speed and filtering valid runs.
    """
    df["distance_km"] = df["distance"].str.replace("km", "", regex=False).astype(float)
    df["duration_hours"] = df["duration"].astype(float) / 60
    df["speed_kmh"] = df["distance_km"] / df["duration_hours"]
    return df


def get_top_fastest_runs(df, standard_distance, tolerance=0.5, top_n=5):
    """
    Get the top N fastest runs for a given standard distance.
    """
    filtered_runs = df[
        (df["distance_km"] >= standard_distance - tolerance)
        & (df["distance_km"] <= standard_distance + tolerance)
    ]
    top_runs = filtered_runs.nlargest(top_n, "speed_kmh")[
        ["start_date", "distance_km", "duration_hours", "speed_kmh"]
    ]
    return top_runs


def visualise_top_fastest_runs(top_runs, distance):
    """
    Visualise the top fastest runs as a bar chart, with annotated speeds.
    """
    # prepare data for plotting
    labels = top_runs["start_date"].dt.strftime("%d-%m-%Y")
    speeds = top_runs["speed_kmh"]

    # create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, speeds, color="skyblue", edgecolor="black")

    # add annotations for speeds on top of each bar
    for bar, speed in zip(bars, speeds):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{speed:.2f} km/h",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
        )

    # add labels, title, and layout adjustments
    plt.xlabel("Run Date")
    plt.ylabel("Speed (km/h)")
    plt.title(f"Top Five Fastest Runs for {distance}km in 2023")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # save the plot
    filename = f"top_fastest_{distance}km_runs_2023.png"
    save_plot(plt.gcf(), filename)
    plt.show()


def preprocess_form_data(df):
    """
    Preprocess the data to prepare stride length and vertical oscillation metrics.
    """
    # ensure relevant columns are numeric and handle missing data
    df["stride_length_avg"] = pd.to_numeric(df["stride_length_avg"], errors="coerce")
    df["vertical_oscillation_avg"] = pd.to_numeric(
        df["vertical_oscillation_avg"], errors="coerce"
    )
    df["distance_km"] = df["distance"].str.replace("km", "", regex=False).astype(float)

    # filter rows with valid stride length and vertical oscillation values
    return df.dropna(
        subset=["stride_length_avg", "vertical_oscillation_avg", "distance_km"]
    )


def analyse_form_trends(df):
    """
    Analyse trends in stride length and vertical oscillation with distance and terrain.
    """
    # group data by distance (rounded to nearest km)
    df["distance_rounded"] = df["distance_km"].round()

    # calculate average stride length and vertical oscillation for each distance group
    trends = df.groupby("distance_rounded")[
        ["stride_length_avg", "vertical_oscillation_avg"]
    ].mean()
    return trends


def visualise_form_trends(trends):
    """
    Visualise trends in stride length and vertical oscillation with distance.
    """
    # plot stride length trend
    plt.figure(figsize=(12, 6))
    plt.plot(
        trends.index,
        trends["stride_length_avg"],
        marker="o",
        label="Stride Length (Avg)",
        linestyle="--",
    )
    plt.title("Stride Length Trend by Distance in 2023")
    plt.xlabel("Distance (km)")
    plt.ylabel("Stride Length (cm)")
    plt.grid(alpha=0.7)
    plt.legend()
    save_plot(plt.gcf(), "stride_length_trend_2023.png")
    plt.show()

    # plot vertical oscillation trend
    plt.figure(figsize=(12, 6))
    plt.plot(
        trends.index,
        trends["vertical_oscillation_avg"],
        marker="o",
        label="Vertical Oscillation (Avg)",
        linestyle="--",
    )
    plt.title("Vertical Oscillation Trend by Distance in 2023")
    plt.xlabel("Distance (km)")
    plt.ylabel("Vertical Oscillation (cm)")
    plt.grid(alpha=0.7)
    plt.legend()
    save_plot(plt.gcf(), "vertical_oscillation_trend_2023.png")
    plt.show()


def visualise_form_trends_outdoor(df):
    """
    Visualise trends for outdoor runs only.
    """
    # filter data for outdoor runs
    outdoor_data = df[df["indoor"] == 0]

    # analyse trends for outdoor data
    trends = analyse_form_trends(outdoor_data)

    # create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(
        trends.index,
        trends["stride_length_avg"],
        marker="o",
        label="Stride Length (Avg)",
        linestyle="--",
        color="blue",
    )
    plt.plot(
        trends.index,
        trends["vertical_oscillation_avg"],
        marker="o",
        label="Vertical Oscillation (Avg)",
        linestyle="--",
        color="green",
    )
    plt.title("Form Trends by Distance - Outdoor Runs in 2023")
    plt.xlabel("Distance (km)")
    plt.ylabel("Average Metrics (cm)")
    plt.grid(alpha=0.7)
    plt.legend()
    save_plot(plt.gcf(), "form_trends_outdoor_2023.png")
    plt.show()


def main():
    file_path = "data/apple_health_workout_running_data.csv"

    # load the CSV data into a DataFrame
    df = load_running_data(file_path)
    if df is None:
        return

    # preprocess the data to filter for 2023 and convert distances
    df_2023 = preprocess_running_data(df)
    if df_2023.empty:
        print("No running data available for 2023.")
        return

    # calculate the average distance per run for 2023
    average_distance = calculate_average_run_distance(df_2023)
    print(f"Average Distance per Run in 2023: {average_distance:.2f} km")

    # find the longest run
    longest_run = find_longest_run(df_2023)
    print(
        f"Longest Run: {longest_run['distance_km']:.2f} km on {longest_run['start_date']}"
    )

    # preprocess data for running form analysis
    df = preprocess_form_data(df)

    # visualise the charts and save them as images
    visualise_average_run_distance(average_distance)
    visualise_monthly_total_distances(df_2023)
    visualise_monthly_total_runs(df_2023)
    visualise_weekly_total_runs(df_2023)
    visualise_weekly_total_distances_bar(df_2023)
    visualise_longest_run(longest_run)
    visualise_run_frequency_heatmap(df_2023)
    visualise_longest_run(longest_run)
    trends = analyse_form_trends(df)
    visualise_form_trends(trends)
    visualise_form_trends_outdoor(df)

    # calculate and visualise top fastest runs for standard distances
    df_2023 = calculate_speed_and_filter(df_2023)
    standard_distances = [5, 10]
    for distance in standard_distances:
        top_runs = get_top_fastest_runs(df_2023, standard_distance=distance)
        print(f"Top {len(top_runs)} Fastest Runs for {distance}km:\n", top_runs)
        visualise_top_fastest_runs(top_runs, distance)


if __name__ == "__main__":
    main()
