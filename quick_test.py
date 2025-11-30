#!/usr/bin/env python3
"""
Quick Test - Verify all modules work
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_modules():
    print("Testing Red Team Toolkit Modules")
    print("=" * 40)
    
    try:
        # Test SMB Module
        from smb_lateral import SMBLateralMovement
        print("[1] Testing SMB Module...")
        smb = SMBLateralMovement()
        shares = smb.discover_shares("127.0.0.1")
        print(f"   SMB Shares found: {len(shares)}")
        
        # Test WMI Module  
        from wmi_remote import WMIRemoteExecution
        print("[2] Testing WMI Module...")
        wmi = WMIRemoteExecution()
        accessible = wmi.test_wmi_connectivity("127.0.0.1")
        print(f"   WMI Accessible: {accessible}")
        
        # Test Network Scanner
        from network_scanner import NetworkScanner
        print("[3] Testing Network Scanner...")
        scanner = NetworkScanner()
        print("   Scanner initialized successfully")
        
        print("All modules loaded successfully!")
        print("Run 'python main_controller.py' to start!")
        
    except Exception as e:
        print(f"Module test failed: {e}")
        print("Make sure you're on Windows and have required permissions")

if __name__ == "__main__":
    test_modules()
