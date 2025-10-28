# Mist API Troubleshooting Reference

## Overview
This document provides detailed Mist API endpoints and parameters for troubleshooting the three main areas: Authentication/Authorization, DHCP/DNS issues, and Signal Strength problems.

## Base API Configuration

```python
BASE_URL = "https://api.eu.mist.com/api/v1"
HEADERS = {
    "Authorization": f"Token {API_TOKEN}",
    "Content-Type": "application/json"
}
```

## 1. Authentication & Authorization Issues

### 1.1 Client Authentication Events
**Purpose**: Get authentication failures and authorization events for specific clients

```http
GET /orgs/{org_id}/clients/search
```
**Parameters**:
- `mac`: Client MAC address (required)
- `limit`: Number of results (default: 100)
- `start`: Start time (epoch timestamp)
- `end`: End time (epoch timestamp)

**Example**:
```python
params = {
    'mac': 'aa:bb:cc:dd:ee:ff',
    'limit': 1
}
```

**Response Fields for Auth Analysis**:
- `auth_state`: Current authentication state
- `last_seen`: Last authentication attempt
- `username`: Authenticated username (if available)
- `auth_method`: Authentication method used

### 1.2 Client-Specific Authentication Events
**Purpose**: Get detailed authentication event history

```http
GET /orgs/{org_id}/clients/{client_mac}/events
```
**Parameters**:
- `start`: Start time (epoch - seconds)
- `end`: End time (epoch - seconds)  
- `limit`: Max events to return (default: 100)

**Example**:
```python
import time
end_time = int(time.time())
start_time = end_time - (24 * 3600)  # Last 24 hours

params = {
    'start': start_time,
    'end': end_time,
    'limit': 100
}
```

**Key Event Types to Monitor**:
- `client_auth_failure`
- `client_dot1x_failure` 
- `client_auth_denied`
- `client_authorization_failure`
- `auth_failed`
- `assoc_failed`
- `eap_failure`
- `radius_failure`
- `802_1x_failure`
- `psk_failure`

### 1.3 Site-Wide Authentication Events
**Purpose**: Get authentication events across entire site

```http
GET /sites/{site_id}/events
```
**Parameters**:
- `duration`: Time range (e.g., '1d', '12h', '4h')
- `type`: Filter by event type
- `limit`: Max events (default: 100)

**Example**:
```python
params = {
    'duration': '1d',
    'type': 'client_auth_failure',
    'limit': 50
}
```

### 1.4 RADIUS/ISE Integration Events
**Purpose**: Get RADIUS server interaction events

```http
GET /sites/{site_id}/events
```
**Filter for RADIUS Events**:
```python
radius_event_types = [
    'radius_timeout',
    'radius_reject', 
    'radius_failure',
    'radius_server_down'
]
```

## 2. DHCP & DNS Issues

### 2.1 Client IP Assignment Events
**Purpose**: Track DHCP lease and IP assignment issues

```http
GET /orgs/{org_id}/clients/{client_mac}/events
```
**Key Event Types**:
- `dhcp_failure`
- `dhcp_timeout`
- `no_dhcp_response`
- `client_ip_conflict`
- `dhcp_nak`
- `dhcp_decline`

**Example Event Filtering**:
```python
def check_dhcp_events(events):
    dhcp_issues = []
    for event in events:
        event_type = event.get('type', '').lower()
        event_text = event.get('text', '').lower()
        
        if any(issue in event_type for issue in [
            'dhcp_failure', 'dhcp_timeout', 'no_dhcp_response'
        ]) or any(keyword in event_text for keyword in [
            'dhcp fail', 'no ip address', 'dhcp timeout'
        ]):
            dhcp_issues.append(event)
    return dhcp_issues
```

### 2.2 DNS Resolution Events
**Purpose**: Track DNS resolution failures

```http
GET /sites/{site_id}/events
```
**Key Event Types**:
- `dns_failure`
- `dns_timeout`
- `dns_server_unreachable`

