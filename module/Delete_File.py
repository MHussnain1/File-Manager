from pathlib import Path

def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Delete File ")
    print("==============================")

def get_file_path():
    """Prompts until the user enters a valid path to an existing FILE."""
    while True:
        filepath = input("Enter file path to delete: ").strip()

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
def user_confirmation(path):
    while True:
        choice = input(f"Are you sure you want to delete '{path.name}'?(y/n): ").strip().lower()
        
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
            
        print("Invalid response. Please enter 'y' or 'n'.")
def unlink_file(file_path):
    # Normalize input with .strip().lower() to accept 'y', 'Y', 'yes', etc.    
    try:
        file_path.unlink()
        return f"Successfully deleted: {file_path.name}"
    except FileNotFoundError:
        return f"Error: The file '{file_path.name}' does not exist in that path."
    except PermissionError:
        return f"Error: Permission denied. File may be in use."
    except IsADirectoryError:
        return f"Error: '{file_path}' is a directory, not a file."


def display_result(result):

    print(result)

def controller():
    try: 
        display_header()
        filepath = get_file_path()
        
        if user_confirmation(filepath):
            result = unlink_file(filepath)
            display_result(result)
        else:
            print("Operation cancelled. File was not deleted.")
    except KeyboardInterrupt:
        print("Operation cancelled by user.")
    