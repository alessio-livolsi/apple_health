# python
import csv
import re
import xml.etree.ElementTree as ET


def clean_source_name(source_name):
    """Clean up the source name by removing special characters."""
    if source_name:
        # replace non-ASCII characters and normalize spaces
        source_name = re.sub(r"[^\x00-\x7F]+", "", source_name)
        return source_name.replace(" ", " ").strip()
    return source_name


def clean_device(device):
    """Extract relevant details from the device information."""
    if device and device.startswith("<<HKDevice"):
        # extract the part after '>, ' and return it
        return device.split(">, ")[1] if ">, " in device else device
    return device


def format_distance(distance):
    """Format the distance to two decimal places with 'km' suffix."""
    if distance:
        return f"{float(distance):.2f}km"
    return None


def extract_running_workouts(xml_path, csv_path):
    # open and parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # prepare CSV columns
    csv_columns = [
        "workout_type",
        "duration",
        "duration_unit",
        "source_name",
        "source_version",
        "device",
        "creation_date",
        "start_date",
        "end_date",
        "indoor",
        "elevation_ascended",
        "timezone",
        "weather_humidity",
        "weather_temperature",
        "average_mets",
        "steps",
        "ground_contact_time_avg",
        "ground_contact_time_min",
        "ground_contact_time_max",
        "running_power_avg",
        "running_power_min",
        "running_power_max",
        "active_energy_burned",
        "basal_energy_burned",
        "vertical_oscillation_avg",
        "vertical_oscillation_min",
        "vertical_oscillation_max",
        "running_speed_avg",
        "running_speed_min",
        "running_speed_max",
        "stride_length_avg",
        "stride_length_min",
        "stride_length_max",
        "distance",
        "heart_rate_avg",
        "heart_rate_min",
        "heart_rate_max",
    ]

    # create a list to store the data
    workouts = []

    # iterate over each <Workout> element in the XML
    for workout in root.findall("Workout"):
        if workout.get("workoutActivityType") != "HKWorkoutActivityTypeRunning":
            continue

        # extract common workout attributes
        indoor = workout.find("MetadataEntry[@key='HKIndoorWorkout']")
        source_name = clean_source_name(workout.get("sourceName"))
        device = clean_device(workout.get("device"))
        workout_data = {
            "workout_type": (
                "Indoor"
                if indoor is not None and indoor.get("value") == "1"
                else "Outdoor"
            ),
            "duration": workout.get("duration"),
            "duration_unit": workout.get("durationUnit"),
            "source_name": source_name,
            "source_version": workout.get("sourceVersion"),
            "device": device,
            "creation_date": workout.get("creationDate"),
            "start_date": workout.get("startDate"),
            "end_date": workout.get("endDate"),
            "indoor": indoor.get("value") if indoor is not None else None,
        }

        # extract metadata entries
        elevation = workout.find("MetadataEntry[@key='HKElevationAscended']")
        workout_data["elevation_ascended"] = (
            elevation.get("value") if elevation is not None else None
        )

        timezone = workout.find("MetadataEntry[@key='HKTimeZone']")
        workout_data["timezone"] = (
            timezone.get("value") if timezone is not None else None
        )

        humidity = workout.find("MetadataEntry[@key='HKWeatherHumidity']")
        workout_data["weather_humidity"] = (
            humidity.get("value") if humidity is not None else None
        )

        temperature = workout.find("MetadataEntry[@key='HKWeatherTemperature']")
        workout_data["weather_temperature"] = (
            temperature.get("value") if temperature is not None else None
        )

        mets = workout.find("MetadataEntry[@key='HKAverageMETs']")
        workout_data["average_mets"] = mets.get("value") if mets is not None else None

        # extract <WorkoutStatistics> elements for various metrics
        for stat in workout.findall("WorkoutStatistics"):
            stat_type = stat.get("type")
            if stat_type == "HKQuantityTypeIdentifierStepCount":
                workout_data["steps"] = stat.get("sum")
            elif stat_type == "HKQuantityTypeIdentifierRunningGroundContactTime":
                workout_data["ground_contact_time_avg"] = stat.get("average")
                workout_data["ground_contact_time_min"] = stat.get("minimum")
                workout_data["ground_contact_time_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierRunningPower":
                workout_data["running_power_avg"] = stat.get("average")
                workout_data["running_power_min"] = stat.get("minimum")
                workout_data["running_power_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierActiveEnergyBurned":
                workout_data["active_energy_burned"] = stat.get("sum")
            elif stat_type == "HKQuantityTypeIdentifierBasalEnergyBurned":
                workout_data["basal_energy_burned"] = stat.get("sum")
            elif stat_type == "HKQuantityTypeIdentifierRunningVerticalOscillation":
                workout_data["vertical_oscillation_avg"] = stat.get("average")
                workout_data["vertical_oscillation_min"] = stat.get("minimum")
                workout_data["vertical_oscillation_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierRunningSpeed":
                workout_data["running_speed_avg"] = stat.get("average")
                workout_data["running_speed_min"] = stat.get("minimum")
                workout_data["running_speed_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierRunningStrideLength":
                workout_data["stride_length_avg"] = stat.get("average")
                workout_data["stride_length_min"] = stat.get("minimum")
                workout_data["stride_length_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                workout_data["distance"] = format_distance(stat.get("sum"))
            elif stat_type == "HKQuantityTypeIdentifierHeartRate":
                workout_data["heart_rate_avg"] = stat.get("average")
                workout_data["heart_rate_min"] = stat.get("minimum")
                workout_data["heart_rate_max"] = stat.get("maximum")

        # add the workout data to the list
        workouts.append(workout_data)

    # write the extracted data to a CSV file
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(workouts)

    print(f"Data has been successfully saved to {csv_path}")


if __name__ == "__main__":
    extract_running_workouts(
        "data/export.xml", "data/apple_health_workout_running_data.csv"
    )
