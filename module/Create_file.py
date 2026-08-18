from pathlib import Path


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" File Manager")
    print("==============================")


def get_filename():
    """Get a non-empty file path from the user."""
    while True:
        filename = input("Enter file name: ").strip()

        if filename:
            return filename

        print("Error: File name cannot be empty. Please try again.")


def create_file(filename):
    """Create a new empty file and return its Path object."""
    file_path = Path(filename)

    if file_path.exists():
        raise RuntimeError("File already exists.")

    try:
        file_path.touch()
        return file_path

    except OSError as e:
        raise RuntimeError(f"Failed to create file: {e}") from e


def display_result(file_path):
    """Display the result of the file-creation operation."""
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    if file_path.is_file():
        print(f"\nFile created successfully: {file_path}")
    else:
        print("\nFile was not created.")


def controller():
    """Run the file-creation workflow."""
    try:
        display_header()

        filename = get_filename()
        file_path = create_file(filename)

        display_result(file_path)

    except RuntimeError as e:
        print(f"\nError: {e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")