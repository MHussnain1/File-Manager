from pathlib import Path


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Delete Directory ")
    print("==============================")


def get_directory_path():
    while True:
        directory_path = input("Enter directory path to delete: ").strip()

        if not directory_path:
            print("Error: Path cannot be empty.")
            continue

        path = Path(directory_path)

        # 1. Path does not exist
        if not path.exists():
            print(f"Error: Path '{directory_path}' does not exist.")
            continue

        if path.is_file():
            print(f"Error: '{directory_path}' is a file, not a directory.")
            print("Hint: Use a File Manager module to remove file.")
            continue

        if path.is_dir():
            return path


def confirmation(path):
    while True:
        choice = (
            input(f"Are you sure you want to delete 'projects'? (y/n): ")
            .strip()
            .lower()
        )

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False

        print("Invalid response. Please enter 'y' or 'n'.")


def remove_directory(path):
    try:
        path.rmdir()
        return f"Successfully deleted: {path.name}"
    except FileNotFoundError:
        return f"Error: The Directory '{path.name}' does not exist in that path."
    except PermissionError:
        return f"Error: Permission denied. directory may be in use."
    except IsADirectoryError:
        return f"Error: '{path}' is a file, not a directory."
    except OSError:
        return f"Error: Directory '{path.name}' is not empty."


def display_result(results):
    print(results)


def controller():
    try:
        display_header()
        dir_path = get_directory_path()

        if confirmation(dir_path):
            result = remove_directory(dir_path)
            display_result(result)
        else:
            print("Operation cancelled. Directory was not deleted.")
    except KeyboardInterrupt:
        print("Operation cancelled by user.")
