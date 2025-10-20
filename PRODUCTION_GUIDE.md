# Wireless Troubleshooter - Production Guide

## 🚀 Quick Start

### Basic Troubleshooting
```bash
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP>
```

### Example
```bash
python office_automation_cli.py wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100
```

## 📋 Common Commands

### Authentication
```bash
# Test API connection
python office_automation_cli.py auth test

# List organizations
python office_automation_cli.py orgs list
```

### Wireless Troubleshooting
```bash
# Standard troubleshoot
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP>

# Verbose output
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP> --verbose

# Extended history (48 hours)
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP> --hours-back 48

# Specify organization
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP> --org-id <ORG_ID>
```

## 🔧 Troubleshooting Workflow

### Step 1: Client Discovery
Locates client in Mist system and validates association

### Step 2: Authentication Analysis
Checks for 802.1X/PSK/RADIUS failures

### Step 3: Network Infrastructure
Validates DHCP/DNS functionality

### Step 4: Health Metrics
Analyzes RSSI, SNR, retry rates, latency

### Step 5: Connectivity Testing
Performs ping tests and reachability analysis

### Step 6: AP Hardware Status
Monitors AP resources (CPU, memory, temperature)

### Step 7: RF Environment
Analyzes channel utilization and interference

## 📊 Output Interpretation

### Issue Priorities
- **🔴 HIGH**: Critical issues requiring immediate attention
- **🟡 MEDIUM**: Issues that may impact performance
- **🟢 LOW**: Minor issues or informational items

### Escalation Paths
- **Security Team**: Authentication/Authorization failures
- **Infrastructure Team**: DHCP/DNS issues
- **Network Team**: RF environment problems

## 📁 Log Files

Detailed logs saved to: `logs/troubleshooting-YYYYMMDD-HHMMSS.log`

### View Recent Logs (PowerShell)
```powershell
# List recent logs
Get-ChildItem logs\troubleshooting-*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# View latest log
Get-Content (Get-ChildItem logs\troubleshooting-*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
```

## 🔐 Security

- API token stored in `.env` file (never commit to git)
- All communications over HTTPS
- Read-only API operations
- No configuration changes made

## 📞 Support

### Environment Check
```bash
python validate_setup.py
```

### Test Suite
```bash
python -m pytest tests/ -v
```

### Authentication Test
```bash
python office_automation_cli.py auth test
```

## 🎯 Production Deployment

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Action: Start a program
4. Program: `python`
5. Arguments: `D:\office-automation-project\office_automation_cli.py wireless troubleshoot --client-mac <MAC> --client-ip <IP>`
6. Start in: `D:\office-automation-project`


## 📈 Performance

- Average analysis time: 10-30 seconds
- API rate limit: Respects Mist API quotas
- Concurrent analysis: Supported for multiple clients

## ✅ Production Checklist

- [ ] `.env` file configured with valid API token
- [ ] `python validate_setup.py` passes
- [ ] `python -m pytest tests/ -v` passes (5 tests)
- [ ] `python office_automation_cli.py auth test` succeeds
- [ ] Test troubleshoot command with known client
- [ ] Verify logs directory is writable
- [ ] Document wrapper scripts/functions for your team
- [ ] Set up scheduled monitoring (if needed)

## 🎓 Training

### For Network Engineers
1. Show basic troubleshoot command
2. Demonstrate verbose output
3. Explain log interpretation
4. Review escalation paths

### For Automation Teams
1. Show programmatic usage via Python API
2. Demonstrate JSON output parsing
3. Explain integration patterns
4. Review error handling

## 📚 Additional Resources

- **Main Documentation**: `README.md`
- **Project Overview**: `docs/project-overview.md`
- **API Quick Reference**: `docs/mist_api_quick_reference.md`
- **Troubleshooting Reference**: `docs/mist_api_troubleshooting_reference.md`

---

**Status**: ✅ Production Ready  
**Version**: 1.75.1  
**Last Updated**: 2025-10-20
