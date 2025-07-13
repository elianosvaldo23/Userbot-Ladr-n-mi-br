#!/usr/bin/env python3
"""
Test script for Telegram UserBot functionality
This script validates all core components without requiring real API credentials
"""

import sys
import os
import asyncio
import logging

# Add current directory to path
sys.path.append('.')

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import pyrogram
        print(f"✅ Pyrogram {pyrogram.__version__} imported")
    except ImportError as e:
        print(f"❌ Pyrogram import failed: {e}")
        return False
    
    try:
        from pyrogram.errors import FloodWait, UserPrivacyRestricted, PeerFlood, UserNotMutualContact
        print("✅ Pyrogram error classes imported")
    except ImportError as e:
        print(f"❌ Pyrogram errors import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration management"""
    print("\n🧪 Testing configuration...")
    
    # Clear any cached config
    if 'config' in sys.modules:
        del sys.modules['config']
    
    try:
        from config import Config
        print("✅ Config class imported")
        
        # Test validation without credentials
        try:
            Config.validate()
            print("❌ Config should fail without credentials")
            return False
        except ValueError:
            print("✅ Config validation correctly fails without credentials")
        
        # Set mock credentials
        os.environ['API_ID'] = '12345'
        os.environ['API_HASH'] = 'mock_hash'
        os.environ['PHONE_NUMBER'] = '+1234567890'
        
        # Test with credentials
        if 'config' in sys.modules:
            del sys.modules['config']
        from config import Config
        
        Config.validate()
        print("✅ Config validation passes with mock credentials")
        
        # Test getters
        assert Config.get_api_id() == '12345'
        assert Config.get_api_hash() == 'mock_hash'
        assert Config.get_phone_number() == '+1234567890'
        print("✅ Config getters work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_userbot_classes():
    """Test userbot class instantiation"""
    print("\n🧪 Testing userbot classes...")
    
    # Clear cached modules
    for module in ['main', 'example_usage']:
        if module in sys.modules:
            del sys.modules[module]
    
    try:
        from main import TelegramUserBot
        bot = TelegramUserBot()
        print("✅ TelegramUserBot instantiated successfully")
        
        # Check required methods
        required_methods = [
            'get_group_members',
            'add_member_to_group',
            'transfer_members', 
            'get_group_info',
            'start',
            'stop'
        ]
        
        for method in required_methods:
            if hasattr(bot, method) and callable(getattr(bot, method)):
                print(f"✅ Method {method} exists and is callable")
            else:
                print(f"❌ Method {method} missing or not callable")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ UserBot class test failed: {e}")
        return False

def test_example_bot():
    """Test example bot class"""
    print("\n🧪 Testing example bot...")
    
    try:
        from example_usage import MemberTransferBot
        example_bot = MemberTransferBot()
        print("✅ MemberTransferBot instantiated successfully")
        
        if hasattr(example_bot, 'transfer_members_simple'):
            print("✅ transfer_members_simple method exists")
            return True
        else:
            print("❌ transfer_members_simple method missing")
            return False
            
    except Exception as e:
        print(f"❌ Example bot test failed: {e}")
        return False

def test_file_structure():
    """Test project file structure"""
    print("\n🧪 Testing file structure...")
    
    required_files = {
        'main.py': 'Main userbot script',
        'config.py': 'Configuration management',
        'example_usage.py': 'Example usage script',
        'requirements.txt': 'Python dependencies',
        '.env.example': 'Environment variables template',
        'README.md': 'Documentation'
    }
    
    all_exist = True
    for file, description in required_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} exists ({size} bytes) - {description}")
        else:
            print(f"❌ {file} missing - {description}")
            all_exist = False
    
    return all_exist

def test_logging():
    """Test logging configuration"""
    print("\n🧪 Testing logging...")
    
    try:
        from main import logger
        print(f"✅ Logger imported: {logger.name}")
        
        # Test log levels
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        print("✅ Logging functions work")
        
        return True
        
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Telegram UserBot Test Suite\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("UserBot Classes", test_userbot_classes),
        ("Example Bot", test_example_bot),
        ("File Structure", test_file_structure),
        ("Logging", test_logging)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED\n")
            else:
                print(f"❌ {test_name} test FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}\n")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! UserBot is ready to use.")
        print("\n📋 Next steps:")
        print("1. Get your API credentials from https://my.telegram.org/")
        print("2. Copy .env.example to .env and fill in your credentials")
        print("3. Run: python main.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
