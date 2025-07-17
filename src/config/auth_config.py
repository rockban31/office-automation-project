"""
Configuration settings for Mist API authentication.

This module provides configuration management for the Mist API authentication
system, including environment variable handling and default settings.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MistAuthConfig:
    """Configuration class for Mist API authentication."""
    
    # Default configuration values
    DEFAULT_BASE_URL = "https://api.mist.com/api/v1"
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_BACKOFF_FACTOR = 1.0
    DEFAULT_RATE_LIMIT_THRESHOLD = 10
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get authentication configuration from environment variables.
        
        Returns:
            Dictionary containing configuration values
        """
        return {
            'api_token': os.getenv('MIST_API_TOKEN'),
            'base_url': os.getenv('MIST_BASE_URL', cls.DEFAULT_BASE_URL),
            'org_id': os.getenv('MIST_ORG_ID'),
            'timeout': int(os.getenv('MIST_TIMEOUT', cls.DEFAULT_TIMEOUT)),
            'max_retries': int(os.getenv('MIST_MAX_RETRIES', cls.DEFAULT_MAX_RETRIES)),
            'backoff_factor': float(os.getenv('MIST_BACKOFF_FACTOR', cls.DEFAULT_BACKOFF_FACTOR)),
            'rate_limit_threshold': int(os.getenv('MIST_RATE_LIMIT_THRESHOLD', cls.DEFAULT_RATE_LIMIT_THRESHOLD))
        }
    
    @classmethod
    def validate_config(cls, config: Dict[str, Any]) -> None:
        """
        Validate configuration values.
        
        Args:
            config: Configuration dictionary
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not config.get('api_token'):
            raise ValueError("MIST_API_TOKEN environment variable is required")
        
        if config.get('timeout', 0) <= 0:
            raise ValueError("Timeout must be positive")
        
        if config.get('max_retries', 0) < 0:
            raise ValueError("Max retries must be non-negative")
        
        if config.get('backoff_factor', 0) < 0:
            raise ValueError("Backoff factor must be non-negative")
    
    @classmethod
    def get_validated_config(cls) -> Dict[str, Any]:
        """
        Get and validate configuration.
        
        Returns:
            Validated configuration dictionary
            
        Raises:
            ValueError: If configuration is invalid
        """
        config = cls.get_config()
        cls.validate_config(config)
        return config

# Environment variable template for .env file
ENV_TEMPLATE = """
# Mist API Configuration
MIST_API_TOKEN=your_api_token_here
MIST_ORG_ID=your_organization_id_here
MIST_BASE_URL=https://api.mist.com/api/v1
MIST_TIMEOUT=30
MIST_MAX_RETRIES=3
MIST_BACKOFF_FACTOR=1.0
MIST_RATE_LIMIT_THRESHOLD=10
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
