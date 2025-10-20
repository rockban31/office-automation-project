#!/usr/bin/env python3
"""
Demonstrate STEP 4: Client Health Metrics Analysis
Shows exactly what data is checked and how it's evaluated
"""

from src.auth.mist_auth import MistAuth
from src.troubleshooting.mist_wireless import MistWirelessTroubleshooter
import json

# Initialize troubleshooter
auth = MistAuth()
troubleshooter = MistWirelessTroubleshooter(auth_instance=auth, enable_logging=False)

# Get a currently connected client for demonstration
print("=" * 80)
print("STEP 4: CLIENT HEALTH METRICS ANALYSIS - DETAILED EXPLANATION")
print("=" * 80)

# Get sites
sites = auth.make_request(f'/orgs/{auth.org_id}/sites')
if sites and len(sites) > 0:
    site_id = sites[0].get('id')
    site_name = sites[0].get('name')
    
    # Get first connected client
    clients = auth.make_request(f'/sites/{site_id}/stats/clients', params={'limit': 1})
    
    if clients and len(clients) > 0:
        client = clients[0]
        
        print(f"\n📍 Analyzing Client: {client.get('hostname', 'Unknown')}")
        print(f"   Site: {site_name}")
        print(f"   MAC: {client.get('mac')}")
        print(f"   IP: {client.get('ip')}")
        print(f"   Connected to AP: {client.get('ap_mac')}")
        
        print("\n" + "=" * 80)
        print("HEALTH METRIC DETAILS:")
        print("=" * 80)
        
        # 1. RSSI Analysis
        rssi = client.get('rssi')
        print(f"\n1️⃣  RSSI (Received Signal Strength Indicator)")
        print(f"   Current Value: {rssi} dBm")
        if rssi:
            if rssi > -67:
                print(f"   Status: ✅ EXCELLENT - Strong signal")
                print(f"   Impact: Optimal performance, no concerns")
            elif rssi > -70:
                print(f"   Status: ✅ GOOD - Acceptable signal")
                print(f"   Impact: Normal operation expected")
            elif rssi > -80:
                print(f"   Status: ⚠️  FAIR - Weak signal")
                print(f"   Impact: May experience slower speeds, occasional dropouts")
            else:
                print(f"   Status: 🔴 POOR - Very weak signal")
                print(f"   Impact: Frequent disconnections, very slow performance")
            print(f"   Recommendation: {'None needed' if rssi > -70 else 'Check AP placement, move closer to AP, or add APs'}")
        
        # 2. SNR Analysis
        snr = client.get('snr')
        print(f"\n2️⃣  SNR (Signal-to-Noise Ratio)")
        print(f"   Current Value: {snr} dB")
        if snr:
            if snr > 25:
                print(f"   Status: ✅ EXCELLENT - Very clean signal")
                print(f"   Impact: Optimal data rates, minimal errors")
            elif snr > 20:
                print(f"   Status: ✅ GOOD - Clean signal")
                print(f"   Impact: Good performance expected")
            elif snr > 15:
                print(f"   Status: ⚠️  FAIR - Some noise present")
                print(f"   Impact: Performance may be affected")
            else:
                print(f"   Status: 🔴 POOR - High noise environment")
                print(f"   Impact: Significant interference, poor performance")
            print(f"   Recommendation: {'None needed' if snr > 20 else 'Check for RF interference sources (microwaves, other APs, etc.)'}")
        
        # 3. Retry Rate Analysis
        tx_retries = client.get('tx_retries', 0)
        rx_retries = client.get('rx_retries', 0)
        tx_pkts = client.get('tx_pkts', 0)
        rx_pkts = client.get('rx_pkts', 0)
        
        tx_retry_rate = (tx_retries / tx_pkts * 100) if tx_pkts > 0 else 0
        rx_retry_rate = (rx_retries / rx_pkts * 100) if rx_pkts > 0 else 0
        
        print(f"\n3️⃣  Retry Rates (Packet Retransmissions)")
        print(f"   TX Retry Rate: {tx_retry_rate:.2f}% ({tx_retries:,} retries / {tx_pkts:,} packets)")
        print(f"   RX Retry Rate: {rx_retry_rate:.2f}% ({rx_retries:,} retries / {rx_pkts:,} packets)")
        
        max_retry = max(tx_retry_rate, rx_retry_rate)
        if max_retry < 5:
            print(f"   Status: ✅ EXCELLENT - Very low retry rate")
            print(f"   Impact: Optimal efficiency, minimal overhead")
        elif max_retry < 10:
            print(f"   Status: ✅ GOOD - Normal retry rate")
            print(f"   Impact: Good performance")
        elif max_retry < 20:
            print(f"   Status: ⚠️  FAIR - Elevated retry rate")
            print(f"   Impact: Some inefficiency, reduced throughput")
        else:
            print(f"   Status: 🔴 POOR - High retry rate")
            print(f"   Impact: Significant performance degradation")
        
        print(f"   Recommendation: {'None needed' if max_retry < 10 else 'Check signal quality, channel congestion, or client adapter'}")
        
        # 4. Data Rate Analysis
        tx_rate = client.get('tx_rate', 0)
        rx_rate = client.get('rx_rate', 0)
        
        print(f"\n4️⃣  Data Rates (Link Speed)")
        print(f"   TX Rate: {tx_rate} Mbps (Client → AP)")
        print(f"   RX Rate: {rx_rate} Mbps (AP → Client)")
        
        # 5. Additional Metrics
        print(f"\n5️⃣  Additional Connection Details")
        print(f"   Band: {client.get('band')} GHz")
        print(f"   Channel: {client.get('channel')}")
        print(f"   Protocol: {client.get('proto', 'Unknown').upper()}")
        print(f"   SSID: {client.get('ssid')}")
        print(f"   VLAN: {client.get('vlan_id')}")
        print(f"   Security: {client.get('key_mgmt', 'Unknown')}")
        print(f"   Uptime: {client.get('uptime', 0) / 3600:.1f} hours")
        
        # 6. Throughput Analysis
        tx_bps = client.get('tx_bps', 0)
        rx_bps = client.get('rx_bps', 0)
        
        print(f"\n6️⃣  Current Throughput (Actual Usage)")
        print(f"   TX Throughput: {tx_bps / 1000:.1f} Kbps ({tx_bps / 1_000_000:.2f} Mbps)")
        print(f"   RX Throughput: {rx_bps / 1000:.1f} Kbps ({rx_bps / 1_000_000:.2f} Mbps)")
        print(f"   Total Traffic: TX {client.get('tx_bytes', 0) / 1_000_000:.1f} MB, RX {client.get('rx_bytes', 0) / 1_000_000:.1f} MB")
        
        # Now run the actual health check analysis
        print("\n" + "=" * 80)
        print("AUTOMATED HEALTH ANALYSIS RESULT:")
        print("=" * 80)
        
        health_issues = troubleshooter.analyze_client_health(client)
        
        if health_issues:
            print(f"\n⚠️  {len(health_issues)} Issue(s) Detected:\n")
            for i, issue in enumerate(health_issues, 1):
                severity_emoji = "🔴" if issue['severity'] == 'HIGH' else "🟡"
                print(f"{i}. {severity_emoji} {issue['metric']}: {issue['issue']} [{issue['severity']}]")
        else:
            print("\n✅ All health metrics are within normal ranges!")
            print("   No issues detected with this client's connection.")
        
        print("\n" + "=" * 80)
        print("WHAT HAPPENS NEXT IN TROUBLESHOOTER:")
        print("=" * 80)
        print("\nIf health issues are detected, the troubleshooter proceeds with:")
        print("  • STEP 4a: Client Connectivity & Reachability Tests (ping, packet loss)")
        print("  • STEP 4b: AP Uptime Analysis (check if AP needs reboot)")
        print("  • STEP 4c: AP Hardware Status (CPU, memory, temperature)")
        print("  • STEP 4d: RF Environment Analysis (channel congestion, interference)")
        
    else:
        print("\n❌ No connected clients found in the site")
else:
    print("\n❌ No sites found in organization")

print("\n" + "=" * 80)
