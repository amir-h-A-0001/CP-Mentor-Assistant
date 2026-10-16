from src.controllers.controller import Controller
import itertools
import sys
import threading
import time

# ANSI terminal colors
RESET = "\033[0m"
GRAY = "\033[37m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"


def log(message, color=GRAY):
    print(f"{color}{message}{RESET}")


def success(message):
    log(f"[SUCCESS] {message}", GREEN)


def warning(message):
    log(f"[WARNING] {message}", YELLOW)


def error(message):
    log(f"[ERROR] {message}", RED)


def title(message):
    print(f"\n{CYAN}{BOLD}{'=' * 40}")
    print(f"  {message}")
    print(f"{'=' * 40}{RESET}")


def working(message="Please wait..."):
    class Spinner:
        def __enter__(self):
            self.running = True
            self.spinner = itertools.cycle(["|", "/", "-", "\\"])

            def animate():
                while self.running:
                    sys.stdout.write(
                        f"\r\033[33m{next(self.spinner)} {message}\033[0m"
                    )
                    sys.stdout.flush()
                    time.sleep(0.1)

            self.thread = threading.Thread(target=animate, daemon=True)
            self.thread.start()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.running = False
            self.thread.join()
            sys.stdout.write("\r\033[K")
            sys.stdout.flush()

    return Spinner()


def ask_bool(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} [y/n]: ").strip().lower()

        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False

        warning("Please enter y or n.")


def ask_int(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= minimum:
                return value
            warning(f"Enter a number >= {minimum}.")
        except ValueError:
            warning("Please enter a valid integer.")


def ask_optional_float(prompt: str) -> float | None:
    while True:
        value = input(prompt).strip()

        if not value:
            return None

        try:
            return float(value)
        except ValueError:
            warning("Please enter a valid number or leave it empty.")


def show_menu(app: Controller):
    title("CP Mentor Assistant")

    log(f"Active spreadsheet: {app.sheet_name}", CYAN)

    print("""
  1. Add contest
  2. Add batch of contests
  3. Create final report
  4. Switch spreadsheet
  5. Show available spreadsheets
  0. Exit
""")


def add_contest(app: Controller):
    title("Add Contest")

    short_title = input("Short title: ").strip()
    url = input("Contest URL: ").strip()

    if not short_title or not url:
        warning("Title and URL cannot be empty.")
        return

    include_virtuals = ask_bool("Include virtual participants?")
    create_standings = ask_bool("Create standings?")

    platform_name = input(
        "Platform name (leave empty for automatic selection): "
    ).strip() or None

    weight = ask_optional_float(
        "Contest weight (leave empty for default): "
    )

    with working():
        result = app.add_contest(
            short_title=short_title,
            url=url,
            include_virtuals=include_virtuals,
            create_standings=create_standings,
            exists=False,
            platform_name=platform_name,
            weight=weight,
        )

    if result == "Done":
        success("Contest operation completed.")
    else:
        error(result)


def add_batch(app: Controller):
    title("Add Batch of Contests")

    include_virtuals = ask_bool("Include virtual participants?")
    create_standings = ask_bool("Create standings?")

    with working():
        results = app.add_batch_contests( 
            include_virtuals=include_virtuals,
            create_standings=create_standings,
        )

    if isinstance(results, str):
        error(results)
    else:
        for ok, message in results:
            if ok:
                success(message)
            else:
                error(message)

    success("Batch operation completed.")


def create_report(app: Controller):
    title("Create Final Report")

    report_title = input("Report title: ").strip()

    if not report_title:
        warning("Report title cannot be empty.")
        return

    number_of_contests = ask_int("Number of contests: ", minimum=1)
    most_absences = ask_int("Most absences: ")
    best_first = ask_bool("Sort best participants first?")
    weighted = ask_bool("Use contest weights?")

    with working():
        app.create_final_table(
            title=report_title,
            number_of_contests=number_of_contests,
            most_absences=most_absences,
            best_first=best_first,
            weighted=weighted,
        )

    success("Final report created.")


def switch_sheet(app: Controller):
    title("Switch Spreadsheet")

    names = app.get_sheet_names()

    if not names:
        warning("No configured spreadsheets found.")
        return

    for i, name in enumerate(names, start=1):
        marker = " (active)" if name == app.sheet_name else ""
        print(f"  {CYAN}{i}.{RESET} {name}{marker}")

    choice = ask_int("Select a spreadsheet (0 to cancel): ", minimum=0)

    if choice == 0:
        return

    if choice > len(names):
        warning("Invalid selection.")
        return

    selected = names[choice - 1]

    if selected == app.sheet_name:
        warning("That spreadsheet is already active.")
        return

    app.switch_sheet(selected)
    success(f"Switched to '{selected}'.")


def run():
    try:
        app = Controller()
    except Exception as exc:
        error(f"Could not initialize the application: {exc}")
        return

    title("Welcome to CP Mentor Assistant")
    success(f"Connected to '{app.sheet_name}'.")

    actions = {
        "1": add_contest,
        "2": add_batch,
        "3": create_report,
        "4": switch_sheet,
    }

    while True:
        show_menu(app)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            log("Goodbye!", CYAN)
            break

        if choice == "5":
            title("Available Spreadsheets")
            for name in app.get_sheet_names():
                marker = " (active)" if name == app.sheet_name else ""
                log(f"- {name}{marker}")
            continue

        action = actions.get(choice)

        if action is None:
            warning("Invalid option. Choose 0-5.")
            continue

        try:
            action(app)
        except KeyboardInterrupt:
            print()
            warning("Operation interrupted.")
        except Exception as exc:
            error(f"Operation failed: {exc}")

        input(f"\n{GRAY}Press Enter to continue...{RESET}")


if __name__ == "__main__":
    run()
