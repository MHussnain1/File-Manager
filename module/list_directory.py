from pathlib import Path

def display_header():
    """Prints the application banner to the user interface."""
    print("="*16)
    print("List_Directory")
    print("="*16)

def get_directory():
    directory_path = input("Enter Directory path: ").strip()
    if not directory_path:
        return Path.cwd()
    
    return Path(directory_path)

def list_directory(path):
    """Return directory contents as (type, name) tuples."""
    if not path.exists():
        raise RuntimeError("The specified path does not exist.")

    if not path.is_dir():
        raise RuntimeError("The specified path is not a directory.")

    results = []

    for item in path.iterdir():
        if item.is_file():
            results.append(("FILE", item.name))

        elif item.is_dir():
            results.append(("DIR", item.name))

    return results


def display_result(results):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")


    if not results:
        print("Directory is empty.")
        return

    for item_type, name in results:
        print(f"{item_type:<5} {name}")

def controller():
    try:
        display_header()
        path = get_directory()
        result = list_directory(path)
        display_result(result)
    except RuntimeError as e:
        print(f"\nError: {e}")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")



