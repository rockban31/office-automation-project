#!/usr/bin/env python3
"""
Basic tests for the Mist API authentication module.

This module contains unit tests for the MistAuth class to ensure
proper functionality of authentication and API request handling.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, Mock

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth import MistAuth, MistAuthError, MistRateLimitError

class TestMistAuth(unittest.TestCase):
    """Test cases for MistAuth class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_token = "test_token_12345"
        self.test_org_id = "test_org_id_12345"
        self.test_base_url = "https://api.mist.com/api/v1"
        
    @patch('auth.mist_auth.mistapi.APISession')
    def test_init_with_token(self, mock_session):
        """Test initialization with API token."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.login.return_value = None
        
        auth = MistAuth(
            api_token=self.test_token,
            org_id=self.test_org_id,
            base_url=self.test_base_url
        )
        
        self.assertEqual(auth.api_token, self.test_token)
        self.assertEqual(auth.org_id, self.test_org_id)
        self.assertEqual(auth.base_url, self.test_base_url)
        mock_session_instance.login.assert_called_once()
        
    @patch.dict(os.environ, {}, clear=True)
    def test_init_without_token(self):
        """Test initialization without API token raises error."""
        with self.assertRaises(MistAuthError) as context:
            MistAuth(api_token=None)
        
        self.assertIn("API token must be provided", str(context.exception))
        
    @patch('auth.mist_auth.mistapi.APISession')
    def test_make_request_success(self, mock_session):
        """Test successful API request."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.login.return_value = None
        
        # Mock API response from mistapi
        mock_response = Mock()
        mock_response.data = {"data": "test_data"}
        mock_session_instance.mist_get.return_value = mock_response
        
        auth = MistAuth(api_token=self.test_token)
        result = auth.make_request("/test/endpoint")
        
        self.assertEqual(result, {"data": "test_data"})
        mock_session_instance.mist_get.assert_called_once_with("/api/v1/test/endpoint", query=None)
        
    @patch('auth.mist_auth.mistapi.APISession')
    def test_make_request_rate_limit(self, mock_session):
        """Test rate limit error handling."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.login.return_value = None
        
        # Mock rate limit exception from mistapi
        mock_session_instance.mist_get.side_effect = Exception("Rate limit exceeded. Retry after 60 seconds")
        
        auth = MistAuth(api_token=self.test_token)
        
        with self.assertRaises(MistAuthError) as context:
            auth.make_request("/test/endpoint")
        
        self.assertIn("API request failed", str(context.exception))
        
    @patch('auth.mist_auth.mistapi.APISession')
    def test_context_manager(self, mock_session):
        """Test context manager functionality."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.login.return_value = None
        mock_session_instance.logout.return_value = None
        
        with MistAuth(api_token=self.test_token) as auth:
            self.assertIsNotNone(auth)
            self.assertEqual(auth.api_token, self.test_token)
        
        # Verify session logout was called
        mock_session_instance.logout.assert_called_once()

if __name__ == "__main__":
    unittest.main()
