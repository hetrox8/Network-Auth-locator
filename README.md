# Network Red Team Toolkit

> **⚠️ DISCLAIMER: This toolkit is intended for authorized security testing and educational purposes only. Unauthorized access to computer systems is illegal. Always obtain proper authorization before conducting any security assessments.**

A comprehensive Python-based red team toolkit for network security testing, credential verification, and authorized penetration testing engagements.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Credentials Setup](#credentials-setup)
- [Usage](#usage)
- [Modules](#modules)
- [Legal Notice](#legal-notice)

## ✨ Features

- **Network Discovery**: Ping sweep and port scanning
- **SMB Lateral Movement**: Share discovery and file operations
- **WMI Remote Execution**: Remote command execution via WMI
- **Interactive Attack Console**: Menu-driven attack selection
- **Comprehensive Reporting**: JSON-based engagement reports

## 📦 Prerequisites

- **Operating System**: Windows (recommended) or Linux with Wine
- **Python Version**: Python 3.6+
- **Network Access**: Administrative access to target network
- **Permissions**: Local administrator privileges

### Required Python Packages

```bash
pycryptodome
requests
pillow
psutil
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hetrox8/Network-Auth-locator.git
   cd Network-Auth-locator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python quick_test.py
   ```

## ⚙️ Configuration

### Network Configuration

Configure the target subnet in the toolkit:

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `subnet` | `192.168.1.0/24` | Target network subnet for scanning |
| `timeout` | `1` second | Ping timeout for host discovery |
| `max_workers` | `50` | Thread pool size for concurrent scanning |

### Port Configuration

Common ports scanned by default:

```python
common_ports = [21, 22, 23, 53, 80, 135, 139, 443, 445, 3389, 5985, 5986]
```

| Port | Service |
|------|---------|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 53 | DNS |
| 80 | HTTP |
| 135 | RPC |
| 139 | NetBIOS |
| 443 | HTTPS |
| 445 | SMB |
| 3389 | RDP |
| 5985/5986 | WinRM |

## 🔐 Credentials Setup

### Windows Domain Credentials

For authenticated scanning and lateral movement, configure the following credentials:

```bash
# Set environment variables for authentication
set DOMAIN_USER=<your_domain_username>
set DOMAIN_PASS=<your_domain_password>
set DOMAIN_NAME=<your_domain_name>
```

Or on Linux/macOS:

```bash
export DOMAIN_USER=<your_domain_username>
export DOMAIN_PASS=<your_domain_password>
export DOMAIN_NAME=<your_domain_name>
```

### Credential Requirements

| Credential Type | Required For | Privilege Level |
|-----------------|--------------|-----------------|
| Domain Admin | Full network access | Highest |
| Local Admin | Single host access | High |
| Standard User | Basic enumeration | Low |

### SMB Authentication

For SMB-based operations, ensure:

1. **Credential Storage**: Credentials are passed via Windows session or explicitly configured
2. **Share Access**: User has read/write access to target shares
3. **Network Authentication**: NTLM or Kerberos authentication enabled

### WMI Authentication

For WMI remote execution:

```bash
# Windows command line authentication
wmic /node:<TARGET_IP> /user:<USERNAME> /password:<PASSWORD> <command>
```

### C2 Server Configuration (For Advanced Use)

If using reverse shell capabilities, configure:

```python
C2_HOST = "192.168.1.100"  # Your command & control server IP
C2_PORT = 4444              # Listening port
```

## 📖 Usage

### Interactive Attack Console

Launch the interactive menu-driven console:

```bash
python launch.py
```

### Main Controller

Run a full engagement workflow:

```bash
python main_controller.py
```

### Individual Modules

**Network Scanning**:
```bash
python network_scanner.py
```

**SMB Testing**:
```bash
python smb_lateral.py
```

**WMI Testing**:
```bash
python wmi_remote.py
```

### Example Workflow

1. **Start the console**:
   ```bash
   python launch.py
   ```

2. **Scan the network**: Enter target subnet when prompted (e.g., `192.168.1.0/24`)

3. **Select targets**: Choose from discovered hosts

4. **Choose attacks**: Select attack types (remote access, data collection, reconnaissance)

5. **Execute**: Confirm and run selected attacks

6. **Review results**: Check `red_team_report.json` for detailed findings

## 📁 Modules

| Module | File | Description |
|--------|------|-------------|
| Network Scanner | `network_scanner.py` | Host discovery and port scanning |
| SMB Lateral | `smb_lateral.py` | SMB share operations and file copy |
| WMI Remote | `wmi_remote.py` | Remote command execution via WMI |
| Attack Library | `attack_library.py` | Collection of attack techniques |
| Attack Console | `attack_console.py` | Interactive attack menu |
| Main Controller | `main_controller.py` | Automated engagement workflow |

### Attack Categories

**Remote Access**:
- SMB Backdoor
- WMI Persistence
- RDP Backdoor
- Service Backdoor

**Data Collection**:
- Keylogger
- Credential Dumper
- Browser Stealer
- Network Sniffer

**Reconnaissance**:
- System Info
- Network Scan
- User Enumeration

## 📊 Output Files

| File | Description |
|------|-------------|
| `red_team_report.json` | Engagement results and findings |
| `interactive_attack_report.json` | Attack console session report |
| `test_payload.txt` | Sample payload for testing |

## ⚖️ Legal Notice

**IMPORTANT**: This toolkit is provided for **authorized security testing only**.

- ✅ Use only on networks you own or have explicit written permission to test
- ✅ Obtain proper authorization before any engagement
- ✅ Follow responsible disclosure practices
- ✅ Comply with all applicable laws and regulations

- ❌ Do NOT use for unauthorized access
- ❌ Do NOT use for malicious purposes
- ❌ Do NOT use without proper authorization

**The authors are not responsible for any misuse or damage caused by this toolkit.**

## 📝 License

This project is intended for educational and authorized security testing purposes only.

## 🤝 Contributing

Contributions for defensive improvements and educational enhancements are welcome. Please ensure all contributions follow responsible security practices.

---

**Remember: Always get authorization before testing!**
