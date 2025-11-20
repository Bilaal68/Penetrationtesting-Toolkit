# Mr-s0l0x - Educational Security Research Framework

## ⚠️ LEGAL WARNING

**This tool is for EDUCATIONAL and AUTHORIZED SECURITY TESTING ONLY.**

- Use only on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is ILLEGAL
- Violators may face criminal prosecution
- The authors are not responsible for misuse of this tool

## Features

This educational framework demonstrates various security concepts:

1. **Command & Control (C2) Server** - Educational demonstration of C2 architecture
2. **Payload Generator** - Generates payloads for Windows and Linux (for authorized testing)
3. **Keylogger Generator** - Educational keylogger code generation
4. **Password Cracker** - Dictionary and brute force password cracking (for password recovery on your own systems)

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main framework:

```bash
python main.py
```

Or on Linux/Mac:

```bash
python3 main.py
```

## Modules

### Command & Control Server
- Creates a C2 server for managing remote connections
- Educational demonstration of C2 architecture
- Use only for authorized security testing

### Payload Generator
- Generates reverse shell payloads for:
  - Windows (Python)
  - Linux (Python)
  - Linux (Bash)
  - Windows (PowerShell)
- All payloads include educational warnings

### Keylogger Generator
- Generates educational keylogger code
- Demonstrates keyboard monitoring concepts
- **Use only on systems you own**

### Password Cracker
- Dictionary-based password cracking
- Brute force capabilities
- Supports MD5, SHA1, SHA256, SHA512
- **For password recovery on your own systems only**

## Ethical Use Guidelines

1. **Always obtain proper authorization** before testing
2. **Use only on systems you own** or have written permission to test
3. **Do not use for malicious purposes**
4. **Respect privacy and laws**
5. **Report vulnerabilities responsibly**

## Disclaimer

This tool is provided for educational purposes only. The authors and contributors are not responsible for any misuse or damage caused by this tool. Users are solely responsible for ensuring they have proper authorization before using any security testing tools.

## License

This project is for educational purposes only. Use responsibly and ethically.

