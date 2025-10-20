import os
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging BEFORE importing mistapi to suppress debug output
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'  # Simplified format
)

import mistapi

# Aggressively suppress mistapi library verbose logging AFTER import
for logger_name in ['mistapi', 'mistapi.apisession', 'mistapi.apirequest', 'mistapi.apiresponse', 'mistapi.api']:
    mistapi_logger = logging.getLogger(logger_name)
    mistapi_logger.setLevel(logging.CRITICAL)  # Only show critical errors
    mistapi_logger.propagate = False  # Don't propagate to root logger
    # Remove all handlers
    mistapi_logger.handlers = []
    # Disable all logging for this logger
    mistapi_logger.disabled = True

# Set up our own logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MistAuthError(Exception):
    """Custom exception for Mist authentication errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class MistRateLimitError(Exception):
    """Custom exception for Mist rate limit errors."""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after

class MistAuth:
    """
    Mist API Authentication and HTTP Client
    
    This class provides secure authentication and HTTP client functionality
    for interacting with the Mist API using the official mistapi library.
    It maintains backward compatibility with the original interface while
    leveraging the efficiency and features of the mistapi module.
    """
    
    def __init__(self, api_token: Optional[str] = None, 
                 base_url: Optional[str] = None,
                 org_id: Optional[str] = None,
                 timeout: int = 30,
                 max_retries: int = 3,
                 backoff_factor: float = 1.0):
        """
        Initialize Mist API authentication using mistapi.
        
        Args:
            api_token: Mist API token (can be set via MIST_API_TOKEN env var)
            base_url: Base URL for Mist API (default: https://api.mist.com/api/v1)
            org_id: Organization ID (can be set via MIST_ORG_ID env var)
            timeout: Request timeout in seconds (for backward compatibility)
            max_retries: Maximum number of retry attempts (for backward compatibility)
            backoff_factor: Backoff factor for retry delays (for backward compatibility)
        """
        self.api_token = api_token or os.getenv('MIST_API_TOKEN')
        self.org_id = org_id or os.getenv('MIST_ORG_ID')
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
        # Extract host from base_url for mistapi
        if base_url:
            # Convert https://api.eu.mist.com/api/v1 to api.eu.mist.com
            import urllib.parse
            parsed = urllib.parse.urlparse(base_url)
            self.host = parsed.netloc
        else:
            # Use environment variables or default
            env_base_url = os.getenv('MIST_BASE_URL')
            if env_base_url:
                import urllib.parse
                parsed = urllib.parse.urlparse(env_base_url)
                self.host = parsed.netloc
            else:
                self.host = os.getenv('MIST_HOST', 'api.mist.com')
        
        # For backward compatibility
        self.base_url = f"https://{self.host}/api/v1"
        
        # Validate required parameters
        if not self.api_token:
            raise MistAuthError('API token must be provided via environment variable MIST_API_TOKEN or constructor parameter.')
        
        # Initialize mistapi session
        try:
            self.session = mistapi.APISession(
                apitoken=self.api_token,
                host=self.host,
                console_log_level=logging.WARNING,  # Reduce console noise
                show_cli_notif=False  # Disable decorative text
            )
            self.session.login()
            
            # Rate limiting tracking (for backward compatibility)
            self.rate_limit_remaining = None
            self.rate_limit_reset = None
            self.last_request_time = None
            
        except Exception as e:
            raise MistAuthError(f"Failed to initialize mistapi session: {e}")
        
        logger.info(f"MistAuth initialized successfully using mistapi for org_id: {self.org_id}")
    
    def _get_mistapi_response_data(self, response: Any) -> Dict[str, Any]:
        """
        Extract data from mistapi response object.
        
        Args:
            response: mistapi.APIResponse object
            
        Returns:
            Dictionary containing response data
        """
        if hasattr(response, 'data') and response.data is not None:
            return response.data
        elif hasattr(response, 'result') and response.result is not None:
            return response.result
        else:
            return {}
    
    def make_request(self, endpoint: str, method: str = 'GET', 
                    params: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the Mist API using mistapi.
        
        Args:
            endpoint: API endpoint (e.g., '/orgs/{org_id}/clients')
            method: HTTP method (GET, POST, PUT, DELETE)
            params: Query parameters
            json_data: JSON data for POST/PUT requests
            **kwargs: Additional arguments (for backward compatibility)
        
        Returns:
            JSON response as dictionary
        
        Raises:
            MistAuthError: For authentication or HTTP errors
            MistRateLimitError: For rate limit errors
        """
        try:
            # Replace {org_id} placeholder if present
            if '{org_id}' in endpoint and self.org_id:
                endpoint = endpoint.replace('{org_id}', self.org_id)
            
            # Ensure endpoint starts with /api/v1
            if not endpoint.startswith('/api/v1'):
                endpoint = f'/api/v1{endpoint}' if endpoint.startswith('/') else f'/api/v1/{endpoint}'
            
            # Use mistapi methods based on HTTP method
            if method.upper() == 'GET':
                response = self.session.mist_get(endpoint, query=params)
            elif method.upper() == 'POST':
                response = self.session.mist_post(endpoint, body=json_data)
            elif method.upper() == 'PUT':
                response = self.session.mist_put(endpoint, body=json_data)
            elif method.upper() == 'DELETE':
                response = self.session.mist_delete(endpoint, query=params)
            else:
                raise MistAuthError(f"Unsupported HTTP method: {method}")
            
            # Extract data from mistapi response
            return self._get_mistapi_response_data(response)
            
        except Exception as e:
            error_msg = f"API request failed: {e}"
            logger.error(error_msg)
            raise MistAuthError(error_msg)
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """
        Get list of organizations accessible to the authenticated user.
        
        Returns:
            List of organization dictionaries
        """
        # Get user self information which includes accessible organizations
        response = mistapi.api.v1.self.self.getSelf(self.session)
        user_data = self._get_mistapi_response_data(response)
        
        # Extract organizations from user data
        orgs = []
        if 'privileges' in user_data:
            seen_org_ids = set()
            for privilege in user_data['privileges']:
                if 'org_id' in privilege and privilege['org_id'] not in seen_org_ids:
                    org_info = {
                        'id': privilege['org_id'],
                        'name': privilege.get('name', 'Unknown'),
                        'role': privilege.get('role', 'Unknown'),
                        'scope': privilege.get('scope', 'Unknown')
                    }
                    orgs.append(org_info)
                    seen_org_ids.add(privilege['org_id'])
        
        return orgs
    
    def get_organization_info(self, org_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get information about a specific organization.
        
        Args:
            org_id: Organization ID (uses self.org_id if not provided)
        
        Returns:
            Organization information dictionary
        """
        org_id = org_id or self.org_id
        if not org_id:
            raise MistAuthError("Organization ID must be provided")
        
        response = mistapi.api.v1.orgs.orgs.getOrg(self.session, org_id)
        return self._get_mistapi_response_data(response)
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection and return connection status.
        
        Returns:
            Dictionary containing connection status and user information
        """
        try:
            # Get user info using mistapi
            user_response = mistapi.api.v1.self.self.getSelf(self.session)
            user_info = self._get_mistapi_response_data(user_response)
            
            # Get org info if org_id is set
            org_info = None
            if self.org_id:
                try:
                    org_info = self.get_organization_info()
                except Exception as e:
                    logger.warning(f"Could not get org info: {e}")
            
            return {
                'status': 'connected',
                'user_info': user_info,
                'org_info': org_info,
                'rate_limit_remaining': self.rate_limit_remaining,
                'rate_limit_reset': self.rate_limit_reset.isoformat() if self.rate_limit_reset else None
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def close(self) -> None:
        """
        Close the mistapi session.
        """
        if hasattr(self.session, 'logout'):
            try:
                self.session.logout()
            except Exception as e:
                logger.warning(f"Error during logout: {e}")
    
    def __enter__(self):
        """
        Context manager entry.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        """
        self.close()
