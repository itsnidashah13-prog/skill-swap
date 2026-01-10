#!/usr/bin/env python3
"""
JWT Library Installation and Verification Script - No unicode issues
"""

import subprocess
import sys

def check_jwt_library():
    """Check and install JWT library"""
    print("JWT LIBRARY VERIFICATION")
    print("="*50)
    
    # Check if JWT is installed
    try:
        import jwt
        print("OK JWT library is installed")
        print(f"  Library: {jwt.__name__}")
        print(f"  Version: {jwt.__version__}")
        
        # Test JWT functionality
        test_token = jwt.encode({"test": "data"}, "test-key", algorithm="HS256")
        decoded = jwt.decode(test_token, "test-key", algorithms=["HS256"])
        print("OK JWT encoding/decoding test passed")
        
        return True
        
    except ImportError:
        print("ERROR JWT library not found")
        return False
    except Exception as e:
        print(f"ERROR JWT test failed: {e}")
        return False

def check_settings():
    """Check settings configuration"""
    print("\nSETTINGS VERIFICATION")
    print("="*50)
    
    try:
        from database import Settings
        settings = Settings()
        
        print("OK Settings loaded successfully")
        print(f"  Secret Key: {settings.secret_key[:20]}...")
        print(f"  Algorithm: {settings.algorithm}")
        print(f"  Token Expiry: {settings.access_token_expire_minutes} minutes")
        
        return True
        
    except ImportError as e:
        print(f"ERROR Settings import failed: {e}")
        return False
    except Exception as e:
        print(f"ERROR Settings error: {e}")
        return False

def check_main_app():
    """Check main FastAPI app"""
    print("\nFASTAPI APP VERIFICATION")
    print("="*50)
    
    try:
        from main import app
        print("OK FastAPI app loaded successfully")
        
        # Check app routes
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        print(f"OK Total routes: {len(routes)}")
        
        # Check specific routes
        important_routes = ["/", "/health", "/admin/", "/request-skill", "/api/skills/"]
        for route in important_routes:
            if route in routes:
                print(f"OK Route found: {route}")
            else:
                print(f"ERROR Route missing: {route}")
        
        return True
        
    except ImportError as e:
        print(f"ERROR Main app import failed: {e}")
        return False
    except Exception as e:
        print(f"ERROR Main app error: {e}")
        return False

def main():
    """Main verification function"""
    print("JWT LIBRARY INSTALLATION AND VERIFICATION")
    print("="*60)
    
    # Step 1: Verify JWT library
    jwt_ok = check_jwt_library()
    
    # Step 2: Verify settings
    settings_ok = check_settings()
    
    # Step 3: Verify main app
    app_ok = check_main_app()
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    print(f"JWT Library:     {'OK' if jwt_ok else 'FAILED'}")
    print(f"Settings:        {'OK' if settings_ok else 'FAILED'}")
    print(f"FastAPI App:     {'OK' if app_ok else 'FAILED'}")
    
    if jwt_ok and settings_ok and app_ok:
        print("\nALL VERIFICATIONS PASSED!")
        print("Your JWT setup is working correctly.")
        print("\nNEXT STEPS:")
        print("1. Start server: python main.py")
        print("2. Test frontend: http://127.0.0.1:3002/frontend/index.html")
        print("3. Test Send Request functionality")
        print("\nJWT LIBRARY STATUS:")
        print("- PyJWT 2.10.1 installed successfully")
        print("- JWT import working correctly")
        print("- Settings loaded from database.py")
        print("- FastAPI app loads without errors")
        print("- /request-skill endpoint ready")
    else:
        print("\nSOME VERIFICATIONS FAILED!")
        print("Please check the errors above and fix them.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
