#!/usr/bin/env python3
"""
WMI Remote Execution Module
Use Windows Management Instrumentation for remote commands
"""

import subprocess
import time

class WMIRemoteExecution:
    def __init__(self):
        self.wmi_commands = {
            'process_create': 'wmic /node:TARGET process call create "COMMAND"',
            'service_list': 'wmic /node:TARGET service list brief',
            'process_list': 'wmic /node:TARGET process list brief',
            'share_list': 'wmic /node:TARGET share get name,path',
            'computer_info': 'wmic /node:TARGET computersystem get name,domain,manufacturer,model',
            'user_list': 'wmic /node:TARGET useraccount get name,disabled'
        }
    
    def execute_wmi_command(self, target_ip, command_type, **kwargs):
        """Execute WMI command on remote system"""
        print(f"[*] Executing WMI command on {target_ip}: {command_type}")
        
        if command_type not in self.wmi_commands:
            return {'success': False, 'error': f"Unknown command type: {command_type}"}
        
        command = self.wmi_commands[command_type].replace('TARGET', target_ip)
        
        if 'process_command' in kwargs:
            command = command.replace('COMMAND', kwargs['process_command'])
        
        try:
            print(f"[*] WMI Command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            
            output = {
                'success': result.returncode == 0,
                'command': command,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
            if result.returncode == 0:
                print(f"[+] WMI command executed successfully")
                print(f"[*] Output: {result.stdout[:500]}...")
            else:
                print(f"[-] WMI command failed: {result.stderr}")
            
            return output
            
        except Exception as e:
            error_msg = f"WMI execution error: {str(e)}"
            print(f"[-] {error_msg}")
            return {'success': False, 'error': error_msg}
    
    def remote_code_execution(self, target_ip, command):
        """Execute commands remotely via WMI"""
        print(f"[*] Attempting remote code execution on {target_ip}")
        print(f"[*] Command: {command}")
        
        return self.execute_wmi_command(target_ip, 'process_create', process_command=command)
    
    def gather_system_info(self, target_ip):
        """Gather comprehensive system information via WMI"""
        print(f"[*] Gathering system information from {target_ip}")
        
        info = {}
        commands = ['computer_info', 'service_list', 'user_list', 'share_list']
        
        for cmd in commands:
            result = self.execute_wmi_command(target_ip, cmd)
            info[cmd] = result
        
        return info
    
    def test_wmi_connectivity(self, target_ip):
        """Test if WMI is accessible on target"""
        print(f"[*] Testing WMI connectivity to {target_ip}")
        
        # Simple WMI query to test connectivity
        test_cmd = f'wmic /node:{target_ip} computersystem get name /value'
        
        try:
            result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and 'Name=' in result.stdout:
                print(f"[+] WMI accessible on {target_ip}")
                return True
            else:
                print(f"[-] WMI not accessible on {target_ip}")
                return False
                
        except Exception as e:
            print(f"[-] WMI test failed: {e}")
            return False

# Test function
def test_wmi():
    """Test WMI functionality"""
    wmi = WMIRemoteExecution()
    
    # Test with localhost
    test_ip = "127.0.0.1"
    print(f"Testing WMI with {test_ip}...")
    
    # Test connectivity
    accessible = wmi.test_wmi_connectivity(test_ip)
    print(f"WMI accessible: {accessible}")
    
    if accessible:
        # Test simple command
        result = wmi.remote_code_execution(test_ip, "whoami")
        print(f"Command execution result: {result.get('success', False)}")
        
        # Gather system info
        info = wmi.gather_system_info(test_ip)
        print("System info gathered")

if __name__ == "__main__":
    test_wmi()
