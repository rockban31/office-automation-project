import os
from dotenv import load_dotenv
import mistapi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    # Load environment variables
    load_dotenv()
    
    # Get credentials from environment
    api_token = os.getenv('MIST_API_TOKEN')
    
    try:
        # Initialize session with correct host format
        session = mistapi.APISession(
            host="api.eu.mist.com",
            apitoken=api_token
        )
        
        # Test authentication - use correct API endpoint
        result = session.mist_get("/api/v1/self")
        
        if result and result.data:
            logger.info(f"Authentication successful! User: {result.data.get('email')}")
            return True
        else:
            logger.error("Authentication failed: No valid response data")
            return False
            
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()