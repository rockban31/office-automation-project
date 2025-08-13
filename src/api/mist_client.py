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
    
    def __init__(self, auth: Optional[MistAuth] = None, **auth_kwargs):
        """
        Initialize the Mist Network Client.
        
        Args:
            auth: Existing MistAuth instance, or None to create a new one
            **auth_kwargs: Arguments to pass to MistAuth constructor if auth is None
        """
        if auth is not None:
            self.auth = auth
            self._owns_auth = False
        else:
            self.auth = MistAuth(**auth_kwargs)
            self._owns_auth = True
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._owns_auth:
            self.auth.close()
    
    # Site Management
    def get_sites(self) -> List[Dict[str, Any]]:
        """Get all sites in the organization."""
        try:
            return self.auth.make_request('/orgs/{org_id}/sites')
        except Exception as e:
            logger.error(f"Failed to get sites: {e}")
            raise
    
    def get_site_info(self, site_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific site."""
        try:
            return self.auth.make_request(f'/sites/{site_id}')
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
            if site_id:
                return self.auth.make_request(f'/sites/{site_id}/devices')
            else:
                return self.auth.make_request('/orgs/{org_id}/devices')
        except Exception as e:
            logger.error(f"Failed to get devices: {e}")
            raise
    
    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get current status of a specific device."""
        try:
            return self.auth.make_request(f'/sites/{self._get_site_id_for_device(device_id)}/devices/{device_id}/status')
        except Exception as e:
            logger.error(f"Failed to get device status for {device_id}: {e}")
            raise
    
    # Client Management
    def get_clients(self, site_id: str, duration: int = 24) -> List[Dict[str, Any]]:
        """
        Get clients connected to a site.
        
        Args:
            site_id: Site identifier
            duration: Hours of history to include (default: 24)
        """
        try:
            params = {'duration': f'{duration}h'}
            return self.auth.make_request(f'/sites/{site_id}/clients', params=params)
        except Exception as e:
            logger.error(f"Failed to get clients for site {site_id}: {e}")
            raise
    
    def get_client_sessions(self, site_id: str, client_mac: str) -> List[Dict[str, Any]]:
        """Get session history for a specific client."""
        try:
            return self.auth.make_request(f'/sites/{site_id}/clients/{client_mac}/sessions')
        except Exception as e:
            logger.error(f"Failed to get client sessions for {client_mac}: {e}")
            raise
    
    # Network Insights & Analytics
    def get_site_stats(self, site_id: str) -> Dict[str, Any]:
        """Get site statistics and metrics."""
        try:
            return self.auth.make_request(f'/sites/{site_id}/stats')
        except Exception as e:
            logger.error(f"Failed to get site stats for {site_id}: {e}")
            raise
    
    def get_device_stats(self, site_id: str, device_id: str) -> Dict[str, Any]:
        """Get device statistics and metrics."""
        try:
            return self.auth.make_request(f'/sites/{site_id}/devices/{device_id}/stats')
        except Exception as e:
            logger.error(f"Failed to get device stats for {device_id}: {e}")
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
            if site_id:
                return self.auth.make_request(f'/sites/{site_id}/alarms')
            else:
                return self.auth.make_request('/orgs/{org_id}/alarms')
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
