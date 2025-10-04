#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run script for Al-Awael Daycare System
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("⚠️  Python 3.8 or higher is required")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        issues.append("⚠️  .env file not found. Please copy .env.example to .env")
    else:
        print("✅ .env file found")
    
    # Check critical environment variables
    critical_vars = ['SECRET_KEY', 'JWT_SECRET_KEY']
    for var in critical_vars:
        if not os.getenv(var):
            issues.append(f"⚠️  {var} not set in .env")
    
    if not issues:
        print("✅ Environment check passed")
        return True
    else:
        print("\n❌ Environment check failed:")
        for issue in issues:
            print(f"  {issue}")
        return False


def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy',
        'flask_cors',
        'flask_jwt_extended',
        'flask_mail',
        'flask_migrate',
        'bcrypt',
        'python-dotenv',
        'werkzeug',
        'PIL'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing packages:")
        for package in missing:
            print(f"  - {package}")
        print("\n💡 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed")
        return True


def initialize_database():
    """Initialize database if needed"""
    print("\n🗄️  Initializing database...")
    
    try:
        from seed_data import run_seeds
        from 'ملف موقع الاوائل 2' import app, db
        
        run_seeds(app, db)
        return True
    except Exception as e:
        print(f"⚠️  Database initialization: {e}")
        return False


def run_application():
    """Run the Flask application"""
    print("\n🚀 Starting application...")
    print("=" * 50)
    
    try:
        # Import the main application
        from 'ملف موقع الاوائل 2' import app
        
        # Get configuration
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'True').lower() == 'true'
        
        print(f"🌐 Server running on http://{host}:{port}")
        print(f"📱 Access from browser: http://localhost:{port}")
        print("=" * 50)
        print("\n⏸️  Press CTRL+C to stop the server\n")
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    print("=" * 50)
    print("مراكز الأوائل للرعاية النهارية")
    print("Al-Awael Daycare System")
    print("=" * 50)
    print()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Initialize database (optional, will skip if already initialized)
    initialize_database()
    
    # Run application
    run_application()


if __name__ == '__main__':
    main()
