# Office Automation Project

## Overview
A comprehensive network automation platform built around Mist API integration for automated network monitoring, troubleshooting, and management. This project provides enterprise-grade tools for network administrators to automate routine tasks, monitor network health, and proactively address issues.

## 🎯 Key Features
- **Complete Mist API Integration** - Full authentication and high-level API client
- **Network Monitoring** - Real-time device, site, and client monitoring
- **Automated Troubleshooting** - Intelligent issue detection and resolution
- **Comprehensive Testing** - Unit tests ensuring reliability
- **Production Ready** - Proper error handling, logging, and security

## 🚀 Current Capabilities
### ✅ Implemented
- **Authentication System** (`src/auth/`) - Secure Mist API authentication with token management
- **API Client Library** (`src/api/`) - High-level network operations client
- **Mist Wireless Troubleshooter** (`src/troubleshooting/`) - Complete flowchart-based wireless troubleshooting (Core Module)
- **Unified CLI Interface** (`office_automation_cli.py`) - Comprehensive command-line interface
- **Testing Suite** (`tests/`) - Authentication unit tests
- **Example Scripts** (`examples/`) - Real-world usage demonstrations
- **Project Automation** - Setup scripts and validation tools

### 🔧 Ready for Development
- **Monitoring Modules** (`src/monitoring/`) - Network health and performance monitoring
- **Alert Management** (`src/alerts/`) - Notification and escalation systems
- **Web Dashboard** (`src/dashboard/`) - Visual network management interface

See `docs/project-overview.md` for detailed technical documentation, `MIST_TROUBLESHOOTER_CORE_MODULE.md` for core module details, and `docs/output-examples.md` for sample troubleshooting outputs.

## 📶 Mist Wireless Network Troubleshooter (Core Module)

The Office Automation Project's built-in Mist Wireless Network Troubleshooter provides comprehensive, flowchart-based diagnosis of wireless client connectivity issues.

### 🎯 Key Features
- **Complete Flowchart Implementation**: Follows exact troubleshooting decision tree
- **Smart Escalation Paths**: Automatic routing to appropriate troubleshooting teams
- **Priority-Based Classification**: Issues categorized as HIGH/MEDIUM/LOW severity
- **Comprehensive Analysis**: Client health, AP hardware, RF environment, infrastructure checks
- **Native Implementation**: Built on Office Automation's auth and API infrastructure

### 🔍 Troubleshooting Flow
1. **Client Association Status & Events** - Validates client presence and recent activity
2. **Authentication & Authorization** - Detects ISE/RADIUS/802.1X issues → Routes to Security team
3. **DHCP/DNS Problem Detection** - Identifies network infrastructure issues → Routes to Infrastructure team
4. **Client Health Metrics** - RSSI, SNR, retries, latency analysis
5. **Detailed Analysis** (if health issues found):
   - Client connectivity & reachability testing
   - AP hardware status monitoring
   - RF environment analysis
   - Comprehensive prioritized recommendations

### 🚀 Quick Start
```bash
# Set your API token (one-time setup)
export MIST_API_TOKEN="your_mist_api_token_here"

# Troubleshoot a wireless client
python office_automation_cli.py wireless troubleshoot \
  --client-mac aa:bb:cc:dd:ee:ff \
  --client-ip 192.168.1.100
```

### 📊 Sample Output
```
======================================================================
MIST WIRELESS NETWORK TROUBLESHOOTER
======================================================================
🔍 [STEP 1] Gathering Client Association Status & Events...
✅ Client found: TestDevice on AP ac:12:34:56:78:90

🔍 [STEP 2] Checking Authentication and Authorization Failure Logs...
✅ No authentication/authorization issues detected

🔍 [STEP 3] Checking DNS/DHCP Lease Errors...
✅ No DNS/DHCP lease errors detected

🔍 [STEP 4] Analyzing Client Health Metrics...
🟡 CLIENT HEALTH ISSUES DETECTED:
   • RSSI: Poor signal strength: -75 dBm [MEDIUM]
   • Channel Utilization (5GHz): High utilization: 78% [MEDIUM]

🎯 COMPREHENSIVE TROUBLESHOOTING COMPLETE
   Issues found: 3 (0 HIGH, 3 MEDIUM)

📁 Detailed logs saved to: logs/troubleshooting-20250930-213045.log
======================================================================
```

## Getting Started

### Quick Setup
1. **Validate project structure**: `python validate_setup.py`
2. **Run setup script**: `python setup.py`
3. **Update configuration**: Edit `.env` file with your Mist API credentials
4. **Activate virtual environment**: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
5. **Test installation**: `python examples/auth_example.py`

