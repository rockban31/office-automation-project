# AP Health Check Features

## Overview

The Mist Wireless Troubleshooting system includes comprehensive AP (Access Point) health monitoring that analyzes uptime patterns and correlates them with client signal issues to provide actionable recommendations for network optimization.

## Implemented Health Check Features

### 1. **AP Uptime Monitoring**

The system tracks Access Point uptime and provides intelligent reboot recommendations based on industry best practices.

**Detection Thresholds:**
- **High Uptime**: AP uptime > 180 days → Reboot recommended
- **Recent Restart**: AP uptime < 1 hour → May indicate stability issues

**Implementation:**
```python
def check_ap_uptime(self, site_id: str, ap_id: str) -> Optional[Dict[str, Any]]:
    """Check AP uptime and suggest reboot if needed"""
    ap_stats = self.get_ap_stats(site_id, ap_id)
    uptime = ap_stats.get('uptime')
    uptime_hours = uptime / 3600
    
    needs_reboot = uptime_hours > (180 * 24) or uptime_hours < 1
```

**Example Output:**
```
🟡 High AP uptime detected: 45.2 days (Office-Floor-AP-01)
   💡 Recommended: Consider scheduling AP reboot for optimal performance
```

### 2. **Signal Quality + Uptime Correlation**

When poor signal strength (RSSI < -70 dBm) is detected in combination with extended AP uptime (> 14 days), the system recognizes this pattern and suggests AP reboot as a potential remediation.

**Trigger Conditions:**
- Client RSSI < -70 dBm (poor signal)
- AND AP uptime > 14 days

**Recommendation:**
"Consider rebooting AP to improve signal performance and stability"

**Example Scenario:**
```
Client: Guest-Device
Signal Strength: -75 dBm (Poor)
AP Uptime: 18.3 days
AP Name: Conference-Room-AP

Analysis Result:
🟡 Signal issues + Extended AP uptime detected
   💡 Recommended: Reboot AP to potentially improve signal performance
```

## Health Metrics Analyzed

### Client-Side Metrics
- **RSSI (Signal Strength)**: Good: > -67 dBm | Poor: < -70 dBm
- **SNR (Signal-to-Noise)**: Good: > 20 dB | Poor: < 15 dB
- **Retry Rates**: Good: < 10% | Concerning: > 10%
- **Latency**: Good: < 100ms | Concerning: > 100ms

### AP-Side Metrics
- **Uptime**: Normal: 1hr - 180 days | High: > 180 days
- **Recent Restart**: < 1 hour (potential stability issue)
- **AP Status**: Connected vs. Disconnected
- **AP Name Resolution**: Automatic lookup from MAC address

## Client Summary Enhancement

When troubleshooting completes, the system provides a comprehensive client summary including AP health context:

```
📊 CLIENT SUMMARY:
   🏷️  Hostname: JohnDoe-Laptop
   🌐 IP Address: 192.168.1.100
   📱 MAC Address: 00:11:22:33:44:55
   📍 Site: Main Campus
   📶 Signal Strength: -45 dBm (Excellent)
   📊 SNR: 35 dB (Excellent)
   📡 Access Point: Conference-Room-AP-01
   ⏱️  AP Uptime: 12.5 days (Normal)
   🔘 AP Status: connected
```


## Technical Implementation

### Troubleshooting Workflow

The AP health check is integrated into the complete troubleshooting workflow:

1. **Client Discovery**: Locate client by IP/MAC across all sites
2. **Client Health Analysis**: Analyze RSSI, SNR, retry rates, latency
3. **AP Identification**: Extract AP MAC and resolve AP name
4. **AP Health Check**: Retrieve and analyze AP uptime
5. **Correlation Analysis**: Detect patterns between client issues and AP health
6. **Recommendation Generation**: Provide actionable remediation steps

### API Endpoints Used

| Purpose | Endpoint | Method |
|---------|----------|--------|
| Client Search | `/sites/{site_id}/stats/clients` | GET |
| AP Device Info | `/sites/{site_id}/devices/{ap_mac}` | GET |
| AP Statistics | `/sites/{site_id}/stats/devices/{ap_mac}` | GET |
| Client Events | `/orgs/{org_id}/clients/{mac}/events` | GET |

