#!/usr/bin/env python3
"""
Tests for the Mist API Client module.

This module contains unit tests for the MistNetworkClient class to ensure
proper functionality of network operations and API interactions.
"""

import os
import sys
import unittest
from unittest.mock import patch, Mock, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.mist_client import MistNetworkClient
from auth.mist_auth import MistAuth


class TestMistNetworkClient(unittest.TestCase):
    """Test cases for MistNetworkClient class."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_auth = Mock(spec=MistAuth)
        self.client = MistNetworkClient(auth=self.mock_auth)
        
    def test_init_with_existing_auth(self):
        """Test initialization with existing MistAuth instance."""
        client = MistNetworkClient(auth=self.mock_auth)
        self.assertEqual(client.auth, self.mock_auth)
        self.assertFalse(client._owns_auth)
    
    @patch('api.mist_client.MistAuth')
    def test_init_without_auth(self, mock_auth_class):
        """Test initialization without existing auth (creates new instance)."""
        mock_auth_instance = Mock()
        mock_auth_class.return_value = mock_auth_instance
        
        client = MistNetworkClient(api_token="test_token")
        
        mock_auth_class.assert_called_once_with(api_token="test_token")
        self.assertEqual(client.auth, mock_auth_instance)
        self.assertTrue(client._owns_auth)
    
    def test_get_sites(self):
        """Test getting sites."""
        expected_sites = [
            {'id': 'site1', 'name': 'Main Office'},
            {'id': 'site2', 'name': 'Branch Office'}
        ]
        self.mock_auth.make_request.return_value = expected_sites
        
        result = self.client.get_sites()
        
        self.mock_auth.make_request.assert_called_once_with('/orgs/{org_id}/sites')
        self.assertEqual(result, expected_sites)
    
    def test_get_site_info(self):
        """Test getting site information."""
        site_id = "test_site_123"
        expected_info = {'id': site_id, 'name': 'Test Site', 'address': 'Test Address'}
        self.mock_auth.make_request.return_value = expected_info
        
        result = self.client.get_site_info(site_id)
        
        self.mock_auth.make_request.assert_called_once_with(f'/sites/{site_id}')
        self.assertEqual(result, expected_info)
    
    def test_get_devices_all(self):
        """Test getting all devices."""
        expected_devices = [
            {'id': 'device1', 'name': 'AP-1'},
            {'id': 'device2', 'name': 'AP-2'}
        ]
        self.mock_auth.make_request.return_value = expected_devices
        
        result = self.client.get_devices()
        
        self.mock_auth.make_request.assert_called_once_with('/orgs/{org_id}/devices')
        self.assertEqual(result, expected_devices)
    
    def test_get_devices_by_site(self):
        """Test getting devices for a specific site."""
        site_id = "test_site_123"
        expected_devices = [{'id': 'device1', 'name': 'AP-1', 'site_id': site_id}]
        self.mock_auth.make_request.return_value = expected_devices
        
        result = self.client.get_devices(site_id=site_id)
        
        self.mock_auth.make_request.assert_called_once_with(f'/sites/{site_id}/devices')
        self.assertEqual(result, expected_devices)
    
    def test_get_clients(self):
        """Test getting clients for a site."""
        site_id = "test_site_123"
        duration = 48
        expected_clients = [
            {'mac': '00:11:22:33:44:55', 'hostname': 'laptop1'},
            {'mac': '00:11:22:33:44:66', 'hostname': 'phone1'}
        ]
        self.mock_auth.make_request.return_value = expected_clients
        
        result = self.client.get_clients(site_id, duration=duration)
        
        self.mock_auth.make_request.assert_called_once_with(
            f'/sites/{site_id}/clients', 
            params={'duration': f'{duration}h'}
        )
        self.assertEqual(result, expected_clients)
    
    def test_get_alarms_all(self):
        """Test getting all alarms."""
        expected_alarms = [
            {'id': 'alarm1', 'type': 'device_down', 'severity': 'critical'},
            {'id': 'alarm2', 'type': 'high_cpu', 'severity': 'warning'}
        ]
        self.mock_auth.make_request.return_value = expected_alarms
        
        result = self.client.get_alarms()
        
        self.mock_auth.make_request.assert_called_once_with('/orgs/{org_id}/alarms')
        self.assertEqual(result, expected_alarms)
    
    def test_get_alarms_by_site(self):
        """Test getting alarms for a specific site."""
        site_id = "test_site_123"
        expected_alarms = [{'id': 'alarm1', 'site_id': site_id, 'type': 'device_down'}]
        self.mock_auth.make_request.return_value = expected_alarms
        
        result = self.client.get_alarms(site_id=site_id)
        
        self.mock_auth.make_request.assert_called_once_with(f'/sites/{site_id}/alarms')
        self.assertEqual(result, expected_alarms)
    
    def test_health_check_success(self):
        """Test successful health check."""
        # Mock auth test_connection
        self.mock_auth.test_connection.return_value = {
            'status': 'connected',
            'user_info': {'email': 'test@example.com'}
        }
        
        # Mock get_sites and get_devices
        self.mock_auth.make_request.side_effect = [
            [{'id': 'site1'}, {'id': 'site2'}],  # sites
            [{'id': 'device1'}, {'id': 'device2'}, {'id': 'device3'}]  # devices
        ]
        
        result = self.client.health_check()
        
        self.assertEqual(result['status'], 'healthy')
        self.assertEqual(result['summary']['total_sites'], 2)
        self.assertEqual(result['summary']['total_devices'], 3)
        self.assertIn('timestamp', result['summary'])
    
    def test_health_check_failure(self):
        """Test health check when API calls fail."""
        self.mock_auth.test_connection.side_effect = Exception("Connection failed")
        
        result = self.client.health_check()
        
        self.assertEqual(result['status'], 'unhealthy')
        self.assertIn('error', result)
        self.assertIn('timestamp', result)
    
    def test_context_manager(self):
        """Test context manager functionality."""
        # Test with owned auth
        with patch('api.mist_client.MistAuth') as mock_auth_class:
            mock_auth_instance = Mock()
            mock_auth_class.return_value = mock_auth_instance
            
            with MistNetworkClient(api_token="test") as client:
                self.assertTrue(client._owns_auth)
            
            # Should close auth when owned
            mock_auth_instance.close.assert_called_once()
        
        # Test with existing auth (not owned)
        with MistNetworkClient(auth=self.mock_auth) as client:
            self.assertFalse(client._owns_auth)
        
        # Should not close auth when not owned
        self.mock_auth.close.assert_not_called()
    
    def test_api_error_handling(self):
        """Test proper error handling when API calls fail."""
        self.mock_auth.make_request.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            self.client.get_sites()
        
        # Verify error was logged (we'd need to capture logs to test this fully)
        self.mock_auth.make_request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
