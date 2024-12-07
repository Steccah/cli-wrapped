from datetime import datetime
import sys
from termcolor import colored
from time import sleep
import subprocess


global debug

def parse_args():
    global debug
    debug = False
    for arg in sys.argv[1:]:
        if arg == "--help" or arg == "-h":
            print("Usage: cli-wrapped.py [--debug]")
            sys.exit(0)
        if arg == "--debug" or arg == "-d":
            debug = True
            global sleep
            sleep = lambda x: None

def get_fish_history():
    result = subprocess.run(["fish", "-c", "history --show-time"], capture_output=True, text=True)
    return result.stdout

def parse_history(data):
    current_year = datetime.now().year
    cutoff_date = datetime.strptime(f"{current_year}-01-01", "%Y-%m-%d")
    lines = data.strip().split("\n")
    filtered_lines = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("#"):
            timestamp_line = lines[i].lstrip("# ").strip()
            try:
                timestamp = datetime.strptime(timestamp_line, "%a %d %b %Y %I:%M:%S %p %Z")
            except ValueError:
                if debug: print(f"Could not parse timestamp: {timestamp_line}")
                i += 1
                continue
            if timestamp >= cutoff_date:
                if i + 1 < len(lines):
                    filtered_lines.append(lines[i + 1])
            i += 2
        else:
            i += 1
    return filtered_lines

def count_commands(lines):
    commands = {}
    invocations = {}
    while lines:
        command_line = lines.pop(0).strip()
        try:
            base_command = command_line.split()[0]
        except IndexError:
            if debug: print(f"Could not extract base command from: {command_line}")
            continue
        commands[base_command] = commands.get(base_command, 0) + 1
        invocations[command_line] = invocations.get(command_line, 0) + 1
    return commands, invocations

def display_results(lines_count, commands, invocations):
    sorted_commands = sorted(commands.items(), key=lambda x: x[1], reverse=True)
    sorted_invocations = sorted(invocations.items(), key=lambda x: x[1], reverse=True)
    print("\033[H\033[J")
    print(colored("""
 ██████╗██╗     ██╗      ██╗    ██╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝██║     ██║      ██║    ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║     ██║     ██║█████╗██║ █╗ ██║██████╔╝███████║██████╔╝██████╔╝█████╗  ██║  ██║
██║     ██║     ██║╚════╝██║███╗██║██╔══██╗██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██║  ██║
╚██████╗███████╗██║      ╚███╔███╔╝██║  ██║██║  ██║██║     ██║     ███████╗██████╔╝
 ╚═════╝╚══════╝╚═╝       ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═════╝ 
    """, "magenta"))
    print(f'This year you used {colored(lines_count, "red", attrs=["bold"])} commands, of which {colored(len(commands), "red", attrs=["bold"])} were unique.')
    print("Let's see what you used the most...")
    sleep(3)
    print("")
    print("Your top commands were:")
    for command, count in sorted_commands[:5]:
        sleep(1)
        print(f"{colored(command, 'cyan', attrs=['bold'])}: {count}")
    print("")
    sleep(3)

    # bruh this doesnt make sense
    print("Your top invocations were: (to be implemented)")
    for invocation, count in sorted_invocations[:5]:
        sleep(1)
        print(f"{colored(invocation, 'green', attrs=['bold'])}: {count}")


def main():
    parse_args()
    data = get_fish_history()
    lines = parse_history(data)
    lines_count = len(lines)
    commands, invocations = count_commands(lines)
    display_results(lines_count, commands, invocations)

if __name__ == "__main__":
    main()
