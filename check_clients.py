#!/usr/bin/env python3
"""Quick script to check currently connected clients"""
from src.auth.mist_auth import MistAuth
import json

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
                    hostname = client.get('hostname', 'Unknown')
                    ap_mac = client.get('ap_mac', 'N/A')
                    rssi = client.get('rssi', 'N/A')
                    print(f"        • {hostname} - MAC: {mac}, AP: {ap_mac}, RSSI: {rssi}")
            else:
                print(f"     No currently connected clients")
        print()
else:
    print("No sites found or error retrieving sites")

print("=" * 70)
