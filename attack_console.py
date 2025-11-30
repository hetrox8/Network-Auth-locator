#!/usr/bin/env python3
"""
Interactive Network Attack Console
Scan network ‚Üí Choose targets ‚Üí Select attacks ‚Üí Execute
"""

import os
import sys
import time
from network_scanner import NetworkScanner
from target_manager import TargetManager
from attack_library import AttackLibrary

class AttackConsole:
    def __init__(self):
        self.scanner = NetworkScanner()
        self.target_manager = TargetManager()
        self.attacks = AttackLibrary()
        self.current_targets = []
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_banner(self):
        self.clear_screen()
        print("ÌæØ INTERACTIVE NETWORK ATTACK CONSOLE")
        print("=" * 50)
        print("Scan ‚Üí Choose ‚Üí Attack ‚Üí Control")
        print("=" * 50)
        print()
    
    def scan_network_menu(self):
        """Scan network and display discovered hosts"""
        print("[1] NETWORK SCANNING")
        print("-" * 30)
        
        subnet = input("Enter subnet to scan [192.168.1.0/24]: ") or "192.168.1.0/24"
        
        print(f"Scanning {subnet}...")
        results = self.scanner.comprehensive_scan(subnet)
        
        # Add to target database
        for ip, info in results.items():
            self.target_manager.add_target(
                ip=ip,
                ports=info.get('ports', []),
                services=info.get('netbios', {})
            )
        
        self.current_targets = list(results.keys())
        return results
    
    def select_targets_menu(self, discovered_hosts):
        """Let user select which targets to attack"""
        print("\n[2] TARGET SELECTION")
        print("-" * 30)
        print("Discovered Hosts:")
        print("-" * 30)
        
        targets_list = []
        for i, (ip, info) in enumerate(discovered_hosts.items(), 1):
            ports = info.get('ports', [])
            port_info = f"Ports: {ports}" if ports else "No open ports"
            print(f"{i}. {ip:15} - {port_info}")
            targets_list.append(ip)
        
        print("\nSelect targets to attack:")
        print("  [a] All hosts")
        print("  [s] Select specific hosts")
        print("  [w] Windows hosts only (SMB/RDP)")
        print("  [c] Custom selection")
        
        choice = input("\nYour choice: ").lower()
        
        selected_targets = []
        
        if choice == 'a':
            selected_targets = targets_list
            print(f"Selected ALL {len(targets_list)} targets")
        
        elif choice == 'w':
            for ip, info in discovered_hosts.items():
                ports = info.get('ports', [])
                if any(p in ports for p in [135, 139, 445, 3389, 5985]):
                    selected_targets.append(ip)
            print(f"Selected {len(selected_targets)} Windows hosts")
        
        elif choice == 's' or choice == 'c':
            print("\nEnter target numbers (comma-separated):")
            for i, ip in enumerate(targets_list, 1):
                print(f"  {i}. {ip}")
            
            try:
                selections = input("\nTarget numbers: ").strip()
                if selections:
                    indices = [int(x.strip()) - 1 for x in selections.split(',')]
                    selected_targets = [targets_list[i] for i in indices if i < len(targets_list)]
                    print(f"Selected {len(selected_targets)} targets")
            except:
                print("Invalid selection")
        
        return selected_targets
    
    def attack_selection_menu(self, targets):
        """Let user choose which attacks to launch"""
        print("\n[3] ATTACK SELECTION")
        print("-" * 30)
        
        available_attacks = self.attacks.get_available_attacks()
        
        print("Available Attacks:")
        print("-" * 30)
        for i, (attack_id, attack_info) in enumerate(available_attacks.items(), 1):
            print(f"{i}. {attack_info['name']:20} - {attack_info['description']}")
        
        print("\nSelect attacks to launch:")
        print("  [a] All attacks")
        print("  [s] Select specific attacks")
        print("  [r] Remote access attacks only")
        print("  [d] Data collection attacks only")
        
        choice = input("\nYour choice: ").lower()
        
        selected_attacks = []
        
        if choice == 'a':
            selected_attacks = list(available_attacks.keys())
            print(f"Selected ALL {len(selected_attacks)} attacks")
        
        elif choice == 'r':
            for attack_id, attack_info in available_attacks.items():
                if attack_info['category'] == 'remote_access':
                    selected_attacks.append(attack_id)
            print(f"Selected {len(selected_attacks)} remote access attacks")
        
        elif choice == 'd':
            for attack_id, attack_info in available_attacks.items():
                if attack_info['category'] == 'data_collection':
                    selected_attacks.append(attack_id)
            print(f"Selected {len(selected_attacks)} data collection attacks")
        
        elif choice == 's':
            print("\nEnter attack numbers (comma-separated):")
            attack_list = list(available_attacks.items())
            for i, (attack_id, attack_info) in enumerate(attack_list, 1):
                print(f"  {i}. {attack_info['name']}")
            
            try:
                selections = input("\nAttack numbers: ").strip()
                if selections:
                    indices = [int(x.strip()) - 1 for x in selections.split(',')]
                    selected_attacks = [attack_list[i][0] for i in indices if i < len(attack_list)]
                    print(f"Selected {len(selected_attacks)} attacks")
            except:
                print("Invalid selection")
        
        return selected_attacks
    
    def execute_attacks(self, targets, attacks):
        """Execute selected attacks on chosen targets"""
        print("\n[4] EXECUTING ATTACKS")
        print("-" * 30)
        print(f"Targets: {len(targets)} | Attacks: {len(attacks)}")
        print()
        
        results = {}
        
        for target_ip in targets:
            print(f"ÌæØ Attacking: {target_ip}")
            target_results = {}
            
            for attack_id in attacks:
                attack_info = self.attacks.get_attack_info(attack_id)
                print(f"  Ì∫Ä {attack_info['name']}...", end=' ')
                
                try:
                    # Execute the attack
                    result = self.attacks.execute_attack(attack_id, target_ip)
                    target_results[attack_id] = result
                    
                    if result.get('success'):
                        print("‚úÖ SUCCESS")
                    else:
                        print("‚ùå FAILED")
                    
                    # Log result
                    self.target_manager.log_attack_result(
                        target_ip, attack_id, result.get('success', False), result
                    )
                    
                except Exception as e:
                    print(f"‚ùå ERROR: {e}")
                    target_results[attack_id] = {'success': False, 'error': str(e)}
            
            results[target_ip] = target_results
            print()
        
        return results
    
    def display_results(self, results):
        """Display attack results"""
        print("\n[5] ATTACK RESULTS")
        print("-" * 30)
        
        successful_attacks = 0
        total_attacks = 0
        
        for target_ip, target_results in results.items():
            print(f"\nÌ≥ä {target_ip}:")
            for attack_id, result in target_results.items():
                total_attacks += 1
                status = "‚úÖ SUCCESS" if result.get('success') else "‚ùå FAILED"
                attack_name = self.attacks.get_attack_info(attack_id)['name']
                print(f"  {attack_name:20} - {status}")
                
                if result.get('success'):
                    successful_attacks += 1
        
        print(f"\nÌ≥à SUMMARY: {successful_attacks}/{total_attacks} attacks successful")
        
        # Save detailed report
        report = {
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'results': results,
            'summary': {
                'successful_attacks': successful_attacks,
                'total_attacks': total_attacks,
                'success_rate': (successful_attacks / total_attacks * 100) if total_attacks > 0 else 0
            }
        }
        
        import json
        with open('interactive_attack_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Ì≥Ñ Detailed report saved: interactive_attack_report.json")
    
    def main_menu(self):
        """Main interactive menu"""
        self.display_banner()
        
        try:
            # Step 1: Scan Network
            discovered_hosts = self.scan_network_menu()
            if not discovered_hosts:
                print("No hosts discovered!")
                return
            
            input("\nPress Enter to continue...")
            self.display_banner()
            
            # Step 2: Select Targets
            selected_targets = self.select_targets_menu(discovered_hosts)
            if not selected_targets:
                print("No targets selected!")
                return
            
            input("\nPress Enter to continue...")
            self.display_banner()
            
            # Step 3: Select Attacks
            selected_attacks = self.attack_selection_menu(selected_targets)
            if not selected_attacks:
                print("No attacks selected!")
                return
            
            # Confirm execution
            print(f"\nReady to launch {len(selected_attacks)} attacks on {len(selected_targets)} targets")
            confirm = input("Execute attacks? (y/n): ").lower()
            
            if confirm == 'y':
                # Step 4: Execute Attacks
                results = self.execute_attacks(selected_targets, selected_attacks)
                
                # Step 5: Display Results
                self.display_results(results)
            else:
                print("Attack cancelled")
        
        except KeyboardInterrupt:
            print("\n\n‚èπÔ∏è  Attack console stopped by user")
        except Exception as e:
            print(f"\n‚ùå Error: {e}")

def main():
    console = AttackConsole()
    console.main_menu()

if __name__ == "__main__":
    main()
