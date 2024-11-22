# Apple Health Analysis

This repository contains tools and scripts for extracting, processing, and visualising your workout data from Apple Health. It is specifically designed to analyse **running** workout data, helping you visualise trends and insights from your fitness workouts.

## Features
- **Data extraction**: Extract running and cycling workout data from Apple Health **XML files** and convert them into CSV files.
- **Data processing**: Filter and preprocess data to focus on specific years (e.g., 2024).
- **Data visualization**: Generate charts to visualise weekly and monthly trends for running distances, frequencies, and averages.

## Data Visualisation Examples
Currently, the visualisations focus on **running workouts**, including:
- Total running distance per week in 2024 (line chart).
- Total number of runs per month (bar chart).
- Average distance per run (bar chart).
- Horizontal bar charts to visualize weekly totals with exact distances.

In the future, I plan to add similar visualisations for **cycling workouts** to provide insights into both running and cycling activities.

## Requirements
- **Python**: 3.12
- **Packages**:
  - `pandas`
  - `matplotlib`
  - `numpy`

You can install the required packages using:
```bash
pip install -r requirements.txt
