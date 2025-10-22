#!/usr/bin/env python3
"""Quick script to check currently connected clients"""
from src.auth.mist_auth import MistAuth
import json

def get_ap_name(auth, site_id, ap_mac):
    """Get AP name/hostname from MAC address"""
    try:
        devices = auth.make_request(f"/sites/{site_id}/devices")
        if devices and isinstance(devices, list):
            search_mac = ap_mac.lower().replace(':', '').replace('-', '')
            for device in devices:
                device_mac = device.get('mac', '').lower().replace(':', '').replace('-', '')
                if device_mac == search_mac and device.get('type') == 'ap':
                    return device.get('name', 'Unknown')
    except Exception:
        pass
    return 'Unknown'

auth = MistAuth()

print("=" * 70)
print("CHECKING MIST ORGANIZATION")
print("=" * 70)

# Get sites
print("\nFetching sites...")
sites = auth.make_request(f'/orgs/{auth.org_id}/sites')
if sites and isinstance(sites, list):
    print(f"Found {len(sites)} site(s):\n")
    for i, site in enumerate(sites[:10], 1):
        print(f"  {i}. {site.get('name')} (ID: {site.get('id')})")
        
        # Try to get clients for each site
        site_id = site.get('id')
        if site_id:
            print(f"     Checking for connected clients...")
            
            # Try stats endpoint
            clients = auth.make_request(f'/sites/{site_id}/stats/clients')
            if clients and isinstance(clients, list) and len(clients) > 0:
                print(f"     ✅ Found {len(clients)} connected client(s)")
                for client in clients[:3]:
                    mac = client.get('mac', 'N/A')
                    # Format MAC address properly (add colons)
                    if mac != 'N/A' and len(mac) == 12:
                        mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)])
                    hostname = client.get('hostname', 'Unknown')
                    ap_mac = client.get('ap_mac', 'N/A')
                    ap_name = get_ap_name(auth, site_id, ap_mac) if ap_mac != 'N/A' else 'N/A'
                    rssi = client.get('rssi', 'N/A')
                    ssid = client.get('ssid', 'N/A')
                    print(f"        • {hostname} - MAC: {mac}, SSID: {ssid}, AP: {ap_name}, RSSI: {rssi}")
            else:
                print(f"     No currently connected clients")
        print()
else:
    print("No sites found or error retrieving sites")

print("=" * 70)
