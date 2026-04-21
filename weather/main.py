import argparse
from weather import fetch_weather, parse_weather, display_weather


def main():
    parser = argparse.ArgumentParser(description="Weather Dashboard")
    parser.add_argument("city", help="City name (e.g. 'Sao Paulo', 'London')")
    args = parser.parse_args()

    try:
        data = fetch_weather(args.city)
        weather = parse_weather(data)
        display_weather(weather)
    except ValueError as e:
        print(f"Error: {e}")
    except EnvironmentError as e:
        print(f"Config error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