### Manual Setup
If you prefer manual setup:
1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and update with your credentials

## 🔧 API Usage

### Unified CLI Interface (Recommended)
```bash
# Set environment variable (one-time setup)
export MIST_API_TOKEN="your_mist_api_token_here"

# Test authentication
python office_automation_cli.py auth test

# List organizations
python office_automation_cli.py orgs list

# Troubleshoot wireless client (main feature)
python office_automation_cli.py wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100

# Verbose troubleshooting with extended history
python office_automation_cli.py wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100 --verbose --hours-back 48
```

### Basic Authentication (Programmatic)
```python
from src.auth.mist_auth import MistAuth

# Using environment variables (.env file)
with MistAuth() as auth:
    # Test connection
    status = auth.test_connection()
    print(f"Connection status: {status['status']}")
```

### Network Client Operations
```python
from src.api.mist_client import MistNetworkClient

# High-level network operations
with MistNetworkClient() as client:
    # Get organization sites
    sites = client.get_sites()
    print(f"Found {len(sites)} sites")
    
    # Get all network devices
    devices = client.get_devices()
    print(f"Managing {len(devices)} devices")
    
    # Get current alarms
    alarms = client.get_alarms()
    print(f"Active alarms: {len(alarms)}")
    
    # Perform health check
    health = client.health_check()
    print(f"Network health: {health['status']}")
```

### Wireless Network Troubleshooting (Main Feature)
```python
from src.troubleshooting.mist_wireless import MistWirelessTroubleshooter

# Complete wireless troubleshooting workflow
with MistWirelessTroubleshooter() as troubleshooter:
    results = troubleshooter.troubleshoot_client(
        client_ip="192.168.1.100",
        client_mac="aa:bb:cc:dd:ee:ff",
        hours_back=24
    )
    
    print(f"Status: {results['status']}")
    print(f"Issues found: {len(results['issues_found'])}")
    print(f"Escalation: {results.get('escalation_path')}")
```

### Example Scripts
- `examples/auth_example.py` - Basic authentication testing
- `examples/network_client_example.py` - Network client operations demo
- `office_automation_cli.py` - **Main CLI interface with wireless troubleshooting**

## 🧪 Testing

### Run All Tests
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v
```

### Test Coverage
- **Authentication Tests**: 5 tests covering token validation, error handling, context management
- **Total**: Focused unit tests ensuring core reliability

## 📁 Project Structure
```
office-automation-project/
├── README.md                           # This file
├── NETWORK_AUTOMATION_PLAN.md          # Detailed technical documentation
├── office_automation_cli.py            # ✨ NEW! Unified CLI interface
├── requirements.txt                    # Python dependencies
├── setup.py                           # Automated project setup
├── validate_setup.py                  # Project validation tool
├── .env                               # Environment configuration (not in git)
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
├── LICENSE                            # MIT license
├── config/                            # Configuration files
├── data/                              # Data storage directory
├── logs/                              # 📝 Troubleshooting and application logs
│   ├── README.md                      # Logs documentation
│   └── troubleshooting-*.log          # Auto-generated troubleshooting logs
├── docs/                              # Additional documentation
├── examples/                          # Usage examples
│   ├── auth_example.py                # Basic authentication demo
│   └── network_client_example.py     # Network client operations demo
├── src/                               # Source code
│   ├── __init__.py                    # Package initialization
│   ├── auth/                          # ✅ Authentication system
│   │   ├── __init__.py
│   │   ├── mist_auth.py               # Mist API authentication
│   │   └── README.md                  # Auth module documentation
│   ├── api/                           # ✅ API client library
│   │   ├── __init__.py
│   │   └── mist_client.py             # High-level network client
│   ├── config/                        # ✅ Configuration management
│   │   ├── __init__.py
│   │   └── auth_config.py             # Authentication configuration
│   ├── troubleshooting/               # ✅ Mist Wireless Network Troubleshooter (Core Module)
│   │   ├── __init__.py                # Module exports
│   │   └── mist_wireless.py           # Complete wireless troubleshooting (766 lines)
│   ├── monitoring/                    # 🔧 Network monitoring (ready for development)
│   │   └── __init__.py
│   ├── alerts/                        # 🔧 Alert management (ready for development)
│   │   └── __init__.py
│   └── dashboard/                     # 🔧 Web dashboard (ready for development)
│       └── __init__.py
└── tests/                             # ✅ Test suite
    └── test_auth.py                   # Authentication tests (5 tests)
```

## Contributing
- Follow consistent naming conventions
- Document all scripts and tools
- Test thoroughly before committing changes

## License
MIT License (see LICENSE file)
