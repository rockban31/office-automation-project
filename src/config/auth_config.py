"""
Simple configuration for Mist API authentication.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_mist_config() -> Dict[str, Any]:
    """
    Get Mist API configuration from environment variables for mistapi.
    
    Returns:
        Dictionary containing configuration values compatible with mistapi
    """
    return {
        'api_token': os.getenv('MIST_API_TOKEN'),
        'base_url': os.getenv('MIST_BASE_URL', 'https://api.mist.com/api/v1'),
        'host': os.getenv('MIST_HOST', 'api.mist.com'),  # Added for mistapi
        'org_id': os.getenv('MIST_ORG_ID'),
        'timeout': int(os.getenv('MIST_TIMEOUT', '30')),
        'max_retries': int(os.getenv('MIST_MAX_RETRIES', '3'))
    }

# Environment variable template for .env file
ENV_TEMPLATE = """
# Mist API Configuration (compatible with mistapi)
MIST_API_TOKEN=your_api_token_here
MIST_ORG_ID=your_organization_id_here
MIST_HOST=api.mist.com
MIST_BASE_URL=https://api.mist.com/api/v1
MIST_TIMEOUT=30
MIST_MAX_RETRIES=3
MIST_BACKOFF_FACTOR=1.0
MIST_RATE_LIMIT_THRESHOLD=10

# mistapi specific settings (optional)
MIST_CONSOLE_LOG_LEVEL=20
MIST_LOGGING_LOG_LEVEL=10
"""

def create_env_template(file_path: str = ".env") -> None:
    """
    Create a template .env file with Mist API configuration variables.
    
    Args:
        file_path: Path to create the .env file
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(ENV_TEMPLATE.strip())
        print(f"Created .env template at {file_path}")
    else:
        print(f".env file already exists at {file_path}")