### Decision Logic

```python
# Uptime-based recommendations
if uptime_hours > (180 * 24):
    recommendation = "High uptime - schedule reboot during maintenance window"
elif uptime_hours < 1:
    recommendation = "Recent restart - monitor for stability issues"

# Combined signal + uptime analysis
if rssi < -70 and uptime_days > 14:
    recommendation = "Signal issues + Extended uptime - reboot may improve performance"
```

## JSON Output Structure

The troubleshooting system can output results in JSON format for automation:

```json
{
  "client_info": {
    "hostname": "JohnDoe-Laptop",
    "ip": "192.168.1.100",
    "mac": "00:11:22:33:44:55",
    "site": "Main Campus",
    "rssi": -45,
    "snr": 35,
    "ap_name": "Conference-Room-AP-01",
    "ap_uptime_days": 12.5,
    "ap_status": "connected"
  },
  "issues": [
    {
      "severity": "MEDIUM",
      "metric": "AP Uptime",
      "value": "35.8 days",
      "issue": "High AP uptime detected",
      "recommendation": "Schedule AP reboot during maintenance window"
    }
  ],
  "recommendations": [
    "Consider scheduling AP reboot for optimal performance",
    "Monitor signal quality after reboot",
    "Document maintenance window and client impact"
  ]
}
```

## Best Practices

### 1. **Proactive Maintenance**
- Schedule AP reboots during maintenance windows when uptime exceeds 180 days
- Monitor APs that have recently restarted for recurring issues
- Track uptime patterns across all APs to identify outliers

### 2. **Signal Optimization**
- When signal issues coincide with high AP uptime, prioritize AP reboot
- Verify signal improvements after AP maintenance
- Document baseline performance metrics for comparison

### 3. **Troubleshooting Strategy**
- Always check AP uptime when investigating client connectivity issues
- Correlate multiple data points (RSSI + SNR + uptime + retry rates)
- Use historical data to identify patterns and trends

### 4. **Documentation**
- Log all AP reboots and maintenance activities
- Track "before and after" metrics for reboots
- Maintain uptime statistics for capacity planning

## Benefits

1. **Predictive Maintenance**: Identify APs needing attention before performance degrades
2. **Root Cause Analysis**: Correlate client issues with AP health for targeted fixes
3. **Automated Recommendations**: Clear guidance on when and why to reboot APs
4. **Historical Tracking**: Comprehensive logging of all health checks and recommendations
5. **Operational Efficiency**: Reduce troubleshooting time with automated health analysis

## Command-Line Usage

```bash
# Basic troubleshooting with AP health check
python office_automation_cli.py wireless troubleshoot --client-ip <IP>

# Using MAC address
python office_automation_cli.py wireless troubleshoot --client-mac <MAC>

# Verbose output for detailed AP analysis
python office_automation_cli.py wireless troubleshoot --client-ip <IP> --verbose

# JSON output for automation/integration
python office_automation_cli.py wireless troubleshoot --client-mac <MAC> --json
```

## Programmatic Usage

```python
from src.troubleshooting.mist_wireless import MistWirelessTroubleshooter
from src.auth.mist_auth import MistAuth

# Initialize
auth = MistAuth()
troubleshooter = MistWirelessTroubleshooter(auth_instance=auth, enable_logging=True)

# Run troubleshooting
result = troubleshooter.troubleshoot_client(
    client_identifier="192.168.1.100",
    identifier_type="ip"
)

# Access AP health data
if result['success']:
    client_info = result['client_info']
    ap_uptime = client_info.get('ap_uptime_days')
    print(f"AP Uptime: {ap_uptime} days")
    
    # Check for uptime-related issues
    for issue in result['issues']:
        if 'uptime' in issue['metric'].lower():
            print(f"[{issue['severity']}] {issue['issue']}")
            print(f"Recommendation: {issue.get('recommendation', 'N/A')}")
```

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Compatibility**: Office Automation Project v1.76.0+  
**Feature Status**: ✅ Production Ready & Tested
