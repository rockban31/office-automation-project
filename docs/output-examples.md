# Enhanced Output Examples

## Scenario 1: Signal Issues + High AP Uptime (Your Requested Feature)

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 192.168.1.150 --mac 00:1A:2B:3C:4D:5E
```

### Output:
```
🔍 Mist Network Troubleshooting Tool
==================================================
📍 Target IP: 192.168.1.150
📍 Target MAC: 00:1A:2B:3C:4D:5E
📝 Log File: D:\logs\troubleshooting-20250911-123554.log

==================================================

[1/4] Verifying Mist API connectivity...
   ✅ Connected to Mist API (15 sites found)

[2/4] Checking authentication & authorization events...
   ✅ No authentication failures detected

[3/4] Checking DNS & DHCP lease issues...
   ✅ No DNS/DHCP issues detected

[4/4] Analyzing client health metrics...
   ✅ Client found: Marketing-Laptop (192.168.1.150)
   🟡 Poor signal strength: -78 dBm
      Check AP placement or client location
   🟡 Signal issues + High uptime (18.3 days)
      💡 Suggested: Consider rebooting AP to improve signal performance

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🟡 2 WARNING(S) DETECTED:
   • Poor WiFi signal strength (-78 dBm)
     💡 Suggested: Check AP placement, client location, or interference
   • Signal issues + High AP uptime: 18.3 days (Conference-Room-AP-02)
     💡 Suggested: Consider rebooting AP to improve signal performance and stability

📊 CLIENT SUMMARY:
   🏷️  Hostname: Marketing-Laptop
   🌐 IP Address: 192.168.1.150
   📱 MAC Address: 00:1A:2B:3C:4D:5E
   📍 Site: Main Office
   📶 Signal Strength: -78 dBm
   📊 SNR: 15 dB
   📡 Access Point: Conference-Room-AP-02
   ⏱️  AP Uptime: 18.3 days
   🔘 AP Status: connected

📁 Detailed logs saved to: D:\logs\troubleshooting-20250911-123554.log
============================================================
```

---

## Scenario 2: High AP Uptime Warning (30+ days)

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 10.0.1.75 --mac 11:22:33:44:55:66
```

### Output:
```
🔍 Mist Network Troubleshooting Tool
==================================================
📍 Target IP: 10.0.1.75
📍 Target MAC: 11:22:33:44:55:66
📝 Log File: D:\logs\troubleshooting-20250911-123558.log

==================================================

[1/4] Verifying Mist API connectivity...
   ✅ Connected to Mist API (15 sites found)

[2/4] Checking authentication & authorization events...
   ✅ No authentication failures detected

[3/4] Checking DNS & DHCP lease issues...
   ✅ No DNS/DHCP issues detected

[4/4] Analyzing client health metrics...
   ✅ Client found: Finance-Desktop (10.0.1.75)
   🟡 High AP uptime: 125.7 days (Finance-Floor-AP-01)
      💡 Suggested: Consider checking and rebooting AP for optimal performance

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🟡 1 WARNING(S) DETECTED:
   • High AP uptime: 125.7 days (Finance-Floor-AP-01)
     💡 Suggested: Consider checking and rebooting AP for optimal performance and stability

📊 CLIENT SUMMARY:
   🏷️  Hostname: Finance-Desktop
   🌐 IP Address: 10.0.1.75
   📱 MAC Address: 11:22:33:44:55:66
   📍 Site: Corporate HQ
   📶 Signal Strength: -45 dBm
   📊 SNR: 38 dB
   📡 Access Point: Finance-Floor-AP-01
   ⏱️  AP Uptime: 125.7 days
   🔘 AP Status: connected

✅ All network health indicators are within normal parameters
   → Client is properly connected and performing well
   → Consider AP maintenance due to high uptime
   → Continue with standard troubleshooting if needed

📁 Detailed logs saved to: D:\logs\troubleshooting-20250911-123558.log
============================================================
```

---

