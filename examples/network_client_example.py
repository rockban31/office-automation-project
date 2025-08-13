#!/usr/bin/env python3
"""
Mist Network Client Example

This example demonstrates how to use the MistNetworkClient class
for common network automation tasks.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.mist_client import MistNetworkClient
from auth.mist_auth import MistAuthError
import json
from datetime import datetime


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def print_json(data, title=""):
    """Pretty print JSON data."""
    if title:
        print(f"\n{title}:")
        print("-" * len(title))
    print(json.dumps(data, indent=2, default=str))


def main():
    """Main example function."""
    print("=== Mist Network Client Example ===\n")
    
    try:
        # Initialize the network client (will use environment variables)
        print("1. Initializing Mist Network Client...")
        with MistNetworkClient() as client:
            print("✓ Client initialized successfully")
            
            # Perform health check
            print_section("Health Check")
            health = client.health_check()
            print_json(health, "System Health")
            
            if health['status'] != 'healthy':
                print("⚠️  System is not healthy, continuing with limited functionality...")
            
            # Get sites
            print_section("Organization Sites")
            try:
                sites = client.get_sites()
                print(f"Found {len(sites)} sites:")
                for i, site in enumerate(sites[:5]):  # Show first 5 sites
                    print(f"  {i+1}. {site.get('name', 'N/A')} (ID: {site.get('id', 'N/A')})")
                if len(sites) > 5:
                    print(f"  ... and {len(sites) - 5} more sites")
            except Exception as e:
                print(f"❌ Failed to get sites: {e}")
                sites = []
            
            # Get devices
            print_section("Network Devices")
            try:
                devices = client.get_devices()
                print(f"Found {len(devices)} devices:")
                device_types = {}
                for device in devices:
                    device_type = device.get('type', 'Unknown')
                    device_types[device_type] = device_types.get(device_type, 0) + 1
                
                for device_type, count in device_types.items():
                    print(f"  - {device_type}: {count}")
                    
                # Show details of first few devices
                print("\nSample devices:")
                for i, device in enumerate(devices[:3]):
                    print(f"  {i+1}. {device.get('name', 'N/A')} "
                          f"({device.get('type', 'N/A')}) - "
                          f"Status: {device.get('status', 'N/A')}")
                          
            except Exception as e:
                print(f"❌ Failed to get devices: {e}")
                devices = []
            
            # Get alarms
            print_section("Current Alarms")
            try:
                alarms = client.get_alarms()
                if alarms:
                    print(f"Found {len(alarms)} active alarms:")
                    severity_counts = {}
                    for alarm in alarms:
                        severity = alarm.get('severity', 'Unknown')
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                    for severity, count in severity_counts.items():
                        print(f"  - {severity}: {count}")
                    
                    # Show details of critical alarms
                    critical_alarms = [a for a in alarms if a.get('severity') == 'critical']
                    if critical_alarms:
                        print(f"\n⚠️  Critical alarms ({len(critical_alarms)}):")
                        for i, alarm in enumerate(critical_alarms[:3]):
                            print(f"  {i+1}. {alarm.get('type', 'N/A')} - "
                                  f"{alarm.get('text', 'No description')}")
                else:
                    print("✅ No active alarms")
                    
            except Exception as e:
                print(f"❌ Failed to get alarms: {e}")
            
            # Site-specific operations (if sites available)
            if sites:
                print_section(f"Site Analysis: {sites[0].get('name', 'First Site')}")
                site_id = sites[0].get('id')
                
                try:
                    # Get site info
                    site_info = client.get_site_info(site_id)
                    print(f"Site: {site_info.get('name')}")
                    print(f"Address: {site_info.get('address', 'N/A')}")
                    print(f"Timezone: {site_info.get('timezone', 'N/A')}")
                    
                    # Get site devices
                    site_devices = client.get_devices(site_id=site_id)
                    print(f"Devices at this site: {len(site_devices)}")
                    
                    # Get clients (if devices exist)
                    if site_devices:
                        try:
                            clients = client.get_clients(site_id, duration=1)  # Last hour
                            print(f"Active clients (last hour): {len(clients)}")
                            
                            if clients:
                                # Show sample clients
                                print("Sample clients:")
                                for i, client_info in enumerate(clients[:5]):
                                    mac = client_info.get('mac', 'N/A')
                                    hostname = client_info.get('hostname', 'Unknown')
                                    print(f"  {i+1}. {hostname} ({mac})")
                        except Exception as e:
                            print(f"⚠️  Could not get client info: {e}")
                    
                    # Get site events (last hour)
                    try:
                        events = client.get_site_events(site_id, duration=1)
                        print(f"Recent events (last hour): {len(events)}")
                        
                        if events:
                            event_types = {}
                            for event in events:
                                event_type = event.get('type', 'Unknown')
                                event_types[event_type] = event_types.get(event_type, 0) + 1
                            
                            print("Event breakdown:")
                            for event_type, count in sorted(event_types.items()):
                                print(f"  - {event_type}: {count}")
                    except Exception as e:
                        print(f"⚠️  Could not get site events: {e}")
                        
                except Exception as e:
                    print(f"❌ Failed to analyze site: {e}")
            
            # Summary
            print_section("Summary")
            summary = {
                'timestamp': datetime.now().isoformat(),
                'sites_count': len(sites),
                'devices_count': len(devices),
                'health_status': health['status']
            }
            print_json(summary, "Network Overview")
            
    except MistAuthError as e:
        print(f"❌ Authentication error: {e}")
        print("Please check your API token in the .env file")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n=== Example completed ===")


if __name__ == "__main__":
    main()
