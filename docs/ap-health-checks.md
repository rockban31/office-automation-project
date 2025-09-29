# AP Health Check Features

## Overview
The automated network troubleshooting script now includes comprehensive AP (Access Point) health checks that analyze signal issues, uptime, performance metrics, and provide specific recommendations including AP reboot suggestions.

## New AP Health Check Features

### 1. **High AP Uptime Detection**
- **Warning Threshold**: AP uptime > 90 days
- **Critical Threshold**: AP uptime > 180 days
- **Recommendation**: "Consider checking and rebooting AP for optimal performance and stability"

```
🟡 High AP uptime: 125.4 days (Main-Floor-AP-01)
   💡 Suggested: Consider checking and rebooting AP for optimal performance and stability
```

### 2. **Combined Signal Issues + High Uptime**
- **Trigger**: Client RSSI < -70 dBm AND AP uptime > 14 days
- **Recommendation**: "Consider rebooting AP to improve signal performance and stability"

```
🟡 Signal issues + High AP uptime: 25.3 days (Conference-Room-AP)
   💡 Suggested: Consider rebooting AP to improve signal performance and stability
```

### 3. **Channel Utilization Monitoring**
- **Warning Threshold**: Channel utilization > 80%
- **Recommendation**: "Check for RF interference or consider AP load balancing"

```
🟡 High channel utilization: 85% on 2.4GHz (Lobby-AP-03)
   💡 Suggested: Check for RF interference or consider AP load balancing
```

### 4. **AP Status Monitoring**
- **Critical Issues**: AP status not 'connected' or 'online'
- **Recommendation**: "Check AP connectivity, power status, and network configuration"

```
🔴 AP status issue: disconnected (Warehouse-AP-07)
   💡 Action: Check AP connectivity, power status, and network configuration
```

### 5. **Memory and CPU Usage**
- **Memory Warning**: > 90% usage → "Consider rebooting AP to free memory"
- **CPU Warning**: > 90% usage → "Check AP load and consider rebooting"

```
🟡 High memory usage: 94% (Office-AP-12)
   💡 Suggested: Consider rebooting AP to free memory and improve performance
```

## Enhanced Client Summary

When AP health checks complete successfully, the client summary now includes:

```
📊 CLIENT SUMMARY:
   🏷️  Hostname: JohnDoe-Laptop
   🌐 IP Address: 192.168.1.100
   📱 MAC Address: 00:11:22:33:44:55
   📍 Site: Main Campus
   📶 Signal Strength: -45 dBm
   📊 SNR: 35 dB
   📡 Access Point: Conference-Room-AP-01
   ⏱️  AP Uptime: 12.5 days
   🔘 AP Status: connected
```

## Sample Output Examples

### Example 1: AP Reboot Recommendation Due to High Uptime
```
[4/4] Analyzing client health metrics...
   ✅ Client found: Marketing-Laptop (10.0.1.150)
   🟡 High AP uptime: 125.3 days (Marketing-Floor-AP)
      💡 Suggested: Consider checking and rebooting AP for optimal performance

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🟡 1 WARNING(S) DETECTED:
   • High AP uptime: 125.3 days (Marketing-Floor-AP)
     💡 Suggested: Consider checking and rebooting AP for optimal performance and stability
```

### Example 2: Signal Issues Combined with High Uptime
```
[4/4] Analyzing client health metrics...
   ✅ Client found: Guest-Device (192.168.50.75)
   🟡 Poor signal strength: -78 dBm
   🟡 Signal issues + High uptime (18.3 days)
      💡 Suggested: Consider rebooting AP to improve signal performance

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🟡 2 WARNING(S) DETECTED:
   • Poor WiFi signal strength (-78 dBm)
     💡 Suggested: Check AP placement, client location, or interference
   • Signal issues + High AP uptime: 18.3 days (Guest-WiFi-AP)
     💡 Suggested: Consider rebooting AP to improve signal performance and stability
```

### Example 3: Critical AP Issues
```
[4/4] Analyzing client health metrics...
   ❌ AP status issue: offline (Storage-Room-AP)
   🔴 Very high AP uptime: 205.8 days (Storage-Room-AP)
      💡 Action: Reboot AP immediately to prevent performance degradation

============================================================
📋 TROUBLESHOOTING SUMMARY
============================================================
✅ Completed 4/4 checks

🔴 2 CRITICAL ISSUE(S) FOUND:
   • AP status issue: offline (Storage-Room-AP)
     💡 Action: Check AP connectivity, power status, and network configuration
   • Very high AP uptime: 205.8 days (Storage-Room-AP)
     💡 Action: Reboot AP immediately to prevent performance degradation

🛑 IMMEDIATE ACTION REQUIRED:
   → Verify client is connected to Mist network
   → Check client device settings
   → Review AP placement and coverage
```

## Technical Implementation

### AP Health Check Process
1. **Client Discovery**: Find client by IP/MAC across all sites
2. **AP Identification**: Extract AP ID from client information
3. **AP Data Retrieval**: Get AP device details via Mist API
4. **Health Analysis**: Check uptime, status, performance metrics
5. **Issue Detection**: Compare against thresholds and generate recommendations
6. **Summary Integration**: Add AP info to client summary

### Thresholds and Recommendations

| Metric | Warning | Critical | Recommendation |
|--------|---------|----------|----------------|
| AP Uptime | > 90 days | > 180 days | Consider checking and rebooting/Immediately reboot AP |
| Signal + Uptime | RSSI < -70 & > 14 days | - | Reboot AP for signal improvement |
| Channel Utilization | > 80% | - | Check interference/load balancing |
| Memory Usage | > 90% | - | Reboot AP to free memory |
| CPU Usage | > 90% | - | Check load and reboot AP |
| AP Status | Not connected/online | - | Check connectivity and power |

## JSON Output Enhancement

The JSON output now includes AP-specific information:

```json
{
  "client_summary": {
    "hostname": "JohnDoe-Laptop",
    "ip": "192.168.1.100",
    "mac": "00:11:22:33:44:55",
    "site": "Main Campus",
    "rssi": "-45 dBm",
    "snr": "35 dB",
    "ap_name": "Conference-Room-AP-01",
    "ap_uptime_days": "12.5 days",
    "ap_status": "connected"
  },
  "issues_detected": [
    {
      "level": "WARNING",
      "message": "High AP uptime: 42.1 days (Marketing-Floor-AP)",
      "category": "health",
      "recommendation": "Consider rebooting AP for optimal performance and stability"
    }
  ]
}
```

## Benefits

1. **Proactive Maintenance**: Identifies APs that need reboots before performance degrades
2. **Signal Optimization**: Correlates poor signal with AP health for targeted fixes  
3. **Performance Monitoring**: Tracks CPU, memory, and channel utilization
4. **Comprehensive Analysis**: Provides full AP context for client issues
5. **Actionable Recommendations**: Clear guidance on when to reboot APs
6. **Operational Insights**: Helps network teams maintain optimal AP performance

This enhancement makes the troubleshooting script more comprehensive by addressing not just client-side issues but also the underlying AP infrastructure health.
