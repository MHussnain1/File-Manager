import sys

try:
    from module.list_directory import controller as list_controller
except ImportError as e:
    print("\n==============================")
    print(" Initialization Error")
    print("==============================")
    print(f"\nFailed to load a Network Toolkit module:")
    print(f"{e}")
    print("\nPlease check that:")
    print("  - All module files exist.")
    print("  - Module filenames are correct.")
    print("  - Required packages are installed.")
    print("  - You are running the program from the project root.")
    sys.exit(1)


def get_menu_dispatch():
    """Return a mapping between menu choices and module controllers."""
    return {
        "1": list_controller,
    }


def display_menu():
    print("\n==============================")
    print(" Network Toolkit - File Manager")
    print("==============================")
    print("1: List Directory")
    print("0: Exit")


def pause():
    """Pause execution before returning to the main menu."""
    try:
        input("\nPress Enter to return to the main menu...")
    except KeyboardInterrupt:
        print("\n\nReturning to main menu...")


def main():
    """Run the main Network Toolkit application loop."""
    dispatch = get_menu_dispatch()
    max_option = len(dispatch)

    while True:
        try:
            display_menu()

            choice = input(f"\nEnter your choice (0-{max_option}): ").strip()

            # ------------------------------------------------
            # Exit
            # ------------------------------------------------
            if choice == "0":
                print("\nExiting Network Toolkit. Goodbye!")
                break

            # ------------------------------------------------
            # Execute selected module
            # ------------------------------------------------
            if choice in dispatch:
                print()
                controller = dispatch[choice]
                controller()
                pause()

            # ------------------------------------------------
            # Invalid choice
            # ------------------------------------------------
            else:
                print(
                    f"\nInvalid choice."
                    f"\nPlease enter a number between 0 and {max_option}."
                )

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")

            try:
                continue_running = input(
                    "\nPress Enter to return to the menu "
                    "or type '0' to exit: "
                ).strip()

                if continue_running == "0":
                    print("\nExiting Network Toolkit. Goodbye!")
                    break

            except KeyboardInterrupt:
                print("\n\nExiting Network Toolkit. Goodbye!")
                break

        except RuntimeError as e:
            print("\n==============================")
            print(" Tool Error")
            print("==============================")
            print(f"\n{e}")
            pause()

        except Exception as e:
            # Last-resort protection so one unexpected module
            # error does not terminate the entire toolkit.
            print("\n==============================")
            print(" Unexpected Error")
            print("==============================")
            print(f"\n{type(e).__name__}: {e}")
            pause()


if __name__ == "__main__":
    main()