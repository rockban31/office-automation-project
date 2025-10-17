#!/usr/bin/env python3
"""
Example script demonstrating Mist API authentication usage.

This script shows how to use the MistAuth class to authenticate with the Mist API
and perform basic operations like getting organization information and testing
the connection.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth import MistAuth, MistAuthError, MistRateLimitError
from config.auth_config import get_mist_config, create_env_template

def main():
    """Main function demonstrating Mist API authentication."""
    
    print("=== Mist API Authentication Example ===\n")
    
    # Create .env template if it doesn't exist
    create_env_template()
    
    try:
        # Option 1: Using environment variables (recommended)
        print("1. Initializing MistAuth with environment variables...")
        auth = MistAuth()
        
        # Option 2: Using configuration function
        # config = get_mist_config()
        # auth = MistAuth(**config)
        
        # Option 3: Direct parameters
        # auth = MistAuth(
        #     api_token="your_token_here",
        #     org_id="your_org_id_here"
        # )
        
        print(f"✓ Authentication initialized successfully!")
        print(f"  Base URL: {auth.base_url}")
        print(f"  Organization ID: {auth.org_id}")
        print(f"  Timeout: {auth.timeout} seconds")
        print(f"  Max Retries: {auth.max_retries}")
        print()
        
        # Test the connection
        print("2. Testing API connection...")
        connection_status = auth.test_connection()
        
        if connection_status['status'] == 'connected':
            print("✓ Connection successful!")
            print()
            
            # Get organization information
            if auth.org_id:
                print("3. Getting organization information...")
                org_info = auth.get_organization_info()
                print(f"✓ Organization: {org_info.get('name', 'Unknown')}")
                print(f"  ID: {org_info.get('id', 'Unknown')}")
                print(f"  Created: {org_info.get('created_time', 'Unknown')}")
                print()
            
            # List available organizations
            print("4. Listing available organizations...")
            orgs = auth.get_organizations()
            print(f"✓ Found {len(orgs)} organizations:")
            for org in orgs[:5]:  # Show first 5
                print(f"  - {org.get('name', 'Unknown')} ({org.get('id', 'Unknown')})")
            if len(orgs) > 5:
                print(f"  ... and {len(orgs) - 5} more")
            print()
            
            
        else:
            print("✗ Connection failed!")
            print(f"  Error: {connection_status['error']}")
            
    except MistAuthError as e:
        print(f"✗ Authentication error: {e}")
        if e.status_code == 401:
            print("  Please check your API token in the .env file")
        elif e.status_code == 403:
            print("  Please check your API token permissions")
        
    except MistRateLimitError as e:
        print(f"✗ Rate limit error: {e}")
        print(f"  Retry after: {e.retry_after} seconds")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        
    finally:
        # Clean up
        if 'auth' in locals():
            auth.close()
        print("\n=== Example completed ===")

if __name__ == "__main__":
    main()
