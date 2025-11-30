#!/usr/bin/env python3
"""
One-command launcher for interactive attack console
"""

from attack_console import AttackConsole

if __name__ == "__main__":
    print("íº Starting Interactive Attack Console...")
    console = AttackConsole()
    console.main_menu()
