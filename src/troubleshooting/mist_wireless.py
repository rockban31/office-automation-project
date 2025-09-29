#!/usr/bin/env python3
"""
Mist Wireless Network Troubleshooter - Integrated Module

Complete flowchart-based troubleshooting solution for Mist wireless network connectivity issues.
This module is integrated with the Office Automation Project's authentication system.
"""

import os
import subprocess
import socket
import statistics
import time
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
import ipaddress

from ..auth.mist_auth import MistAuth, MistAuthError


class MistWirelessTroubleshooter:
    """
    Mist Wireless Network Troubleshooter
    
    Implements complete flowchart-based troubleshooting workflow for wireless client
    connectivity issues using the Office Automation Project's authentication system.
    """
    
    def __init__(self, auth_instance: Optional[MistAuth] = None, org_id: Optional[str] = None):
        """
        Initialize the troubleshooter with existing auth or create new instance.
        
        Args:
            auth_instance: Existing MistAuth instance (optional)
            org_id: Organization ID (optional, will auto-detect if not provided)
        """
        if auth_instance:
            self.auth = auth_instance
            self.org_id = org_id or auth_instance.org_id
        else:
            self.auth = MistAuth(org_id=org_id)
            self.org_id = org_id or self.auth.org_id
        
        self.base_url = self.auth.base_url
    
    def make_api_request(self, endpoint: str, method: str = 'GET', 
                        params: Optional[Dict[str, Any]] = None,
                        json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make API request using the integrated auth system"""
        try:
            return self.auth.make_request(endpoint, method, params, json_data)
        except MistAuthError as e:
            print(f"API request failed: {e}")
            return None
    
    def get_client_info(self, mac_address: str) -> Optional[Dict[str, Any]]:
        """Get client information and current session"""
        endpoint = f"/orgs/{self.org_id}/clients/search"
        params = {
            "mac": mac_address,
            "limit": 1
        }
        
        result = self.make_api_request(endpoint, params=params)
        if result and result.get('results'):
            return result['results'][0]
        return None
    
    def get_client_events(self, mac_address: str, hours_back: int = 24) -> Optional[Dict[str, Any]]:
        """Get client events and logs for analysis"""
        end_time = int(time.time())
        start_time = end_time - (hours_back * 3600)
        
        endpoint = f"/orgs/{self.org_id}/clients/{mac_address}/events"
        params = {
            "start": start_time,
            "end": end_time,
            "limit": 100
        }
        
        return self.make_api_request(endpoint, params=params)
    
    def get_ap_info(self, ap_mac: str) -> Optional[Dict[str, Any]]:
        """Get Access Point information"""
        endpoint = f"/orgs/{self.org_id}/devices/{ap_mac}"
        return self.make_api_request(endpoint)
    
    def get_ap_stats(self, ap_mac: str) -> Optional[Dict[str, Any]]:
        """Get AP statistics and uptime"""
        endpoint = f"/orgs/{self.org_id}/devices/{ap_mac}/stats"
        return self.make_api_request(endpoint)
    
    def analyze_auth_issues(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for authentication and authorization failures"""
        auth_failures = []
        
        if not events:
            return auth_failures
        
        for event in events:
            event_type = event.get('type', '').lower()
            
            # Check for various authentication failure types
            if any(failure_type in event_type for failure_type in [
                'auth_failed', 'assoc_failed', 'eap_failure', 
                'radius_failure', '802_1x_failure', 'psk_failure'
            ]):
                auth_failures.append({
                    'timestamp': event.get('timestamp'),
                    'type': event.get('type'),
                    'reason': event.get('reason', 'Unknown'),
                    'details': event.get('text', '')
                })
        
        return auth_failures
    
    def analyze_dhcp_dns_issues(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check for DHCP and DNS related issues"""
        network_issues = []
        
        if not events:
            return network_issues
        
        for event in events:
            event_type = event.get('type', '').lower()
            event_text = event.get('text', '').lower()
            
            # Check for DHCP issues
            if any(issue in event_type or issue in event_text for issue in [
                'dhcp_failure', 'dhcp_timeout', 'no_dhcp_response',
                'dns_failure', 'dns_timeout', 'ip_conflict'
            ]):
                network_issues.append({
                    'timestamp': event.get('timestamp'),
                    'type': event.get('type'),
                    'issue_type': 'DHCP/DNS',
                    'details': event.get('text', '')
                })
        
        return network_issues
    
    def analyze_client_health(self, client_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze client health metrics"""
        health_issues = []
        
        if not client_info:
            return health_issues
        
        # Check RSSI (Signal Strength) - typically good above -67 dBm
        rssi = client_info.get('rssi')
        if rssi and rssi < -70:
            health_issues.append({
                'metric': 'RSSI',
                'value': rssi,
                'issue': f'Poor signal strength: {rssi} dBm (should be > -67 dBm)',
                'severity': 'HIGH' if rssi < -80 else 'MEDIUM'
            })
        
        # Check SNR (Signal-to-Noise Ratio) - typically good above 20 dB
        snr = client_info.get('snr')
        if snr and snr < 15:
            health_issues.append({
                'metric': 'SNR',
                'value': snr,
                'issue': f'Poor signal quality: {snr} dB SNR (should be > 20 dB)',
                'severity': 'HIGH' if snr < 10 else 'MEDIUM'
            })
        
        # Check retry rates
        tx_retries = client_info.get('tx_retries', 0)
        rx_retries = client_info.get('rx_retries', 0)
        
        if tx_retries > 20 or rx_retries > 20:
            health_issues.append({
                'metric': 'Retries',
                'value': f'TX: {tx_retries}%, RX: {rx_retries}%',
                'issue': f'High retry rates detected (TX: {tx_retries}%, RX: {rx_retries}%)',
                'severity': 'MEDIUM'
            })
        
        # Check latency if available
        latency = client_info.get('latency_ms')
        if latency and latency > 100:
            health_issues.append({
                'metric': 'Latency',
                'value': f'{latency} ms',
                'issue': f'High latency detected: {latency} ms',
                'severity': 'MEDIUM' if latency < 200 else 'HIGH'
            })
        
        return health_issues
    
    def check_ap_uptime(self, ap_mac: str) -> Optional[Dict[str, Any]]:
        """Check AP uptime and suggest reboot if needed"""
        ap_stats = self.get_ap_stats(ap_mac)
        
        if not ap_stats:
            return None
        
        uptime = ap_stats.get('uptime', 0)
        uptime_hours = uptime / 3600
        
        # Suggest reboot if uptime is very high (>30 days) or very low (<1 hour, indicating recent issues)
        needs_reboot = uptime_hours > (30 * 24) or uptime_hours < 1
        
        return {
            'uptime_hours': uptime_hours,
            'uptime_days': uptime_hours / 24,
            'needs_reboot': needs_reboot,
            'reason': 'High uptime - consider scheduled reboot' if uptime_hours > (30 * 24) 
                     else 'Recent restart detected - may indicate stability issues' if uptime_hours < 1 
                     else 'Uptime normal'
        }
    
    def check_network_infrastructure(self, client_ip: str) -> List[Dict[str, Any]]:
        """Check network infrastructure (LAN/WAN/DHCP and DNS)"""
        infra_issues = []
        
        # Check DNS resolution
        print("   Checking DNS resolution...")
        try:
            test_domains = ['google.com', 'cloudflare.com', '8.8.8.8']
            dns_failures = 0
            
            for domain in test_domains:
                try:
                    socket.gethostbyname(domain)
                except socket.gaierror:
                    dns_failures += 1
            
            if dns_failures > len(test_domains) / 2:
                infra_issues.append({
                    'component': 'DNS',
                    'issue': f'DNS resolution failing for {dns_failures}/{len(test_domains)} test domains',
                    'severity': 'HIGH'
                })
        except Exception as e:
            infra_issues.append({
                'component': 'DNS',
                'issue': f'DNS check failed: {str(e)}',
                'severity': 'MEDIUM'
            })
        
        # Check internet connectivity
        print("   Checking internet connectivity...")
        try:
            import requests
            response = requests.get('https://8.8.8.8', timeout=5)
            if response.status_code != 200:
                infra_issues.append({
                    'component': 'WAN',
                    'issue': 'Internet connectivity issues detected',
                    'severity': 'HIGH'
                })
        except requests.RequestException:
            infra_issues.append({
                'component': 'WAN',
                'issue': 'Unable to reach internet',
                'severity': 'HIGH'
            })
        
        # Check local gateway reachability (if we can determine it)
        if client_ip and client_ip != "unknown":
            print(f"   Checking gateway reachability from {client_ip}...")
            try:
                # Try to ping potential gateways based on IP subnet
                network = ipaddress.IPv4Network(f"{client_ip}/24", strict=False)
                gateway_ip = str(network.network_address + 1)  # Common gateway .1
                
                # Use ping command (cross-platform)
                ping_cmd = ['ping', '-c', '1', '-W', '2', gateway_ip] if os.name != 'nt' else ['ping', '-n', '1', '-w', '2000', gateway_ip]
                result = subprocess.run(ping_cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    infra_issues.append({
                        'component': 'LAN',
                        'issue': f'Gateway {gateway_ip} unreachable',
                        'severity': 'HIGH'
                    })
            except Exception:
                # If we can't determine gateway, skip this check
                pass
        
        return infra_issues
    
    def check_client_connectivity_reachability(self, client_ip: str, client_mac: str, 
                                             client_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check client connectivity and reachability for drops and latency"""
        connectivity_issues = []
        
        if client_ip == "unknown":
            connectivity_issues.append({
                'metric': 'IP Address',
                'value': 'Unknown',
                'issue': 'Client IP address not provided - skipping connectivity tests',
                'severity': 'MEDIUM'
            })
            return connectivity_issues
        
        print(f"   Checking client reachability to {client_ip}...")
        
        # Ping test for latency and packet loss
        try:
            ping_cmd = ['ping', '-c', '10', '-i', '0.2', client_ip] if os.name != 'nt' else ['ping', '-n', '10', '-l', '32', client_ip]
            result = subprocess.run(ping_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                output_lines = result.stdout.lower()
                
                # Parse ping results for packet loss
                if '% loss' in output_lines or '% packet loss' in output_lines:
                    loss_match = re.search(r'(\d+)%.*loss', output_lines)
                    if loss_match:
                        packet_loss = int(loss_match.group(1))
                        if packet_loss > 5:
                            connectivity_issues.append({
                                'metric': 'Packet Loss',
                                'value': f'{packet_loss}%',
                                'issue': f'High packet loss: {packet_loss}% (should be < 5%)',
                                'severity': 'HIGH' if packet_loss > 15 else 'MEDIUM'
                            })
                
                # Parse average latency if available
                latency_match = re.search(r'avg[^=]*=\s*(\d+(?:\.\d+)?)\s*ms', output_lines)
                if latency_match:
                    avg_latency = float(latency_match.group(1))
                    if avg_latency > 100:
                        connectivity_issues.append({
                            'metric': 'Ping Latency',
                            'value': f'{avg_latency:.1f}ms',
                            'issue': f'High ping latency: {avg_latency:.1f}ms (should be < 100ms)',
                            'severity': 'MEDIUM' if avg_latency < 200 else 'HIGH'
                        })
            else:
                connectivity_issues.append({
                    'metric': 'Reachability',
                    'value': 'Failed',
                    'issue': f'Client {client_ip} is unreachable via ping',
                    'severity': 'HIGH'
                })
        
        except Exception as e:
            connectivity_issues.append({
                'metric': 'Connectivity Test',
                'value': 'Error',
                'issue': f'Failed to test connectivity: {str(e)}',
                'severity': 'MEDIUM'
            })
        
        # Check for frequent disconnections in client events
        print("   Analyzing client disconnect patterns...")
        events = self.get_client_events(client_mac, hours_back=4)  # Check last 4 hours
        if events and events.get('results'):
            disconnect_count = 0
            for event in events['results']:
                event_type = event.get('type', '').lower()
                if 'disconnect' in event_type or 'disassoc' in event_type:
                    disconnect_count += 1
            
            if disconnect_count > 5:  # More than 5 disconnects in 4 hours
                connectivity_issues.append({
                    'metric': 'Disconnection Frequency',
                    'value': f'{disconnect_count} in 4h',
                    'issue': f'Frequent disconnections detected: {disconnect_count} in the last 4 hours',
                    'severity': 'HIGH' if disconnect_count > 10 else 'MEDIUM'
                })
        
        return connectivity_issues
    
    def check_ap_hardware(self, ap_mac: str) -> List[Dict[str, Any]]:
        """Check AP hardware status"""
        hardware_issues = []
        
        print(f"   Checking AP {ap_mac} hardware status...")
        
        # Get AP device info
        ap_info = self.get_ap_info(ap_mac)
        if not ap_info:
            hardware_issues.append({
                'component': 'AP Communication',
                'issue': f'Unable to retrieve AP {ap_mac} information',
                'severity': 'HIGH'
            })
            return hardware_issues
        
        # Check AP status
        status = ap_info.get('status', 'unknown')
        if status.lower() not in ['connected', 'online']:
            hardware_issues.append({
                'component': 'AP Status',
                'issue': f'AP status is {status} (expected: connected/online)',
                'severity': 'HIGH'
            })
        
        # Check last seen timestamp
        last_seen = ap_info.get('last_seen')
        if last_seen:
            time_diff = time.time() - last_seen
            if time_diff > 300:  # More than 5 minutes
                hardware_issues.append({
                    'component': 'AP Connectivity',
                    'issue': f'AP last seen {time_diff/60:.1f} minutes ago',
                    'severity': 'HIGH' if time_diff > 900 else 'MEDIUM'
                })
        
        # Check AP statistics for hardware health indicators
        ap_stats = self.get_ap_stats(ap_mac)
        if ap_stats:
            # Check memory utilization
            memory_usage = ap_stats.get('memory_usage')
            if memory_usage and memory_usage > 85:
                hardware_issues.append({
                    'component': 'Memory',
                    'issue': f'High memory usage: {memory_usage}% (should be < 85%)',
                    'severity': 'HIGH' if memory_usage > 95 else 'MEDIUM'
                })
            
            # Check CPU utilization
            cpu_usage = ap_stats.get('cpu_usage')
            if cpu_usage and cpu_usage > 80:
                hardware_issues.append({
                    'component': 'CPU',
                    'issue': f'High CPU usage: {cpu_usage}% (should be < 80%)',
                    'severity': 'HIGH' if cpu_usage > 90 else 'MEDIUM'
                })
            
            # Check temperature if available
            temperature = ap_stats.get('temperature')
            if temperature and temperature > 70:
                hardware_issues.append({
                    'component': 'Temperature',
                    'issue': f'High temperature: {temperature}°C (should be < 70°C)',
                    'severity': 'HIGH' if temperature > 80 else 'MEDIUM'
                })
        
        return hardware_issues
    
    def analyze_rf_environment(self, ap_mac: str, client_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze RF environment for the AP and client"""
        rf_issues = []
        
        print(f"   Analyzing RF environment for AP {ap_mac}...")
        
        # Get AP radio statistics
        ap_stats = self.get_ap_stats(ap_mac)
        if not ap_stats:
            rf_issues.append({
                'component': 'RF Analysis',
                'issue': 'Unable to retrieve AP radio statistics',
                'severity': 'MEDIUM'
            })
            return rf_issues
        
        # Check channel utilization
        channel_utilization = ap_stats.get('channel_utilization')
        if channel_utilization:
            if isinstance(channel_utilization, dict):
                for band, util in channel_utilization.items():
                    if util > 70:
                        rf_issues.append({
                            'component': f'Channel Utilization ({band})',
                            'issue': f'High channel utilization: {util}% (should be < 70%)',
                            'severity': 'HIGH' if util > 85 else 'MEDIUM'
                        })
        
        # Check noise levels
        noise_level = ap_stats.get('noise_level')
        if noise_level:
            if isinstance(noise_level, dict):
                for band, noise in noise_level.items():
                    if noise > -85:  # Noise above -85 dBm is concerning
                        rf_issues.append({
                            'component': f'Noise Level ({band})',
                            'issue': f'High noise level: {noise} dBm (should be < -85 dBm)',
                            'severity': 'HIGH' if noise > -80 else 'MEDIUM'
                        })
        
        # Check for neighboring APs on same channel
        endpoint = f"/orgs/{self.org_id}/devices"
        params = {'type': 'ap', 'limit': 100}
        devices = self.make_api_request(endpoint, params=params)
        
        if devices and client_info:
            client_channel = client_info.get('channel')
            client_band = client_info.get('band')
            same_channel_aps = 0
            
            for device in devices:
                if device.get('mac') != ap_mac:  # Don't count the same AP
                    device_stats = self.get_ap_stats(device.get('mac'))
                    if device_stats:
                        device_channel = device_stats.get('channel')
                        device_band = device_stats.get('band')
                        
                        if device_channel == client_channel and device_band == client_band:
                            same_channel_aps += 1
            
            if same_channel_aps > 2:
                rf_issues.append({
                    'component': 'Channel Overlap',
                    'issue': f'Multiple APs ({same_channel_aps}) detected on same channel {client_channel}',
                    'severity': 'MEDIUM'
                })
        
        # Check client signal metrics again for RF context
        rssi = client_info.get('rssi') if client_info else None
        snr = client_info.get('snr') if client_info else None
        
        if rssi and rssi < -70:
            rf_issues.append({
                'component': 'Signal Coverage',
                'issue': f'Poor signal coverage at client location: {rssi} dBm',
                'severity': 'HIGH' if rssi < -80 else 'MEDIUM'
            })
        
        if snr and snr < 15:
            rf_issues.append({
                'component': 'RF Interference',
                'issue': f'Possible RF interference detected: {snr} dB SNR',
                'severity': 'HIGH' if snr < 10 else 'MEDIUM'
            })
        
        return rf_issues
    
    def troubleshoot_client(self, client_ip: str, client_mac: str, hours_back: int = 24) -> Dict[str, Any]:
        """
        Main troubleshooting function following the complete flowchart logic
        
        Args:
            client_ip: Client IP address
            client_mac: Client MAC address
            hours_back: Hours of historical data to analyze
            
        Returns:
            Dictionary containing analysis results and recommendations
        """
        results = {
            'client_ip': client_ip,
            'client_mac': client_mac,
            'analysis_time': datetime.now().isoformat(),
            'steps_completed': [],
            'issues_found': [],
            'recommendations': [],
            'escalation_path': None,
            'status': 'unknown'
        }
        
        print(f"\n{'='*70}")
        print(f"MIST WIRELESS NETWORK TROUBLESHOOTING (Office Automation Integration)")
        print(f"{'='*70}")
        print(f"Client IP: {client_ip}")
        print(f"Client MAC: {client_mac}")
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Organization: {self.org_id}")
        print(f"{'='*70}")
        
        try:
            # STEP 1: Get Client Association Status & Events (INPUT)
            print(f"\n🔍 [STEP 1] Gathering Client Association Status & Events...")
            client_info = self.get_client_info(client_mac)
            
            if not client_info:
                print(f"❌ ERROR: Client {client_mac} not found in Mist database")
                results['status'] = 'error'
                results['recommendations'] = [
                    "Verify client MAC address format",
                    "Check if client is connected to this Mist organization",
                    "Ensure API token has proper permissions"
                ]
                return results
            
            print(f"✅ Client found: {client_info.get('hostname', 'Unknown')} on AP {client_info.get('ap_mac', 'Unknown')}")
            results['steps_completed'].append('client_association_check')
            
            # Get client events for analysis
            events = self.get_client_events(client_mac, hours_back)
            
            # STEP 2: Check Authentication and Authorization Failure Logs
            print(f"\n🔍 [STEP 2] Checking Authentication and Authorization Failure Logs...")
            auth_issues = self.analyze_auth_issues(events.get('results', []) if events else [])
            
            if auth_issues:
                print(f"\n🔴 AUTHENTICATION/AUTHORIZATION ISSUES DETECTED:")
                for issue in auth_issues[-3:]:  # Show last 3 issues
                    print(f"   • {issue['type']}: {issue['reason']} ({issue.get('details', '')})")
                
                results['status'] = 'authentication_issues'
                results['escalation_path'] = 'troubleshoot_on_ise'
                results['issues_found'].extend(auth_issues)
                results['recommendations'] = [
                    "Check RADIUS server connectivity",
                    "Verify user credentials and certificates", 
                    "Review ISE authorization policies",
                    "Check 802.1X supplicant configuration"
                ]
                results['steps_completed'].append('authentication_check')
                
                print(f"\n📋 FLOWCHART DECISION: Authentication/Authorization Failure → Troubleshoot on ISE")
                print(f"\n🎯 ESCALATION: Route to Network Security / Identity Management team")
                return results
            
            print(f"✅ No authentication/authorization issues detected")
            results['steps_completed'].append('authentication_check')
            
            # STEP 3: Check DNS/DHCP Lease Errors
            print(f"\n🔍 [STEP 3] Checking DNS/DHCP Lease Errors...")
            dhcp_dns_issues = self.analyze_dhcp_dns_issues(events.get('results', []) if events else [])
            
            if dhcp_dns_issues:
                print(f"\n🔴 DHCP/DNS ISSUES DETECTED:")
                for issue in dhcp_dns_issues[-3:]:  # Show last 3 issues
                    print(f"   • {issue['type']}: {issue.get('details', '')}")
                
                # Perform network infrastructure checks
                print(f"\n🔍 [STEP 3a] Performing Network Infrastructure Checks...")
                infra_issues = self.check_network_infrastructure(client_ip)
                
                results['status'] = 'network_infrastructure_issues'
                results['escalation_path'] = 'check_lan_wan_dhcp_dns'
                results['issues_found'].extend(dhcp_dns_issues + infra_issues)
                results['recommendations'] = [
                    "Check DHCP server configuration and availability",
                    "Verify DHCP pool has available addresses",
                    "Test DNS server connectivity and resolution",
                    "Check LAN/WAN connectivity",
                    "Verify VLAN configuration"
                ]
                results['steps_completed'].extend(['dhcp_dns_check', 'infrastructure_check'])
                
                print(f"\n📋 FLOWCHART DECISION: DNS/DHCP Lease Errors → Check Network Infrastructure")
                print(f"\n🎯 ESCALATION: Route to Network Infrastructure team")
                return results
            
            print(f"✅ No DNS/DHCP lease errors detected")
            results['steps_completed'].append('dhcp_dns_check')
            
            # STEP 4: Check Client Health Metrics (RSSI, SNR, Retries, Latency)
            print(f"\n🔍 [STEP 4] Analyzing Client Health Metrics...")
            health_issues = self.analyze_client_health(client_info)
            
            if health_issues:
                print(f"\n🟡 CLIENT HEALTH ISSUES DETECTED:")
                for issue in health_issues:
                    print(f"   • {issue['metric']}: {issue['issue']} [{issue['severity']}]")
                
                # Proceed with detailed analysis as per flowchart
                ap_mac = client_info.get('ap_mac')
                connectivity_issues = []
                hardware_issues = []
                rf_issues = []
                
                if ap_mac:
                    print(f"\n🔍 [STEP 4a] Performing Client Connectivity & Reachability Checks...")
                    connectivity_issues = self.check_client_connectivity_reachability(client_ip, client_mac, client_info)
                    
                    print(f"\n🔍 [STEP 4b] Checking AP and Radio Performance...")
                    ap_uptime = self.check_ap_uptime(ap_mac)
                    if ap_uptime:
                        print(f"   AP Uptime: {ap_uptime['uptime_days']:.1f} days ({ap_uptime['reason']})")
                    
                    print(f"\n🔍 [STEP 4c] Checking AP Hardware Status...")
                    hardware_issues = self.check_ap_hardware(ap_mac)
                    
                    print(f"\n🔍 [STEP 4d] Analyzing RF Environment...")
                    rf_issues = self.analyze_rf_environment(ap_mac, client_info)
                
                # Compile all issues and prioritize
                all_issues = health_issues + connectivity_issues + hardware_issues + rf_issues
                high_issues = [i for i in all_issues if i.get('severity') == 'HIGH']
                medium_issues = [i for i in all_issues if i.get('severity') == 'MEDIUM']
                
                results['status'] = 'client_health_issues'
                results['escalation_path'] = 'detailed_analysis_complete'
                results['issues_found'] = all_issues
                results['steps_completed'].extend(['health_check', 'connectivity_check', 'hardware_check', 'rf_analysis'])
                
                # Generate recommendations based on issue types
                recommendations = []
                if any('Signal' in str(i) or 'RSSI' in str(i) or 'SNR' in str(i) for i in all_issues):
                    recommendations.extend([
                        "Check AP placement and antenna orientation",
                        "Analyze RF coverage and interference", 
                        "Consider additional AP deployment"
                    ])
                
                if any('Hardware' in str(i) or 'CPU' in str(i) or 'Memory' in str(i) for i in all_issues):
                    recommendations.extend([
                        "Schedule AP maintenance or replacement",
                        "Check AP firmware version"
                    ])
                
                if any('Connectivity' in str(i) or 'Latency' in str(i) for i in all_issues):
                    recommendations.extend([
                        "Check network path between client and destination",
                        "Verify QoS policies"
                    ])
                
                results['recommendations'] = recommendations
                
                print(f"\n🎯 COMPREHENSIVE TROUBLESHOOTING COMPLETE")
                print(f"   Issues found: {len(all_issues)} ({len(high_issues)} HIGH, {len(medium_issues)} MEDIUM)")
                return results
            
            print(f"✅ No client health metric issues detected")
            results['steps_completed'].append('health_check')
            
            # STEP 5: All Checks Passed
            print(f"\n✅ ALL AUTOMATED CHECKS COMPLETED SUCCESSFULLY!")
            results['status'] = 'all_good'
            results['escalation_path'] = 'manual_steps_if_needed'
            results['recommendations'] = [
                "All automated checks passed",
                "Check application-specific connectivity if issues persist",
                "Review firewall and security policies",
                "Consider end-to-end network testing"
            ]
            results['steps_completed'].append('all_checks_complete')
            
            return results
            
        except Exception as e:
            print(f"\n❌ ERROR: Analysis failed: {str(e)}")
            results['status'] = 'error'
            results['issues_found'].append({'error': str(e)})
            return results
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """List all organizations accessible to the authenticated user"""
        try:
            return self.auth.get_organizations()
        except Exception as e:
            print(f"Failed to get organizations: {e}")
            return []
    
    def auto_select_org(self) -> Optional[str]:
        """Automatically select organization if only one exists"""
        orgs = self.get_organizations()
        if not orgs:
            print("❌ No organizations found for this API token")
            return None
        
        if len(orgs) == 1:
            print(f"✅ Auto-selected organization: {orgs[0]['name']} ({orgs[0]['id']})")
            return orgs[0]['id']
        
        print(f"\n📋 Multiple organizations found:")
        for i, org in enumerate(orgs, 1):
            print(f"   {i}. {org['name']} ({org['id']})")
        
        while True:
            try:
                choice = input(f"\nSelect organization (1-{len(orgs)}): ")
                idx = int(choice) - 1
                if 0 <= idx < len(orgs):
                    selected_org = orgs[idx]
                    print(f"✅ Selected: {selected_org['name']} ({selected_org['id']})")
                    return selected_org['id']
                else:
                    print(f"❌ Please enter a number between 1 and {len(orgs)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if hasattr(self, 'auth') and self.auth:
            self.auth.close()