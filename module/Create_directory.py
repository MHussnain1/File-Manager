from pathlib import Path


def display_header():
    """Prints the application banner to the user interface."""
    print("=" * 16)
    print("Create Directory")
    print("=" * 16)


def get_directory_name():
    """Prompts the user for a directory name and validates the input."""
    while True:
        directory_name = input("Enter directory name: ").strip()

        if directory_name:
            return directory_name

        print("Error: Directory name cannot be empty. Please try again.")


def create_directory(directory_name):
    """Creates a new directory and returns its Path object."""
    directory_path = Path(directory_name)

    if directory_path.exists():
        raise RuntimeError("Directory already exists.")

    try:
        directory_path.mkdir()
        return directory_path
    except OSError as e:
        raise RuntimeError(f"Failed to create directory: {e}") from e


def display_result(directory_path):
    """Displays the result of the directory creation operation."""
    if directory_path.exists() and directory_path.is_dir():
        print(f"\nDirectory created successfully: {directory_path}")
    else:
        print("\nDirectory was not created.")


def controller():
    """Runs the create-directory workflow."""
    try:
        display_header()

        directory_name = get_directory_name()
        directory_path = create_directory(directory_name)

        display_result(directory_path)

    except RuntimeError as e:
        print(f"\nError: {e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")