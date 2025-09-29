"""
Mist API Client for Network Operations

This module provides high-level functions for common network automation tasks
using the Mist API, built on top of the MistAuth authentication module.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from auth.mist_auth import MistAuth, MistAuthError

logger = logging.getLogger(__name__)


class MistNetworkClient:
    """
    High-level Mist API client for network operations.
    
    This class provides convenient methods for common network automation tasks
    without requiring direct API endpoint knowledge.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, auth: Optional[MistAuth] = None):
        """
        Initialize the Mist Network Client.
        
        Args:
            config: Configuration dictionary with auth settings
            auth: Existing MistAuth instance (optional)
        """
        if auth is not None:
            self.auth = auth
            self._owns_auth = False
        elif config is not None:
            self.auth = MistAuth(**config)
            self._owns_auth = True
        else:
            raise ValueError("Either config or auth must be provided")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._owns_auth:
            self.auth.close()
    
    # Site Management
    def get_sites(self) -> List[Dict[str, Any]]:
        """Get all sites in the organization."""
        try:
            import mistapi
            response = mistapi.api.v1.orgs.sites.listOrgSites(self.auth.session, self.auth.org_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get sites: {e}")
            raise
    
    def get_site_info(self, site_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific site."""
        try:
            import mistapi
            response = mistapi.api.v1.sites.getSiteInfo(self.auth.session, site_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get site info for {site_id}: {e}")
            raise
    
    # Device Management
    def get_devices(self, site_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get devices, optionally filtered by site.
        
        Args:
            site_id: If provided, get devices for specific site only
        """
        try:
            import mistapi
            if site_id:
                response = mistapi.api.v1.sites.devices.listSiteDevices(self.auth.session, site_id)
            else:
                response = mistapi.api.v1.orgs.devices.listOrgDevices(self.auth.session, self.auth.org_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get devices: {e}")
            raise
    
    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get current status of a specific device."""
        try:
            import mistapi
            # For device status, we need to find the site first, or use org-level call
            response = mistapi.api.v1.orgs.devices.getOrgDevice(self.auth.session, self.auth.org_id, device_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get device status for {device_id}: {e}")
            raise
    
    # Client Management
    def get_clients(self, site_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get clients, optionally filtered by site.
        
        Args:
            site_id: Site identifier (optional)
        """
        try:
            import mistapi
            if site_id:
                response = mistapi.api.v1.sites.clients.listSiteClients(self.auth.session, site_id)
                return self.auth._get_mistapi_response_data(response)
            else:
                # Get all clients across organization using mistapi
                response = mistapi.api.v1.orgs.clients.searchOrgClients(self.auth.session, self.auth.org_id)
                return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get clients: {e}")
            raise
    
    def get_client_sessions(self, site_id: str, client_mac: str) -> List[Dict[str, Any]]:
        """Get session history for a specific client."""
        try:
            return self.auth.make_request(f'/sites/{site_id}/clients/{client_mac}/sessions')
        except Exception as e:
            logger.error(f"Failed to get client sessions for {client_mac}: {e}")
            raise
    
    def search_clients(self, mac_address: str, limit: int = 1) -> Dict[str, Any]:
        """Search for clients by MAC address across organization."""
        try:
            import mistapi
            # Use mistapi's search functionality
            response = mistapi.api.v1.orgs.clients.searchOrgClients(
                self.auth.session, 
                self.auth.org_id,
                mac=mac_address,
                limit=limit
            )
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to search for client {mac_address}: {e}")
            raise
    
    def get_client_info(self, mac_address: str) -> Dict[str, Any]:
        """Get client information by MAC address."""
        try:
            result = self.search_clients(mac_address, limit=1)
            if result and result.get('results'):
                return result['results'][0]
            return None
        except Exception as e:
            logger.error(f"Failed to get client info for {mac_address}: {e}")
            raise
    
    def get_client_events(self, mac_address: str, hours_back: int = 24) -> Dict[str, Any]:
        """Get events for a specific client by MAC address."""
        try:
            import time
            end_time = int(time.time())
            start_time = end_time - (hours_back * 3600)
            
            params = {
                'start': start_time,
                'end': end_time,
                'limit': 100
            }
            return self.auth.make_request(f'/orgs/{{org_id}}/clients/{mac_address}/events', params=params)
        except Exception as e:
            logger.error(f"Failed to get client events for {mac_address}: {e}")
            raise
    
    # Network Insights & Analytics
    def get_site_stats(self, site_id: str) -> Dict[str, Any]:
        """Get site statistics and metrics."""
        try:
            import mistapi
            response = mistapi.api.v1.sites.stats.getSiteStats(self.auth.session, site_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get site stats for {site_id}: {e}")
            raise
    
    def get_device_stats(self, site_id: str, device_id: str) -> Dict[str, Any]:
        """Get device statistics and metrics."""
        try:
            import mistapi
            response = mistapi.api.v1.sites.stats.devices.getSiteDeviceStats(
                self.auth.session, site_id, device_id
            )
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get device stats for {device_id}: {e}")
            raise
    
    def get_ap_info(self, ap_mac: str) -> Dict[str, Any]:
        """Get Access Point information by MAC address."""
        try:
            return self.auth.make_request(f'/orgs/{{org_id}}/devices/{ap_mac}')
        except Exception as e:
            logger.error(f"Failed to get AP info for {ap_mac}: {e}")
            raise
    
    def get_ap_stats(self, ap_mac: str) -> Dict[str, Any]:
        """Get AP statistics and uptime by MAC address."""
        try:
            return self.auth.make_request(f'/orgs/{{org_id}}/devices/{ap_mac}/stats')
        except Exception as e:
            logger.error(f"Failed to get AP stats for {ap_mac}: {e}")
            raise
    
    # Troubleshooting Methods
    def get_site_events(self, site_id: str, duration: int = 24) -> List[Dict[str, Any]]:
        """
        Get events for a site.
        
        Args:
            site_id: Site identifier
            duration: Hours of history to include
        """
        try:
            params = {'duration': f'{duration}h'}
            return self.auth.make_request(f'/sites/{site_id}/events', params=params)
        except Exception as e:
            logger.error(f"Failed to get site events for {site_id}: {e}")
            raise
    
    def get_device_events(self, device_id: str, duration: int = 24) -> List[Dict[str, Any]]:
        """Get events for a specific device."""
        try:
            site_id = self._get_site_id_for_device(device_id)
            params = {'device_id': device_id, 'duration': f'{duration}h'}
            return self.auth.make_request(f'/sites/{site_id}/events', params=params)
        except Exception as e:
            logger.error(f"Failed to get device events for {device_id}: {e}")
            raise
    
    def get_alarms(self, site_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get current alarms, optionally filtered by site."""
        try:
            import mistapi
            if site_id:
                response = mistapi.api.v1.sites.alarms.listSiteAlarms(self.auth.session, site_id)
            else:
                response = mistapi.api.v1.orgs.alarms.listOrgAlarms(self.auth.session, self.auth.org_id)
            return self.auth._get_mistapi_response_data(response)
        except Exception as e:
            logger.error(f"Failed to get alarms: {e}")
            raise
    
    # Helper Methods
    def _get_site_id_for_device(self, device_id: str) -> str:
        """Helper to find site ID for a device (simplified implementation)."""
        # In a real implementation, you might cache this or make it more efficient
        devices = self.get_devices()
        for device in devices:
            if device.get('id') == device_id:
                return device.get('site_id', '')
        raise ValueError(f"Device {device_id} not found")
    
    # Convenience Methods
    def health_check(self) -> Dict[str, Any]:
        """Perform a basic health check of the API connection and organization."""
        try:
            # Test API connectivity
            connection_status = self.auth.test_connection()
            
            # Get basic org info
            sites = self.get_sites()
            devices = self.get_devices()
            
            return {
                'status': 'healthy',
                'connection': connection_status,
                'summary': {
                    'total_sites': len(sites),
                    'total_devices': len(devices),
                    'timestamp': datetime.now().isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
