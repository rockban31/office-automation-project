import os
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    for interacting with the Mist API. It includes features such as:
    - Token-based authentication
    - Rate limiting handling
    - Request retry logic
    - Session management
    - Error handling
    """
    
    def __init__(self, api_token: Optional[str] = None, 
                 base_url: Optional[str] = None,
                 org_id: Optional[str] = None,
                 timeout: int = 30,
                 max_retries: int = 3,
                 backoff_factor: float = 1.0):
        """
        Initialize Mist API authentication.
        
        Args:
            api_token: Mist API token (can be set via MIST_API_TOKEN env var)
            base_url: Base URL for Mist API (default: https://api.mist.com/api/v1)
            org_id: Organization ID (can be set via MIST_ORG_ID env var)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            backoff_factor: Backoff factor for retry delays
        """
        self.api_token = api_token or os.getenv('MIST_API_TOKEN')
        self.base_url = base_url or os.getenv('MIST_BASE_URL', 'https://api.mist.com/api/v1')
        self.org_id = org_id or os.getenv('MIST_ORG_ID')
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        
        # Rate limiting tracking
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        self.last_request_time = None
        
        # Validate required parameters
        if not self.api_token:
            raise MistAuthError('API token must be provided via environment variable MIST_API_TOKEN or constructor parameter.')
        
        # Initialize session with retry strategy
        self.session = self._create_session()
        
        # Validate authentication on initialization
        self._validate_auth()
        
        logger.info(f"MistAuth initialized successfully for org_id: {self.org_id}")
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry strategy and authentication headers.
        
        Returns:
            Configured requests.Session object
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set authentication headers
        session.headers.update({
            'Authorization': f'Token {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Mist-Network-Automation-Tool/1.0'
        })
        
        session.verify = False  # <--- Add this line to disable SSL verification
        return session
    
    def _validate_auth(self) -> None:
        """
        Validate authentication by making a test API call.
        
        Raises:
            MistAuthError: If authentication fails
        """
        try:
            response = self.session.get(
                f"{self.base_url}/self",
                timeout=self.timeout
            )
            response.raise_for_status()
            
            user_info = response.json()
            logger.info(f"Authentication successful for user: {user_info.get('email', 'Unknown')}")
            
            # Update rate limit info
            self._update_rate_limit_info(response)
            
        except HTTPError as e:
            if e.response.status_code == 401:
                raise MistAuthError("Invalid API token. Please check your MIST_API_TOKEN.", 401)
            elif e.response.status_code == 403:
                raise MistAuthError("Insufficient permissions. Please check your API token privileges.", 403)
            else:
                raise MistAuthError(f"Authentication validation failed: {e}", e.response.status_code)
        except Exception as e:
            raise MistAuthError(f"Failed to validate authentication: {e}")
    
    def _update_rate_limit_info(self, response: requests.Response) -> None:
        """
        Update rate limit information from response headers.
        
        Args:
            response: HTTP response object
        """
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        
        reset_time = response.headers.get('X-RateLimit-Reset')
        if reset_time:
            self.rate_limit_reset = datetime.fromtimestamp(int(reset_time))
        
        self.last_request_time = datetime.now()
    
    def _check_rate_limit(self) -> None:
        """
        Check if we're approaching rate limits and implement backoff if necessary.
        """
        if self.rate_limit_remaining is not None and self.rate_limit_remaining < 10:
            if self.rate_limit_reset:
                sleep_time = (self.rate_limit_reset - datetime.now()).total_seconds()
                if sleep_time > 0:
                    logger.warning(f"Rate limit approaching. Sleeping for {sleep_time:.2f} seconds.")
                    time.sleep(sleep_time)
    
    def make_request(self, endpoint: str, method: str = 'GET', 
                    params: Optional[Dict[str, Any]] = None,
                    json_data: Optional[Dict[str, Any]] = None,
                    **kwargs) -> Dict[str, Any]:
        """
        Make an authenticated request to the Mist API.
        
        Args:
            endpoint: API endpoint (e.g., '/orgs/{org_id}/clients')
            method: HTTP method (GET, POST, PUT, DELETE)
            params: Query parameters
            json_data: JSON data for POST/PUT requests
            **kwargs: Additional arguments for requests
        
        Returns:
            JSON response as dictionary
        
        Raises:
            MistAuthError: For authentication or HTTP errors
            MistRateLimitError: For rate limit errors
        """
        # Check rate limits before making request
        self._check_rate_limit()
        
        # Prepare URL
        url = f"{self.base_url}{endpoint}"
        
        # Replace {org_id} placeholder if present
        if '{org_id}' in url and self.org_id:
            url = url.replace('{org_id}', self.org_id)
        
        try:
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
                **kwargs
            )
            
            # Update rate limit information
            self._update_rate_limit_info(response)
            
            # Handle different response status codes
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                raise MistRateLimitError(
                    f"Rate limit exceeded. Retry after {retry_after} seconds.",
                    retry_after
                )
            
            response.raise_for_status()
            
            # Handle empty responses
            if response.status_code == 204:
                return {}
            
            try:
                return response.json()
            except json.JSONDecodeError:
                logger.warning(f"Non-JSON response received: {response.text}")
                return {'raw_response': response.text}
                
        except HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            logger.error(error_msg)
            raise MistAuthError(error_msg, e.response.status_code)
            
        except Timeout as e:
            error_msg = f"Request timed out after {self.timeout} seconds: {e}"
            logger.error(error_msg)
            raise MistAuthError(error_msg)
            
        except RequestException as e:
            error_msg = f"Request failed: {e}"
            logger.error(error_msg)
            raise MistAuthError(error_msg)
    
    def get_organizations(self) -> List[Dict[str, Any]]:
        """
        Get list of organizations accessible to the authenticated user.
        
        Returns:
            List of organization dictionaries
        """
        return self.make_request('/orgs')
    
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
        
        return self.make_request(f'/orgs/{org_id}')
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the API connection and return connection status.
        
        Returns:
            Dictionary containing connection status and user information
        """
        try:
            user_info = self.make_request('/self')
            org_info = self.get_organization_info() if self.org_id else None
            
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
        Close the HTTP session.
        """
        if self.session:
            self.session.close()
    
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