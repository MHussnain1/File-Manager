from pathlib import Path


def display_header():
    """Print the Create Directory module banner."""
    print("\n================")
    print("Create Directory")
    print("================")


def get_directory_name():
    """Get a non-empty directory name from the user."""
    while True:
        directory_name = input("Enter directory name: ").strip()

        if directory_name:
            return directory_name

        print("Error: Directory name cannot be empty. Please try again.")


def create_directory(directory_name):
    """Create a directory and return its Path object."""
    directory_path = Path(directory_name)

    if directory_path.exists():
        if directory_path.is_dir():
            raise RuntimeError("Directory already exists.")
        raise RuntimeError("A file with this name already exists.")

    try:
        directory_path.mkdir(parents=False)
        return directory_path

    except OSError as e:
        raise RuntimeError(f"Failed to create directory: {e}") from e


def display_result(directory_path):
    """Display the directory creation result."""
    if directory_path.exists() and directory_path.is_dir():
        print(f"\nDirectory created successfully: {directory_path}")
    else:
        print("\nDirectory was not created.")


def controller():
    """Run the Create Directory workflow."""
    try:
        display_header()

        directory_name = get_directory_name()
        directory_path = create_directory(directory_name)

        display_result(directory_path)

    except RuntimeError as e:
        print(f"\nError: {e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")