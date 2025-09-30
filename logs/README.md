# Logs Directory

This directory contains detailed log files from Office Automation Project operations.

## 🎯 Purpose

The logs directory automatically collects detailed troubleshooting output and diagnostic information when running the Mist Wireless Network Troubleshooter and other Office Automation tools.

## 📁 File Structure

### Troubleshooting Logs
- **Format**: `troubleshooting-YYYYMMDD-HHMMSS.log`
- **Content**: Detailed step-by-step troubleshooting analysis
- **Example**: `troubleshooting-20250930-213045.log`

### Log Content Includes:
- 📊 **Session Details** - Client information, timestamps, organization
- 🔍 **Analysis Steps** - Each troubleshooting step with detailed results
- ⚠️ **Issues Detected** - Authentication, DHCP/DNS, client health problems
- 🎯 **Recommendations** - Specific actions to resolve issues
- 📋 **API Responses** - Detailed Mist API interaction logs
- 🛑 **Errors** - Any errors encountered during analysis

## 🚀 Usage

Logs are automatically generated when running troubleshooting commands:

```bash
# Logs are created automatically
python office_automation_cli.py wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100

# Log file path is displayed in output:
# 📝 Log File: D:\office-automation-project\logs\troubleshooting-20250930-213045.log
```

## 📋 Example Log Output

```
2025-09-30 21:30:45 - INFO - ============================================================
2025-09-30 21:30:45 - INFO - MIST WIRELESS NETWORK TROUBLESHOOTING SESSION STARTED
2025-09-30 21:30:45 - INFO - ============================================================
2025-09-30 21:30:45 - INFO - Organization ID: org_12345678
2025-09-30 21:30:45 - INFO - Log file: D:\office-automation-project\logs\troubleshooting-20250930-213045.log
2025-09-30 21:30:45 - INFO - Troubleshooting session started for client aa:bb:cc:dd:ee:ff (192.168.1.100)
2025-09-30 21:30:45 - INFO - Hours back for analysis: 24
2025-09-30 21:30:45 - INFO - STEP 1: Starting client association status and events check
2025-09-30 21:30:46 - INFO - Client found: Marketing-Laptop (MAC: aa:bb:cc:dd:ee:ff) connected to AP ac:12:34:56:78:90
2025-09-30 21:30:46 - INFO - Client details: RSSI=-78, SNR=15, IP=192.168.1.100
2025-09-30 21:30:46 - INFO - STEP 2: Starting authentication and authorization failure analysis
2025-09-30 21:30:47 - INFO - STEP 2 completed: No authentication/authorization issues detected
...
```

## 🔐 Security & Privacy

- ✅ **API Tokens**: Never logged in plaintext (only masked versions)
- ✅ **Client Data**: Only network connectivity data, no personal information
- ✅ **Git Ignored**: Log files are automatically excluded from version control
- ✅ **Local Only**: Logs remain on your local system

## 📈 Log Retention

- **Automatic Cleanup**: None implemented (manual cleanup required)
- **File Size**: Typically 50-200KB per troubleshooting session
- **Recommendation**: Archive or delete old logs periodically to manage disk space

## 🛠️ Troubleshooting

If logs aren't being created:
1. Check disk space availability
2. Verify write permissions to the logs directory
3. Ensure the Office Automation Project has proper file system access

## 📚 Related Documentation

- **Main README**: `../README.md` - Project overview and usage
- **Core Module**: `../MIST_TROUBLESHOOTER_CORE_MODULE.md` - Technical details
- **Output Examples**: `../docs/output-examples.md` - Sample troubleshooting outputs