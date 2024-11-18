# python
import csv
import re
import xml.etree.ElementTree as ET


def clean_source_name(source_name):
    """Clean up the source name by removing special characters."""
    if source_name:
        source_name = re.sub(r"[^\x00-\x7F]+", "", source_name)
        return source_name.replace(" ", " ").strip()
    return source_name


def clean_device(device):
    """Extract relevant details from the device information."""
    if (
        device is not None
        and isinstance(device, str)
        and device.startswith("<<HKDevice")
    ):
        # extract everything after '>, ' and clean any trailing characters
        cleaned_device = device.split(">, ")[-1].replace(">", "").strip()
        return cleaned_device.rstrip(">").strip()
    return device


def format_distance(distance):
    """Format the distance to two decimal places with 'km' suffix."""
    if distance:
        return f"{float(distance):.2f}km"
    return None


def extract_cycling_workouts(xml_path, csv_path):
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
        "cadence_avg",
        "cadence_min",
        "cadence_max",
        "cycling_power_avg",
        "cycling_power_min",
        "cycling_power_max",
        "cycling_speed_avg",
        "cycling_speed_min",
        "cycling_speed_max",
        "active_energy_burned",
        "basal_energy_burned",
        "distance",
        "heart_rate_avg",
        "heart_rate_min",
        "heart_rate_max",
    ]

    workouts = []

    # iterate over each <Workout> element in the XML
    for workout in root.findall("Workout"):
        if workout.get("workoutActivityType") != "HKWorkoutActivityTypeCycling":
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

        # extract statistics
        for stat in workout.findall("WorkoutStatistics"):
            stat_type = stat.get("type")
            if stat_type == "HKQuantityTypeIdentifierHeartRate":
                workout_data["heart_rate_avg"] = stat.get("average")
                workout_data["heart_rate_min"] = stat.get("minimum")
                workout_data["heart_rate_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierDistanceCycling":
                workout_data["distance"] = format_distance(stat.get("sum"))
            elif stat_type == "HKQuantityTypeIdentifierActiveEnergyBurned":
                workout_data["active_energy_burned"] = stat.get("sum")
            elif stat_type == "HKQuantityTypeIdentifierBasalEnergyBurned":
                workout_data["basal_energy_burned"] = stat.get("sum")
            elif stat_type == "HKQuantityTypeIdentifierCyclingCadence":
                workout_data["cadence_avg"] = stat.get("average")
                workout_data["cadence_min"] = stat.get("minimum")
                workout_data["cadence_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierCyclingPower":
                workout_data["cycling_power_avg"] = stat.get("average")
                workout_data["cycling_power_min"] = stat.get("minimum")
                workout_data["cycling_power_max"] = stat.get("maximum")
            elif stat_type == "HKQuantityTypeIdentifierCyclingSpeed":
                workout_data["cycling_speed_avg"] = stat.get("average")
                workout_data["cycling_speed_min"] = stat.get("minimum")
                workout_data["cycling_speed_max"] = stat.get("maximum")

        workouts.append(workout_data)

    # write data to CSV
    with open(csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(workouts)

    print(f"Data has been successfully saved to {csv_path}")


if __name__ == "__main__":
    extract_cycling_workouts("data/export.xml", "data/cycling_workout_data.csv")
