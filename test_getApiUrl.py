#!/usr/bin/env python3
"""
Test getApiUrl Function
"""

def test_getApiUrl():
    """Test getApiUrl function logic"""
    
    print('Testing getApiUrl Function Logic...')
    print('='*50)
    
    # Simulate the JavaScript getApiUrl function
    API_BASE_URL = 'http://127.0.0.1:8001'
    
    def getApiUrl(endpoint):
        # Remove leading slash if present
        cleanEndpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        
        # Special handling for users endpoints (they don't have /api prefix)
        if cleanEndpoint.startswith('users/'):
            return f'{API_BASE_URL}/{cleanEndpoint}'
        
        # Add /api prefix for other endpoints if not already present
        if not cleanEndpoint.startswith('api/'):
            return f'{API_BASE_URL}/api/{cleanEndpoint}'
        
        return f'{API_BASE_URL}/{cleanEndpoint}'
    
    # Test various endpoints
    test_cases = [
        'users/register',
        'users/login',
        'skills/',
        'exchanges/request-skill',
        '/users/register',
        '/skills/',
        'api/skills/',
        'api/exchanges/'
    ]
    
    print('Test Cases:')
    for endpoint in test_cases:
        url = getApiUrl(endpoint)
        print(f'   getApiUrl("{endpoint}") = {url}')
    
    print()
    print('Expected Results:')
    print('   users endpoints: http://127.0.0.1:8001/users/...')
    print('   other endpoints: http://127.0.0.1:8001/api/...')
    
    print()
    print('getApiUrl Function Testing Complete!')

if __name__ == "__main__":
    test_getApiUrl()