**Example**:
```python
params = {
    'duration': '4h',
    'type': 'dns_failure'
}
```

### 2.3 Network Infrastructure Events
**Purpose**: Get VLAN and network-level issues

```http
GET /sites/{site_id}/events
```
**Key Event Types**:
- `vlan_mismatch`
- `network_unreachable`
- `gateway_unreachable`
- `subnet_conflict`

### 2.4 Site Network Configuration
**Purpose**: Get current network/VLAN configuration

```http
GET /sites/{site_id}/networks
```
**Response Analysis**:
```python
def analyze_network_config(networks):
    for network in networks:
        dhcp_enabled = network.get('dhcp_enabled', False)
        dns_servers = network.get('dns_servers', [])
        vlan_id = network.get('vlan_id')
        
        if not dhcp_enabled:
            print(f"DHCP disabled on VLAN {vlan_id}")
        if not dns_servers:
            print(f"No DNS servers configured for VLAN {vlan_id}")
```

## 3. Signal Strength Issues

### 3.1 Client Signal Metrics
**Purpose**: Get current client signal strength and quality

```http
GET /orgs/{org_id}/clients/search?mac={client_mac}
```
**Key Response Fields**:
- `rssi`: Signal strength in dBm
- `snr`: Signal-to-noise ratio in dB
- `tx_rate`: Transmission rate in Mbps
- `rx_rate`: Reception rate in Mbps
- `tx_retries`: Transmission retry percentage
- `rx_retries`: Reception retry percentage
- `channel`: Current channel
- `band`: WiFi band (2.4GHz/5GHz)

**Signal Quality Analysis**:
```python
def analyze_signal_quality(client_data):
    rssi = client_data.get('rssi')
    snr = client_data.get('snr')
    
    issues = []
    
    # RSSI Analysis
    if rssi:
        if rssi < -80:
            issues.append(f"Very poor signal: {rssi} dBm")
        elif rssi < -70:
            issues.append(f"Poor signal: {rssi} dBm")
        elif rssi < -60:
            issues.append(f"Moderate signal: {rssi} dBm")
    
    # SNR Analysis  
    if snr:
        if snr < 10:
            issues.append(f"Very poor SNR: {snr} dB")
        elif snr < 20:
            issues.append(f"Poor SNR: {snr} dB")
    
    return issues
```

### 3.2 Access Point Uptime Statistics
**Purpose**: Get AP uptime and health data for maintenance planning

```http
GET /sites/{site_id}/stats/devices/{ap_mac}
```
**Key Response Fields**:
- `uptime`: AP uptime in seconds (primary health metric)
- `status`: AP connection status (connected/disconnected)
- `name`: AP name/identifier
- `mac`: AP MAC address

**AP Uptime Analysis Example**:
```python
def check_ap_uptime(site_id, ap_id):
    """Check AP uptime and provide reboot recommendations"""
    ap_stats = get_ap_stats(site_id, ap_id)
    
    if not ap_stats:
        return None
    
    uptime = ap_stats.get('uptime')
    if not uptime:
        return None
    
    uptime_hours = uptime / 3600
    uptime_days = uptime_hours / 24
    
    # Industry best practice thresholds (180 days)
    if uptime_hours > (180 * 24):
        return {
            'status': 'WARNING',
            'uptime_days': uptime_days,
            'needs_reboot': True,
            'recommendation': 'High uptime - schedule AP reboot during maintenance window'
        }
    elif uptime_hours < 1:
        return {
            'status': 'WARNING',
            'uptime_days': uptime_days,
            'needs_reboot': True,
            'recommendation': 'Recent restart detected - monitor for stability issues'
        }
    else:
        return {
            'status': 'NORMAL',
            'uptime_days': uptime_days,
            'needs_reboot': False,
            'recommendation': 'Uptime within normal range (1hr - 180 days)'
        }
```