## Scenario 3: Critical AP Issues (60+ days + Performance Problems)

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 172.16.1.200 --mac AA:BB:CC:DD:EE:FF
```

### Output:
```
🔍 Mist Network Troubleshooting Tool
==================================================
📍 Target IP: 172.16.1.200
📍 Target MAC: AA:BB:CC:DD:EE:FF
📝 Log File: D:\logs\troubleshooting-20250911-123602.log

==================================================

[1/4] Verifying Mist API connectivity...
   ✅ Connected to Mist API (15 sites found)

[2/4] Checking authentication & authorization events...
   ✅ No authentication failures detected

[3/4] Checking DNS & DHCP lease issues...
   ✅ No DNS/DHCP issues detected

[4/4] Analyzing client health metrics...
   ✅ Client found: Warehouse-Scanner (172.16.1.200)
   🔴 Very high AP uptime: 198.5 days (Warehouse-AP-05)
      💡 Action: Reboot AP immediately to prevent performance degradation
   🟡 High memory usage: 94% (Warehouse-AP-05)
      💡 Suggested: Consider rebooting AP to free memory
   🟡 High channel utilization: 87% on 2.4GHz (Warehouse-AP-05)
      💡 Suggested: Check for interference or consider AP load balancing

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🔴 1 CRITICAL ISSUE(S) FOUND:
   • Very high AP uptime: 78.2 days (Warehouse-AP-05)
     💡 Action: Reboot AP immediately to prevent performance degradation

🟡 2 WARNING(S) DETECTED:
   • High memory usage: 94% (Warehouse-AP-05)
     💡 Suggested: Consider rebooting AP to free memory and improve performance
   • High channel utilization: 87% on 2.4GHz (Warehouse-AP-05)
     💡 Suggested: Check for RF interference or consider AP load balancing

🛑 IMMEDIATE ACTION REQUIRED:
   → Verify client is connected to Mist network
   → Check client device settings
   → Review AP placement and coverage

📊 CLIENT SUMMARY:
   🏷️  Hostname: Warehouse-Scanner
   🌐 IP Address: 172.16.1.200
   📱 MAC Address: AA:BB:CC:DD:EE:FF
   📍 Site: Distribution Center
   📶 Signal Strength: -52 dBm
   📊 SNR: 28 dB
   📡 Access Point: Warehouse-AP-05
   ⏱️  AP Uptime: 78.2 days
   🔘 AP Status: connected

📁 Detailed logs saved to: D:\logs\troubleshooting-20250911-123602.log
============================================================
```

---

## Scenario 4: Perfect Health - No Issues Detected

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 192.168.50.100 --mac 12:34:56:78:9A:BC
```

### Output:
```
🔍 Mist Network Troubleshooting Tool
==================================================
📍 Target IP: 192.168.50.100
📍 Target MAC: 12:34:56:78:9A:BC
📝 Log File: D:\logs\troubleshooting-20250911-123605.log

==================================================

[1/4] Verifying Mist API connectivity...
   ✅ Connected to Mist API (15 sites found)

[2/4] Checking authentication & authorization events...
   ✅ No authentication failures detected

[3/4] Checking DNS & DHCP lease issues...
   ✅ No DNS/DHCP issues detected

[4/4] Analyzing client health metrics...
   ✅ Client found: CEO-MacBook (192.168.50.100)
   ✅ Client health metrics are within normal ranges

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

✅ NO CRITICAL ISSUES DETECTED

📊 CLIENT SUMMARY:
   🏷️  Hostname: CEO-MacBook
   🌐 IP Address: 192.168.50.100
   📱 MAC Address: 12:34:56:78:9A:BC
   📍 Site: Executive Floor
   📶 Signal Strength: -42 dBm
   📊 SNR: 45 dB
   📡 Access Point: Executive-AP-01
   ⏱️  AP Uptime: 8.3 days
   🔘 AP Status: connected

✅ All network health indicators are within normal parameters
   → Client is properly connected and performing well
   → No immediate network issues detected
   → Continue with standard troubleshooting if needed

📁 Detailed logs saved to: D:\logs\troubleshooting-20250911-123605.log
============================================================
```

