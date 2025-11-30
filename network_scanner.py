#!/usr/bin/env python3
"""
Network Discovery and Scanning Module
Find active hosts and services on the network
"""

import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import socket

class NetworkScanner:
    def __init__(self):
        self.active_hosts = []
        self.common_ports = [21, 22, 23, 53, 80, 135, 139, 443, 445, 3389, 5985, 5986]
    
    def ping_sweep(self, subnet="192.168.1.0/24", timeout=1):
        """Perform ping sweep to discover active hosts"""
        print(f"[*] Starting ping sweep for {subnet}")
        
        network = ipaddress.ip_network(subnet, strict=False)
        active_hosts = []
        
        def ping_host(ip):
            try:
                # Windows ping command
                result = subprocess.run(f"ping -n 1 -w {timeout * 1000} {ip}", 
                                      shell=True, capture_output=True, text=True)
                if result.returncode == 0 and "TTL=" in result.stdout:
                    return str(ip)
            except:
                pass
            return None
        
        # Use threading for faster scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(ping_host, network.hosts())
            
            for ip in results:
                if ip:
                    active_hosts.append(ip)
                    print(f"[+] Active host found: {ip}")
        
        self.active_hosts = active_hosts
        print(f"[+] Found {len(active_hosts)} active hosts")
        return active_hosts
    
    def port_scan(self, target_ip, ports=None):
        """Scan for open ports on target"""
        if ports is None:
            ports = self.common_ports
        
        print(f"[*] Scanning ports on {target_ip}")
        open_ports = []
        
        def check_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(1)
                    result = sock.connect_ex((target_ip, port))
                    if result == 0:
                        return port
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(check_port, ports)
            for port in results:
                if port:
                    open_ports.append(port)
                    print(f"[+] Port {port} open on {target_ip}")
        
        return open_ports
    
    def netbios_scan(self, target_ip):
        """Get NetBIOS information from target"""
        print(f"[*] Scanning NetBIOS info for {target_ip}")
        
        commands = [
            f'nbtstat -A {target_ip}',
            f'nmblookup -A {target_ip}'
        ]
        
        netbios_info = {}
        for cmd in commands:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                netbios_info[cmd] = result.stdout
                print(f"[*] NetBIOS command: {cmd}")
            except Exception as e:
                netbios_info[cmd] = f"Error: {e}"
        
        return netbios_info
    
    def comprehensive_scan(self, subnet="192.168.1.0/24"):
        """Perform comprehensive network scan"""
        print("[*] Starting comprehensive network scan")
        print("=" * 50)
        
        # Step 1: Discover active hosts
        hosts = self.ping_sweep(subnet)
        
        scan_results = {}
        
        # Step 2: Scan each active host
        for host in hosts[:5]:  # Limit to first 5 hosts for demo
            print(f"\\n[*] Scanning host: {host}")
            
            host_info = {
                'ports': self.port_scan(host),
                'netbios': self.netbios_scan(host)
            }
            
            scan_results[host] = host_info
            
            # Display summary
            print(f"    Open ports: {host_info['ports']}")
            if host_info['netbios']:
                print(f"    NetBIOS info gathered")
        
        return scan_results

# Test function
def test_scanner():
    """Test network scanner functionality"""
    scanner = NetworkScanner()
    
    # Test with small subnet or localhost
    print("Testing network scanner...")
    
    # Scan local network (adjust subnet as needed)
    results = scanner.comprehensive_scan("192.168.1.0/24")
    
    print(f"\\n[*] Scan completed. Found {len(results)} hosts with details.")
    
    return results

if __name__ == "__main__":
    test_scanner()
