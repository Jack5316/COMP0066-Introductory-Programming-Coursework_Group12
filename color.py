# Method 1: Using ANSI Escape Codes
def ansi_demo():
    print("\033[31mThis is red text (ANSI)\033[0m")  # Red text
    print("\033[32mThis is green text (ANSI)\033[0m")  # Green text
    print("\033[33mThis is yellow text (ANSI)\033[0m")  # Yellow text
    print("\033[41mThis has a red background (ANSI)\033[0m")  # Red background
    print("\033[1mThis is bold text (ANSI)\033[0m")  # Bold text
    print("\033[4mThis is underlined text (ANSI)\033[0m")  # Underlined text


# Method 2: Using colorama Library
def colorama_demo():
    from colorama import Fore, Back, Style
    print(Fore.RED + "This is red text (colorama)")
    print(Fore.GREEN + "This is green text (colorama)")
    print(Back.YELLOW + "This has a yellow background (colorama)")
    print(Style.BRIGHT + "This is bright text (colorama)")
    print(Style.RESET_ALL + "This resets the style (colorama)")


# Method 3: Using rich Library
def rich_demo():
    from rich.console import Console
    console = Console()
    console.print("[red]This is red text (rich)[/red]")
    console.print("[green]This is green text (rich)[/green]")
    console.print("[bold yellow]This is bold yellow text (rich)[/bold yellow]")
    console.print("[bold magenta on white]This is magenta on white (rich)[/bold magenta on white]")


# Run all demos
if __name__ == "__main__":
    print("=== ANSI Escape Codes Demo ===")
    ansi_demo()

    print("\n=== Colorama Demo ===")
    try:
        colorama_demo()
    except ImportError:
        print("colorama is not installed. Run 'pip install colorama' to use this feature.")

    print("\n=== Rich Library Demo ===")
    try:
        rich_demo()
    except ImportError:
        print("rich is not installed. Run 'pip install rich' to use this feature.")
