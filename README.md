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

#### 📈 **Automated Analysis**
- **Client Discovery** - Live client data with SSID, AP name, RSSI, SNR, IP
- **Authentication Check** - Detects ISE/RADIUS/802.1X failures
- **Network Infrastructure** - DHCP/DNS validation with DNS resolution, internet connectivity, gateway reachability tests
- **Health Metrics** - RSSI, SNR, retry rates, latency analysis with clear thresholds
- **Disconnection Patterns** - 5-minute window analysis (≥7 events threshold)
- **AP Uptime** - Identifies high uptime (>180 days) or recent restarts (<1 hour)

#### 📊 **AP Uptime Thresholds**

| Condition | Threshold | Recommendation |
|-----------|-----------|----------------|
| **High Uptime** | > **180 days** | Reboot recommended during maintenance window |
| **Normal Uptime** | **1 hour - 180 days** | Normal operation |
| **Recent Restart** | < **1 hour** | May indicate stability issues - monitor |

#### 🚀 **Smart Features**
- **DEBUG Logging**: Comprehensive file-based logging (API calls, site searches, data resolution)
- **Team Routing**: Automatic escalation to Security/Infrastructure teams or manual guidance
- **Metric Thresholds**: Clear Good/Fair/Poor references for all metrics
- **Utility Scripts**: `check_clients.py` for quick overview of connected clients

### 🔍 Troubleshooting Workflow
1. 🔍 **Client Discovery** - Locate and validate client association (displays SSID, AP name, RSSI, SNR, IP)
2. 🔐 **Authentication Analysis** - Check for 802.1X/PSK/RADIUS failures
3. 🌐 **Network Infrastructure** - Validate DHCP/DNS functionality
4. 📈 **Health Metrics Analysis** - When issues detected (RSSI, SNR, Retries, Latency):
   - **4a**: Disconnection pattern analysis (5-minute window, ≥7 events threshold)
   - **4a**: Packet loss and latency checks via ping
   - **4b**: AP uptime analysis (using AP ID)
   - **Manual Guidance**: Provides metric thresholds and suggested actions for engineer assessment
5. ✅ **Result Summary** - Comprehensive analysis with escalation paths or manual troubleshooting guidance

### 📝 Technical Specifications

#### 🔍 **Module Details**
- **Location**: `src/troubleshooting/mist_wireless.py`
- **Main Class**: `MistWirelessTroubleshooter`
- **Logging**: DEBUG level to file only (no console clutter)
- **Dependencies**: Built on Office Automation auth and API infrastructure

#### 📁 **Key Functions**
- `get_client_info()` - Searches live clients across all sites, falls back to historical data
- `get_ap_name()` - Resolves AP MAC to friendly hostname
- `analyze_auth_issues()` - Detects authentication failures
- `analyze_dhcp_dns_issues()` - Identifies network infrastructure problems
- `analyze_client_health()` - Evaluates RSSI, SNR, retry rates, latency
- `analyze_disconnection_patterns()` - 5-minute window disconnect analysis
- `check_client_connectivity_ping()` - Packet loss and latency via ping
- `check_ap_uptime()` - AP uptime check using AP ID

#### ⚙️ **Configuration**
- **Authentication**: `.env` file or environment variables
  - `MIST_API_TOKEN` - Required
  - `MIST_ORG_ID` - Optional (auto-detected)
  - `MIST_BASE_URL` - Optional (defaults to EU region)
- **Timeframes**: Configurable (default: 24 hours historical, 5 minutes for disconnects)

### 👍 Production Features

#### 📈 **Diagnostic Coverage**
- **5-Step Workflow**: Client discovery → Authentication → Infrastructure → Health Metrics → Manual Guidance
- **Multi-Site Search**: Automatically searches all sites for client
- **Live Data Priority**: Fetches real-time stats over historical data
- **Comprehensive Logging**: DEBUG logs to file with API traces, site searches, data resolution

#### 🚀 **Enterprise Ready**
- **Multi-Organization Support**: Handles multiple Mist organizations
- **Smart Escalation**: Routes to Security (auth), Infrastructure (DHCP/DNS), or Manual (health)
- **Audit Trail**: Complete session logging with DEBUG details for troubleshooting
- **Error Recovery**: Graceful handling of API failures and missing data

#### 🔐 **Security**
- API tokens via environment variables (never hardcoded)
- Read-only operations (no configuration changes)
- HTTPS-only communication with Mist Cloud
- No sensitive data in logs

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
✅ Client found: Soumya-s-M31 connected to AP PHOENIX-FF-AP10 (ac23160e4683)
   SSID: COLLEAGUE
   Client details: RSSI=-57, SNR=37, IP=10.21.9.247

🔍 [STEP 2] Checking Authentication and Authorization Failure Logs...
✅ No authentication/authorization issues detected

🔍 [STEP 3] Checking DNS/DHCP Lease Errors...
✅ No DNS/DHCP lease errors detected

🔍 [STEP 4] Analyzing Client Health Metrics...
🟡 CLIENT HEALTH ISSUES DETECTED:
   • Retries: High retry rates detected - TX: 19.9%, RX: 0.1% [MEDIUM]

🔍 [STEP 4a] Analyzing Disconnection Patterns (past 5 minutes)...
🔍 [STEP 4a] Checking Packet Loss and Average Latency via Ping...
🔍 [STEP 4b] Checking AP Uptime (using AP ID)...
   AP Uptime: 137.0 days (High uptime - consider scheduled reboot)

🎯 AUTOMATED ANALYSIS COMPLETE
   Issues found: 2 (0 HIGH, 2 MEDIUM)

📋 All automated checks complete. Proceed with manual troubleshooting if needed.

Recommendations:
  📋 Manual Troubleshooting Steps for Engineer:
     1. Perform LAN/WAN/DHCP/DNS checks based on client metrics
     2. Assess AP & Radio Performance (client load, channel utilization, noise)
  
  🔍 Use the following metrics for assessment:
     • RSSI: -57 dBm (Good: > -67 dBm, Fair: -67 to -70, Poor: < -70)
     • SNR: 37 dB (Good: > 20 dB, Fair: 15-20, Poor: < 15)
     • TX Retry Rate: 19.9% (Good: < 5%, Concern: 10%+, Critical: 20%+)
     • RX Retry Rate: 0.1% (Good: < 5%, Concern: 10%+, Critical: 20%+)
  
  💡 Suggested Actions Based on Metrics:
     • High Retries: Check for channel congestion, co-channel interference, or RF obstacles

📁 Detailed logs saved to: logs/troubleshooting-20251022-124117.log
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
