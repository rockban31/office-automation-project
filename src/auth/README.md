# Mist API Authentication Module

This module provides secure authentication and HTTP client functionality for interacting with the Mist API. It includes comprehensive error handling, rate limiting, request retry logic, and session management.

## Features

- **Token-based authentication** with automatic header management
- **Rate limiting protection** with automatic backoff
- **Request retry logic** with exponential backoff
- **Session management** with connection pooling
- **Comprehensive error handling** with custom exceptions
- **Context manager support** for proper resource cleanup
- **Logging integration** for debugging and monitoring

## Quick Start

### 1. Environment Setup

Copy the `.env.example` file to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your Mist API token and organization ID:

```bash
MIST_API_TOKEN=your_api_token_here
MIST_ORG_ID=your_organization_id_here
```

### 2. Basic Usage

```python
from auth import MistAuth, MistAuthError, MistRateLimitError

# Initialize authentication
try:
    auth = MistAuth()  # Uses environment variables
    
    # Test connection
    status = auth.test_connection()
    print(f"Connection status: {status['status']}")
    
    # Make API requests
    organizations = auth.get_organizations()
    print(f"Found {len(organizations)} organizations")
    
    # Custom API request
    sites = auth.make_request('/orgs/{org_id}/sites')
    print(f"Found {len(sites)} sites")
    
except MistAuthError as e:
    print(f"Authentication error: {e}")
except MistRateLimitError as e:
    print(f"Rate limit error: {e}")
finally:
    auth.close()
```

### 3. Using Context Manager (Recommended)

```python
from auth import MistAuth

with MistAuth() as auth:
    # Your code here
    orgs = auth.get_organizations()
    # Session is automatically closed when exiting the context
```

### 4. Custom Configuration

```python
from auth import MistAuth

# Custom configuration
auth = MistAuth(
    api_token="your_token",
    org_id="your_org_id",
    timeout=60,
    max_retries=5,
    backoff_factor=2.0
)
```

## API Reference

### MistAuth Class

#### Constructor Parameters

- `api_token` (str, optional): Mist API token. Defaults to `MIST_API_TOKEN` environment variable.
- `base_url` (str, optional): Base URL for Mist API. Defaults to `https://api.mist.com/api/v1`.
- `org_id` (str, optional): Organization ID. Defaults to `MIST_ORG_ID` environment variable.
- `timeout` (int, optional): Request timeout in seconds. Default: 30.
- `max_retries` (int, optional): Maximum retry attempts. Default: 3.
- `backoff_factor` (float, optional): Backoff factor for retries. Default: 1.0.

#### Methods

##### `make_request(endpoint, method='GET', params=None, json_data=None, **kwargs)`

Make an authenticated request to the Mist API.

**Parameters:**
- `endpoint` (str): API endpoint (e.g., '/orgs/{org_id}/clients')
- `method` (str): HTTP method (GET, POST, PUT, DELETE)
- `params` (dict, optional): Query parameters
- `json_data` (dict, optional): JSON data for POST/PUT requests
- `**kwargs`: Additional arguments for requests

**Returns:** Dictionary containing JSON response

**Raises:** `MistAuthError`, `MistRateLimitError`

##### `get_organizations()`

Get list of organizations accessible to the authenticated user.

**Returns:** List of organization dictionaries

##### `get_organization_info(org_id=None)`

Get information about a specific organization.

**Parameters:**
- `org_id` (str, optional): Organization ID. Uses `self.org_id` if not provided.

**Returns:** Organization information dictionary

##### `test_connection()`

Test the API connection and return connection status.

**Returns:** Dictionary containing connection status and user information

##### `close()`

Close the HTTP session.

## Error Handling

The module provides custom exceptions for different error scenarios:

### MistAuthError

Raised for authentication and HTTP errors.

```python
try:
    auth = MistAuth(api_token="invalid_token")
except MistAuthError as e:
    print(f"Error: {e}")
    print(f"Status code: {e.status_code}")
```

### MistRateLimitError

Raised when API rate limits are exceeded.

```python
try:
    result = auth.make_request('/some/endpoint')
except MistRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    print(f"Retry after: {e.retry_after} seconds")
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MIST_API_TOKEN` | Yes | - | Your Mist API token |
| `MIST_ORG_ID` | No | - | Your organization ID |
| `MIST_BASE_URL` | No | `https://api.mist.com/api/v1` | Mist API base URL |
| `MIST_TIMEOUT` | No | `30` | Request timeout in seconds |
| `MIST_MAX_RETRIES` | No | `3` | Maximum retry attempts |
| `MIST_BACKOFF_FACTOR` | No | `1.0` | Backoff factor for retries |
| `MIST_RATE_LIMIT_THRESHOLD` | No | `10` | Rate limit warning threshold |

### Getting Your API Token

1. Log in to your Mist dashboard
2. Go to Organization Settings > API Tokens
3. Create a new token with appropriate permissions
4. Copy the token to your `.env` file

## Rate Limiting

The module automatically handles rate limiting by:

1. Tracking rate limit headers from API responses
2. Implementing automatic backoff when approaching limits
3. Raising `MistRateLimitError` when limits are exceeded
4. Providing retry-after information for proper handling

## Logging

The module uses Python's standard logging framework. Configure logging levels in your application:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('auth.mist_auth')
```

## Testing

Run the unit tests:

```bash
python -m pytest tests/test_auth.py -v
```

Or run the example script:

```bash
python examples/auth_example.py
```

## Security Considerations

1. **Never commit API tokens** to version control
2. **Use environment variables** for sensitive configuration
3. **Implement proper error handling** to avoid exposing tokens in logs
4. **Use HTTPS only** for all API communications
5. **Regularly rotate API tokens** for security

## Troubleshooting

### Common Issues

1. **Invalid API Token (401 error)**
   - Check that your token is correct in `.env`
   - Verify token hasn't expired
   - Ensure token has required permissions

2. **Organization Not Found (404 error)**
   - Verify organization ID is correct
   - Check that your token has access to the organization

3. **Rate Limit Exceeded (429 error)**
   - The module handles this automatically
   - Consider reducing request frequency
   - Check for any loops making excessive requests

4. **Connection Timeout**
   - Check your internet connection
   - Increase timeout value if needed
   - Verify Mist API service status

For more help, check the logs or run the example script with debug logging enabled.
