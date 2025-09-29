# Mist API Quick Reference - Troubleshooting

## Essential API Endpoints Summary

| **Issue Category** | **API Endpoint** | **Purpose** | **Key Parameters** |
|-------------------|------------------|-------------|-------------------|
| **Authentication** | `/orgs/{org_id}/clients/search` | Find client by MAC | `mac`, `limit` |
| **Authentication** | `/orgs/{org_id}/clients/{mac}/events` | Client auth events | `start`, `end`, `limit` |
| **Authentication** | `/sites/{site_id}/events` | Site-wide auth events | `duration`, `type` |
| **DHCP/DNS** | `/orgs/{org_id}/clients/{mac}/events` | Client network events | `start`, `end`, `limit` |
| **DHCP/DNS** | `/sites/{site_id}/networks` | Network configuration | None |
| **Signal Issues** | `/orgs/{org_id}/clients/search` | Client signal metrics | `mac` |
| **Signal Issues** | `/orgs/{org_id}/devices/{ap_mac}/stats` | AP radio statistics | None |
| **Signal Issues** | `/orgs/{org_id}/devices/{ap_mac}` | AP device info | None |
| **Signal Issues** | `/sites/{site_id}/clients/{mac}/sessions` | Connection history | None |

## Critical Event Types to Monitor

### Authentication Issues
```
client_auth_failure, client_dot1x_failure, client_auth_denied,
auth_failed, assoc_failed, eap_failure, radius_failure, 
802_1x_failure, psk_failure
```

### DHCP/DNS Issues  
```
dhcp_failure, dhcp_timeout, no_dhcp_response, client_ip_conflict,
dns_failure, dns_timeout, vlan_mismatch, gateway_unreachable
```

### Signal Quality Thresholds
| **Metric** | **Good** | **Warning** | **Critical** |
|------------|----------|-------------|--------------|
| **RSSI** | > -60 dBm | -60 to -70 dBm | < -70 dBm |
| **SNR** | > 20 dB | 10-20 dB | < 10 dB |
| **TX/RX Retries** | < 10% | 10-20% | > 20% |
| **Channel Util** | < 60% | 60-80% | > 80% |
| **AP Uptime** | 1-90 days | 90-180 days | > 180 days |

## API Rate Limits
- **5000 requests/hour** per API token
- **100 requests/minute** burst limit
- Monitor `X-RateLimit-*` headers

## Quick Code Examples

### Get Client Info & Events
```python
# Find client
client_info = client.search_clients("aa:bb:cc:dd:ee:ff")

# Get recent events (24h)
events = client.get_client_events("aa:bb:cc:dd:ee:ff", hours_back=24)
```

### Check AP Health
```python
# Get AP stats
ap_stats = client.get_ap_stats("5c:5b:35:00:00:01")
uptime_days = ap_stats.get('uptime', 0) / (24 * 3600)

# Check radio utilization
radio_stats = ap_stats.get('radio_stat', {})
for band, stats in radio_stats.items():
    util = stats.get('util_all', 0)
    if util > 80:
        print(f"High utilization: {util}% on {band}")
```

### Filter Events
```python
def find_auth_failures(events):
    auth_types = ['auth_failed', 'eap_failure', 'radius_failure']
    return [e for e in events if e.get('type') in auth_types]

def find_dhcp_issues(events):
    dhcp_types = ['dhcp_failure', 'dhcp_timeout', 'no_dhcp_response']
    return [e for e in events if e.get('type') in dhcp_types]
```

## Response Data Keys

### Client Data
```json
{
  "mac": "aa:bb:cc:dd:ee:ff",
  "ip": "192.168.1.100", 
  "hostname": "device-name",
  "ap_mac": "5c:5b:35:00:00:01",
  "rssi": -65,
  "snr": 25,
  "tx_rate": 144.4,
  "rx_rate": 86.7,
  "tx_retries": 5.2,
  "rx_retries": 3.1,
  "channel": 36,
  "band": "5"
}
```

### AP Stats Data
```json
{
  "uptime": 2592000,
  "memory_usage": 45,
  "cpu_usage": 12,
  "radio_stat": {
    "band_24": {
      "util_all": 35,
      "util_non_wifi": 12
    },
    "band_5": {
      "util_all": 28,
      "util_non_wifi": 8
    }
  }
}
```

### Event Data
```json
{
  "timestamp": 1694534400,
  "type": "client_auth_failure",
  "text": "Authentication failed: Invalid credentials",
  "mac": "aa:bb:cc:dd:ee:ff",
  "ap": "AP-Office-01",
  "reason": "eap_failure"
}
```