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

## 📶 Mist Wireless Network Troubleshooter (Core Module)

**Status:** ✅ **PRODUCTION READY**

The Mist Wireless Network Troubleshooter is a **core operational module** of the Office Automation Project, providing comprehensive, flowchart-based troubleshooting capabilities for wireless network connectivity issues. This module leverages the project's shared authentication and API infrastructure to deliver enterprise-grade network troubleshooting.

### 🏢 Core Module Architecture

#### 🔧 **Shared Infrastructure**
- **Authentication System**: Built on `src.auth.MistAuth` for consistent API access
- **API Client**: Leverages shared HTTP client and error handling
- **Configuration Management**: Uses project-wide configuration system
- **Logging & Error Handling**: Integrated with project logging infrastructure

#### 📱 **CLI Interface**
```bash
# Core troubleshooting commands
python office_automation_cli.py auth test
python office_automation_cli.py orgs list  
python office_automation_cli.py wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100
```

#### 🐍 **Programmatic API**
```python
from src.troubleshooting.mist_wireless import MistWirelessTroubleshooter
from src.auth.mist_auth import MistAuth

# Native module usage
with MistAuth() as auth:
    troubleshooter = MistWirelessTroubleshooter(auth_instance=auth)
    results = troubleshooter.troubleshoot_client(...)
```

### 🎯 Core Features

#### 📈 **Comprehensive Analysis**
- **Client Association Status & Events** - Validates connectivity and recent activity
- **Authentication & Authorization** - Detects ISE/RADIUS/802.1X issues
- **Network Infrastructure** - DHCP/DNS problem detection and resolution
- **Client Health Metrics** - RSSI, SNR, retries, latency analysis
- **AP Hardware Status** - Memory, CPU, temperature monitoring
- **RF Environment Analysis** - Channel utilization, noise, interference detection

#### 🚀 **Smart Escalation**
- **Priority Classification**: HIGH/MEDIUM/LOW severity categorization
- **Team Routing**: Automatic escalation to Security/Infrastructure teams
- **Actionable Recommendations**: Specific steps for issue resolution

### 🔍 Troubleshooting Workflow
1. 🔍 **Client Discovery** - Locate and validate client association
2. 🔐 **Authentication Analysis** - Check for 802.1X/PSK/RADIUS failures
3. 🌐 **Network Infrastructure** - Validate DHCP/DNS functionality
4. 📈 **Health Metrics** - Analyze signal strength, SNR, retry rates
5. 📶 **Connectivity Testing** - Ping tests and reachability analysis
6. 💻 **AP Hardware Status** - Monitor AP resources and performance
7. 📡 **RF Environment** - Channel utilization and interference analysis

### 📝 Technical Specifications

#### 🔍 **Module Details**
- **Location**: `src/troubleshooting/mist_wireless.py`
- **Lines of Code**: 766 lines
- **Main Class**: `MistWirelessTroubleshooter`
- **Dependencies**: Built on Office Automation auth and API infrastructure

#### 📁 **Module Structure**
```
src/troubleshooting/
├── __init__.py                    # Module exports and initialization
└── mist_wireless.py               # Core troubleshooter implementation (766 lines)
    ├── MistWirelessTroubleshooter  # Main troubleshooter class
    ├── get_client_info()           # Client discovery and validation
    ├── analyze_auth_issues()       # Authentication failure detection
    ├── analyze_dhcp_dns_issues()   # Network infrastructure analysis
    ├── analyze_client_health()     # Health metrics evaluation
    ├── check_connectivity()        # Network reachability testing
    ├── analyze_ap_hardware()       # AP resource monitoring
    └── analyze_rf_environment()    # RF interference analysis
```

#### ⚙️ **Configuration**
- **Authentication**: Environment variables or `.env` file
- **Organization**: Auto-detection or explicit specification
- **Timeframes**: Configurable event history (default: 24 hours)

### 👍 Enterprise Capabilities

#### 📈 **Diagnostic Coverage**
- **Full Troubleshooting Workflow**: Implements complete Mist troubleshooting flowchart
- **Multi-Layer Analysis**: From client association to RF environment evaluation
- **Real-Time Monitoring**: Live client health and AP status monitoring
- **Historical Analysis**: Event correlation and trend identification

#### 🚀 **Enterprise Features**
- **Scalable Architecture**: Handles multiple organizations and sites
- **API-First Design**: Programmatic access for automation and integration
- **Comprehensive Logging**: Detailed troubleshooting audit trails
- **Error Recovery**: Robust error handling and graceful failure modes

#### 🔍 **Advanced Analysis**
- **Smart Correlation**: Links symptoms to root causes
- **Priority-Based Triage**: Automatic severity classification
- **Team Escalation**: Routes issues to appropriate technical teams
- **Actionable Output**: Specific recommendations for issue resolution

### 🔐 **Security Considerations**
- API tokens stored securely via environment variables
- No sensitive data logged or stored locally
- Read-only API operations (no configuration changes)
- Secure HTTPS communication with Mist Cloud

### 📈 **Performance & Scalability**
- Optimized API calls with intelligent caching
- Concurrent processing for multi-client analysis
- Configurable timeout and retry mechanisms
- Efficient memory usage for large-scale deployments

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
├── README.md                           # This comprehensive documentation file
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