### 3.3 AP Device Information
**Purpose**: Get AP name and basic device details

```http
GET /sites/{site_id}/devices/{ap_mac}
```
**Key Response Fields**:
- `name`: AP name/identifier (resolved from MAC)
- `mac`: AP MAC address
- `model`: AP model
- `type`: Device type (should be 'ap')

**AP Name Resolution Example**:
```python
def get_ap_name(site_id, ap_mac):
    """Get AP name from MAC address"""
    devices = make_api_request(f"/sites/{site_id}/devices")
    
    # Normalize MAC for comparison
    search_mac = ap_mac.lower().replace(':', '').replace('-', '')
    
    for device in devices:
        device_mac = device.get('mac', '').lower().replace(':', '').replace('-', '')
        if device_mac == search_mac and device.get('type') == 'ap':
            return device.get('name', 'Unknown')
    
    return 'Unknown'
```

### 3.4 Client Health Metrics
**Purpose**: Get real-time client wireless performance data

```http
GET /sites/{site_id}/stats/clients?mac={client_mac}
```
**Key Response Fields for Health Analysis**:
- `rssi`: Signal strength (dBm) - Good: > -67 dBm, Poor: < -70 dBm
- `snr`: Signal-to-Noise ratio (dB) - Good: > 20 dB, Poor: < 15 dB
- `tx_retries`: TX packet retransmissions
- `rx_retries`: RX packet retransmissions
- `tx_pkts`: Total TX packets
- `rx_pkts`: Total RX packets
- `ap_mac`: Connected AP MAC address

**Client Health Analysis Example**:
```python
def analyze_client_health(client_info):
    issues = []
    
    # Check RSSI (Signal Strength)
    rssi = client_info.get('rssi')
    if rssi and rssi < -70:
        issues.append({
            'metric': 'RSSI',
            'value': rssi,
            'severity': 'HIGH' if rssi < -80 else 'MEDIUM',
            'issue': f'Poor signal strength: {rssi} dBm (should be > -67 dBm)'
        })
    
    # Check SNR (Signal Quality)
    snr = client_info.get('snr')
    if snr and snr < 15:
        issues.append({
            'metric': 'SNR',
            'value': snr,
            'severity': 'HIGH' if snr < 10 else 'MEDIUM',
            'issue': f'Poor signal quality: {snr} dB SNR (should be > 20 dB)'
        })
    
    # Check Retry Rates
    tx_retries = client_info.get('tx_retries', 0)
    rx_retries = client_info.get('rx_retries', 0)
    tx_pkts = client_info.get('tx_pkts', 0)
    rx_pkts = client_info.get('rx_pkts', 0)
    
    tx_retry_rate = (tx_retries / tx_pkts * 100) if tx_pkts > 0 else 0
    rx_retry_rate = (rx_retries / rx_pkts * 100) if rx_pkts > 0 else 0
    
    if tx_retry_rate > 10 or rx_retry_rate > 10:
        issues.append({
            'metric': 'Retries',
            'value': f'TX: {tx_retry_rate:.1f}%, RX: {rx_retry_rate:.1f}%',
            'severity': 'HIGH' if tx_retry_rate > 20 or rx_retry_rate > 20 else 'MEDIUM',
            'issue': f'High retry rates (should be < 10%)'
        })
    
    return issues
```

## 4. Combined Troubleshooting Queries

### 4.1 Complete Client Analysis
**Purpose**: Get comprehensive client troubleshooting data

```python
def get_comprehensive_client_data(client, mac_address):
    # 1. Basic client info
    client_info = client.search_clients(mac_address)
    
    # 2. Recent events (24 hours)
    events = client.get_client_events(mac_address, hours_back=24)
    
    # 3. If client found, get AP details
    if client_info and client_info.get('results'):
        client_data = client_info['results'][0]
        ap_mac = client_data.get('ap_mac')
        
        if ap_mac:
            # 4. AP information and stats
            ap_info = client.get_ap_info(ap_mac)
            ap_stats = client.get_ap_stats(ap_mac)
            
            return {
                'client': client_data,
                'events': events,
                'ap_info': ap_info,
                'ap_stats': ap_stats
            }
    
    return None
```