---

## Scenario 5: Authentication Issues (Early Exit)

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 10.50.1.25 --mac 98:76:54:32:10:AB
```

### Output:
```
🔍 Mist Network Troubleshooting Tool
==================================================
📍 Target IP: 10.50.1.25
📍 Target MAC: 98:76:54:32:10:AB
📝 Log File: D:\logs\troubleshooting-20250911-123608.log

==================================================

[1/4] Verifying Mist API connectivity...
   ✅ Connected to Mist API (15 sites found)

[2/4] Checking authentication & authorization events...
   🔴 Authentication failures detected
      💡 Recommendation: Check ISE/RADIUS configuration and policies

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 1/4 checks

🔴 1 CRITICAL ISSUE(S) FOUND:
   • Authentication/authorization failures detected via Mist API
     💡 Action: Check ISE/RADIUS configuration and user policies

🛑 IMMEDIATE ACTION REQUIRED:
   → Check ISE/RADIUS server configuration
   → Verify user credentials and policies
   → Review authentication logs

📁 Detailed logs saved to: D:\logs\troubleshooting-20250911-123608.log
============================================================
```

---

## Scenario 6: JSON Output Example

### Command:
```bash
python scripts/automated_network_troubleshooting.py --ip 192.168.1.150 --mac 00:1A:2B:3C:4D:5E --json
```

### Output:
```json
{
  "target_ip": "192.168.1.150",
  "target_mac": "00:1A:2B:3C:4D:5E",
  "has_auth_errors": false,
  "has_dns_errors": false,
  "has_dhcp_errors": false,
  "has_client_health_issues": true,
  "issues_detected": [
    {
      "level": "WARNING",
      "message": "Poor WiFi signal strength (-78 dBm)",
      "category": "health",
      "recommendation": "Check AP placement, client location, or interference"
    },
    {
      "level": "WARNING", 
      "message": "Signal issues + High AP uptime: 18.3 days (Conference-Room-AP-02)",
      "category": "health",
      "recommendation": "Consider rebooting AP to improve signal performance and stability"
    }
  ],
  "log_path": "D:\\logs\\troubleshooting-20250911-123554.log",
  "timestamp": "2025-09-11T12:35:54.123456",
  "mist_device_found": true,
  "mist_device_info": {
    "hostname": "Marketing-Laptop",
    "ip": "192.168.1.150",
    "mac": "00:1A:2B:3C:4D:5E",
    "rssi": -78,
    "snr": 15,
    "ap_id": "ap-conf-room-02"
  },
  "client_summary": {
    "hostname": "Marketing-Laptop",
    "ip": "192.168.1.150", 
    "mac": "00:1A:2B:3C:4D:5E",
    "site": "Main Office",
    "rssi": "-78 dBm",
    "snr": "15 dB",
    "ap_name": "Conference-Room-AP-02",
    "ap_uptime_days": "18.3 days",
    "ap_status": "connected"
  },
  "total_checks": 4,
  "completed_checks": 4
}
```

---

## Key Visual Elements

### **🎨 Color Coding:**
- 🔍 **Blue**: Headers and informational elements
- ✅ **Green**: Success indicators and healthy metrics  
- 🟡 **Yellow**: Warning issues that need attention
- 🔴 **Red**: Critical issues requiring immediate action
- 💡 **Yellow**: Recommendations and suggested actions
- 🛑 **Red**: Immediate action required sections

### **📊 Progress Tracking:**
- `[1/4]`, `[2/4]`, `[3/4]`, `[4/4]` show real-time progress
- `✅ Completed X/4 checks` in summary shows final progress

### **🎯 Your Specific Feature:**
```
🟡 Signal issues + High uptime (18.3 days)
   💡 Suggested: Consider rebooting AP to improve signal performance
```

This enhanced output provides **clear, actionable intelligence** for network troubleshooting with **specific AP reboot recommendations** based on the correlation between signal quality and AP uptime! 🚀
