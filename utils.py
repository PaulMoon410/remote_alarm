"""
Utility scripts for managing the boiler alarm system.
Provides command-line tools for testing and configuration.
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from services.email_service import EmailService
from services.alarm_monitor import AlarmMonitor

def test_email():
    """Test email configuration and send a test alert."""
    print("🧪 Testing email configuration...")
    
    try:
        settings = Settings()
        email_service = EmailService(settings)
        
        # Validate connection
        print("📡 Testing SMTP connection...")
        if email_service.validate_connection():
            print("✅ SMTP connection successful")
        else:
            print("❌ SMTP connection failed")
            return False
        
        # Send test email
        print("📧 Sending test alert...")
        if email_service.send_test_alert():
            print("✅ Test alert sent successfully")
            return True
        else:
            print("❌ Failed to send test alert")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_gpio():
    """Test GPIO configuration and alarm detection."""
    print("🔌 Testing GPIO configuration...")
    
    try:
        settings = Settings()
        
        if settings.simulation_mode:
            print("⚠️  Running in simulation mode - GPIO testing skipped")
            return True
        
        print(f"📍 Testing GPIO pin {settings.alarm_gpio_pin}")
        
        # Try to initialize GPIO
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            
            if settings.gpio_pull_up:
                GPIO.setup(settings.alarm_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(settings.alarm_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            # Read current state
            pin_state = GPIO.input(settings.alarm_gpio_pin)
            print(f"📊 Current pin state: {'HIGH' if pin_state else 'LOW'}")
            
            GPIO.cleanup()
            print("✅ GPIO test successful")
            return True
            
        except ImportError:
            print("❌ RPi.GPIO not available - install with: pip install RPi.GPIO")
            return False
        except Exception as e:
            print(f"❌ GPIO error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_status():
    """Show current system status."""
    print("📊 Boiler Alarm System Status")
    print("=" * 40)
    
    try:
        settings = Settings()
        print(f"Building: {settings.building_name}")
        print(f"GPIO Pin: {settings.alarm_gpio_pin}")
        print(f"Active State: {settings.alarm_active_state}")
        print(f"Simulation Mode: {settings.simulation_mode}")
        print(f"Recipients: {len(settings.alert_recipients)}")
        print(f"SMTP Server: {settings.smtp_server}:{settings.smtp_port}")
        
        # Test email service
        email_service = EmailService(settings)
        if email_service.validate_connection():
            print("📧 Email: ✅ Connected")
        else:
            print("📧 Email: ❌ Connection Failed")
        
        # Test alarm monitor
        alarm_monitor = AlarmMonitor(settings, email_service)
        status = alarm_monitor.get_status()
        print(f"🔍 Monitoring: {'✅ Active' if status['monitoring'] else '❌ Inactive'}")
        
        if status.get('current_pin_state'):
            print(f"🔌 GPIO State: {status['current_pin_state']}")
        
    except Exception as e:
        print(f"❌ Error getting status: {e}")

def trigger_test_alarm():
    """Manually trigger a test alarm."""
    print("🚨 Triggering test alarm...")
    
    try:
        settings = Settings()
        email_service = EmailService(settings)
        alarm_monitor = AlarmMonitor(settings, email_service)
        
        alarm_monitor.trigger_test_alarm()
        print("✅ Test alarm triggered")
        
    except Exception as e:
        print(f"❌ Error triggering test alarm: {e}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Boiler Alarm System Utilities")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Test email command
    subparsers.add_parser('test-email', help='Test email configuration')
    
    # Test GPIO command
    subparsers.add_parser('test-gpio', help='Test GPIO configuration')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Test alarm command
    subparsers.add_parser('test-alarm', help='Trigger a test alarm')
    
    args = parser.parse_args()
    
    if args.command == 'test-email':
        test_email()
    elif args.command == 'test-gpio':
        test_gpio()
    elif args.command == 'status':
        show_status()
    elif args.command == 'test-alarm':
        trigger_test_alarm()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()