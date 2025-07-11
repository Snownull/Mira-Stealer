#!/usr/bin/env python3
"""
Test script for the Python conversion
Tests the modules without opening GUI windows
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.translation_manager import TranslationManager
        print("✓ TranslationManager imported successfully")
        
        from src.language_selector import LanguageState
        print("✓ LanguageSelector imported successfully")
        
        from src.models import ClientData, MnemonicData, CredentialData
        print("✓ Models imported successfully")
        
        from src.network_server import NetworkServer
        print("✓ NetworkServer imported successfully")
        
        # Test translation manager
        languages = TranslationManager.get_supported_languages()
        print(f"✓ Supported languages: {languages}")
        
        # Test translation
        spanish_title = TranslationManager.get_translation("Spain", "window_title")
        print(f"✓ Spanish translation example: {spanish_title}")
        
        # Test data models
        client = ClientData(ip="192.168.1.1", country="US", os="Windows 10")
        print(f"✓ ClientData created: {client.ip} from {client.country}")
        
        print("\n✅ All imports and basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_enhanced_functionality():
    """Test the enhanced functionality"""
    print("\nTesting enhanced functionality...")
    try:
        from src.report_form import NotificationManager, ReportForm
        print("✓ ReportForm imported successfully")
        
        from src.data_viewer import DataGrid, ClientDataViewer
        print("✓ DataViewer imported successfully")
        
        from src.builder import BuilderInterface, BuilderConfig
        print("✓ Builder imported successfully")
        
        # Test config
        config = BuilderConfig()
        assert config.server_ip == "127.0.0.1"
        print("✓ BuilderConfig created successfully")
        
        print("✅ Enhanced functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Testing Mira Stealer Python Conversion ===\n")
    
    tests = [
        test_imports,
        test_enhanced_functionality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results: {passed}/{len(tests)} tests passed ===")
    
    if passed == len(tests):
        print("🎉 All tests passed! The conversion is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)