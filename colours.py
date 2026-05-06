# colours.py
# Innovation Feature - All colorama helper functions 
# for the Conference Management System storted here. 
# Author: Niamh Hogan

from colorama import init, Fore, Style

# colours reset automatically after every print
init(autoreset=True)

# HEADER - cyan
def print_header(text):
    print(Fore.CYAN + Style.BRIGHT + text)
    print(Fore.CYAN + "-" * len(text))
    
# SUCCESS - green
def print_success(text):
    print(Fore.GREEN + Style.BRIGHT + text)
    
# ERROR - red
def print_error(text):
    print(Fore.RED + Style.BRIGHT + "*** ERROR *** " + text)
    
# MENU ITEM OPTIONS - white
def print_menu_item(text):
    print(Fore.WHITE + text)
    
# DATA ROW OUTPUT- yellow
def print_data_row(text):
    print(Fore.YELLOW + text)
    
# PROMPT - magenta
def print_prompt(text):
    return input(Fore.MAGENTA + text)

# INFO - white/dim
def print_info(text):
    print(Fore.WHITE + Style.DIM + text)