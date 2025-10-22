#!/usr/bin/env python3
"""
Mist Wireless Network Troubleshooter - Core Module

Complete flowchart-based troubleshooting solution for Mist wireless network connectivity issues.
This is a core module of the Office Automation Project, built on the project's authentication
and API infrastructure to provide comprehensive wireless network troubleshooting capabilities.
"""

import os
import subprocess
import socket
import statistics
import time
import re
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
import ipaddress

from ..auth.mist_auth import MistAuth, MistAuthError


class MistWirelessTroubleshooter:
    """
    Mist Wireless Network Troubleshooter - Core Module
    
    Implements complete flowchart-based troubleshooting workflow for wireless client
    connectivity issues. This core module leverages the Office Automation Project's
    authentication and API infrastructure for comprehensive network troubleshooting.
    """
    
    def __init__(self, auth_instance: Optional[MistAuth] = None, org_id: Optional[str] = None, 
                 enable_logging: bool = True, log_file: Optional[str] = None):
        """
        Initialize the troubleshooter with existing auth or create new instance.
        
        Args:
            auth_instance: Existing MistAuth instance (optional)
            org_id: Organization ID (optional, will auto-detect if not provided)
            enable_logging: Enable detailed logging to file (default: True)
            log_file: Custom log file path (optional, will auto-generate if not provided)
        """
        if auth_instance:
            self.auth = auth_instance
            self.org_id = org_id or auth_instance.org_id
        else:
            self.auth = MistAuth(org_id=org_id)
            self.org_id = org_id or self.auth.org_id
        
        self.base_url = self.auth.base_url
        self.enable_logging = enable_logging
        self.log_file = log_file
        self.logger = self._setup_logging() if enable_logging else None
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration for troubleshooting session with DEBUG level"""
        # Generate log filename if not provided
        if not self.log_file:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            # Get project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logs_dir = os.path.join(project_root, 'logs')
            
            # Ensure logs directory exists
            os.makedirs(logs_dir, exist_ok=True)
            
            self.log_file = os.path.join(logs_dir, f'troubleshooting-{timestamp}.log')
        
        # Create logger with DEBUG level
        logger = logging.getLogger(f'mist_troubleshooter_{id(self)}')
        logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all log levels
        
        # Prevent propagation to root logger (keeps debug out of console)
        logger.propagate = False
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create file handler with DEBUG level
        file_handler = logging.FileHandler(self.log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # File captures DEBUG and above
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        # Log session start
        logger.info("=" * 60)
        logger.info("MIST WIRELESS NETWORK TROUBLESHOOTING SESSION STARTED")
        logger.info("=" * 60)
        logger.info(f"Organization ID: {self.org_id}")
        logger.info(f"Log file: {self.log_file}")
        logger.debug(f"Base URL: {self.base_url}")
        logger.debug(f"Logging level: DEBUG (file only)")
        
        return logger
    
    def log(self, message: str, level: str = 'INFO'):
        """Log message to file if logging is enabled"""
        if self.logger:
            if level.upper() == 'ERROR':
                self.logger.error(message)
            elif level.upper() == 'WARNING':
                self.logger.warning(message)
            elif level.upper() == 'DEBUG':
                self.logger.debug(message)
            else:
                self.logger.info(message)
    
    def make_api_request(self, endpoint: str, method: str = 'GET',
                        params: Optional[Dict[str, Any]] = None,
                        json_data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make API request using the integrated auth system"""
        self.log(f"DEBUG: API Request - {method} {endpoint}", 'DEBUG')
        if params:
            self.log(f"DEBUG: Request params: {params}", 'DEBUG')
        try:
            result = self.auth.make_request(endpoint, method, params, json_data)
            self.log(f"DEBUG: API Response received - Status: Success", 'DEBUG')
            return result
        except MistAuthError as e:
            self.log(f"ERROR: API request failed - {method} {endpoint}: {e}", 'ERROR')
            print(f"API request failed: {e}")
            return None
    
    def get_ap_name(self, site_id: str, ap_mac: str) -> str:
        """Get AP name/hostname from MAC address"""
        self.log(f"DEBUG: Fetching AP name for MAC: {ap_mac} in site: {site_id}", 'DEBUG')
        try:
            # Get all devices for the site
            devices = self.make_api_request(f"/sites/{site_id}/devices")
            if devices and isinstance(devices, list):
                self.log(f"DEBUG: Found {len(devices)} devices in site", 'DEBUG')
                # Normalize MAC for comparison
                search_mac = ap_mac.lower().replace(':', '').replace('-', '')
                for device in devices:
                    device_mac = device.get('mac', '').lower().replace(':', '').replace('-', '')
                    if device_mac == search_mac and device.get('type') == 'ap':
                        ap_name = device.get('name', 'Unknown')
                        self.log(f"DEBUG: AP name resolved: {ap_name}", 'DEBUG')
                        return ap_name
                self.log(f"DEBUG: No matching AP found for MAC: {ap_mac}", 'DEBUG')
        except Exception as e:
            self.log(f"Failed to get AP name for {ap_mac}: {e}", 'WARNING')
        return 'Unknown'
    
    def get_client_info(self, mac_address: str, hours_back: int = 24) -> Optional[Dict[str, Any]]:
        """Get client information and current session"""
        self.log(f"DEBUG: Searching for client MAC: {mac_address}", 'DEBUG')
        # First, try to get currently connected client from all sites (live data with RSSI/SNR)
        # Get all sites in organization
        sites = self.make_api_request(f"/orgs/{self.org_id}/sites")
        if sites and isinstance(sites, list):
            self.log(f"DEBUG: Searching across {len(sites)} sites", 'DEBUG')
            # Search each site for the client
            for site in sites:
                site_id = site.get('id')
                site_name = site.get('name')
                if site_id:
                    self.log(f"DEBUG: Checking site: {site_name} ({site_id})", 'DEBUG')
                    # Get currently connected clients for this site
                    clients = self.make_api_request(f"/sites/{site_id}/stats/clients", params={"mac": mac_address})
                    if clients and isinstance(clients, list):
                        self.log(f"DEBUG: Found {len(clients)} client(s) in site {site_name}", 'DEBUG')
                        # Normalize MAC address for comparison (remove colons/hyphens)
                        search_mac = mac_address.lower().replace(':', '').replace('-', '')
                        for client in clients:
                            client_mac = client.get('mac', '').lower().replace(':', '').replace('-', '')
                            if client_mac == search_mac:
                                self.log(f"DEBUG: Client found in site: {site_name}", 'DEBUG')
                                # Add site info to client data
                                client['site_id'] = site_id
                                client['site_name'] = site.get('name')
                                
                                # Fetch and add AP name
                                ap_mac = client.get('ap_mac')
                                if ap_mac:
                                    ap_name = self.get_ap_name(site_id, ap_mac)
                                    client['ap_name'] = ap_name
                                
                                self.log(f"DEBUG: Returning live client data", 'DEBUG')
                                return client
        
        # If not currently connected, search historical data
        self.log(f"DEBUG: Client not found in live data, searching historical data", 'DEBUG')
        end_time = int(time.time())
        start_time = end_time - (hours_back * 3600)
        
        endpoint = f"/orgs/{self.org_id}/clients/search"
        params = {
            "mac": mac_address,
            "limit": 1,
            "start": start_time,
            "end": end_time
        }
        
        result = self.make_api_request(endpoint, params=params)
        if result and result.get('results'):
            self.log(f"DEBUG: Client found in historical data", 'DEBUG')
            return result['results'][0]
        
        self.log(f"DEBUG: Client not found in historical data either", 'DEBUG')
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
    
    def get_ap_info(self, site_id: str, ap_mac: str) -> Optional[Dict[str, Any]]:
        """Get Access Point information"""
        endpoint = f"/sites/{site_id}/devices/{ap_mac}"
        return self.make_api_request(endpoint)
    
    def get_ap_stats(self, site_id: str, ap_mac: str) -> Optional[Dict[str, Any]]:
        """Get AP statistics and uptime"""
        endpoint = f"/sites/{site_id}/stats/devices/{ap_mac}"
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
        tx_pkts = client_info.get('tx_pkts', 0)
        rx_pkts = client_info.get('rx_pkts', 0)
        
        # Calculate retry rates as percentage of total packets
        tx_retry_rate = (tx_retries / tx_pkts * 100) if tx_pkts > 0 else 0
        rx_retry_rate = (rx_retries / rx_pkts * 100) if rx_pkts > 0 else 0
        
        # Flag if retry rate exceeds 10% (industry threshold for concern)
        if tx_retry_rate > 10 or rx_retry_rate > 10:
            health_issues.append({
                'metric': 'Retries',
                'value': f'TX: {tx_retry_rate:.1f}% ({tx_retries}/{tx_pkts}), RX: {rx_retry_rate:.1f}% ({rx_retries}/{rx_pkts})',
                'issue': f'High retry rates detected - TX: {tx_retry_rate:.1f}%, RX: {rx_retry_rate:.1f}% (should be < 10%)',
                'severity': 'HIGH' if tx_retry_rate > 20 or rx_retry_rate > 20 else 'MEDIUM'
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
    
    def check_ap_uptime(self, site_id: str, ap_id: str) -> Optional[Dict[str, Any]]:
        """STEP 4b: Check AP uptime using AP ID (not AP MAC) and suggest reboot if needed"""
        # Get AP stats using the device ID (not MAC)
        ap_stats = self.get_ap_stats(site_id, ap_id)
        
        if not ap_stats or not isinstance(ap_stats, dict):
            self.log(f"AP stats not available for {ap_id} (API limitation)", 'INFO')
            return None
        
        uptime = ap_stats.get('uptime')
        if not uptime:
            self.log(f"AP uptime not available in stats for {ap_id}", 'INFO')
            return None
        
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
    
    def analyze_disconnection_patterns(self, client_mac: str) -> List[Dict[str, Any]]:
        """STEP 4a: Analyze client disconnection patterns over the past 5 minutes"""
        connectivity_issues = []
        
        print("   Analyzing client disconnect patterns (past 5 minutes)...")
        
        # Check for frequent disconnections in the last 5 minutes
        events = self.get_client_events(client_mac, hours_back=0.084)  # ~5 minutes in hours (5/60)
        if events and events.get('results'):
            disconnect_count = 0
            for event in events['results']:
                event_type = event.get('type', '').lower()
                if 'disconnect' in event_type or 'disassoc' in event_type:
                    disconnect_count += 1
            
            if disconnect_count >= 7:  # 7 or more disconnects in 5 minutes
                connectivity_issues.append({
                    'metric': 'Disconnection Pattern',
                    'value': f'{disconnect_count} disconnects in 5min',
                    'issue': f'Frequent disconnections detected: {disconnect_count} in the last 5 minutes (threshold: ≥7)',
                    'severity': 'HIGH'
                })
        
        return connectivity_issues
    
    def check_client_connectivity_ping(self, client_ip: str) -> List[Dict[str, Any]]:
        """Check client connectivity via ping for packet loss and latency"""
        connectivity_issues = []
        
        if client_ip == "unknown":
            connectivity_issues.append({
                'metric': 'IP Address',
                'value': 'Unknown',
                'issue': 'Client IP address not provided - skipping ping tests',
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
                            'metric': 'Average Latency',
                            'value': f'{avg_latency:.1f}ms',
                            'issue': f'High average latency: {avg_latency:.1f}ms (should be < 100ms)',
                            'severity': 'MEDIUM' if avg_latency < 200 else 'HIGH'
                        })
        
        except Exception as e:
            connectivity_issues.append({
                'metric': 'Connectivity Test',
                'value': 'Error',
                'issue': f'Failed to test connectivity: {str(e)}',
                'severity': 'MEDIUM'
            })
        
        return connectivity_issues
    
    
    
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
        print(f"MIST WIRELESS NETWORK TROUBLESHOOTER")
        print(f"{'='*70}")
        print(f"Client IP: {client_ip}")
        print(f"Client MAC: {client_mac}")
        if self.enable_logging and self.log_file:
            print(f"📝 Log File: {self.log_file}")
        print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Organization: {self.org_id}")
        print(f"{'='*70}")
        
        # Log session details
        self.log(f"Troubleshooting session started for client {client_mac} ({client_ip})")
        self.log(f"Hours back for analysis: {hours_back}")
        
        try:
            # STEP 1: Get Client Association Status & Events (INPUT)
            print(f"\n🔍 [STEP 1] Gathering Client Association Status & Events...")
            self.log("STEP 1: Starting client association status and events check")
            client_info = self.get_client_info(client_mac, hours_back=hours_back)
            
            if not client_info:
                error_msg = f"Client {client_mac} not found in Mist database"
                print(f"❌ ERROR: {error_msg}")
                self.log(f"ERROR: {error_msg}", 'ERROR')
                results['status'] = 'error'
                results['recommendations'] = [
                    "Verify client MAC address format",
                    "Check if client is connected to this Mist organization",
                    "Ensure API token has proper permissions"
                ]
                self.log("Session ended with error - client not found")
                return results
            
            client_name = client_info.get('hostname') or client_info.get('username') or 'Unknown'
            ap_mac = client_info.get('ap_mac') or client_info.get('ap_id') or 'Unknown'
            ap_name = client_info.get('ap_name', 'Unknown') if ap_mac != 'Unknown' else 'Unknown'
            ssid = client_info.get('ssid', 'Unknown')
            
            # Display client and AP info
            if ap_mac != 'Unknown':
                print(f"✅ Client found: {client_name} connected to AP {ap_name} ({ap_mac})")
                print(f"   SSID: {ssid}")
            else:
                print(f"✅ Client found: {client_name} (not currently connected to any AP)")
            
            # Get and display client details
            rssi = client_info.get('rssi')
            snr = client_info.get('snr')
            ip_addr = client_info.get('ip') or client_ip
            
            print(f"   Client details: RSSI={rssi if rssi else 'N/A'}, SNR={snr if snr else 'N/A'}, IP={ip_addr}")
            
            # Warn if critical data is missing
            if not rssi or not snr or ap_mac == 'Unknown':
                print(f"\n⚠️  WARNING: Incomplete client data - client may not be currently connected")
                print(f"   This may limit the depth of analysis. Try:")
                print(f"   1. Verify the client MAC address is correct")
                print(f"   2. Ensure the client is currently connected to the network")
                print(f"   3. Increase the search time range with --hours-back parameter")
                self.log("WARNING: Incomplete client data detected", 'WARNING')
            
            self.log(f"Client found: {client_name} (MAC: {client_mac}) connected to AP {ap_name} ({ap_mac})")
            self.log(f"SSID: {ssid}")
            self.log(f"Client details: RSSI={rssi}, SNR={snr}, IP={ip_addr}")
            results['steps_completed'].append('client_association_check')
            
            # Get client events for analysis
            events = self.get_client_events(client_mac, hours_back)
            
            # STEP 2: Check Authentication and Authorization Failure Logs
            print(f"\n🔍 [STEP 2] Checking Authentication and Authorization Failure Logs...")
            self.log("STEP 2: Starting authentication and authorization failure analysis")
            auth_issues = self.analyze_auth_issues(events.get('results', []) if events else [])
            
            if auth_issues:
                print(f"\n🔴 AUTHENTICATION/AUTHORIZATION ISSUES DETECTED:")
                self.log(f"Authentication issues detected: {len(auth_issues)} issues found", 'WARNING')
                for issue in auth_issues[-3:]:  # Show last 3 issues
                    print(f"   • {issue['type']}: {issue['reason']} ({issue.get('details', '')})")
                    self.log(f"Auth issue: {issue['type']} - {issue['reason']} - {issue.get('details', '')}", 'WARNING')
                
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
                self.log("Session ended with escalation to Network Security team for authentication issues")
                return results
            
            print(f"✅ No authentication/authorization issues detected")
            self.log("STEP 2 completed: No authentication/authorization issues detected")
            results['steps_completed'].append('authentication_check')
            
            # STEP 3: Check DNS/DHCP Lease Errors
            print(f"\n🔍 [STEP 3] Checking DNS/DHCP Lease Errors...")
            self.log("STEP 3: Starting DNS/DHCP lease error analysis")
            dhcp_dns_issues = self.analyze_dhcp_dns_issues(events.get('results', []) if events else [])
            
            if dhcp_dns_issues:
                print(f"\n🔴 DHCP/DNS ISSUES DETECTED:")
                self.log(f"DHCP/DNS issues detected: {len(dhcp_dns_issues)} issues found", 'WARNING')
                for issue in dhcp_dns_issues[-3:]:  # Show last 3 issues
                    print(f"   • {issue['type']}: {issue.get('details', '')}")
                    self.log(f"DHCP/DNS issue: {issue['type']} - {issue.get('details', '')}", 'WARNING')
                
                # Perform network infrastructure checks
                print(f"\n🔍 [STEP 3a] Performing Network Infrastructure Checks...")
                self.log("STEP 3a: Performing network infrastructure checks")
                infra_issues = self.check_network_infrastructure(client_ip)
                
                if infra_issues:
                    self.log(f"Infrastructure issues found: {len(infra_issues)} issues", 'WARNING')
                    for infra_issue in infra_issues:
                        self.log(f"Infrastructure issue: {infra_issue.get('component')} - {infra_issue.get('issue')}", 'WARNING')
                
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
                self.log("Session ended with escalation to Network Infrastructure team for DHCP/DNS issues")
                return results
            
            print(f"✅ No DNS/DHCP lease errors detected")
            self.log("STEP 3 completed: No DNS/DHCP lease errors detected")
            results['steps_completed'].append('dhcp_dns_check')
            
            # STEP 4: Check Client Health Metrics (RSSI, SNR, Retries, Latency)
            print(f"\n🔍 [STEP 4] Analyzing Client Health Metrics...")
            self.log("STEP 4: Starting client health metrics analysis")
            health_issues = self.analyze_client_health(client_info)
            
            if health_issues:
                print(f"\n🟡 CLIENT HEALTH ISSUES DETECTED:")
                self.log(f"Client health issues detected: {len(health_issues)} issues found", 'WARNING')
                for issue in health_issues:
                    print(f"   • {issue['metric']}: {issue['issue']} [{issue['severity']}]")
                    self.log(f"Health issue: {issue['metric']} - {issue['issue']} - Severity: {issue['severity']}", 'WARNING')
                
                # Proceed with detailed analysis as per new workflow
                ap_mac = client_info.get('ap_mac')
                ap_id = client_info.get('ap_id') or ap_mac  # Prefer ap_id, fallback to ap_mac
                site_id = client_info.get('site_id')
                all_issues = health_issues.copy()
                
                # STEP 4a: Disconnection Pattern Analysis (5 minutes)
                print(f"\n🔍 [STEP 4a] Analyzing Disconnection Patterns (past 5 minutes)...")
                self.log("STEP 4a: Analyzing disconnection patterns (5-minute window)")
                disconnect_issues = self.analyze_disconnection_patterns(client_mac)
                all_issues.extend(disconnect_issues)
                if disconnect_issues:
                    for disc_issue in disconnect_issues:
                        self.log(f"Disconnection issue: {disc_issue.get('metric')} - {disc_issue.get('issue')}", 'WARNING')
                else:
                    self.log("No disconnection pattern issues detected (< 7 events in 5 min)")
                
                # Ping-based connectivity checks (packet loss and latency)
                print(f"\n🔍 [STEP 4a] Checking Packet Loss and Average Latency via Ping...")
                self.log("STEP 4a: Checking packet loss and average latency via ping")
                ping_issues = self.check_client_connectivity_ping(client_ip)
                all_issues.extend(ping_issues)
                if ping_issues:
                    for ping_issue in ping_issues:
                        self.log(f"Ping issue: {ping_issue.get('metric')} - {ping_issue.get('issue')}", 'WARNING')
                else:
                    self.log("No packet loss or latency issues detected via ping")
                
                # STEP 4b: AP Uptime Analysis (moved to last sub-step)
                ap_uptime_info = None
                if site_id and ap_id:
                    print(f"\n🔍 [STEP 4b] Checking AP Uptime (using AP ID)...")
                    self.log(f"STEP 4b: Checking AP uptime for AP ID: {ap_id}")
                    ap_uptime_info = self.check_ap_uptime(site_id, ap_id)
                    if ap_uptime_info:
                        print(f"   AP Uptime: {ap_uptime_info['uptime_days']:.1f} days ({ap_uptime_info['reason']})")
                        self.log(f"AP Uptime: {ap_uptime_info['uptime_days']:.1f} days - {ap_uptime_info['reason']}")
                        if ap_uptime_info.get('needs_reboot'):
                            all_issues.append({
                                'metric': 'AP Uptime',
                                'value': f"{ap_uptime_info['uptime_days']:.1f} days",
                                'issue': ap_uptime_info['reason'],
                                'severity': 'MEDIUM'
                            })
                            self.log(f"AP uptime issue: {ap_uptime_info['reason']}", 'WARNING')
                
                # Compile all issues and prioritize
                high_issues = [i for i in all_issues if i.get('severity') == 'HIGH']
                medium_issues = [i for i in all_issues if i.get('severity') == 'MEDIUM']
                
                results['status'] = 'client_health_issues'
                results['escalation_path'] = 'manual_troubleshooting'
                results['issues_found'] = all_issues
                results['steps_completed'].extend(['health_check', 'disconnection_analysis', 'ping_check', 'ap_uptime_check'])
                
                # Manual troubleshooting recommendations
                recommendations = [
                    "📋 Manual Troubleshooting Steps for Engineer:",
                    "   1. Perform LAN/WAN/DHCP/DNS checks based on client metrics",
                    "   2. Assess AP & Radio Performance (client load, channel utilization, noise)",
                    "   3. Evaluate AP Hardware health if needed",
                    "   4. Analyze full RF Environment for interference and coverage",
                    "",
                    "🔍 Use the following metrics for assessment:"
                ]
                
                # Add specific metric-based recommendations
                rssi = client_info.get('rssi')
                snr = client_info.get('snr')
                tx_retries = client_info.get('tx_retries', 0)
                rx_retries = client_info.get('rx_retries', 0)
                tx_pkts = client_info.get('tx_pkts', 0)
                rx_pkts = client_info.get('rx_pkts', 0)
                
                tx_retry_rate = (tx_retries / tx_pkts * 100) if tx_pkts > 0 else 0
                rx_retry_rate = (rx_retries / rx_pkts * 100) if rx_pkts > 0 else 0
                
                recommendations.append(f"   • RSSI: {rssi if rssi else 'N/A'} dBm (Good: > -67 dBm, Fair: -67 to -70, Poor: < -70)")
                recommendations.append(f"   • SNR: {snr if snr else 'N/A'} dB (Good: > 20 dB, Fair: 15-20, Poor: < 15)")
                recommendations.append(f"   • TX Retry Rate: {tx_retry_rate:.1f}% (Good: < 5%, Concern: 10%+, Critical: 20%+)")
                recommendations.append(f"   • RX Retry Rate: {rx_retry_rate:.1f}% (Good: < 5%, Concern: 10%+, Critical: 20%+)")
                
                # Add latency info if available from ping
                for issue in ping_issues:
                    if issue.get('metric') == 'Average Latency':
                        recommendations.append(f"   • Latency: {issue.get('value')} (Good: < 50ms, Fair: 50-100ms, Poor: 100ms+)")
                
                recommendations.append("")
                recommendations.append("💡 Suggested Actions Based on Metrics:")
                
                if rssi and rssi < -70:
                    recommendations.append("   • Low RSSI: Check AP placement, adjust power, or add AP coverage")
                if snr and snr < 15:
                    recommendations.append("   • Low SNR: Investigate RF interference, check for non-WiFi devices")
                if tx_retry_rate > 10 or rx_retry_rate > 10:
                    recommendations.append("   • High Retries: Check for channel congestion, co-channel interference, or RF obstacles")
                
                results['recommendations'] = recommendations
                
                print(f"\n🎯 AUTOMATED ANALYSIS COMPLETE")
                print(f"   Issues found: {len(all_issues)} ({len(high_issues)} HIGH, {len(medium_issues)} MEDIUM)")
                print(f"\n📋 All automated checks complete. Proceed with manual troubleshooting if needed.")
                
                # Log final analysis summary
                self.log("="*60)
                self.log(f"AUTOMATED ANALYSIS COMPLETE")
                self.log(f"Total issues found: {len(all_issues)} (HIGH: {len(high_issues)}, MEDIUM: {len(medium_issues)})")
                self.log(f"Status: {results['status']}")
                self.log(f"Escalation path: {results['escalation_path']}")
                self.log(f"Steps completed: {', '.join(results['steps_completed'])}")
                self.log("Manual troubleshooting guidance provided to engineer")
                self.log("="*60)
                
                return results
            
            print(f"✅ No client health metric issues detected")
            self.log("STEP 4 completed: No client health metric issues detected")
            results['steps_completed'].append('health_check')
            
            # STEP 5: All Checks Passed
            print(f"\n✅ ALL AUTOMATED CHECKS COMPLETED SUCCESSFULLY!")
            print(f"\n📋 All automated checks look good; proceed with manual troubleshooting steps as needed.")
            
            results['status'] = 'all_good'
            results['escalation_path'] = 'manual_steps_if_needed'
            results['recommendations'] = [
                "✅ All automated checks look good; proceed with manual troubleshooting steps as needed."
            ]
            results['steps_completed'].append('all_checks_complete')
            
            # Log final session summary
            self.log("="*60)
            self.log("ALL AUTOMATED CHECKS COMPLETED SUCCESSFULLY")
            self.log(f"Status: {results['status']}")
            self.log(f"Steps completed: {', '.join(results['steps_completed'])}")
            self.log("No issues detected - all metrics within normal thresholds")
            self.log("="*60)
            
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
    
    def close_logging(self):
        """Close logging session"""
        if self.logger:
            self.log("=" * 60)
            self.log("TROUBLESHOOTING SESSION ENDED")
            self.log("=" * 60)
            
            # Close all handlers
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_logging()
        if hasattr(self, 'auth') and self.auth:
            self.auth.close()
