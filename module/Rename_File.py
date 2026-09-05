from pathlib import Path

def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Rename File ")
    print("==============================")

def get_file_path():
    """Prompts until the user enters a valid path to an existing FILE."""
    while True:
        filepath = input("Enter file path to rename: ").strip()

        if not filepath:
            print("Error: Path cannot be empty.")
            continue

        path = Path(filepath)

        # 1. Path does not exist
        if not path.exists():
            print(f"Error: Path '{filepath}' does not exist.")
            continue

        # 2. Path exists, but it's a directory
        if path.is_dir():
            print(f"Error: '{filepath}' is a directory, not a file.")
            print("Hint: Use a Directory Manager module to remove folders.")
            continue

        # 3. Path exists and is a valid file
        if path.is_file():
            return path

def get_new_filename():
    """Prompts until the user enters a valid new filename."""
    while True:
        new_filename = input("Enter new filename: ").strip()

        if new_filename:
            return new_filename

        print("Error: New filename cannot be empty. Please try again.")

def rename_file(file_path, new_filename):
    """Rename the file to the new filename."""
    new_file_path = file_path.with_name(new_filename)

    if new_file_path.exists():
        raise RuntimeError(f"A file with the name '{new_filename}' already exists.")

    try:
        file_path.rename(new_file_path)
        return new_file_path

    except OSError as e:
        raise RuntimeError(f"Failed to rename file: {e}") from e

def display_result(new_file_path):
    """Display the result of the rename operation."""
    if new_file_path.exists() and new_file_path.is_file():
        print(f"\nFile renamed successfully to: {new_file_path}")
    else:
        print("\nFile was not renamed.")

def display_result(new_file_path):
    """Display the result of the rename operation."""
    if new_file_path.exists() and new_file_path.is_file():
        print(f"\nFile renamed successfully to: {new_file_path}")
    else:
        print("\nFile was not renamed.")

def controller():
    """Run the Rename File workflow."""
    try:
        display_header()

        file_path = get_file_path()
        new_filename = get_new_filename()
        new_file_path = rename_file(file_path, new_filename)

        display_result(new_file_path)

    except RuntimeError as e:
        print(f"\nError: {e}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
