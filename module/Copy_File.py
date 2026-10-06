from pathlib import Path
import shutil


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


def get_destination_directory():
    while True:
        destination_directory = input("Enter destination directory: ").strip()

        if not destination_directory:
            print("Error: Path cannot be empty.")
            continue

        path = Path(destination_directory)

        if not path.exists():
            print(f"Error: Path '{destination_directory}' does not exist.")
            continue

        if not path.is_dir():
            print(f"Error: '{destination_directory}' is not a directory.")
            continue

        return path


def get_destination_path(source_file, destination_directory):
    """Construct the path where the source file will be copied."""
    return destination_directory / source_file.name


def destination_exists(destination_path):
    """Return whether the destination path already exists."""
    return destination_path.exists()


def user_confirmation(destination_path):
    """Ask whether to replace an existing destination file."""
    while True:
        choice = (
            input(
                f"File '{destination_path.name}' already exists at the destination.\n"
                "Do you want to replace it? (y/n): "
            )
            .strip()
            .lower()
        )

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False

        print("Invalid response. Please enter 'y' or 'n'.")


def copy_file(source_file, destination_path):
    """Copy a file and return its destination path."""
    try:
        shutil.copy2(source_file, destination_path)
        return destination_path
    except OSError as e:
        raise RuntimeError(f"Failed to copy file: {e}") from e
