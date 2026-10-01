from pathlib import Path


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Copy File ")
    print("==============================")


def get_source_file():
    """Prompt until the user enters a path to an existing file."""
    while True:
        source_file = input("Enter source file path: ").strip()

        if not source_file:
            print("Error: Path cannot be empty.")
            continue

        path = Path(source_file)

        if not path.exists():
            print(f"Error: Path '{source_file}' does not exist.")
            continue

        if not path.is_file():
            print(f"Error: '{source_file}' is not a file.")
            continue

        return path