### 4.2 Event Time Filtering
**Purpose**: Get events for specific time ranges

```python
def get_events_by_timerange(client, mac_address, hours_back=24):
    import time
    
    end_time = int(time.time())
    start_time = end_time - (hours_back * 3600)
    
    params = {
        'start': start_time,
        'end': end_time,
        'limit': 100
    }
    
    return client.auth.make_request(
        f'/orgs/{{org_id}}/clients/{mac_address}/events', 
        params=params
    )
```

## 5. API Rate Limits & Best Practices

### 5.1 Rate Limits
- **Standard**: 5000 requests per hour per API token
- **Burst**: Up to 100 requests per minute
- **Headers**: Check `X-RateLimit-*` headers in responses

### 5.2 Efficient API Usage
```python
def efficient_troubleshooting(client, mac_address):
    try:
        # Single call to get client info
        client_info = client.get_client_info(mac_address)
        
        if not client_info:
            return {"error": "Client not found"}
        
        # Only get additional data if client exists
        ap_mac = client_info.get('ap_mac')
        site_id = client_info.get('site_id')
        
        # Parallel data gathering
        from concurrent.futures import ThreadPoolExecutor
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all API calls concurrently
            events_future = executor.submit(
                client.get_client_events, mac_address, 24
            )
            
            ap_info_future = None
            ap_stats_future = None
            
            if ap_mac:
                ap_info_future = executor.submit(
                    client.get_ap_info, ap_mac
                )
                ap_stats_future = executor.submit(
                    client.get_ap_stats, ap_mac
                )
            
            # Collect results
            results = {
                'client_info': client_info,
                'events': events_future.result(),
                'ap_info': ap_info_future.result() if ap_info_future else None,
                'ap_stats': ap_stats_future.result() if ap_stats_future else None
            }
            
        return results
        
    except Exception as e:
        return {"error": str(e)}
```

## 6. Response Data Examples

### 6.1 Authentication Event Response
```json
{
    "results": [
        {
            "timestamp": 1694534400,
            "type": "client_auth_failure",
            "text": "Client aa:bb:cc:dd:ee:ff authentication failed: Invalid credentials",
            "mac": "aa:bb:cc:dd:ee:ff",
            "ap": "AP-Office-01",
            "reason": "eap_failure",
            "details": {
                "username": "john.doe",
                "auth_method": "dot1x",
                "radius_response": "Access-Reject"
            }
        }
    ]
}
```

### 6.2 DHCP Issue Event Response
```json
{
    "results": [
        {
            "timestamp": 1694534500,
            "type": "dhcp_timeout",
            "text": "Client aa:bb:cc:dd:ee:ff DHCP request timeout",
            "mac": "aa:bb:cc:dd:ee:ff", 
            "ap": "AP-Office-01",
            "vlan": 100,
            "details": {
                "dhcp_server": "192.168.1.1",
                "request_type": "DHCPDISCOVER"
            }
        }
    ]
}
```

### 6.3 Client Signal Response
```json
{
    "results": [
        {
            "mac": "aa:bb:cc:dd:ee:ff",
            "ip": "192.168.1.100",
            "hostname": "johns-laptop",
            "ap_mac": "5c:5b:35:00:00:01",
            "rssi": -72,
            "snr": 18,
            "tx_rate": 144.4,
            "rx_rate": 86.7,
            "tx_retries": 12.5,
            "rx_retries": 8.2,
            "channel": 36,
            "band": "5",
            "last_seen": 1694534600
        }
    ]
}
```

This reference provides comprehensive API details for troubleshooting all three major areas in your network automation workflow.